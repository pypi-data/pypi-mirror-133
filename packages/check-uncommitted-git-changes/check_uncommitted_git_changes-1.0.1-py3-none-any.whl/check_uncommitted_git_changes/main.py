# Copyright (c) 2022, Thomas Aglassinger.
# All rights reserved. Distributed under the BSD License.
import argparse
import logging
import subprocess
import sys

from check_uncommitted_git_changes import __version__

_log = logging.getLogger(__name__)


def main(args=None) -> int:
    logging.basicConfig(format="%(levelname)s %(message)s", level=logging.INFO)
    return main_without_logging_setup(args)


def main_without_logging_setup(args=None) -> int:
    _ = _parsed_args(args)
    result = 0
    _log.info("checking for uncommitted git changes")
    if has_uncommitted_git_changes():
        _log.error("found uncommitted changes")
        print_git_diffs()
        result = 1
    return result


def _parsed_args(args=None):
    parser = argparse.ArgumentParser(
        description="Check for uncommitted git changes to identify outdated generated content"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser.parse_args(args)


def has_uncommitted_git_changes() -> bool:
    git_output = subprocess.run(["git", "status", "--porcelain"], check=True, capture_output=True)
    return len(git_output.stdout) > 0


def print_git_diffs():
    subprocess.run(["git", "--no-pager", "diff"], check=True)


if __name__ == "__main__":
    sys.exit(main_without_logging_setup())
