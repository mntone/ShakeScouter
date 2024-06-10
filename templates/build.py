#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

import cv2 as cv
import numpy as np

from dataclasses import dataclass
from os import chdir, mkdir
from os.path import dirname, exists, join, realpath
from sys import path
from typing import Callable, Optional

# Set current working directory.
chdir(realpath(join(dirname(__file__), '../src/')))
path.append('.')

from constants import assets, env, screen
from utils.images import Frame
from utils.images.model import PartInfo

@dataclass
class AssetData:
	name: str
	input: str
	output: str
	part: PartInfo
	fn: Optional[Callable[[np.ndarray], np.ndarray]] = None

	def buildTemplate(self):
		outputPath = env.TEMPLATE_PATH.format(self.output)
		if exists(outputPath):
			print(f'[{self.name}] Mask file exists (path: {outputPath})')
		else:
			inputPath = env.DEV_ASSET_PATH.format(self.input)
			image = Frame(filepath=inputPath).apply(self.part)
			if self.fn is not None:
				image = self.fn(image)
			cv.imwrite(outputPath, image, [cv.IMWRITE_PNG_COMPRESSION, 0])


ASSET_INFO: list[AssetData] = [
	# Dialog Mask
	AssetData('Matchmaking', 'other/start',                  'start',              screen.MESSAGE_PART),

	# Intro Logo Mask
	AssetData('Intro Logo',  'stages/104_barnacle_and_dime', 'logo',               screen.LOGO_PART),

	# Wave Masks
	AssetData('Wave "n"',    'counts/count100',              'wave',               screen.WAVE_PART, lambda i: i[:, :-72]),
	AssetData('Extra Wave',  'other/wave-extra00',           'wave_ex',            screen.WAVE_PART),

	# Signal Mask
	#AssetData('Signal',      'other/gegg_all',               'signal',             screen.SIGNAL_PART),

	# Kings Masks
	AssetData('Cohozuna',    'kings/cohozuna00',             'kings/cohozuna',     screen.KING_NAME_PART),
	AssetData('Cohozuna',    'kings/horrorboros01',          'kings/horrorboros',  screen.KING_NAME_PART),
	AssetData('Cohozuna',    'kings/megalodontia01',         'kings/megalodontia', screen.KING_NAME_PART),
	AssetData('Cohozuna',    'kings/triumvirate04',          'kings/triumvirate',  screen.KING_NAME_PART),

	# Result Masks
	AssetData('Mr. Grizz',   'other/result02',               'mrgrizz',            screen.GRIZZ_PART),

	# Unstable and Error Masks
	AssetData('Unstable',    'other/unstable',               'unstable',           screen.UNSTABLE_PART),
	AssetData('Error',       'other/error',                  'error',              screen.ERROR_PART),
]

def buildStageTemplate():
	stageTemplateBasePath = env.TEMPLATE_PATH.format('stages/{}')
	stageTemplateDirPath = dirname(stageTemplateBasePath)
	if not exists(stageTemplateDirPath):
		mkdir(stageTemplateDirPath)

	for stageKey in assets.stageKeys:
		outputPath = stageTemplateBasePath.format(stageKey)
		if exists(outputPath):
			print(f'Stage mask file exists (path: {outputPath})')
		else:
			inputPath = env.DEV_ASSET_PATH.format(f'stages/{stageKey}')
			image = Frame(filepath=inputPath).apply(screen.STAGE_NAME_PART)
			cv.imwrite(outputPath, image, [cv.IMWRITE_PNG_COMPRESSION, 0])

def main():
	for asset in ASSET_INFO:
		asset.buildTemplate()
	buildStageTemplate()

if __name__ == "__main__":
	main()
