# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

from os import chdir
from parameterized import parameterized
from pathlib import Path
from unittest import IsolatedAsyncioTestCase

from constants import Color, env
from recognizers import selectDevice
from recognizers.digit import DigitReader
from scenes import SceneEvent, SceneStatus
from scenes.ingame import WaveScene
from scenes.contexttest import TestSceneContext
from utils.images import Frame

COLORS = [
	Color.BLUE,
	Color.SUNYELLOW,
	Color.YELLOW,
]

class TestWaveScene(IsolatedAsyncioTestCase):
	@classmethod
	def setUpClass(cls):
		currentDir = Path(__file__)
		sourceDir  = next(p for p in currentDir.parents if p.name == 'src')
		chdir(sourceDir)

		device = selectDevice('cpu')
		reader = DigitReader(device)
		cls.__ctx   = TestSceneContext()
		cls.__scene = WaveScene(reader)

	@parameterized.expand([[color] for color in COLORS])
	async def test_analysisColor(self, color: Color):
		filepath = env.DEV_ASSET_PATH.format(f'other/color_{color.name}')

		data = self.__scene.setup()
		frame = Frame(filepath=filepath)

		ret = await self.__scene.analysis(self.__ctx, data, frame)
		self.assertEqual(ret, SceneStatus.CONTINUE)
		self.assertEqual(self.__ctx.message['event'], SceneEvent.GAME_UPDATE.value)
		self.assertEqual(self.__ctx.message['color'], color.value.name, color.value)

	@parameterized.expand([
		('test_dead', Color.YELLOW, False, True, True, True)
	])
	async def test_analysisAlive(self, filename: str, color: Color, a0: bool, a1: bool, a2: bool, a3: bool):
		filepath = env.DEV_ASSET_PATH.format(f'other/{filename}')
		frame = Frame(filepath=filepath)

		data = self.__scene.setup()
		data['color'] = color

		ret = await self.__scene.analysis(self.__ctx, data, frame)
		self.assertEqual(ret, SceneStatus.CONTINUE)
		self.assertEqual(self.__ctx.message['event'], SceneEvent.GAME_UPDATE.value)
		self.assertEqual(self.__ctx.message['players'][0]['alive'], a0)
		self.assertEqual(self.__ctx.message['players'][1]['alive'], a1)
		self.assertEqual(self.__ctx.message['players'][2]['alive'], a2)
		self.assertEqual(self.__ctx.message['players'][3]['alive'], a3)
