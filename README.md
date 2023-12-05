# Weather Data Analysis CLI

## Description
This command-line tool allows you to import weather data from a CSV file, perform data analysis, and save the results. The analysis includes identifying temperature trends, humidity changes, and the date with the highest wind speed within a specified date range.

## Features
- Import weather data from a CSV file.
- Analyze data based on a specified date range.
- Replace missing values with column means.
- Generate analysis results and save them to a file.

## Prerequisites
- Python 3.x
- Required Python packages (install using pip):
  - pandas
  - matplotlib
  - seaborn
  - Scikit-Learn

## Installation
1. Clone this repository or download the code.
2. Install the required Python packages

## Usage
1. Run the CLI by executing `main.py`

## Analyze weather data from January 1, 2016 (Start Date), to February 1, 2017(End Date)
python weather_analysis.py weather_data.csv --start_date 2016-01-01 --end_date 2017-02-01




