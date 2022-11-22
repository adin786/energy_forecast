import sys

import git
from loguru import logger

logger.remove()
logger.add(sys.stderr, filter=__name__, level="INFO")


def repo_root(path="."):
    repo = git.Repo(path, search_parent_directories=True)
    repo_path = repo.working_tree_dir
    return repo_path
