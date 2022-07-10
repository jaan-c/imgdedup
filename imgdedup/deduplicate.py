from typing import Iterable, List
import statistics
import dataclasses
from imgdedup.phash import phash_image_file, hamming_distance_percent


@dataclasses.dataclass(frozen=True)
class _Image:
    path: str
    phash: int


def group_duplicate_images(
    paths: Iterable[str],
    threshold: float,
) -> List[List[str]]:
    images: List[_Image] = []
    for p in paths:
        phash = phash_image_file(p)
        images.append(_Image(p, phash))

    groups: List[List[_Image]] = []
    for image in images:
        fit_group_ix = -1
        for ix, group in enumerate(groups):
            phash_group = (i.phash for i in group)
            average_distance = _average_hamming_distance_percent(
                phash,
                phash_group,
            )
            if average_distance <= threshold:
                fit_group_ix = ix
                break

        if fit_group_ix > -1:
            groups[fit_group_ix].append(image)
        else:
            groups.append([image])

    return [[i.path for i in g] for g in groups]


def _average_hamming_distance_percent(
    phash: int,
    phash_group: Iterable[int],
) -> float:
    distances = (hamming_distance_percent(phash, ps) for ps in phash_group)
    return statistics.fmean(distances)
