# Energy_forecast

This repo will contain some timeseries forecast modelling of energy demand based on historic data published on data.gov.uk.

The datasets are:
- [Energy Trends - ET1.2 September 2022](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1107641/ET_1.2_SEP_22.xlsx)
- [Weather historic data](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1012964/Weather_ODS.ods)

## Prerequisites
```
make requirements   # installs python dependencies
make data           # downloads raw data files
```