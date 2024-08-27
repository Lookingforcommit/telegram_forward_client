# (c) @Lookingforcommit

from abc import ABC, abstractmethod
from typing import Dict, Any

from pyrogram import Client
from pyrogram.types import Message


class BaseScenario(ABC):
    DESCRIPTION = "Base class for scenarios"
    ARGUMENTS_TYPES: Dict[str, Any] = {}
    ARGUMENTS_INFO: Dict[str, str] = {}

    @abstractmethod
    async def apply(self, client: Client, message: Message, **kwargs) -> Message:
        pass

    def process_arguments(self, dct: Dict[str, Any]) -> Dict[str, Any]:
        for key in dct:
            dct[key] = self.ARGUMENTS_TYPES[key](dct[key])
        return dct
