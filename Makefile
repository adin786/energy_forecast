.PHONY: clean requirements raw_data transform_data processed_data style data streamlit
.PHONY: init tf_apply lambda_reqs

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Install Python Dependencies
requirements:
	python -m pip install -r requirements.txt

# Transform into cleaned csv file
ENERGY_ODS := data/raw/Total_Energy_ODS.ods
WEATHER_ODS := data/raw/Weather_ODS.ods
TRANSFORMED_CSV := data/interim/transformed_energy_weather.csv
PROCESSED := data/processed/train.csv data/processed/test.csv

$(ENERGY_ODS) $(WEATHER_ODS):
	python scripts/01_download_raw.py

$(TRANSFORMED_CSV): $(ENERGY_ODS) $(WEATHER_ODS)
	python scripts/02_data_transform.py

# Download raw data
raw_data: $(ENERGY_ODS) $(WEATHER_ODS)

# Transform into a sanitised csv file
transform_data: $(TRANSFORMED_CSV)

$(PROCESSED): $(TRANSFORMED_CSV)
	python scripts/03_prepare_train_test.py

# Preprocessed train-test splits
processed_data: $(PROCESSED)

data: $(PROCESSED)

style:
	black ./energy_forecast \
		./app_lambda \
		./app_streamlit \
		./scripts

streamlit:
	streamlit run ./app_streamlit/Home_Page.py

init:
	terraform init

lambda_reqs:
	pip install --target ./app_lambda -r ./app_lambda/requirements.txt

tf_apply:
	terraform plan
	terraform apply
