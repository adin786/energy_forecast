from energy_forecast.utils import repo_root
from energy_forecast.loaders import load_ods, load_ods_sheetnames
from energy_forecast.transform import clean_energy_data, clean_temp_data, \
    clean_wind_data, clean_sun_data, clean_rain_data
from pathlib import Path
import click
import pandas as pd
from loguru import logger

REPO_ROOT = Path(repo_root())
DATA_RAW = REPO_ROOT / 'data' / 'raw'
DATA_INTERIM = REPO_ROOT / 'data' / 'interim'
ENERGY_PATH = DATA_RAW / 'Total_Energy_ODS.ods'
ENERGY_SHEETNAME = '1_2'
WEATHER_PATH = DATA_RAW / 'Weather_ODS.ods'
TEMP_SHEET = '7_1a'
WIND_SHEET = '7_2'
SUN_SHEET = '7_3'
RAIN_SHEET = '7_4'


@click.command
def main():
    logger.info('Starting data transform script')

    logger.info('Loading energy .ods data')
    energy = load_ods(ENERGY_PATH, ENERGY_SHEETNAME)

    logger.info('Transforming energy data')
    energy = clean_energy_data(energy)

    logger.info('Loading weather .ods data')
    temp = load_ods(WEATHER_PATH, TEMP_SHEET)
    wind = load_ods(WEATHER_PATH, WIND_SHEET)
    sun = load_ods(WEATHER_PATH, SUN_SHEET)
    rain = load_ods(WEATHER_PATH, RAIN_SHEET)

    logger.info('Transforming weather data')
    temp = clean_temp_data(temp)
    wind = clean_wind_data(wind)
    sun = clean_sun_data(sun)
    rain = clean_rain_data(rain)

    logger.info('Joining datasets')
    weather = pd.concat([temp, wind, sun, rain], join='outer', axis=1)
    combined = pd.concat([energy, weather], join='outer', axis=1)

    logger.info('Saving combined dataframe to disk')
    combined.to_csv(DATA_INTERIM / 'transformed_energy_weather.csv')
    
    logger.info('Finished data transform script')


if __name__ == "__main__":
    main()