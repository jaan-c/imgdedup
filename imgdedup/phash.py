from typing import *
from PIL import Image
import math
import statistics


def phash_image_file(image_path: str) -> int:
    image = Image.open(image_path)
    image = image.resize((32, 32))
    image = image.convert("L")
    luminance = list(image.getdata())

    dct = _dct_luminances(luminance)
    dct = dct[:64]

    average = statistics.fmean(dct[1:])

    phash = 0
    for d in dct:
        bit = int(d > average)
        phash <<= 1
        phash += bit

    return phash


def _dct_luminances(luminance: List[int]) -> List[float]:
    length = len(luminance)
    factor = math.pi / length

    result: List[float] = []
    for i in range(length):
        sum = 0.0
        for j, lum in enumerate(luminance):
            sum += lum * math.cos((j + 0.5) * i * factor)

        result.append(sum)

    return result


def hamming_distance(a: int, b: int) -> int:
    diff = a ^ b
    count = 0
    while diff > 0:
        count += diff & 1
        diff >>= 1

    return count


def hamming_distance_percent(a: int, b: int) -> float:
    return hamming_distance(a, b) / 64
