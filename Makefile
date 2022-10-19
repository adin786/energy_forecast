.PHONY: clean requirements raw_data transform_data preprocess_data

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
	python -m pip install -U pip setuptools wheel
	python -m pip install -r requirements.txt

# Transform into cleaned csv file
ENERGY_ODS := data/raw/Total_Energy_ODS.ods
WEATHER_ODS := data/raw/Weather_ODS.ods
TRANSFORMED_CSV := data/interim/transformed_energy_weather.csv
Y_PREPROCESSED := data/processed/y_train.csv data/processed/y_test.csv 
X_PREPROCESSED := data/processed/x_train.csv data/processed/x_test.csv 

$(ENERGY_ODS) $(WEATHER_ODS):
	python scripts/01_download_raw.py

$(TRANSFORMED_CSV): $(ENERGY_ODS) $(WEATHER_ODS)
	python scripts/02_data_transform.py

# Download raw data
raw_data: $(ENERGY_ODS) $(WEATHER_ODS)

# Transform into a sanitised csv file
transform_data: $(TRANSFORMED_CSV)


$(Y_PREPROCESSED) $(X_PREPROCESSED): $(TRANSFORMED_CSV)
	python scripts/03_prepare_train_test.py

# Preprocessed train-test splits
preprocess_data: $(Y_PREPROCESSED) $(X_PREPROCESSED)


