from pathlib import Path
from ..utils import repo_root


def test_repo_root():
    output = repo_root()
    output_path = Path()
    assert isinstance(output, str)
    assert Path(output_path).is_dir()
