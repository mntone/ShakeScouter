# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

from copy import deepcopy
from time import time
from typing import Any, Optional

from scenes.context import SceneContext, SceneEvent

class TestSceneContext(SceneContext):
	def __init__(self) -> None:
		self.__message = None
		self.__session = str(time())

	def __newSession(self) -> str:
		self.__session = str(time())
		return self.__session

	@property
	def session(self) -> str:
		return self.__session

	async def sendImmediately(self, event: SceneEvent, message: Optional[dict[str, Any]] = None) -> None:
		eventMessage = {
			'session': self.__newSession() if event == SceneEvent.MATCHMAKING else self.session,
			'event': event.value,
			'timestamp': time(),
		}

		if message is not None:
			# Set additional field
			for key, val in message.items():
				eventMessage[key] = deepcopy(val)

		self.__message = eventMessage

	async def send(self, event: SceneEvent, message: dict[str, Any]) -> None:
		await self.sendImmediately(event, message)

	@property
	def message(self) -> Any:
		return self.__message
