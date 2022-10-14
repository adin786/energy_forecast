from energy_forecast.download import download_file
from energy_forecast.utils import repo_root
from pathlib import Path
import click

REPO_ROOT = Path(repo_root())

@click.command
def main():
    print('Starting file download script')

    URL_ENERGY = 'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1012959/Total_Energy_ODS.ods'
    URL_WEATHER = 'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1012964/Weather_ODS.ods'
    DEST_PATH = REPO_ROOT / 'data' / 'raw'

    for url in [URL_ENERGY, URL_WEATHER]:
        print(f"Downloading file from {url}")

        dest_file = download_file(url, DEST_PATH)
        if dest_file.is_file():
            print(f'File downloaded to {dest_file}')
        else:
            print(f'Download failed')

    print('Finished file download script')


if __name__ == "__main__":
    main()