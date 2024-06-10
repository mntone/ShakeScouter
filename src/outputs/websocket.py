# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

from anyio import sleep_forever, TASK_STATUS_IGNORED
from anyio.abc import TaskGroup, TaskStatus
from json import dumps
from websockets import broadcast, serve, WebSocketServerProtocol

from outputs.base import Output

class WebSocketOutput(Output):
	def __init__(self, args) -> None:
		self.__connections = set()
		self.__host = args.host
		self.__port = args.port

	async def setup(self, tg: TaskGroup):
		await tg.start(self.__runLoop)

	async def __onConnected(self, websocket: WebSocketServerProtocol):
		self.__connections.add(websocket)
		try:
			await websocket.wait_closed()
		finally:
			self.__connections.remove(websocket)

	async def __runLoop(self, task_status: TaskStatus[None] = TASK_STATUS_IGNORED):
		async with serve(self.__onConnected, self.__host, self.__port):
			task_status.started()
			await sleep_forever()

	def __sendMessage(self, message: Output.Message):
		jsonMessage = dumps(message)
		broadcast(self.__connections, jsonMessage)

	def onMessage(self, message: Output.Message):
		self.__sendMessage(message)
