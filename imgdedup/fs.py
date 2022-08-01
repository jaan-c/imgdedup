from typing import List, Iterator
import os
import os.path as pathlib


def find_image_files(
    paths: List[str],
    extensions=["jpg", "jpeg", "png", "webp", "gif"],
) -> Iterator[str]:
    for p in paths:
        if pathlib.isdir(p):
            files = _walk_files_absolute(p)
            yield from filter(
                lambda f: _has_any_extension(f, extensions), files
            )
        else:
            if _has_any_extension(p, extensions):
                yield pathlib.abspath(p)


def _has_any_extension(file: str, extensions: List[str]) -> bool:
    return any(file.endswith("." + e) for e in extensions)


def _walk_files_absolute(root: str) -> Iterator[str]:
    for dirpath, _, filenames in os.walk(root):
        for n in filenames:
            file = pathlib.join(dirpath, n)
            yield pathlib.abspath(file)
