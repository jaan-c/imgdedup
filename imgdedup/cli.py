from typing import List, Optional
import dataclasses
import enum
import argparse
import sys


class CliMode(enum.Enum):
    PRINT = "print"
    COPY = "copy"
    MOVE = "move"


DEFAULT_ARG_MODE = CliMode.PRINT
DEFAULT_ARG_THRESHOLD = 0.4


@dataclasses.dataclass(frozen=True)
class CliArgs:
    paths: List[str]
    mode: CliMode = dataclasses.field(default=DEFAULT_ARG_MODE)
    outdir: Optional[str] = dataclasses.field(default=None)
    threshold: float = dataclasses.field(default=DEFAULT_ARG_THRESHOLD)


def parse(raw_args: Optional[List[str]] = None) -> Optional[CliArgs]:
    if not raw_args:
        raw_args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Deduplicate images with perceptual hash."
    )
    parser.add_argument(
        "--mode",
        default=DEFAULT_ARG_MODE.value,
        choices=[
            CliMode.PRINT.value,
            CliMode.COPY.value,
            CliMode.MOVE.value,
        ],
        help="What to do with duplicate images; `print` displays groups of duplicate image paths, `copy` and `move` copies or moves duplicate images to outdir.",
    )
    parser.add_argument(
        "--outdir",
        help="Where to place copied or moved duplicate images, ignored when --mode is print.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_ARG_THRESHOLD,
        help="Percentage of how much difference to tolerate between images, 0 to 1 only.",
    )
    parser.add_argument(
        "paths",
        nargs="+",
    )

    try:
        args = parser.parse_args(raw_args)
    except argparse.ArgumentError:
        return None

    if args.mode == CliMode.PRINT.value:
        mode = CliMode.PRINT
    elif args.mode == CliMode.COPY.value:
        mode = CliMode.COPY
    elif args.mode == CliMode.MOVE.value:
        mode = CliMode.MOVE
    else:
        raise RuntimeError(f"Unhandled --mode {args.mode}")

    outdir: Optional[str] = args.outdir

    threshold: float = args.threshold
    if not (0 <= threshold <= 1):
        parser.print_help()
        return None

    paths: List[str] = args.paths

    return CliArgs(paths, mode, outdir, threshold)
