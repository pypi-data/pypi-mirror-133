from typing import Optional

import numpy as np
import pandas as pd
from sklearn.decomposition import KernelPCA, PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures, StandardScaler

from fedot.core.data.data import InputData, data_type_is_table, OutputData
from fedot.core.data.data_preprocessing import replace_inf_with_nans, convert_into_column, \
    divide_data_categorical_numerical, find_categorical_columns, data_has_categorical_features
from fedot.core.operations.evaluation.operation_implementations. \
    implementation_interfaces import DataOperationImplementation, EncodedInvariantImplementation


class ComponentAnalysisImplementation(DataOperationImplementation):
    """ Class for applying PCA and kernel PCA models form sklearn

    :param params: optional, dictionary with the arguments
    """

    def __init__(self, **params: Optional[dict]):
        super().__init__()
        self.pca = None
        self.params = None
        self.number_of_features = None
        self.number_of_samples = None

        self.parameters_changed = False

    def fit(self, input_data):
        """
        The method trains the PCA model

        :param input_data: data with features, target and ids for PCA training
        :return pca: trained PCA model (optional output)
        """
        self.number_of_samples, self.number_of_features = np.array(input_data.features).shape

        if self.number_of_features > 1:
            self.check_and_correct_params()
            self.pca.fit(input_data.features)

        return self.pca

    def transform(self, input_data, is_fit_pipeline_stage: Optional[bool]):
        """
        Method for transformation tabular data using PCA

        :param input_data: data with features, target and ids for PCA applying
        :param is_fit_pipeline_stage: is this fit or predict stage for pipeline
        :return input_data: data with transformed features attribute
        """

        if self.number_of_features > 1:
            transformed_features = self.pca.transform(input_data.features)
        else:
            transformed_features = input_data.features

        # Update features
        output_data = self._convert_to_output(input_data,
                                              transformed_features)
        self.update_column_types(output_data)
        return output_data

    def check_and_correct_params(self):
        """ Method check if number of features in data enough for n_components
        parameter in PCA or not. And if not enough - fixes it
        """
        current_parameters = self.pca.get_params()

        if type(current_parameters['n_components']) == int:
            if current_parameters['n_components'] > self.number_of_features:
                current_parameters['n_components'] = self.number_of_features
                self.parameters_changed = True
        elif current_parameters['n_components'] == 'mle':
            # Check that n_samples correctly map with n_features
            if self.number_of_samples < self.number_of_features:
                current_parameters['n_components'] = 0.5
                self.parameters_changed = True

        self.pca.set_params(**current_parameters)
        self.params = current_parameters

    def get_params(self):
        if self.parameters_changed is True:
            params_dict = self.pca.get_params()
            return tuple([params_dict, ['n_components']])
        else:
            return self.pca.get_params()

    @staticmethod
    def update_column_types(output_data: OutputData):
        """ Update column types after applying PCA operations """
        n_rows, n_cols = output_data.predict.shape
        output_data.supplementary_data.column_types['features'] = [str(float) * n_cols]
        return output_data


class PCAImplementation(ComponentAnalysisImplementation):
    """ Class for applying PCA from sklearn

    :param params: optional, dictionary with the hyperparameters
    """

    def __init__(self, **params: Optional[dict]):
        super().__init__()
        if not params:
            # Default parameters
            self.pca = PCA(svd_solver='full', n_components='mle')
        else:
            self.pca = PCA(**params)
        self.params = params
        self.number_of_features = None


class KernelPCAImplementation(ComponentAnalysisImplementation):
    """ Class for applying kernel PCA from sklearn

    :param params: optional, dictionary with the hyperparameters
    """

    def __init__(self, **params: Optional[dict]):
        super().__init__()
        if not params:
            # Default parameters
            self.pca = KernelPCA()
        else:
            self.pca = KernelPCA(**params)
        self.params = params


