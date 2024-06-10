# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

from typing import Any

from constants import screen
from scenes.base import *
from utils.images import calcSimilarity, Frame

# Correlation Param
START_THRESHOLD = 0.9

class MatchmakingScene(Scene):
	def __init__(self) -> None:
		self.__startTemplate = Scene.loadTemplate('start')

	async def analysis(self, context: SceneContext, data: Any, frame: Frame) -> SceneStatus:
		# Detect "Start"
		startImage = frame.apply(screen.MESSAGE_PART)
		startSim = calcSimilarity(startImage, self.__startTemplate)

		if startSim < START_THRESHOLD:
			return SceneStatus.FALSE

		# Send message
		await context.sendImmediately(SceneEvent.MATCHMAKING)

		return SceneStatus.DONE
