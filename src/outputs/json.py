# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

from datetime import datetime
from json import dump

from constants import env
from outputs.base import Output
from scenes.base import SceneEvent

JSON_FILENAME = 'telemetry_%Y%m%d-%H%M'

class JsonOutput(Output):
	def __init__(self, _) -> None:
		self.__curPath = None

	async def setup(self, _):
		pass

	def __writeFile(self, message: Output.Message) -> None:
		if self.__curPath is None or message['event'] == SceneEvent.MATCHMAKING.value:
			self.__curPath = JsonOutput.__getNewFilepath()

		with open(self.__curPath, 'a', encoding='utf8') as fh:
			dump(message, fh, separators=(',', ':'))
			fh.write('\n')

	def onMessage(self, message: Output.Message):
		self.__writeFile(message)

	@staticmethod
	def __getNewFilepath() -> str:
		date = datetime.now()
		filename = date.strftime(JSON_FILENAME)
		filepath = env.TELEMETRY_PATH.format(filename)
		return filepath
