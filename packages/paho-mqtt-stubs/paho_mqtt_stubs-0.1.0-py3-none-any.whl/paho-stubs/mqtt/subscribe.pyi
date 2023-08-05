from typing import Any

from .. import mqtt as mqtt

def callback(
    callback,
    topics,
    qos: int = ...,
    userdata: Any | None = ...,
    hostname: str = ...,
    port: int = ...,
    client_id: str = ...,
    keepalive: int = ...,
    will: Any | None = ...,
    auth: Any | None = ...,
    tls: Any | None = ...,
    protocol=...,
    transport: str = ...,
    clean_session: bool = ...,
    proxy_args: Any | None = ...,
) -> None: ...
def simple(
    topics,
    qos: int = ...,
    msg_count: int = ...,
    retained: bool = ...,
    hostname: str = ...,
    port: int = ...,
    client_id: str = ...,
    keepalive: int = ...,
    will: Any | None = ...,
    auth: Any | None = ...,
    tls: Any | None = ...,
    protocol=...,
    transport: str = ...,
    clean_session: bool = ...,
    proxy_args: Any | None = ...,
): ...
