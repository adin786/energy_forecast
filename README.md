# Energy_forecast

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repo will be used to perform timeseries forecasting of energy demand based on historic energy data from the UK government.

## Data source

The datasets were downloaded from data.gov.uk and are openly available.  Specifically these tables come from the regularly updated Energy Trends publication by the BEIS department.  Additionally data on historic weather patterns (UK average) were also sourced from this site.

- [Energy Trends - ET1.2 September 2022](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1107641/ET_1.2_SEP_22.xlsx)
- [Weather historic data](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1012964/Weather_ODS.ods)

Data ingest from the above pages is fully scripted.  In theory these scripts could be re-run in future to get the most up-to-date tables, however the exact file formatting has been known to be adjusted over time.  You may therefore need to update the data cleaning/transformation scripts.

For reproducibility, all analysis in this repo was performed on the above tables dated Oct 2022.  Raw files for this date are checked into the repo under `data/raw`.

## Data Engineering / Cleaning

- Data files parsed, transformed into monthly timeseries dataframe.
- Temporal train-test split (80:20) applied.
- Target variable (for forecasting) set as "Total Energy" consumption.
- Saved as .csv
- DVC used for data version control, remote stored in GDrive
- ...

## Exploration

- See `notebooks/03_data_exploration.ipynb` for visuals and summary
- ...

## Forecasting

- Variety of forecaster models trained
- Mlflow used for experiment tracking
- ...

## Deployment

- Model deployed for inference as REST-api
- Hosted as serverless Lambda function on AWS
- Streamlit web-app for interactive use
- ...

## Requirements / Reproducibility

All code is developed inside a vscode devcontainer. For configuration, see `.devcontainer/Dockerfile`. Clone and open this repo folder with VSCode to build and attach to the dev environment.  

All code developed for `Python 3.9.13`.

## Helpful commands

See `Makefile` for some useful commands like: 

```
make requirements       # install dependencies
make data               # process all data
make style              # apply black formatter

```
