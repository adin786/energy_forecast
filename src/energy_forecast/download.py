import requests
from pathlib import Path
from .utils import repo_root
from loguru import logger

REPO_ROOT = Path(repo_root())


def download_file(url, dest_file):
    dest_file = Path(dest_file)
    if dest_file.is_file():
        logger.warning('dest_file already exists, overwriting.') 

    r = requests.get(url, allow_redirects=True)
    if not r.ok: 
         raise ValueError(f'Bad response from {url}')

    with dest_file.open('wb') as f:
        f.write(r.content)

    if not dest_file.is_file():
        raise ValueError('Download failed')
    return



