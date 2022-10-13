from energy_forecast.download import download_file
from energy_forecast.utils import repo_root
from pathlib import Path
import click

REPO_ROOT = Path(repo_root())

@click.command
def main():
    print('Starting file download script')

    URL_ENERGY = 'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1107641/ET_1.2_SEP_22.xlsx'
    DEST_PATH = REPO_ROOT / 'data' / 'raw'
    print(f"Downloading file from {URL_ENERGY}")

    dest_file = download_file(URL_ENERGY, DEST_PATH)

    if dest_file.is_file():
        print(f'File downloaded to {dest_file}')
    else:
        print(f'Download failed')

    print('Finished file download script')


if __name__ == "__main__":
    main()