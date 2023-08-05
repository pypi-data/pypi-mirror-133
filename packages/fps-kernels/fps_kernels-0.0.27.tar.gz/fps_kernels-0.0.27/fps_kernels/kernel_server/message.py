import hmac
import hashlib
import json
import struct
from datetime import datetime, timezone
from uuid import uuid4
from typing import List, Dict, Tuple, Any, Optional, cast

from zmq.sugar.socket import Socket
from zmq.utils import jsonapi

protocol_version_info = (5, 3)
protocol_version = "%i.%i" % protocol_version_info

DELIM = b"<IDS|MSG>"


def to_binary(msg: Dict[str, Any]) -> Optional[bytes]:
    if not msg["buffers"]:
        return None
    buffers = msg.pop("buffers")
    bmsg = json.dumps(msg).encode("utf8")
    buffers.insert(0, bmsg)
    n = len(buffers)
    offsets = [4 * (n + 1)]
    for b in buffers[:-1]:
        offsets.append(offsets[-1] + len(b))
    header = struct.pack("!" + "I" * (n + 1), n, *offsets)
    buffers.insert(0, header)
    return b"".join(buffers)


def from_binary(bmsg: bytes) -> Dict[str, Any]:
    n = struct.unpack("!i", bmsg[:4])[0]
    offsets = list(struct.unpack("!" + "I" * n, bmsg[4 : 4 * (n + 1)]))  # noqa
    offsets.append(None)
    buffers = []
    for start, stop in zip(offsets[:-1], offsets[1:]):
        buffers.append(bmsg[start:stop])
    msg = json.loads(buffers[0].decode("utf8"))
    msg["buffers"] = buffers[1:]
    return msg


def pack(obj: Dict[str, Any]) -> bytes:
    return jsonapi.dumps(obj)


def unpack(s: bytes) -> Dict[str, Any]:
    return cast(Dict[str, Any], jsonapi.loads(s))


def sign(msg_list: List[bytes], key: str) -> bytes:
    auth = hmac.new(key.encode("ascii"), digestmod=hashlib.sha256)
    h = auth.copy()
    for m in msg_list:
        h.update(m)
    return h.hexdigest().encode()


def serialize(msg: Dict[str, Any], key: str) -> List[bytes]:
    message = [
        pack(msg["header"]),
        pack(msg["parent_header"]),
        pack(msg["metadata"]),
        pack(msg.get("content", {})),
    ]
    to_send = [DELIM, sign(message, key)] + message + msg.get("buffers", [])
    return to_send


def deserialize(msg_list: List[bytes]) -> Dict[str, Any]:
    message: Dict[str, Any] = {}
    header = unpack(msg_list[1])
    message["header"] = header
    message["msg_id"] = header["msg_id"]
    message["msg_type"] = header["msg_type"]
    message["parent_header"] = unpack(msg_list[2])
    message["metadata"] = unpack(msg_list[3])
    message["content"] = unpack(msg_list[4])
    message["buffers"] = [memoryview(b) for b in msg_list[5:]]
    return message


def feed_identities(msg_list: List[bytes]) -> Tuple[List[bytes], List[bytes]]:
    idx = msg_list.index(DELIM)
    return msg_list[:idx], msg_list[idx + 1 :]  # noqa


def send_message(msg: Dict[str, Any], sock: Socket, key: str) -> None:
    sock.send_multipart(serialize(msg, key), copy=True)


async def receive_message(
    sock: Socket, timeout: float = float("inf")
) -> Optional[Dict[str, Any]]:
    timeout *= 1000  # in ms
    ready = await sock.poll(timeout)
    if ready:
        msg_list = await sock.recv_multipart()
        idents, msg_list = feed_identities(msg_list)
        return deserialize(msg_list)
    return None


def utcnow() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def create_message_header(
    msg_type: str, session_id: str, msg_id: str
) -> Dict[str, Any]:
    if not session_id:
        session_id = uuid4().hex
    if not msg_id:
        msg_id = uuid4().hex
    header = {
        "date": utcnow().isoformat().replace("+00:00", "Z"),
        "msg_id": msg_id,
        "msg_type": msg_type,
        "session": session_id,
        "username": "",
        "version": protocol_version,
    }
    return header


def create_message(
    msg_type: str,
    content: Dict = {},
    session_id: str = "",
    msg_id: str = "",
) -> Dict[str, Any]:
    header = create_message_header(msg_type, session_id, msg_id)
    msg = {
        "header": header,
        "msg_id": header["msg_id"],
        "msg_type": header["msg_type"],
        "parent_header": {},
        "content": content,
        "metadata": {},
        "buffers": [],
    }
    return msg
