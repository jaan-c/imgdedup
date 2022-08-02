from typing import List, Dict
import sys
import datetime
import os
from os import path as pathlib
import shutil
import random
from imgdedup import cli, fs, deduplicate


def print_image_groups(image_groups: List[List[str]]) -> None:
    for ix, group in enumerate(image_groups):
        print(str(ix).ljust(len(image_groups), "0") + ":")
        for img in group:
            print("\t" + img)


def copy_image_groups(image_groups: List[List[str]], outdir: str) -> None:
    for ix, group in enumerate(image_groups):
        group_dir_name = str(ix).ljust(len(image_groups), "0")
        group_dir = pathlib.join(outdir, group_dir_name)

        os.makedirs(group_dir)
        copy_multiple(group, group_dir)


def move_image_groups(image_groups: List[List[str]], outdir: str) -> None:
    for ix, group in enumerate(image_groups):
        group_dir_name = str(ix).ljust(len(image_groups), "0")
        group_dir = pathlib.join(outdir, group_dir_name)

        os.makedirs(group_dir)
        move_multiple(group, group_dir)


def copy_multiple(sources: List[str], destination: str) -> None:
    src_dest: Dict[str, str] = {}
    for s in sources:
        base = pathlib.basename(s)
        dest = pathlib.join(destination, base)

        if dest in src_dest.values():
            dest = append_random_to_path(dest)

        src_dest[s] = dest

    for src, dest in src_dest.items():
        shutil.copy2(src, dest)


def move_multiple(sources: List[str], destination: str) -> None:
    src_dest: Dict[str, str] = {}
    for s in sources:
        base = pathlib.basename(s)
        dest = pathlib.join(destination, base)

        if dest in src_dest.values():
            dest = append_random_to_path(dest)

        src_dest[s] = dest

    for src, dest in src_dest.items():
        shutil.move(src, dest)


def append_random_to_path(path: str) -> str:
    head, ext = pathlib.splitext(path)

    alphanum = "abcdefghijklmnopqrstuvwxyz0123456789"
    chars = random.choices(alphanum, k=6)
    tail = "".join(chars)

    return head + tail + ext


if __name__ == "__main__":
    args = cli.parse()
    if not args:
        sys.exit()

    images = fs.find_image_files(args.paths)
    image_groups = deduplicate.group_duplicate_images(images, args.threshold)

    if args.mode == cli.CliMode.PRINT:
        print_image_groups(image_groups)
        sys.exit()

    outdir = (
        args.outdir or f"imgdedup{int(datetime.datetime.now().timestamp())}"
    )
    os.makedirs(outdir)
    if args.mode == cli.CliMode.COPY:
        copy_image_groups(image_groups, outdir)
    elif args.mode == cli.CliMode.MOVE:
        move_image_groups(image_groups, outdir)
