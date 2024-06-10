# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

from typing import Any

from scenes import Scene, SceneContext, SceneStatus
from utils.images import Frame

class Drop(Scene):
	def __init__(self, child: Scene, rate: float = 1) -> None:
		self.__child = child
		self.__drop  = int(60.0 / rate) # TODO: Don't hardcode at 60fps

	def setup(self) -> Any:
		data = {
			'cache': SceneStatus.FALSE,
			'drop':  self.__drop,

			'child': self.__child.setup(),
		}
		return data

	def reset(self, data: Any) -> None:
		data['cache'] = SceneStatus.FALSE
		data['drop']  = self.__drop
		self.__child.reset(data['child'])

	async def analysis(self, context: SceneContext, data: Any, frame: Frame) -> SceneStatus:
		drop = data['drop']

		if self.__drop <= drop:
			drop = 0
			data['cache'] = await self.__child.analysis(context, data['child'], frame)
		else:
			drop = drop + 1

		# Store "drop" to context
		data['drop'] = drop

		return data['cache']