class PolyFeaturesImplementation(EncodedInvariantImplementation):
    """ Class for application of PolynomialFeatures operation on data,
    where only not encoded features (were not converted from categorical using
    OneHot encoding) are used

    :param params: optional, dictionary with the arguments
    """

    def __init__(self, **params: Optional[dict]):
        super().__init__()
        if not params:
            # Default parameters
            self.operation = PolynomialFeatures(include_bias=False)
        else:
            # Checking the appropriate params are using or not
            poly_params = {k: params[k] for k in
                           ['degree', 'interaction_only']}
            self.operation = PolynomialFeatures(include_bias=False,
                                                **poly_params)
        self.params = params

    def get_params(self):
        return self.operation.get_params()

    def _update_column_types(self, source_features_shape, output_data: OutputData):
        """ Update column types after applying operations. If new columns added, new type for them are defined """
        if len(source_features_shape) < 2:
            return output_data
        else:
            cols_number_added = output_data.predict.shape[1] - source_features_shape[1]
            if cols_number_added > 0:
                # There are new columns in the table
                col_types = output_data.supplementary_data.column_types['features']
                col_types.extend([str(float)] * cols_number_added)
                output_data.supplementary_data.column_types['features'] = col_types


class ScalingImplementation(EncodedInvariantImplementation):
    """ Class for application of Scaling operation on data,
    where only not encoded features (were not converted from categorical using
    OneHot encoding) are used

    :param params: optional, dictionary with the arguments
    """

    def __init__(self, **params: Optional[dict]):
        super().__init__()
        if not params:
            # Default parameters
            self.operation = StandardScaler()
        else:
            self.operation = StandardScaler(**params)
        self.params = params

    def get_params(self):
        return self.operation.get_params()


class NormalizationImplementation(EncodedInvariantImplementation):
    """ Class for application of MinMax normalization operation on data,
    where only not encoded features (were not converted from categorical using
    OneHot encoding) are used

    :param params: optional, dictionary with the arguments
    """

    def __init__(self, **params: Optional[dict]):
        super().__init__()
        if not params:
            # Default parameters
            self.operation = MinMaxScaler()
        else:
            self.operation = MinMaxScaler(**params)
        self.params = params

    def get_params(self):
        return self.operation.get_params()


