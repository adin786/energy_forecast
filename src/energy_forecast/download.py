from py_compile import _get_default_invalidation_mode
import requests
from pathlib import Path
from .utils import repo_root


REPO_ROOT = Path(repo_root())


def download_file(url, dest_path):
    dest_path = Path(dest_path)
    if not dest_path.is_dir():
        raise ValueError('dest_path must be a folder path') 

    r = requests.get(url, allow_redirects=True)
    if not r.ok: 
         raise ValueError(f'Bad response from {url}')
    
    dest_file = dest_path / Path(url).name 
    with dest_file.open('wb') as f:
        f.write(r.content)

    return dest_file



