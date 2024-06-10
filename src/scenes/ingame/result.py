# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

from typing import Any

from constants import screen
from recognizers.digit import DigitReader
from scenes.base import *
from utils.images import calcSimilarity, Frame

# Correlation Param
GRIZZ_THRESHOLD = 0.9

class ResultScene(Scene):
	def __init__(self, reader: DigitReader) -> None:
		self.__reader = reader
		self.__mrgrizzTemplate = Scene.loadTemplate('mrgrizz')

	async def analysis(self, context: SceneContext, data: Any, frame: Frame) -> SceneStatus:
		# Detect "Mr. Grizz"
		grizzImage = frame.apply(screen.GRIZZ_PART)
		grizzSim = calcSimilarity(grizzImage, self.__mrgrizzTemplate)

		if grizzSim < GRIZZ_THRESHOLD:
			return SceneStatus.FALSE

		# Read "golden"
		goldenImage = frame.apply(screen.GEGG_PART)
		goldenInt = self.__reader.read(goldenImage)

		# Read "power"
		powerImage = frame.apply(screen.PEGG_PART)
		powerInt = self.__reader.read(powerImage)

		if goldenInt is None or powerInt is None:
			return SceneStatus.FALSE

		# Send message
		message = {
			'golden': goldenInt,
			'power': powerInt,
		}
		await context.sendImmediately(SceneEvent.GAME_RESULT, message)

		return SceneStatus.DONE
