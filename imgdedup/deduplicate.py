from typing import Iterable, Iterator, List
import dataclasses
from imgdedup.phash import phash_image_file, hamming_distance_percent


@dataclasses.dataclass(frozen=True)
class ImagePhash:
    path: str
    phash: int


def phash_images(paths: Iterable[str]) -> Iterator[ImagePhash]:
    for p in paths:
        phash = phash_image_file(p)
        yield ImagePhash(p, phash)


def group_duplicate_images(
    image_phashes: Iterable[ImagePhash],
    threshold: float,
) -> List[List[str]]:
    groups: List[List[ImagePhash]] = []
    for imgp in image_phashes:
        fit_group_ix = -1
        for ix, group in enumerate(groups):
            distances = map(
                lambda i: hamming_distance_percent(imgp.phash, i.phash), group
            )
            if any(d <= threshold for d in distances):
                fit_group_ix = ix
                break

        if fit_group_ix > -1:
            groups[fit_group_ix].append(imgp)
        else:
            groups.append([imgp])

    duplicates = filter(lambda g: len(g) > 1, groups)
    return [[i.path for i in g] for g in duplicates]
