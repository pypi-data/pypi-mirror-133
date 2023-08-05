from typing import Union

import numpy as np
import pandas as pd

from fedot.core.data.data import InputData, data_type_is_table
from fedot.core.repository.dataset_types import DataTypesEnum


def data_type_is_suitable_preprocessing(data: InputData) -> bool:
    if data.data_type == DataTypesEnum.table or data.data_type == DataTypesEnum.ts:
        return True
    return False


def replace_inf_with_nans(input_data: InputData):
    values_to_replace = [np.inf, -np.inf]
    features_with_replaced_inf = np.where(np.isin(input_data.features,
                                                  values_to_replace),
                                          np.nan,
                                          input_data.features)
    input_data.features = features_with_replaced_inf


def convert_into_column(array: np.array):
    """ Perform conversion for data if it is necessary """
    if len(array.shape) == 1:
        return array.reshape(-1, 1)
    else:
        return array


def divide_data_categorical_numerical(input_data: InputData, categorical_ids: list,
                                      non_categorical_ids: list) -> (InputData, InputData):
    """
    Split tabular InputData into two parts: with numerical and categorical features
    using list with ids of categorical and numerical features.
    """

    if len(categorical_ids) > 0 and len(non_categorical_ids) > 0:
        # Both categorical and numerical features
        numerical_input = input_data.subset_features(non_categorical_ids)
        categorical_input = input_data.subset_features(categorical_ids)
        return numerical_input, categorical_input

    elif len(categorical_ids) == 0 and len(non_categorical_ids) > 0:
        # Only numerical
        numerical_input = input_data.subset_features(non_categorical_ids)
        return numerical_input, None

    elif len(categorical_ids) > 0 and len(non_categorical_ids) == 0:
        # Only categorical
        categorical_input = input_data.subset_features(categorical_ids)
        return None, categorical_input

    else:
        prefix = 'InputData contains no categorical and no numerical features.'
        raise ValueError(f'{prefix} Check data for Nans and inf values')


def find_categorical_columns(table: np.array, column_types: dict = None):
    """
    Method for finding categorical and non-categorical columns in tabular data

    :param table: tabular data for string columns types determination
    :param column_types: list with column types. If None, perform default checking
    :return categorical_ids: indices of categorical columns in table
    :return non_categorical_ids: indices of non categorical columns in table
    """
    if column_types is None:
        # Define if data contains string columns for "unknown table"
        return force_categorical_determination(table)

    categorical_ids = []
    non_categorical_ids = []
    column_id = 0
    for type_name in column_types:
        if 'str' in str(type_name):
            categorical_ids.append(column_id)
        else:
            non_categorical_ids.append(column_id)
        column_id += 1

    return categorical_ids, non_categorical_ids


def force_categorical_determination(table):
    """ Find string columns using 'computationally expensive' approach """
    source_shape = table.shape
    columns_number = source_shape[1] if len(source_shape) > 1 else 1

    categorical_ids = []
    non_categorical_ids = []
    # For every column in table make check for first element
    for column_id in range(0, columns_number):
        column = table[:, column_id] if columns_number > 1 else table
        col_shape = column.shape
        for i in column:
            # Check if element is string object or not until the first appearance
            if len(col_shape) == 2 and isinstance(i[0], str):
                # Column looks like [[n], [n], [n]]
                categorical_ids.append(column_id)
                break
            elif len(col_shape) == 1 and isinstance(i, str):
                # Column [n, n, n]
                categorical_ids.append(column_id)
                break

        if column_id not in categorical_ids:
            non_categorical_ids.append(column_id)

    return categorical_ids, non_categorical_ids


def data_has_missing_values(data: Union[InputData, 'MultiModalData']) -> bool:
    """ Check data for missing values."""

    if not isinstance(data, InputData):
        for data_source_name, values in data.items():
            if data_type_is_table(values):
                return pd.DataFrame(values.features).isna().sum().sum() > 0
    elif data_type_is_suitable_preprocessing(data):
        return pd.DataFrame(data.features).isna().sum().sum() > 0
    return False


def data_has_categorical_features(data: Union[InputData, 'MultiModalData']) -> bool:
    """
    Check data for categorical columns.
    Return bool, whether data has categorical columns or not
    """
    if data.data_type is not DataTypesEnum.table:
        return False
    data_has_categorical_columns = False

    if not isinstance(data, InputData):
        for data_source_name, values in data.items():
            if data_source_name.startswith('data_source_table'):
                features_types = values.supplementary_data.column_types.get('features')
                cat_ids, non_cat_ids = find_categorical_columns(values.features, features_types)
                data_has_categorical_columns = len(cat_ids) > 0

    else:
        features_types = data.supplementary_data.column_types.get('features')
        cat_ids, non_cat_ids = find_categorical_columns(data.features, features_types)
        data_has_categorical_columns = len(cat_ids) > 0

    return data_has_categorical_columns
