from energy_forecast.download import download_file
from energy_forecast.utils import repo_root
from pathlib import Path
import click

REPO_ROOT = Path(repo_root())
URL_ENERGY = 'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1012959/Total_Energy_ODS.ods'
URL_WEATHER = 'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1012964/Weather_ODS.ods'
DEST_ENERGY = REPO_ROOT / 'data' / 'raw' / 'Total_Energy_ODS.ods'
DEST_WEATHER = REPO_ROOT / 'data' / 'raw' / 'Weather_ODS.ods'

@click.command
def main():
    print('Starting file download script')
    targets = [
        {'url': URL_ENERGY, 'dest': DEST_ENERGY},
        {'url': URL_WEATHER, 'dest': DEST_WEATHER},
    ]

    for t in targets:
        print(f"Downloading file from {t['url']}")

        download_file(t['url'], t['dest'])
        if t['dest'].is_file():
            print(f'File downloaded to {t["dest"]}')
        else:
            print(f'Download failed')

    print('Finished file download script')


if __name__ == "__main__":
    main()