class ImputationImplementation(DataOperationImplementation):
    """ Class for applying imputation on tabular data

    :param params: optional, dictionary with the arguments
    """

    def __init__(self, **params: Optional[dict]):
        super().__init__()
        default_params_categorical = {'strategy': 'most_frequent'}
        self.params_cat = {**params, **default_params_categorical}
        self.params_num = params
        self.categorical_ids = None
        self.non_categorical_ids = None
        self.ids_binary_integer_features = {}

        if not params:
            # Default parameters
            self.imputer_cat = SimpleImputer(**default_params_categorical)
            self.imputer_num = SimpleImputer()
        else:
            self.imputer_cat = SimpleImputer(**self.params_cat)
            self.imputer_num = SimpleImputer(**self.params_num)

    def fit(self, input_data: InputData):
        """
        The method trains SimpleImputer

        :param input_data: data with features
        """

        replace_inf_with_nans(input_data)

        if data_type_is_table(input_data):
            # Tabular data contains categorical features
            categorical_ids, non_categorical_ids = find_categorical_columns(input_data.features)
            numerical, categorical = divide_data_categorical_numerical(input_data, categorical_ids,
                                                                       non_categorical_ids)

            if categorical is not None and categorical.features.size > 0:
                categorical.features = convert_into_column(categorical.features)
                # Imputing for categorical values
                self.imputer_cat.fit(categorical.features)

            if numerical is not None and numerical.features.size > 0:
                numerical.features = convert_into_column(numerical.features)
                # Imputing for numerical values
                self.imputer_num.fit(numerical.features)
        else:
            # Time series or other type of non-tabular data
            input_data.features = convert_into_column(input_data.features)
            self.imputer_num.fit(input_data.features)

    def transform(self, input_data, is_fit_pipeline_stage: Optional[bool] = None):
        """
        Method for transformation tabular data using SimpleImputer

        :param input_data: data with features
        :param is_fit_pipeline_stage: is this fit or predict stage for pipeline
        :return input_data: data with transformed features attribute
        """
        replace_inf_with_nans(input_data)

        if data_type_is_table(input_data) and data_has_categorical_features(input_data):
            features_types = input_data.supplementary_data.column_types.get('features')
            self.categorical_ids, self.non_categorical_ids = find_categorical_columns(input_data.features,
                                                                                      features_types)
            numerical, categorical = divide_data_categorical_numerical(input_data, self.categorical_ids,
                                                                       self.non_categorical_ids)

            if categorical is not None:
                categorical_features = convert_into_column(categorical.features)
                categorical_features = self.imputer_cat.transform(categorical_features)

            if numerical is not None:
                numerical_features = convert_into_column(numerical.features)

                # Features with only two unique values must be filled in a specific way
                self._find_binary_features(numerical_features)
                numerical_features = self.imputer_num.transform(numerical_features)
                numerical_features = self._correct_binary_ids_features(numerical_features)

            if categorical is not None and numerical is not None:
                # Stack both categorical and numerical features
                transformed_features = self._categorical_numerical_union(categorical_features,
                                                                         numerical_features)
            elif categorical is not None and numerical is None:
                # Dataset contain only categorical features
                transformed_features = categorical_features
            elif categorical is None and numerical is not None:
                # Dataset contain only numerical features
                transformed_features = numerical_features

        else:
            input_data.features = convert_into_column(input_data.features)
            transformed_features = self.imputer_num.transform(input_data.features)

        output_data = self._convert_to_output(input_data, transformed_features, data_type=input_data.data_type)
        return output_data

    def fit_transform(self, input_data, is_fit_pipeline_stage: Optional[bool] = None):
        """
        Method for training and transformation tabular data using SimpleImputer

        :param input_data: data with features
        :param is_fit_pipeline_stage: is this fit or predict stage for pipeline
        :return input_data: data with transformed features attribute
        """
        self.fit(input_data)
        output_data = self.transform(input_data)
        return output_data

    def _categorical_numerical_union(self, categorical_features: np.array, numerical_features: np.array):
        """ Merge numerical and categorical features in right order (as it was in source table) """
        categorical_df = pd.DataFrame(categorical_features, columns=self.categorical_ids)
        numerical_df = pd.DataFrame(numerical_features, columns=self.non_categorical_ids)
        all_features_df = pd.concat([numerical_df, categorical_df], axis=1)

        # Sort column names
        all_features_df = all_features_df.sort_index(axis=1)
        return np.array(all_features_df)

    def _find_binary_features(self, numerical_features: np.array):
        """ Find indices of features with only two unique values in column.
        All features in table are numerical.
        """
        df = pd.DataFrame(numerical_features)

        # Calculate unique values per column (excluding nans)
        for column_id, col in enumerate(df):
            unique_values = df[col].dropna().unique()
            if len(unique_values) <= 2:
                # Current numerical column has only two values
                column_info = {column_id: {'min': min(unique_values),
                                           'max': max(unique_values)}}
                self.ids_binary_integer_features.update(column_info)

    def _correct_binary_ids_features(self, filled_numerical_features: np.array) -> np.array:
        """ Correct filled features if previously it was binary. Discretization is performed
        for the reconstructed values.
        For example, [1, 1, 0.75, 0] will be transformed into [1, 1, 1, 0]
        """
        list_binary_ids = list(self.ids_binary_integer_features.keys())
        if len(list_binary_ids) == 0:
            # Return source array
            return filled_numerical_features

        for bin_id in list_binary_ids:
            # Correct values inplace
            filled_column = filled_numerical_features[:, bin_id]
            min_value = self.ids_binary_integer_features[bin_id]['min']
            max_value = self.ids_binary_integer_features[bin_id]['max']
            mean_value = (max_value - min_value) / 2

            filled_column[filled_column > mean_value] = max_value
            filled_column[filled_column < mean_value] = min_value

        return filled_numerical_features

    def get_params(self) -> dict:
        features_imputers = {'imputer_categorical': self.params_cat,
                             'imputer_numerical': self.params_num}
        return features_imputers
