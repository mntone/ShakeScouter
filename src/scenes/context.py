# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

from anyio.streams.memory import MemoryObjectSendStream
from copy import deepcopy
from time import time
from typing import Any, Optional

from scenes.base import SceneContext, SceneEvent

class SceneContextImpl(SceneContext):
	EXCLUDE_KEYS = set(['event', 'timestamp'])

	def __init__(self, streams: list[MemoryObjectSendStream[Any]] = []) -> None:
		self.__cache: dict[SceneEvent, dict[str, Any]] = {}
		self.__streams = streams

	def __del__(self) -> None:
		for stream in self.__streams:
			stream.close()

	async def __send(self, message: dict[str, Any]) -> None:
		for stream in self.__streams:
			await stream.send(message)

	async def sendImmediately(self, event: SceneEvent, message: Optional[dict[str, Any]] = None) -> None:
		eventMessage = {
			'event': event.value,
			'timestamp': time(),
		}

		if message is not None:
			# Set additional field
			for key, val in message.items():
				eventMessage[key] = deepcopy(val)

		# Send
		await self.__send(eventMessage)

	async def send(self, event: SceneEvent, message: dict[str, Any]) -> None:
		def compare(dict1: dict, dict2: dict, exclude: set[str]):
			keys1 = set(dict1.keys()) - exclude
			keys2 = set(dict2.keys()) - exclude
			match = all(dict1[key] == dict2[key] for key in keys1 & keys2)
			return match

		# Compare cache
		if event in self.__cache:
			if compare(self.__cache[event], message, SceneContextImpl.EXCLUDE_KEYS):
				return

		eventMessage = {
			'event': event.value,
			'timestamp': time(),
		}

		# Set additional field
		for key, val in message.items():
			eventMessage[key] = deepcopy(val)

		# Add clone message to cache
		self.__cache[event] = eventMessage

		# Send
		await self.__send(eventMessage)
