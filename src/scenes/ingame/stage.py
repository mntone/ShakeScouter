# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

from typing import Any

from constants import assets, screen
from scenes.base import *
from utils.images import calcSimilarity, Frame, getMaxSimilarityKey

# Correlation Param
LOGO_THRESHOLD = 0.8
NAME_THRESHOLD = 0.8

class StageScene(Scene):
	def __init__(self) -> None:
		self.__logoTemplate = Scene.loadTemplate('logo')

		stageTemplates = {
			key: Scene.loadTemplate(f'stages/{key}')
			for key in assets.stageKeys
		}
		self.__stageTemplates = {
			k: v
			for k, v in stageTemplates.items()
			if v is not None
		}

	async def analysis(self, context: SceneContext, data: Any, frame: Frame) -> SceneStatus:
		logoImage = frame.apply(screen.LOGO_PART)
		logoSim = calcSimilarity(logoImage, self.__logoTemplate)

		if logoSim < LOGO_THRESHOLD:
			return SceneStatus.FALSE

		stageImage = frame.apply(screen.STAGE_NAME_PART)
		stageKey = getMaxSimilarityKey(
			stageImage,
			self.__stageTemplates,
			threshold=NAME_THRESHOLD
		)

		if stageKey is None:
			return SceneStatus.FALSE

		# Send message
		message = {
			'stage': stageKey[4:],
		}
		await context.sendImmediately(SceneEvent.GAME_STAGE, message)

		return SceneStatus.DONE
