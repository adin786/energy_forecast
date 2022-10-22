# Energy_forecast

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repo will be used to perform timeseries forecasting of energy demand based on historic energy data from the UK government.

## Data source

The datasets were downloaded from data.gov.uk and are openly available.  Specifically these tables come from the regularly updated Energy Trends publication by the BEIS department.  Additionally data on historic weather patterns (UK average) were also sourced from this site.

- [Energy Trends - ET1.2 September 2022](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1107641/ET_1.2_SEP_22.xlsx)
- [Weather historic data](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1012964/Weather_ODS.ods)

Data ingest from the above pages is fully scripted.  In theory these scripts could be re-run in future to get the most up-to-date tables, however the exact file formatting has been known to be adjusted over time.  You may therefore need to update the data cleaning/transformation scripts.

For convenience, snapshots of the source data (as of Oct 2022) are checked into the repo for archival.

## Requirements

For maximum reproducibility all development was done inside a vscode devcontainer, see `.devcontainer/Dockerfile`. Open this folder with VSCode to access it.

Alternatively you may directly install `requirements.txt` and also the included `energy_forecast` package to make the code work.  This has been developed with Python 3.9.13.

```bash
git clone https://github.com/adin786/energy_forecast.git
cd energy_forecast
pip install -r requirements.txt
pip install git+https://github.com/adin786/energy_forecast.git
```

## Makefile
The following `make` commands are configured.  All analysis notebooks and scripts expect these files to exist.

```
make requirements       # install python dependencies
make data               # prepare all data files
make style
```

## Data cleaning
...in progress

## Exploration
...in progress

## Forecasting
...in progress