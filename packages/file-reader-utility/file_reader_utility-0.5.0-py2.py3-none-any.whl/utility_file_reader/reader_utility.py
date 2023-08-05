from datetime import datetime
import pandas as pd
import datetime
import json
from configparser import ConfigParser
import os
from pathlib import Path
import sys


def get_project_root_unorthodox(venv_root) -> Path:
    # return Path(__file__).parent.parent.parent
    return Path(venv_root).parent.parent.parent


def get_project_venv_root():
    return os.path.dirname(sys.modules['__main__'].__file__)


def trim_with_strip(column_of_data_set):
    return column_of_data_set.strip()


def fill_na_to_null(data_frame):
    return data_frame.fillna('null')


def fill_na_and_blank_to_null(data_frame):
    data_frame = data_frame.fillna('null')
    return data_frame.replace('', 'null')


def reader_without_configuration_file(file_extension, path_from_repository_root_with_extension, delimiter, is_headers_present, column_list, selected_columns, data_types, sorting_required_status, date_column_list):
    try:
        if file_extension == "csv" or file_extension == "tsv" or file_extension == "dat" or file_extension == "txt":

            venv_root_dir = get_project_venv_root()
            root_dir = get_project_root_unorthodox(venv_root_dir)
            file_location = "{}/{}".format(root_dir, path_from_repository_root_with_extension)
            # root_dir = os.path.dirname(os.path.abspath(__file__))
            # file_location_concat = os.path.join(root_dir, path_from_repository_root_with_extension)
            # file_location = "{}".format(file_location_concat)

            if is_headers_present == "yes" and selected_columns == "na" and data_types == "na" and sorting_required_status == "no" and date_column_list == "na":
                data_set = pd.read_csv(file_location, sep=delimiter, header=0,
                                       keep_default_na=False, na_filter=False, error_bad_lines=True, low_memory=False)
                return data_set

            if is_headers_present == "yes" and selected_columns == "na" and data_types != "na" and sorting_required_status == "no" and date_column_list == "na":
                data_set = pd.read_csv(file_location, sep=delimiter, dtype=data_types, quoting=3, header=0,
                                       keep_default_na=False, na_filter=False, error_bad_lines=True, warn_bad_lines=True, low_memory=False)
                return data_set

            if is_headers_present == "yes" and selected_columns != "na" and data_types != "na" and sorting_required_status == "no" and date_column_list == "na":
                data_set = pd.read_csv(file_location, sep=delimiter, dtype=data_types, quoting=3, header=0,
                                       keep_default_na=False, na_filter=False, error_bad_lines=True, warn_bad_lines=True, low_memory=False)
                return data_set[selected_columns]

            if is_headers_present == "no" and selected_columns == "na" and data_types != "na" and sorting_required_status == "no" and date_column_list == "na":
                data_set = pd.read_csv(file_location, sep=delimiter, names=column_list, dtype=data_types, quoting=3, header=0,
                                       keep_default_na=False, na_filter=False, error_bad_lines=True, warn_bad_lines=True, low_memory=False)
                return data_set

            if is_headers_present == "no" and selected_columns != "na" and data_types != "na" and sorting_required_status == "no" and date_column_list == "na":
                data_set = pd.read_csv(file_location, sep=delimiter, names=column_list, dtype=data_types, quoting=3, header=0,
                                       keep_default_na=False, na_filter=False, error_bad_lines=True, warn_bad_lines=True, low_memory=False)
                return data_set[selected_columns]

            if is_headers_present == "no" and selected_columns != "na" and data_types != "na" and sorting_required_status == "no" and date_column_list != "na":
                data_set = pd.read_csv(file_location, sep=delimiter, names=column_list, dtype=data_types, parse_dates=date_column_list, quoting=3, header=0,
                                       keep_default_na=False, na_filter=False, error_bad_lines=True, warn_bad_lines=True, low_memory=False)
                return data_set[selected_columns]

            if is_headers_present == "no" and selected_columns != "na" and data_types != "na" and sorting_required_status == "yes" and date_column_list == "na":
                default_data_set = pd.read_csv(file_location, sep=delimiter, names=column_list, dtype=data_types, quoting=3, header=0,
                                               keep_default_na=False, na_filter=False, error_bad_lines=True, warn_bad_lines=True, low_memory=False)
                data_set = default_data_set.sort_values(by=column_list)
                return data_set[selected_columns]

            if is_headers_present == "no" and selected_columns != "na" and data_types != "na" and sorting_required_status == "yes" and date_column_list != "na":
                default_data_set = pd.read_csv(file_location, sep=delimiter, names=column_list, dtype=data_types, parse_dates=date_column_list, quoting=3, header=0,
                                               keep_default_na=False, na_filter=False, error_bad_lines=True, warn_bad_lines=True, low_memory=False)
                data_set = default_data_set.sort_values(by=column_list)
                return data_set[selected_columns]

        elif file_extension == "json":
            """ read json file """
            file_location = "{}".format(path_from_repository_root_with_extension)
            data_set = pd.read_json(file_location)
            return data_set

        elif file_extension == 'xls' or file_extension == 'xlsx':
            """ read xls, xlsx file """
            file_location = "{}".format(path_from_repository_root_with_extension)
            if is_headers_present == 'no':
                data_set = pd.read_excel(file_location, names=column_list)
            else:
                data_set = pd.read_excel(file_location)
            return data_set

    except IOError as ioer:
        print("*** Some thing went wrong reading the file ***")
        print('Error: {}'.format(ioer))
        quit()
    except OSError as oser:
        print("*** Cannot open/ read file specified***")
        print('Error: {}'.format(oser))
        quit()


