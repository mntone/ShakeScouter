# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

from typing import Any

from constants import screen
from scenes.base import *
from utils.images import calcSimilarity, Frame

# Correlation Param
ERROR_THRESHOLD = 0.9

class ErrorScene(Scene):
	def __init__(self) -> None:
		self.__errorTemplate = Scene.loadTemplate('error')

	async def analysis(self, context: SceneContext, data: Any, frame: Frame) -> SceneStatus:
		# Detect error message
		errorImage = frame.apply(screen.ERROR_PART)
		errorSim = calcSimilarity(errorImage, self.__errorTemplate)

		if errorSim < ERROR_THRESHOLD:
			return SceneStatus.FALSE

		# Send message
		await context.sendImmediately(SceneEvent.GAME_ERROR)

		return SceneStatus.DONE
