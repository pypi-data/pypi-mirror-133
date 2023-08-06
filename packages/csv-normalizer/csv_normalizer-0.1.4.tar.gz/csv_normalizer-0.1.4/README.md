****
Info
****

This is just a simple script that ensures all your .csv files have always same columns and in the same order. Probably
one of the most common issues with .csv files: 

* Some system doesn't respects the columns orders
* Some system doesn't adds a column when there is no data for such column

The script/program resolves both cases in a simple way, process:

Process: 
![alt text](csv_normalizer_process.png "Diagram process")

Normalize: ensure order of columns is always same, add missing columns with empty data.

Example, you have a meteorologic station that should always generate a .csv with the following columns

    Temperature, Humidity, Radiation, Wind, Wind gust

But sometimes one of the sensors doesn't have data and instead of sending all the columns to the .csv it generates partial .csv

    Temperature, Humidity, Wind, Wind gust

In this case the software that process the .csv could fail, so you can use the csv_normalizer to ensure the .csv file is always

    Temperature, Humidity, Radiation, Wind, Wind gust

In this case the csv_normalizer will add the missing column with empty data.
Also the csv_normalizer will ensure the order of the columns is always the same.

Returns always a dict/json like, with the 'ok' or 'fail' list of processed files.
examples:

```sh
{'failed': [],
'ok': [
    {'export_path': 'C:\\temp\\csv_export\\business-financial-data-jun-2021-quarter.csv',
        'import_path': 'C:\\temp\\csv_import\\business-financial-data-jun-2021-quarter.csv'}
        ]
}

# Example when nothing was processed:
{'failed': [],
'ok': []}
```

***************
Example config:
***************

```ini
[common]
csv_import_folder = C:/temp/csv_import
csv_export_folder = C:/temp/csv_export
csv_export_headers = 'Series_reference', 'Period', 'ELEE'
csv_delimiter = ;
csv_encoding = utf-8
# You can use column types, like int64, np.float64 if you want to specify
 # Or you can use type object if you don't want conversion or avoid NaN errors
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
# example: {'column name': 'object'}
'dtype' = {}
```

*****
Usage
*****

```sh
usage: csv_normalizer [-h] [-c [CONFIG_INI]] [--version [VERSION]] [--no_rename [NO_RENAME_OLD]] [--write_config]

optional arguments:
-h, --help            show this help message and exit
-c [CONFIG_INI],      --config_ini [CONFIG_INI]
                        csv_normalizer ini configuration file
--version [VERSION]   Print version and exit
--no_rename [NO_RENAME_OLD]
                        Do not rename to .old the original file
--write_config        Write configuration with default values, useful to get a config file to modify
```

Example usage on Linux

    csv_normalizer -c .\csv_normalizer.ini

On windows:

    csv_normalizer.exe -c .\csv_normalizer.ini

Adding option to not rename the original files:

    csv_normalizer -c .\csv_normalizer.ini --no_rename

By default csv_normalizer will rename the original files to .old so if you run the program again, it will not process same files again.

*******
Install
*******

```sh
pip install --user csv_normalizer

# or for root account

pip install csv_normalizer
```

******
Author
******

Author: Pablo Estigarribia <pablodav at gmail dot com>

Project site: https://github.com/CoffeeITWorks/csv_normalizer