def reader_from_configuration_file(config_file_extension, path_from_repository_root_to_config_file, source_to_read):
    try:
        if config_file_extension == 'ini':
            configure = ConfigParser()
            venv_root_dir = get_project_venv_root()
            root_dir = get_project_root_unorthodox(venv_root_dir)
            file_location = "{}/{}".format(root_dir, path_from_repository_root_to_config_file)
            configure.read(file_location)
            # configure.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), path_from_repository_root_to_config_file))
            file_extension = configure.get('{}'.format(source_to_read), 'extension')
            path_from_repository_root_with_extension = configure.get('{}'.format(source_to_read), 'file_path')
            delimiter = configure.get('{}'.format(source_to_read), 'delimiter_value')
            is_headers_present = configure.get('{}'.format(source_to_read), 'headers_present')
            column_list = configure.get('{}'.format(source_to_read), 'columns')
            selected_columns = configure.get('{}'.format(source_to_read), 'selected_list')
            data_types = configure.get('{}'.format(source_to_read), 'types_list')
            sorting_required_status = configure.get('{}'.format(source_to_read), 'sorting_required')
            date_column_list = configure.get('{}'.format(source_to_read), 'date_columns')

            file_read_df = reader_without_configuration_file(file_extension, path_from_repository_root_with_extension, delimiter,
                                                             is_headers_present, column_list, selected_columns, data_types, sorting_required_status, date_column_list)

            # if file_extension == "csv" or file_extension == "tsv" or file_extension == "dat" or file_extension == "txt":
            #     if is_headers_present == "yes" and selected_columns == "na" and data_types == "na" and sorting_required_status == "na" and date_column_list == "na":
            #         data_set = pd.read_csv(path_from_repository_root_with_extension, sep=delimiter, quoting=3, header=0,
            #                                keep_default_na=False, na_filter=False, error_bad_lines=True, warn_bad_lines=True, low_memory=False)
            #         return data_set

            return file_read_df

    except IOError as ioer:
        print("*** Some thing went wrong reading the file ***")
        print('Error: {}'.format(ioer))
        quit()
    except OSError as oser:
        print("*** Cannot open/ read file specified***")
        print('Error: {}'.format(oser))
        quit()
