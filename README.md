# Energy_forecast 
  
In this project I demonstrate a simple architecture for serverless ML model deployment, building in MLOps principles such as experiment tracking, data versioning and model monitoring.

This project uses only free-tier cloud services, and is geared towards DIY, personal ML projects.


## Technical overview

- **Jupyter** for exploration and model building
- Custom **Python package** for bundling up into a reusable pipeline.
- **Sktime** as framework for forecaster model development 
- **DVC** for dataset versioning, synced to S3
- **Mlflow** for experiment tracking
- Serverless model inference on **AWS Lambda**
- **Streamlit** web-app for interactive demo
- **GH-actions** for continuous deployment:
  - **Pytest** suite of unit tests
  - **Docker** image build & push to **ECR**
  - **Terraform** to manage infra-as-code
- Monitoring with **Cloudwatch**.

![Insert architecture diagram]()


## Data source 
   The datasets were downloaded from data.gov.uk and are openly available.
Specifically these tables come from the regularly updated Energy Trends publication by the BEIS department.
Additionally data on historic weather patterns (UK average) were also sourced from this site.

- [Energy Trends - ET1.2 September 2022](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1107641/ET_1.2_SEP_22.xlsx) 
- [Weather historic data](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1012964/Weather_ODS.ods) 
  
Data ingest from the above pages is fully scripted.  
In theory these scripts could be re-run in future to get the most up-to-date tables, however the exact file formatting has been known to be adjusted over time.  
You may therefore need to update the data cleaning/transformation scripts. 
 For reproducibility, all analysis in this repo was performed on the above tables dated Oct 2022.  Raw files for this date are checked into the repo under `data/raw`. 


## Data Engineering / Cleaning 
 - Data files parsed, transformed into monthly timeseries dataframe. 
- Temporal train-test split (80:20) applied.  - Target variable (for forecasting) set as "Total Energy" consumption. 
- Saved as .csv 
- DVC used for data version control, remote stored in GDrive 


## Exploration 
  
- See `notebooks/03_data_exploration.ipynb` for visuals and summary 


## Forecasting 

- Variety of forecaster models trained 
- Mlflow used for experiment tracking 
- ... 

## Deployment 
  - Deploy model inference api as a **serverless lambda function**
- Deploy interactive front-end as **Streamlit web-app**. 
- Keeping lightweight front-end by abstracting all ML code to lambda. - Using **Docker multi-stage build** to keep image size small (<300mb to stay within ECR free tier). 
- Using **Terraform** to deploy all cloud resources.  Enables easy `terraform destroy` to teardownall cloud resources if it starts to cost money.

  
## Requirements / Reproducibility 
  
All developement done inside a vscode devcontainer. For configuration, see `.devcontainer/Dockerfile`.
Clone and open this repo folder with VSCode to build and attach to the dev environment.
All code developed for `Python 3.9.13`.


## Helpful commands
  
See `Makefile` for some useful commands like:  
  
```bash
 make requirements       # install dependencies 
 make data               # process all data 
 make style              # apply black formatter   
```


## Future enhancements

- Add prediction intervals
- Add pipeline to download latest datafiles from gov.uk and update models.
- Introduce API gateway to expose forecaster as an open REST API.


## Other

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
