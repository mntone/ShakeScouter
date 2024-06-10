# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

from copy import deepcopy
from typing import Any, Optional

from scenes.context import SceneContext, SceneEvent

class TestSceneContext(SceneContext):
	def __init__(self) -> None:
		self.__message = None

	async def sendImmediately(self, event: SceneEvent, message: Optional[dict[str, Any]] = None) -> None:
		if message is None:
			message = {
				'event': event.value,
			}
		else:
			message['event'] = event.value
		self.__message = message

	async def send(self, event: SceneEvent, message: dict[str, Any]) -> None:
		cloneMessage = deepcopy(message)
		cloneMessage['event'] = event.value
		self.__message = cloneMessage

	@property
	def message(self) -> Any:
		return self.__message
