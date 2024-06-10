# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

import cv2 as cv
import numpy as np

def calcSimilarity(image1: np.ndarray, image2: np.ndarray) -> np.float64:
	minShape = np.minimum(image1.shape, image2.shape)
	if not np.array_equal(minShape, image1.shape):
		image1 = image1[:minShape[0], :minShape[1]]
	if not np.array_equal(minShape, image2.shape):
		image2 = image2[:minShape[0], :minShape[1]]

	diff = cv.absdiff(image1, image2)
	similarity = 1 - 0.01 * diff.mean()
	return similarity

def calcSimilarities(targetImage: np.ndarray, imageset: dict[str, np.ndarray]) -> dict[str, np.float64]:
	similarities = {
		k: calcSimilarity(image, targetImage)
		for k, image in imageset.items()
	}
	return similarities

def getMaxSimilarityKey(
	targetImage: np.ndarray,
	imageset: dict[str, np.ndarray],
	threshold: float = 0.8,
) -> str | None:
	similarities = {
		k: s
		for k, s in calcSimilarities(targetImage, imageset).items()
		if s >= threshold
	}

	if len(similarities) > 0:
		key = max(similarities, key=lambda key: similarities[key])
		return key
	else:
		return None
