# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

from typing import Any

from constants import assets, screen
from scenes.base import *
from utils.images import Frame, getMaxSimilarityKey

# Correlation Param
KING_THRESHOLD = 0.8

class KingScene(Scene):
	def __init__(self) -> None:
		kingTemplates = {
			key: Scene.loadTemplate(f'kings/{key}')
			for key in assets.kingKeys
		}
		self.__kingTemplates = {
			k: v
			for k, v in kingTemplates.items()
			if v is not None
		}

	async def analysis(self, context: SceneContext, data: Any, frame: Frame) -> SceneStatus:
		kingImage = frame.apply(screen.KING_NAME_PART)
		kingKey = getMaxSimilarityKey(
			kingImage,
			self.__kingTemplates,
			threshold=KING_THRESHOLD
		)

		if kingKey is None:
			return SceneStatus.FALSE

		# Send message
		message = {
			'king': kingKey,
		}
		await context.sendImmediately(SceneEvent.GAME_KING, message)

		return SceneStatus.DONE
