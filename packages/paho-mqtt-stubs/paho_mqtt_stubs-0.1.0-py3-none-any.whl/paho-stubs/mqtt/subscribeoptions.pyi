from typing import Any

class MQTTException(Exception): ...

class SubscribeOptions:
    RETAIN_SEND_ON_SUBSCRIBE: Any
    RETAIN_SEND_IF_NEW_SUB: Any
    RETAIN_DO_NOT_SEND: Any
    QoS: Any
    noLocal: Any
    retainAsPublished: Any
    retainHandling: Any
    def __init__(
        self,
        qos: int = ...,
        noLocal: bool = ...,
        retainAsPublished: bool = ...,
        retainHandling=...,
    ) -> None: ...
    def __setattr__(self, name, value) -> None: ...
    def pack(self): ...
    def unpack(self, buffer): ...
    def json(self): ...
