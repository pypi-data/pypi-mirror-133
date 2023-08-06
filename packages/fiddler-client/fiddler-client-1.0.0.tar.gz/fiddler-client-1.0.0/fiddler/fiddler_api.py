# TODO: Add License
import copy
import json
import logging
import math
import os.path
import pathlib
import random
import re
import shutil
import tarfile
import tempfile
import textwrap
import threading
import time
from collections import namedtuple
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Union

import numpy as np
import pandas as pd
import yaml
from deepdiff import DeepDiff
from werkzeug.datastructures import FileStorage

from fiddler.connection import Connection
from fiddler.experimental import ExperimentalFeatures
from fiddler.file_processor.src.constants import (
    CSV_EXTENSION,
    PARQUET_EXTENSION,
    SUPPORTABLE_FILE_EXTENSIONS,
)
from fiddler.project import Project

from . import constants
from .aws_utils import validate_gcp_uri_access, validate_s3_uri_access
from .core_objects import (
    CURRENT_SCHEMA_VERSION,
    ArtifactStatus,
    AttributionExplanation,
    BatchPublishType,
    Column,
    DatasetInfo,
    DataType,
    DeploymentOptions,
    DeploymentType,
    EventTypes,
    FiddlerEventColumns,
    FiddlerPublishSchema,
    FiddlerTimestamp,
    InitMonitoringModifications,
    MLFlowParams,
    ModelInfo,
    ModelInputType,
    ModelTask,
    MonitoringViolation,
    MonitoringViolationType,
    MulticlassAttributionExplanation,
    SegmentInfo,
    possible_init_monitoring_modifications,
)
from .file_processor.src.facade import upload_dataset
from .model_info_validator import ModelInfoValidator
from .monitoring_validator import MonitoringValidator
from .utils import cast_input_data, df_from_json_rows
from .utils.exceptions import MalformedSchemaException
from .utils.formatting import (
    formatted_utcnow,
    model_string_to_hostname,
    print_streamed_result,
    sanitized_name,
)
from .utils.general_checks import do_not_proceed, safe_name_check, type_enforce
from .utils.helper import infer_data_source
from .utils.pandas import (
    clean_df_types,
    df_size_exceeds,
    try_series_retype,
    write_dataframe_to_parquet_file,
)

LOG = logging.getLogger()

SUCCESS_STATUS = Connection.SUCCESS_STATUS
FAILURE_STATUS = Connection.FAILURE_STATUS
FIDDLER_ARGS_KEY = Connection.FIDDLER_ARGS_KEY
STREAMING_HEADER_KEY = Connection.STREAMING_HEADER_KEY
AUTH_HEADER_KEY = Connection.AUTH_HEADER_KEY
ROUTING_HEADER_KEY = Connection.ROUTING_HEADER_KEY
ADMIN_SERVICE_PORT = 4100
DATASET_MAX_ROWS = 50_000

# A PredictionEventBundle represents a batch of inferences and their input
# features. All of these share schema, latency, and success status. A bundle
# can consist just one event as well.
PredictionEventBundle = namedtuple(
    'PredictionEventBundle',
    [
        'prediction_status',  # typeof: int # 0 for success, failure otherwise
        'prediction_latency',  # typeof: float # Latency in seconds.
        'input_feature_bundle',  # list of feature vectors.
        'prediction_bundle',  # list of prediction vectors.
        # TODO: Support sending schema as well.
    ],
)

_protocol_version = 1


class FiddlerApi:
    """Broker of all connections to the Fiddler API.
    Conventions:
        - Exceptions are raised for FAILURE reponses from the backend.
        - Methods beginning with `list` fetch lists of ids (e.g. all model ids
            for a project) and do not alter any data or state on the backend.
        - Methods beginning with `get` return a more complex object but also
            do not alter data or state on the backend.
        - Methods beginning with `run` invoke model-related execution and
            return the result of that computation. These do not alter state,
            but they can put a heavy load on the computational resources of
            the Fiddler engine, so they should be paralellized with care.
        - Methods beginning with `delete` permanently, irrevocably, and
            globally destroy objects in the backend. Think "rm -rf"
        - Methods beginning with `upload` convert and transmit supported local
            objects to Fiddler-friendly formats loaded into the Fiddler engine.
            Attempting to upload an object with an identifier that is already
            in use will result in an exception being raised, rather than the
            existing object being overwritten. To update an object in the
            Fiddler engine, please call both the `delete` and `upload` methods
            pertaining to the object in question.

    :param url: The base URL of the API to connect to. Usually either
        https://dev.fiddler.ai (cloud) or http://localhost:4100 (onebox)
    :param org_id: The name of your organization in the Fiddler platform
    :param auth_token: Token used to authenticate. Your token can be
        created, found, and changed at <FIDDLER URL>/settings/credentials.
    :param proxies: optionally, a dict of proxy URLs. e.g.,
                    proxies = {'http' : 'http://proxy.example.com:1234',
                               'https': 'https://proxy.example.com:5678'}
    :param verbose: if True, api calls will be logged verbosely,
                    *warning: all information required for debugging will be
                    logged including the auth_token.
    """

    def __init__(
        self, url=None, org_id=None, auth_token=None, proxies=None, verbose=False
    ):
        self.org_id = org_id
        self.strict_mode = True
        self.connection = Connection(url, org_id, auth_token, proxies, verbose)

        self.monitoring_validator = MonitoringValidator()
        self.experimental = ExperimentalFeatures(client=self)

    def __getattr__(self, function_name):
        """
        Overriding allows us to point unrecognized use cases to the documentation page
        """

        def method(*args, **kwargs):
            # This is a method that is not recognized
            error_msg = (
                f'Function `{function_name}` not found.\n'
                f'Please consult Fiddler documentation at `https://api.fiddler.ai/`'
            )
            raise RuntimeError(error_msg)

        return method

    @staticmethod
    def _abort_dataset_upload(
        dataset: Dict[str, pd.DataFrame], size_check_enabled: bool, max_len: int
    ):
        """
        This method checks if any of the dataframes exeeds size limit.
        In case the size limit is exceeded and size_check_enabled is True
        a warning is issued and the user is required to confirm if they'd
        like to proceed with the upload
        """
        # check if the dataset exceeds size limits
        warn_and_query = size_check_enabled and df_size_exceeds(dataset, max_len)
        if warn_and_query:
            LOG.warning(
                f'The dataset contains more than {max_len} datapoints. '
                f'Please allow for additional time to upload the dataset '
                f'and calculate statistical metrics. '
                f'To disable this message set the flag size_check_enabled to False. '
                f'\n\nAlternately, consider sampling the dataset. '
                f'If you plan to sample the dataset please ensure that the '
                f'representative sample captures all possible '
                f'categorical features, labels and numerical ranges that '
                f'would be encountered during deployment.'
                f'\n\nFor details on how datasets are used and considerations '
                f'for when large datasets are necessary, please refer to '
                f'https://docs.fiddler.ai/pages/user-guide/administration-concepts/project-structure/#dataset'
            )
            user_query = 'Would you like to proceed with the upload (y/n)? '
            return do_not_proceed(user_query)
        return False

    def _check_connection(self, check_client_version=True, check_server_version=True):
        return self.connection.check_connection(
            check_client_version, check_server_version
        )

    def _call_executor_service(
        self,
        path: List[str],
        json_payload: Any = None,
        files: Optional[List[Path]] = None,
        is_get_request: bool = False,
        stream: bool = False,
    ):
        return self.connection.call_executor_service(
            path, json_payload, files, is_get_request, stream
        )

    def _call(
        self,
        path: List[str],
        json_payload: Any = None,
        files: Optional[List[Path]] = None,
        is_get_request: bool = False,
        stream: bool = False,
        timeout: Optional[int] = None,
        num_tries: int = 1,
    ):
        """Issues a request to the API and returns the result,
        logigng and handling errors appropriately.

        Raises a RuntimeError if the response is a failure or cannot be parsed.
        Does not handle any ConnectionError exceptions thrown by the `requests`
        library.

        Note: Parameters `timeout` and `num_tries` are currently only utilized in a workaround
        for a bug involving Mac+Docker communication. See: https://github.com/docker/for-mac/issues/3448
        """
        return self.connection.call(
            path, json_payload, files, is_get_request, stream, timeout, num_tries
        )

    def list_datasets(self, project_id: str) -> List[str]:
        """List the ids of all datasets in the organization.

        :returns: List of strings containing the ids of each dataset.
        """
        return self.project(project_id).list_datasets()

    def list_projects(self, get_project_details: bool = False) -> List[str]:
        """List the ids of all projects in the organization.

        :returns: List of strings containing the ids of each project.
        """
        path = ['list_projects', self.org_id]

        payload = {
            'project_details': get_project_details,
        }

        return self._call(path, json_payload=payload)['projects']

    def project(self, project_id):
        return Project(self.connection, project_id)

    def list_models(self, project_id: str) -> List[str]:
        """List the names of all models in a project.

        :param project_id: The unique identifier of the project on the Fiddler
            engine.
        :returns: List of strings containing the ids of each model in the
            specified project.
        """
        return self.project(project_id).list_models()

    def get_dataset_info(self, project_id: str, dataset_id: str) -> DatasetInfo:
        """Get DatasetInfo for a dataset.

        :param dataset_id: The unique identifier of the dataset on the Fiddler
            engine.

        :returns: A fiddler.DatasetInfo object describing the dataset.
        """
        return self.project(project_id).dataset(dataset_id).get_info()

    def get_model_info(self, project_id: str, model_id: str) -> ModelInfo:
        """Get ModelInfo for a model in a certain project.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.

        :returns: A fiddler.ModelInfo object describing the model.
        """
        return self.project(project_id).model(model_id).get_info()

    def _query_dataset(
        self,
        project_id: str,
        dataset_id: str,
        fields: List[str],
        max_rows: int,
        split: Optional[str] = None,
        sampling=False,
        sampling_seed=0.0,
    ):
        return (
            self.project(project_id)
            .dataset(dataset_id)
            ._query_dataset(fields, max_rows, split, sampling, sampling_seed)
        )

    def get_dataset(
        self,
        project_id: str,
        dataset_id: str,
        max_rows: int = 1_000,
        splits: Optional[List[str]] = None,
        sampling=False,
        dataset_info: Optional[DatasetInfo] = None,
        include_fiddler_id=False,
    ) -> Dict[str, pd.DataFrame]:
        """Fetches data from a dataset on Fiddler.

        :param project_id: The unique identifier of the project on the Fiddler
            engine.
        :param dataset_id: The unique identifier of the dataset on the Fiddler
            engine.
        :param max_rows: Up to this many rows will be fetched from eash split
            of the dataset.
        :param splits: If specified, data will only be fetched for these
            splits. Otherwise, all splits will be fetched.
        :param sampling: If True, data will be sampled up to max_rows. If
            False, rows will be returned in order up to max_rows. The seed
            will be fixed for sampling.∂
        :param dataset_info: If provided, the API will skip looking up the
            DatasetInfo (a necessary precursor to requesting data).
        :param include_fiddler_id: Return the Fiddler engine internal id
            for each row. Useful only for debugging.

        :returns: A dictionary of str -> DataFrame that maps the name of
            dataset splits to the data in those splits. If len(splits) == 1,
            returns just that split as a dataframe, rather than a dataframe.
        """
        return (
            self.project(project_id)
            .dataset(dataset_id)
            .download(max_rows, splits, sampling, dataset_info, include_fiddler_id)
        )

    def get_slice(
        self,
        sql_query: str,
        project_id: str,
        columns_override: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """Fetches data from Fiddler via a *slice query* (SQL query).

        :param sql_query: A special SQL query that begins with the keyword
            "SLICE"
        :param project_id: The unique identifier of the project on the Fiddler
            engine.
        :param columns_override: A list of columns to return even if they are
            not specified in the slice.
        :returns: A table containing the sliced data (as a Pandas DataFrame)
        """
        payload: Dict[str, Any] = dict(sql=sql_query, project=project_id)
        if columns_override is not None:
            payload['slice_columns_override'] = columns_override

        path = ['slice_query', self.org_id, project_id]
        res = self._call(path, json_payload=payload)

        slice_info = res.pop(0)
        if not slice_info['is_slice']:
            raise RuntimeError(
                'Query does not return a valid slice. ' 'Query: ' + sql_query
            )
        column_names = slice_info['columns']
        dtype_strings = slice_info['dtypes']
        df = pd.DataFrame(res, columns=column_names)
        for column_name, dtype in zip(column_names, dtype_strings):
            df[column_name] = try_series_retype(df[column_name], dtype)
        return df

    def delete_dataset(self, project_id: str, dataset_id: str):
        """Permanently delete a dataset.

        :param project_id: The unique identifier of the project on the Fiddler
            engine.
        :param dataset_id: The unique identifier of the dataset on the Fiddler
            engine.

        :returns: Server response for deletion action.
        """
        return self.project(project_id).dataset(dataset_id).delete()

    def delete_model(
        self, project_id: str, model_id: str, delete_prod=False, delete_pred=True
    ):
        """Permanently delete a model.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.
        :param delete_prod: Boolean value to delete the production table.
            By default this table is not dropped.
        :param delete_pred: Boolean value to delete the prediction table.
            By default this table is dropped.

        :returns: Server response for deletion action.
        """
        return self.project(project_id).model(model_id).delete(delete_prod, delete_pred)

    def _delete_model_artifacts(self, project_id: str, model_id: str):
        """Permanently delete a model artifacts.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.

        :returns: Server response for deletion action.
        """
        return self.project(project_id).model(model_id)._delete_artifacts()

    def delete_project(self, project_id: str):
        """Permanently delete a project.

        :param project_id: The unique identifier of the project on the Fiddler
            engine.

        :returns: Server response for deletion action.
        """
        # Type enforcement
        return self.project(project_id).delete()

    ##### Start: Methods related to uploading dataset #####

    def _upload_dataset_files(
        self,
        project_id: str,
        dataset_id: str,
        file_paths: List[Path],
        dataset_info: Optional[DatasetInfo] = None,
    ):
        """Uploads data files to the Fiddler platform."""
        safe_name_check(dataset_id, constants.MAX_ID_LEN, self.strict_mode)

        payload: Dict[str, Any] = dict(dataset_name=dataset_id)

        if dataset_info is not None:
            if self.strict_mode:
                dataset_info.validate()

            payload['dataset_info'] = dict(dataset=dataset_info.to_dict())

        payload['split_test'] = False
        path = ['dataset_upload', self.org_id, project_id]

        LOG.info(f'Uploading the dataset {dataset_id} ...')

        result = self._call(path, json_payload=payload, files=file_paths)

        return result

    def upload_dataset(
        self,
        project_id: str,
        dataset: Dict[str, pd.DataFrame],
        dataset_id: str,
        info: Optional[DatasetInfo] = None,
        size_check_enabled: bool = True,
    ):
        """Uploads a representative dataset to the Fiddler engine.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param dataset: A dictionary mapping name -> DataFrame
            containing data to be uploaded to the Fiddler engine.
        :param dataset_id: The unique identifier of the dataset on the Fiddler
            engine. Must be a short string without whitespace.
        :param info: A DatasetInfo object specifying all the details of the
            dataset. If not provided, a DatasetInfo will be inferred from the
            dataset and a warning raised.
        :param size_check_enabled: Flag to enable the dataframe size check.
            Default behavior is to raise a warning and present an interactive
            dialogue if the size of the dataframes exceeds the default limit.
            Set this flag to False to disable the checks.

        :returns: The server response for the upload.
        """
        # Type enforcement
        # @question: Shouldn't we just throw this as an error from server if we already don't do it?
        project_id = type_enforce('project_id', project_id, str)
        dataset_id = type_enforce('dataset_id', dataset_id, str)

        assert (
            ' ' not in dataset_id
        ), 'The dataset identifier should not contain whitespace'
        safe_name_check(dataset_id, constants.MAX_ID_LEN, self.strict_mode)

        # get a dictionary of str -> pd.DataFrame for all data to upload
        if not isinstance(dataset, dict):
            raise ValueError('dataset must be a dictionary mapping name -> DataFrame')

        # check if the dataset exceeds size limits
        # @todo: why is checking for filesize even an option, shouldn't it be default?
        abort_upload = self._abort_dataset_upload(
            dataset, size_check_enabled, DATASET_MAX_ROWS
        )
        if abort_upload:
            raise RuntimeError('Dataset upload aborted.')

        if info:
            # Since we started populating stats recently, some older yamls
            # dont have it. Or the user might just supply us the basic
            # schema without stats.
            # If the user provided the schema/yaml file, ask the user to
            # re-create dataset info with:
            # info = DatasetInfo.update_stats_for_existing_schema(dataset,
            # info, max_inferred_cardinality)
            # @question: shouldn't these validations be part of DatasetInfo? (high cohesion) and we invoke the method here.
            for column in info.columns:
                if (
                    (column.value_range_min is None) or (column.value_range_max is None)
                ) and column.data_type.is_numeric():
                    raise ValueError(
                        f'Dataset info does not contain min/max values for the numeric feature {column.name}. '
                        f'Please update using fdl.DatasetInfo.update_stats_for_existing_schema() '
                        f'and upload dataset with the updated dataset info.'
                    )
                if (not column.possible_values) and (
                    column.data_type.value
                    in [DataType.CATEGORY.value, DataType.BOOLEAN.value]
                ):
                    raise ValueError(
                        f'Dataset info does not contain possible values for the categorical feature {column.name}. '
                        f'Please update using fdl.DatasetInfo.update_stats_for_existing_schema() '
                        f'and upload dataset with the updated dataset info.'
                    )

            # Validate column names
            for name, df in dataset.items():
                for info_column in info.columns:
                    if info_column.name not in df:
                        raise RuntimeError(
                            f'{info_column.name}({name}) column not found in the dataframe, '
                            f'but passed in the info'
                        )

        # use inferred info with a warning if not `info` is passed
        else:
            inferred_info = DatasetInfo.from_dataframe(
                df=dataset.values(),
                display_name=dataset_id,
                dataset_id=dataset_id,
                max_inferred_cardinality=1000,
            )
            # @question: we only do validation when info is passed and not when it is inferred? Why should this be the case?
            LOG.warning(
                f'Heads up! We are inferring the details of your dataset from '
                f'the dataframe(s) provided. Please take a second to check '
                f'our work.'
                f'\n\nIf the following DatasetInfo is an incorrect '
                f'representation of your data, you can construct a '
                f'DatasetInfo with the DatasetInfo.from_dataframe() method '
                f'and modify that object to reflect the correct details of '
                f'your dataset.'
                f'\n\nAfter constructing a corrected DatasetInfo, please '
                f're-upload your dataset with that DatasetInfo object '
                f'explicitly passed via the `info` parameter of '
                f'FiddlerApi.upload_dataset().'
                f'\n\nYou may need to delete the initially uploaded version'
                f"via FiddlerApi.delete_dataset('{dataset_id}')."
                f'\n\nInferred DatasetInfo to check:'
                f'\n{textwrap.indent(repr(inferred_info), "  ")}'
            )
            info = inferred_info

        if self.strict_mode:
            info.validate()

        return self._upload_dataset_with_compression(
            project_id=project_id,
            dataset=dataset,
            dataset_id=dataset_id,
            dataset_info=info,
        )

    def upload_dataset_from_dir(
        self,
        project_id: str,
        dataset_id: str,
        dataset_dir: Path,
        file_type: str = 'csv',
        file_schema=None,
        size_check_enabled: bool = False,
    ):
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)
        dataset_id = type_enforce('dataset_id', dataset_id, str)
        dataset_dir = type_enforce('dataset_dir', dataset_dir, Path)

        if f'.{file_type}' not in SUPPORTABLE_FILE_EXTENSIONS:
            raise ValueError(
                f'Invalid file_type :{file_type}. Valid file types are : {SUPPORTABLE_FILE_EXTENSIONS}'
            )

        if file_type.endswith('avro'):
            # TODO: This was missing the last two positional arguments,
            # size_check_enabled and info; added size_check_enabled, None for
            # now.
            return self.process_avro(
                project_id,
                dataset_id,
                dataset_dir,
                file_schema,
                size_check_enabled,
                None,
            )

        if not dataset_dir.is_dir():
            raise ValueError(f'{dataset_dir} is not a directory')

        dataset_yaml = dataset_dir / f'{dataset_id}.yaml'

        if not dataset_yaml.is_file():
            raise ValueError(f'YAML file not found: {dataset_yaml}')

        with dataset_yaml.open() as f:
            dataset_info = DatasetInfo.from_dict(yaml.safe_load(f))

        files = dataset_dir.glob('*.csv')
        csv_files = [x for x in files if x.is_file()]

        LOG.info(f'Found CSV file {csv_files}')

        # Lets make sure that we add stats if they are not already there.
        # We need to read the datasets in pandas and create a dataset dictionary
        dataset = {}
        csv_paths = []
        for file in csv_files:
            csv_name = str(file).split('/')[-1]
            csv_paths.append(csv_name)
            name = csv_name[:-4]

            # @TODO Change the flow so that we can read the CSV in chunks
            dataset[name] = pd.read_csv(file, dtype=dataset_info.get_pandas_dtypes())

        # check if the dataset exceeds size limits
        abort_upload = self._abort_dataset_upload(
            dataset, size_check_enabled, DATASET_MAX_ROWS
        )
        if abort_upload:
            raise RuntimeError('Dataset upload aborted.')

        # Update stats
        dataset_info = DatasetInfo.update_stats_for_existing_schema(
            dataset, dataset_info
        )
        updated_infos = []
        for item in dataset.values():
            update_info = DatasetInfo.check_and_update_column_info(dataset_info, item)
            updated_infos.append(update_info)

        dataset_info = DatasetInfo.as_combination(
            updated_infos, display_name=dataset_info.display_name
        )

        return self._upload_dataset_with_compression(
            project_id=project_id,
            dataset=dataset,
            dataset_id=dataset_id,
            dataset_info=dataset_info,
        )

    def upload_dataset_from_file(
        self,
        project_id: str,
        dataset_id: str,
        file_path: str,
        file_type: str = 'csv',
        file_schema=Dict[str, Any],
        info: Optional[DatasetInfo] = None,
        size_check_enabled: bool = False,
    ):
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)
        dataset_id = type_enforce('dataset_id', dataset_id, str)
        file_path = type_enforce('dataset_dir', file_path, Path)

        if file_type.endswith('avro'):
            return self.process_avro(
                project_id,
                dataset_id,
                pathlib.Path(file_path),
                file_schema,
                size_check_enabled,
                info,
            )
        elif file_type.endswith('csv'):
            return self.process_csv(
                project_id,
                dataset_id,
                pathlib.Path(file_path),
                size_check_enabled,
                info,
            )

        raise ValueError(
            f'Invalid file_type :{file_type}. Valid file types are : {SUPPORTABLE_FILE_EXTENSIONS}'
        )

    def process_csv(
        self, project_id, dataset_id, csv_file_path: Path, size_check_enabled, info
    ):
        dataset = {}
        # @TODO Read and process the CSV file in chunks
        dataset[csv_file_path.name] = pd.read_csv(csv_file_path)
        return self.upload_dataset(
            project_id,
            dataset,
            dataset_id,
            size_check_enabled=size_check_enabled,
            info=info,
        )

    def process_avro(
        self,
        project_id: str,
        dataset_id: str,
        avro_file_path: Path,
        file_schema: Dict,
        size_check_enabled,
        info,
    ):
        dataset = {}
        LOG.info(f'avro_file : {avro_file_path}')
        with open(avro_file_path, 'rb') as fh:
            buf = BytesIO(fh.read())
            files = {avro_file_path: FileStorage(buf, str(avro_file_path))}
            results = upload_dataset(files, 'LOCAL_DISK', 'avro', file_schema)
            df = pd.DataFrame(results)
            dataset[avro_file_path.name] = df
            return self.upload_dataset(
                project_id=project_id,
                dataset_id=dataset_id,
                dataset=dataset,
                size_check_enabled=size_check_enabled,
                info=info,
            )

    def _upload_dataset_with_compression(
        self,
        project_id: str,
        dataset: Dict[str, pd.DataFrame],
        dataset_id: str,
        dataset_info: DatasetInfo,
    ):
        schema = dataset_info.get_arrow_schema()

        # dump the data to named parquet temp file
        with tempfile.TemporaryDirectory() as tmp:
            file_paths = []
            for name, df in dataset.items():
                # Adding .csv to support legacy way of converting everything to CSV
                filename = f'{name}.{CSV_EXTENSION}.{PARQUET_EXTENSION}'
                file_path = Path(tmp) / filename
                file_paths.append(file_path)

                # Data type conversion as per dataset_info
                # Data types like date/time/datetime should be converted to string before creating parquet file
                df = df.astype(dtype=dataset_info.get_pandas_dtypes())

                write_dataframe_to_parquet_file(
                    df=df, file_path=file_path, schema=schema
                )

            # add files to the DatasetInfo on the fly
            dataset_info = copy.deepcopy(dataset_info)
            dataset_info.files = [
                fp.name.replace(f'.{PARQUET_EXTENSION}', '') for fp in file_paths
            ]

            # upload the parquet files
            LOG.info(f'[{dataset_id}] dataset upload: upload and import dataset files')

            res = self._upload_dataset_files(
                project_id=project_id,
                dataset_id=dataset_id,
                file_paths=file_paths,
                dataset_info=dataset_info,
            )

            LOG.info(f'Dataset uploaded {res}')
            return res

    ##### End: Methods related to uploading dataset #####

    def run_model(
        self,
        project_id: str,
        model_id: str,
        df: pd.DataFrame,
        log_events=False,
        casting_type=False,
    ) -> pd.DataFrame:
        """Executes a model in the Fiddler engine on a DataFrame.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.
        :param df: A dataframe contining model inputs as rows.
        :param log_events: Variable determining if the the predictions
            generated should be logged as production traffic
        :param casting_type: Bool indicating if fiddler should try to cast the data in the event with
        the type referenced in model info. Default to False.

        :returns: A pandas DataFrame containing the outputs of the model.
        """
        return (
            self.project(project_id)
            .model(model_id)
            .predict(df, log_events, casting_type)
        )

    def run_explanation(
        self,
        project_id: str,
        model_id: str,
        df: pd.DataFrame,
        explanations: Union[str, Iterable[str]] = 'shap',
        dataset_id: Optional[str] = None,
        casting_type: Optional[bool] = False,
        return_raw_response=False,
    ) -> Union[
        AttributionExplanation,
        MulticlassAttributionExplanation,
        List[AttributionExplanation],
        List[MulticlassAttributionExplanation],
    ]:
        """Executes a model in the Fiddler engine on a DataFrame.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.
        :param df: A dataframe containing model inputs as rows. Only the first
            row will be explained.
        :param explanations: A single string or list of strings specifying
            which explanation algorithms to run.
        :param dataset_id: The unique identifier of the dataset in the
            Fiddler engine. Required for most tabular explanations, but
            optional for most text explanations.
        :param casting_type: Bool indicating if fiddler should try to cast the data in the event with
        the type referenced in model info. Default to False.

        :returns: A single AttributionExplanation if `explanations` was a
            single string, or a list of AttributionExplanation objects if
            a list of explanations was requested.
        """
        return (
            self.project(project_id)
            .model(model_id)
            .explanation(
                df, explanations, dataset_id, casting_type, return_raw_response
            )
        )

    def run_feature_importance(
        self,
        project_id: str,
        model_id: str,
        dataset_id: str,
        dataset_splits: Optional[List[str]] = None,
        slice_query: Optional[str] = None,
        impact_not_importance: Optional[bool] = False,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get global feature importance for a model over a dataset.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.
        :param dataset_id: The unique identifier of the dataset in the
            Fiddler engine.
        :param dataset_splits: If specified, importance will only be computed
            over these splits. Otherwise, all splits will be used. Only a
            single split is currently supported.
        :param slice_query: A special SQL query.
        :param impact_not_importance: Boolean flag to compute either impact or importance.
        False by default (compute feature importance).
        For text models, only feature impact is implemented.
        :param kwargs: Additional parameters to be passed to the importance
            algorithm. For example, `n_inputs`, `n_iterations`, `n_references`,
            `ci_confidence_level`.
        :return: A named tuple with the explanation results.
        """
        return (
            self.project(project_id)
            .model(model_id)
            .feature_importance(dataset_id, dataset_splits, slice_query, impact_not_importance, **kwargs)
        )

    def run_fairness(
        self,
        project_id: str,
        model_id: str,
        dataset_id: str,
        protected_features: list,
        positive_outcome: Union[str, int],
        slice_query: Optional[str] = None,
        score_threshold: Optional[float] = 0.5,
    ) -> Dict[str, Any]:
        """Get fairness metrics for a model over a dataset.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.
        :param dataset_id: The unique identifier of the dataset in the
            Fiddler engine.
        :param protected_features: List of protected features
        :param positive_outcome: Name or value of the positive outcome
        :param slice_query: If specified, slice the data.
        :param score_threshold: positive score threshold applied to get outcomes
        :return: A dictionary with the fairness metrics, technical_metrics,
        labels distribution and model outcomes distribution
        """
        return (
            self.project(project_id)
            .model(model_id)
            .fairness(
                dataset_id,
                protected_features,
                positive_outcome,
                slice_query,
                score_threshold,
            )
        )

    def get_mutual_information(
        self,
        project_id: str,
        dataset_id: str,
        features: list,
        normalized: Optional[bool] = False,
        slice_query: Optional[str] = None,
        sample_size: Optional[int] = None,
        seed: Optional[float] = 0.25,
    ):
        """
        The Mutual information measures the dependency between two random variables.
        It's a non-negative value. If two random variables are independent MI is equal to zero.
        Higher MI values means higher dependency.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param dataset_id: The unique identifier of the dataset in the
            Fiddler engine.
        :param features: list of features to compute mutual information with respect to all the variables in the dataset.
        :param normalized: If set to True, it will compute Normalized Mutual Information (NMI)
        :param slice_query: Optional slice query
        :param sample_size: Optional sample size for the selected dataset
        :param seed: Optional seed for sampling
        :return: a dictionary of mutual information w.r.t the given features.
        """
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)
        dataset_id = type_enforce('dataset_id', dataset_id, str)

        if isinstance(features, str):
            features = [features]
        if not isinstance(features, list):
            raise ValueError(
                f'Invalid type: {type(features)}. Argument features has to be a list'
            )
        correlation = {}
        for col_name in features:
            payload = dict(
                col_name=col_name,
                normalized=normalized,
                slice_query=slice_query,
                sample_size=sample_size,
                seed=seed,
            )
            path = ['dataset_mutual_information', self.org_id, project_id, dataset_id]
            res = self._call(path, json_payload=payload)
            correlation[col_name] = res
        return correlation

    def create_project(self, project_id: str):
        """Create a new project.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine. Must be a short string without whitespace.

        :returns: Server response for creation action.
        """
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)

        safe_name_check(project_id, constants.MAX_ID_LEN, self.strict_mode)
        res = None
        try:
            path = ['new_project', self.org_id, project_id]
            res = self._call(path)
        except Exception as e:
            if 'already exists' in str(e):
                LOG.error(
                    'Project name already exists, please try with a different name (You may not have access to all the projects)'
                )
            else:
                raise e

        return res

    def share_project(
        self,
        project_name: str,
        role: str,
        user_name: Optional[str] = None,
        team_name: Optional[str] = None,
    ):
        """Share a project with other users and/or teams.

        :param project_name: The name of the project to share.
        :param role: one of ["READ", "WRITE", "OWNER"].
        :param user_name: (optional) username, typically an email address.
        :param team_name: (optional) name of the team.

        :returns: Server response for creation action.
        """
        return self.project(project_name).share(role, user_name, team_name)

    def unshare_project(
        self,
        project_name: str,
        role: str,
        user_name: Optional[str] = None,
        team_name: Optional[str] = None,
    ):
        """un-Share a project with other users and/or teams.

        :param project_name: The name of the project.
        :param role: one of ["READ", "WRITE", "OWNER"].
        :param user_name: (optional) username, typically an email address.
        :param team_name: (optional) name of the team.

        :returns: Server response for creation action.
        """
        return self.project(project_name).unshare(role, user_name, team_name)

    def list_org_roles(self):
        """List the users in the organization.

        :returns: list of users and their roles in the organization.
        """
        path = ['roles', self.org_id]
        return self._call(path, is_get_request=True)

    def list_project_roles(self, project_name: str):
        """List the users and teams with access to a given project.

        :returns: list of users and teams with access to a given project.
        """
        return self.project(project_name).list_roles()

    def list_teams(self):
        """List the teams and the members in each team.

        :returns: dictionary with teams as keys and list of members as values.
        """
        path = ['teams', self.org_id]
        return self._call(path, is_get_request=True)

    ##### Start: Methods related to uploading / registering model #####

    def _import_model_predictions(
        self,
        project_id: str,
        dataset_id: str,
        model_id: str,
        columns: Sequence[Dict],
        file_paths: List[Path],
    ):
        """Uploads model predictions to Fiddler platform."""
        payload: Dict[str, Any] = dict(dataset=dataset_id)
        payload['model'] = model_id
        payload['columns'] = columns

        path = ['import_model_predictions', self.org_id, project_id]
        result = self._call(path, json_payload=payload, files=file_paths)
        return result

    def _create_model(
        self,
        project_id: str,
        dataset_id: str,
        target: str,
        features: Optional[List[str]] = None,
        train_splits: Optional[List[str]] = None,
        model_id: str = 'fiddler_generated_model',
        model_info: Optional[ModelInfo] = None,
    ):
        """Trigger auto-modeling on a dataset already uploaded to Fiddler.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.

        :param dataset_id: The unique identifier of the dataset in the
            Fiddler engine.
        :param target: The column name of the target to be modeled.
        :param features: If specified, a list of column names to use as
            features. If not specified, all non-target columns will be used
            as features.
        :param train_splits: A list of splits to train on. If not specified,
            all splits will be used as training data. Currently only a single
            split can be specified if `train_splits` is not None.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.

        :returns: Server response for creation action.
        """
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)
        dataset_id = type_enforce('dataset_id', dataset_id, str)

        safe_name_check(model_id, constants.MAX_ID_LEN, self.strict_mode)

        if train_splits is not None and len(train_splits) > 1:
            raise NotImplementedError(
                'Sorry, currently only single-split training is '
                'supported. Please only pass a maximum of one element to '
                '`train_splits`.'
            )
        source = None if train_splits is None else train_splits[0]
        dataset_column_names = self.get_dataset_info(
            project_id, dataset_id
        ).get_column_names()

        # raise exception if misspelled target
        if target not in dataset_column_names:
            raise ValueError(
                f'Target "{target}" not found in the columns of '
                f'dataset {dataset_id} ({dataset_column_names})'
            )

        # raise if target in features or features not in columns
        if features is not None:
            if target in features:
                raise ValueError(f'Target "{target}" cannot also be in ' f'features.')
            features_not_in_dataset = set(features) - set(dataset_column_names)
            if len(features_not_in_dataset) > 0:
                raise ValueError(
                    f'All features should be in the dataset, but '
                    f'the following features were not found in '
                    f'the dataset: {features_not_in_dataset}'
                )

        # use all non-target columns from dataset if no features are specified
        if features is None:
            features = list(dataset_column_names)
            features.remove(target)

        payload: Dict[str, Any] = {
            'dataset': dataset_id,
            'model_name': model_id,
            'source': source,
            'inputs': features,
            'targets': [target],
        }

        if model_info:
            if self.strict_mode:
                model_info.validate()
            payload['model_info'] = dict(model=model_info.to_dict())

        path = ['generate', self.org_id, project_id]
        result = self._call_executor_service(path, json_payload=payload)
        return result

    def _upload_model_custom(
        self,
        artifact_path: Path,
        model_info: ModelInfo,
        project_id: str,
        model_id: str,
        associated_dataset_ids: Optional[List[str]] = None,
        deployment_options: Optional[DeploymentOptions] = None,
    ):
        """Uploads a custom model object to the Fiddler engine along with
            custom glue-code for running the model. Optionally, a new runtime
            (k8s deployment) can be specified for the model via
            the deployment_options.

            Note: The parameters namespace, port, replicas, cpus, memory, gpus,
            await_deployment are only used if an image_uri is specified.

        :param artifact_path: A path to a directory containing all of the
            model artifacts needed to run the model. This includes a
            `package.py` file with the glue code needed to run the model.
        :param model_info: A ModelInfo object describing the details of the model.
        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine. Must be a short string without
            whitespace.
        :param associated_dataset_ids: The unique identifiers of datasets in
            the Fiddler engine to associate with the model.
        :param deployment_options: Options to control various deployment characteristics like deployment_type,
            whether to block until deployment completes etc.

        :returns: Server response for upload action.
        """
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)

        safe_name_check(model_id, constants.MAX_ID_LEN, self.strict_mode)

        if not artifact_path.is_dir():
            raise ValueError(f'The {artifact_path} must be a directory.')

        model_info = FiddlerApi._add_dataset_ids_to_model_info(
            model_info, associated_dataset_ids
        )

        if self.strict_mode:
            model_info.validate()

        if not deployment_options:
            deployment_options = DeploymentOptions(
                deployment_type=DeploymentType.PREDICTOR
            )

        # upload the model
        payload = dict(
            project=project_id,
            model=model_id,
            model_schema=dict(model=model_info.to_dict()),
            framework=model_info.framework,
            upload_as_archive=True,
            model_type='custom',
        )

        # Add deployment_options
        payload.update(deployment_options.to_dict())

        with tempfile.TemporaryDirectory() as tmp:
            tarfile_path = Path(tmp) / 'files'
            shutil.make_archive(
                base_name=str(Path(tmp) / 'files'),
                format='tar',
                root_dir=str(artifact_path),
                base_dir='.',
            )
            LOG.info(
                f'[{model_id}] model upload: uploading custom model from'
                f' artifacts in {str(artifact_path)} tarred to '
                f'{str(tarfile_path)}'
            )

            endpoint_path = ['model_upload', self.org_id, project_id]
            result = self._call(
                endpoint_path, json_payload=payload, files=[Path(tmp) / 'files.tar']
            )
            return result

    def upload_model_package(
        self,
        artifact_path: Path,
        project_id: str,
        model_id: str,
        deployment_type: Optional[
            str
        ] = DeploymentType.PREDICTOR,  # model deployment type. One of {'predictor', 'executor'}
        image_uri: Optional[str] = None,  # image to be used for newly uploaded model
        namespace: Optional[str] = None,  # kubernetes namespace
        port: Optional[int] = 5100,  # port on which model is served
        replicas: Optional[int] = 1,  # number of replicas
        cpus: Optional[float] = 0.25,  # number of CPU cores
        memory: Optional[str] = '128m',  # amount of memory required.
        gpus: Optional[int] = 0,  # number of GPU cores
        await_deployment: Optional[bool] = True,  # wait for deployment
    ):
        """Uploads a custom model package to the Fiddler engine along with
            custom glue-code for running the model. Optionally, a new runtime
            (k8s deployment) can be specified for the model via
            the deployment_type and the image_uri parameters.

            Note: The parameters namespace, port, replicas, cpus, memory, gpus,
            await_deployment are only used if an image_uri is specified.

        :param artifact_path: A path to a directory containing all of the
            model artifacts needed to run the model. This includes a
            `package.py` file with the glue code needed to run the model.
        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine. Must be a short string without
            whitespace.
        :param deployment_type: One of {'predictor', 'executor'}
        'predictor': where the model just exposes a `/predict` endpoint
                     - typically simple sklearn like models
        'executor': where fiddler needs the model internals
                     - typically deep models like tensorflow and pytorch etc
        :param image_uri: A URI of the form <registry>/<image-name>:<tag> which
            if specified will be used to create a new runtime and then serve the
            model.
        :param namespace: The kubernetes namespace to use for the newly created
            runtime.
        :param port: The port to use for the newly created runtime.
        :param replicas: The number of replicas running the model.
        :param cpus: The number of CPU cores reserved per replica.
        :param memory: The amount of memory reservation per replica.
        :param gpus: The number of GPU cores reserved per replica.
        :param await_deployment: whether to block until deployment completes.

        :returns: Server response for upload action.
        """

        # Type enforcement
        artifact_path = type_enforce('artifact_path', artifact_path, Path)

        if not artifact_path.is_dir():
            raise ValueError(f'Not a valid model dir: {artifact_path}')

        yaml_file = artifact_path / 'model.yaml'
        if not yaml_file.is_file():
            raise ValueError(f'Model yaml not found {yaml_file}')

        with yaml_file.open() as f:
            model_info = ModelInfo.from_dict(yaml.safe_load(f))

        deployment_type = DeploymentType[deployment_type.upper()]
        valid_deployment_types = [DeploymentType.PREDICTOR, DeploymentType.EXECUTOR]
        if deployment_type not in valid_deployment_types:
            raise ValueError(f'Pass valid deployment type({valid_deployment_types})')

        deployment_options = DeploymentOptions(
            deployment_type=deployment_type,
            image=image_uri,
            namespace=namespace,
            port=port,
            replicas=replicas,
            cpus=cpus,
            memory=memory,
            gpus=gpus,
            await_deployment=await_deployment,
        )

        miv = ModelInfoValidator(model_info, None)
        miv.validate_categoricals(modify=True)
        self._upload_model_custom(
            artifact_path=artifact_path,
            project_id=project_id,
            model_id=model_id,
            model_info=model_info,
            deployment_options=deployment_options,
        )

    @staticmethod
    def _add_dataset_ids_to_model_info(model_info, associated_dataset_ids):
        model_info = copy.deepcopy(model_info)
        # add associated dataset ids to ModelInfo
        if associated_dataset_ids is not None:
            for dataset_id in associated_dataset_ids:
                assert (
                    ' ' not in dataset_id
                ), 'Dataset identifiers should not contain whitespace'
            model_info.misc['datasets'] = associated_dataset_ids
        return model_info

    def _trigger_model_predictions(
        self, project_id: str, model_id: str, dataset_id: str
    ):
        """Makes the Fiddler service compute and cache model predictions on a
        dataset."""
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)
        dataset_id = type_enforce('dataset_id', dataset_id, str)

        payload = dict(model=model_id, dataset=dataset_id)
        result = self._call_executor_service(
            ['dataset_predictions', self.org_id, project_id], payload
        )

        return result

    def trigger_pre_computation(
        self,
        project_id: str,
        model_id: str,
        dataset_id: str,
        overwrite_cache: Optional[bool] = False,
        batch_size: Optional[int] = 10,
        calculate_predictions: Optional[bool] = True,
        cache_global_pdps: Optional[bool] = False,
        cache_global_impact_importance: Optional[bool] = True,
        cache_dataset=False,
    ):
        """Triggers various precomputation steps within the Fiddler service based on input parameters.

        :param project_id:                        the project to which the model whose events are
                                                  being published belongs.
        :param model_id:                          the model whose events are being published.
        :param dataset_id:                        id of the dataset to be used.
        :param overwrite_cache:                   Boolean indicating whether to overwrite previously cached
                                                  information.
        :param batch_size:                        Batch size of global PDP calculation.
        :param calculate_predictions:             Boolean indicating whether to pre-calculate and store model
                                                  predictions.
        :param cache_global_pdps:                 Boolean indicating whether to pre-calculate and cache global partial
                                                  dependence plots.
        :param cache_global_impact_importance:    Boolean indicating whether to pre-calculate and global feature impact
                                                  and global feature importance.
        :param cache_dataset:                     Boolean indicating whether to cache dataset histograms.
                                                  Should be set to True for large datasets.
        """
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)
        dataset_id = type_enforce('dataset_id', dataset_id, str)

        path = ['trigger_pre_computation', self.org_id, project_id, model_id]
        payload = {
            'dataset_id': dataset_id,
            'calculate_predictions': calculate_predictions,
            'cache_global_pdps': cache_global_pdps,
            'cache_global_impact_importance': cache_global_impact_importance,
            'overwrite_cache': overwrite_cache,
            'batch_size': batch_size,
            'cache_dataset': cache_dataset,
        }
        try:
            result = self._call_executor_service(path, payload, stream=True)
            for res in result:
                print_streamed_result(res)
        except Exception as e:
            LOG.exception('Failed while trigger precomputation, error message: ')
            raise e

    def _deploy_container_model(
        self,
        project_id: str,
        model_id: str,
        dataset_id: str,
        model_info: ModelInfo,
        deployment_options: DeploymentOptions,
    ):
        if deployment_options.deployment_type == DeploymentType.FAR:
            deployment_options.deployment_type = DeploymentType.EXECUTOR
        else:
            deployment_options.deployment_type = DeploymentType.PREDICTOR
            if model_info.mlflow_params is None:
                port = 8080
                if deployment_options.port:
                    port = deployment_options.port
                host_name = model_string_to_hostname(
                    f'{self.org_id}-{project_id}-{model_id}'
                )
                default_mlflow_url = f'http://{host_name}:{port}/invocations'
                model_info.mlflow_params = MLFlowParams(
                    relative_path_to_saved_model='.', live_endpoint=default_mlflow_url
                )

        package_py = (
            'def get_model():\n  '
            'raise ValueError("This should not called. '
            'Use mlflow model container instead")'
        )

        with tempfile.TemporaryDirectory() as tmp:
            artifact_path = Path(tmp)
            package_file = artifact_path / 'package.py'
            package_file.write_text(package_py)

            return self._upload_model_custom(
                artifact_path=artifact_path,
                project_id=project_id,
                model_id=model_id,
                model_info=model_info,
                associated_dataset_ids=[dataset_id],
                deployment_options=deployment_options,
            )

    def register_model(
        self,
        project_id: str,
        model_id: str,
        dataset_id: str,
        model_info: ModelInfo,
        deployment: Optional[DeploymentOptions] = None,
        cache_global_impact_importance: bool = True,
        cache_global_pdps: bool = False,
        cache_dataset: bool = True,
    ):
        """
        Register a model in fiddler. This will generate a surrogate model,
        which can be replaced later with original model.

        Note: This method can take a while if the dataset is large. It is
        recommended to call register_model on a smaller representative
        dataset, before trying out on larger dataset.

        :param project_id: id of the project
        :param model_id: name to be used for the dataset and model
        :param dataset_id: id of the dataset to be used
        :param model_info: model info
        :param deployment: Model deployment options
        :param cache_global_impact_importance: Boolean indicating whether to pre-calculate and global feature impact
        and global feature importance.
        :param cache_global_pdps: Boolean indicating whether to pre-calculate and cache global partial dependence plots.
        :param cache_dataset: Boolean indicating whether to cache dataset histograms.
        Should be set to True for large datasets.
        """

        # Input Validation
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)
        dataset_id = type_enforce('dataset_id', dataset_id, str)

        safe_name_check(model_id, constants.MAX_ID_LEN, self.strict_mode)

        if self.strict_mode:
            model_info.validate()

        if not deployment:
            deployment = DeploymentOptions(deployment_type=DeploymentType.SURROGATE)

        # Register a surrogate model or Upload a far container model
        path = ['register_model', self.org_id, project_id, model_id]
        payload = {
            'dataset_id': dataset_id,
            'model_info': dict(model=model_info.to_dict()),
            'deployment_options': deployment.to_dict(),
            'cache_global_pdps': cache_global_pdps,
            'cache_global_impact_importance': cache_global_impact_importance,
            'cache_dataset': cache_dataset,
        }

        try:
            result = self._call_executor_service(path, payload, stream=True)
            for res in result:
                print_streamed_result(res)
        except Exception as e:
            LOG.exception('Failed to register model')
            raise e

    def update_model(
        self,
        project_id: str,
        model_id: str,
        model_dir: Path,
        force_pre_compute: bool = True,
    ):
        """
        update the specified model, with model binary and package.py from
        the specified model_dir

        Note: changes to model.yaml is not supported right now.

        :param project_id: project id
        :param model_id: model id
        :param model_dir: model directory
        :param force_pre_compute: if true refresh the pre-computated values.
               This can also be done manually by calling trigger_pre_computation
        :return: model artifacts
        """
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)
        model_dir = type_enforce('model_dir', model_dir, Path)

        if not model_dir.is_dir():
            raise ValueError(f'not a valid model directory: {model_dir}')
        yaml_file = model_dir / 'model.yaml'
        if not yaml_file.is_file():
            raise ValueError(f'Model yaml not found {yaml_file}')
        with yaml_file.open() as f:
            model_info = ModelInfo.from_dict(yaml.safe_load(f))

        if len(model_info.datasets) < 1:
            raise ValueError('Unable to find dataset in model.yaml')

        if len(model_info.datasets) > 1:
            raise ValueError('More than one dataset specified in model.yaml')
        dataset_id = model_info.datasets[0]

        remote_model_info = self.get_model_info(project_id, model_id)
        ddiff = DeepDiff(remote_model_info, model_info, ignore_order=True)

        if len(ddiff) > 0:
            raise ValueError(
                f'remote model info, does not match '
                f'local model info: {ddiff}. Updating model info '
                f'not currently supported'
            )

        print('Loading dataset info')
        dataset_info = self.get_dataset_info(project_id, dataset_id)

        if self.strict_mode:
            print('Validating ...')
            # todo: enable this validator. It need sklearn etc framework libs
            # in client path. So, not sure if we should do this by default
            # validator = PackageValidator(model_info, dataset_info, model_dir)
            # passed, errors = validator.run_chain()
            # if not passed:
            #     raise ValueError(f'validation failed with errors: {errors}')

            ModelInfoValidator(model_info, dataset_info).validate()
            model_info.validate()
        else:
            print('Validation skipped')

        tmp = tempfile.mkdtemp()
        shutil.make_archive(
            base_name=str(Path(tmp) / 'model_package'),
            format='tar',
            root_dir=str(model_dir),
            base_dir='.',
        )

        payload: Dict[str, Any] = {}
        endpoint_path = ['update_model', self.org_id, project_id, model_id]
        self._call(
            endpoint_path,
            json_payload=payload,
            files=[Path(tmp) / 'model_package.tar'],
        )
        print('Model updated')

        print('Testing updated model')
        should_log = self.connection.capture_server_log
        status = True
        for i in range(3):
            try:
                self.connection.capture_server_log = True
                sample_df = self._get_dataset_sample(project_id, dataset_id, 10)
                self.run_model(project_id, model_id, sample_df, log_events=False)
                print('Server Logs: ')
                print(self.connection.last_server_log)
                print()
                print('All tests passed ..')
                break
            except Exception as e:
                status = False
                if i == 2:
                    print(f'Test failed with error: {e}')
                else:
                    print(f'Retrying test {i}')
            finally:
                self.connection.capture_server_log = should_log

        if status and force_pre_compute:
            try:
                self.trigger_pre_computation(
                    project_id,
                    model_id,
                    dataset_id,
                    overwrite_cache=True,
                    calculate_predictions=True,
                    cache_global_pdps=True,
                    cache_global_impact_importance=True,
                )
            except Exception as e:
                print(
                    'Model was updated successfully, but failed to refresh '
                    'pre-computed values. You can retry this operation by '
                    f'calling trigger_pre_computation(), error: {e}'
                )
                status = False

        shutil.rmtree(tmp)
        return status

    ##### End: Methods related to uploading / registering model #####

    def initialize_monitoring(  # noqa
        self,
        project_id: str,
        model_id: str,
        enable_modify: Optional[bool] = False,
        verbose: Optional[bool] = False,
    ):
        """
        Ensure that monitoring has been setup and Fiddler is ready to ingest events.

        :param project_id:          The project for which to initialize monitoring.
        :param model_id:            The model for which to initialize monitoring.
        :param model_id:            The model for which to initialize monitoring.
        :param enable_modify:       Grant the Fiddler backend permission to
                                    modify model related objects, schema, etc.

                                    Can be bool  `True`/`False`, indicating global
                                    write/read-only permission.

                                    Alternatively, can be a sequence of elements
                                    from `fiddler.core_objects.InitMonitoringModifications`,
                                    in which case all listed elements will be
                                    assumed to be modifiable, and omitted ones
                                    will be read-only.
        :param verbose:             Bool indicating whether to run in verbose
                                    mode with longer debug messages for errors.

        :returns bool indicating whether monitoring could be setup correctly.
        """
        # TODO: only trigger model predictions if they do not already exist
        model_info = None
        dataset_id = None
        try:
            model_info = self.get_model_info(project_id, model_id)
        except Exception as e:
            print(
                f'Did not find ModelInfo for project "{project_id}" and model "{model_id}".'
            )
            raise e
        try:
            assert model_info is not None and model_info.datasets is not None
            dataset_id = model_info.datasets[0]
            assert dataset_id is not None
        except Exception as e:  # TODO: don't catch all exceptions.
            print(
                f'Unable to infer dataset from model_info for given project_id={project_id} and model_id={model_id}. Did your model_info specify a dataset?'
            )
            if verbose:
                print('The inferred dataset_id was: ')
                print(dataset_id)
                print()
                print('The inferred model_info was: ')
                print(model_info)
            raise e
        predictions_exist = False
        try:
            path = ['model_predictions_exist', self.org_id, project_id]
            payload: Dict[str, Any] = {
                'model': model_id,
                'dataset': dataset_id,
            }  # is dataset_id same as dataset_name?
            predictions_exist = self._call(path, json_payload=payload)
        except Exception as e:
            if verbose:
                print('Failed to check for predictions, regenerating by default')
                print(e)
            LOG.warning('Failed to check for predictions, regenerating by default')
            LOG.warning(e)
        if not predictions_exist:
            self._trigger_model_predictions(project_id, model_id, dataset_id)
        else:
            LOG.info(
                f'Predictions already exist for model={model_id}, dataset={dataset_id}'
            )
        default_modify = False
        if isinstance(enable_modify, bool):
            default_modify = enable_modify
        enable_backend_modifications = {
            check.value: default_modify
            for check in possible_init_monitoring_modifications
        }
        if isinstance(enable_modify, list) or isinstance(enable_modify, tuple):
            for mod in enable_modify:
                if type(mod) == InitMonitoringModifications:
                    mod = mod.value
                enable_backend_modifications[mod] = True
        elif type(enable_modify) == bool:
            pass
        else:
            raise NotImplementedError

        overall_result = True
        init_result = None
        try:
            path = ['init_monitoring', self.org_id, project_id, model_id]
            payload = {}
            payload['enable_modifications'] = enable_backend_modifications
            init_result = self._call(path, json_payload=payload)
        except Exception as e:
            print('Failed to setup monitoring, error message: ')
            raise e
        if init_result is not None:
            if init_result['success']:
                if verbose:
                    print(f"ERRORS: {init_result['errors']}")
                    print(f"MESSAGE: {init_result['message']}")
            else:
                print(f"ERRORS: {init_result['errors']}")
                print(f"MESSAGE: {init_result['message']}")
        else:
            print('Failed to setup monitoring, could not parse server response.')
            init_result = {'success': False}
        overall_result = overall_result and init_result['success']
        # For now, we only permit precomputation if no failures are found # TODO: allow precomputations for incomplete schema?
        if init_result['success'] is False:
            return False
        if verbose:
            print('Precomputing Dataset Histograms')
        precompute_result = None
        try:
            path = ['precompute', self.org_id, project_id, model_id]
            payload = {
                # 'dataset': dataset_id,
            }
            precompute_result = self._call(path, json_payload=payload)
        except Exception as e:
            print('Failed to precompute histograms, error message: ')
            raise e
        if precompute_result is not None:
            if precompute_result['success']:
                if verbose:
                    print('Successfully precomputed histograms, details: ')
                    print(precompute_result['message'])
            else:
                print('Failed to precompute histograms, details: ')
                print(precompute_result['message'])
        else:
            print('Failed to precompute histograms, could not parse server response.')
            precompute_result = {'success': False}
        overall_result = overall_result and precompute_result['success']

        if verbose:
            print(
                f'overall_result: {overall_result},\n\t- init_result: {init_result},\n\t- precompute_result: {precompute_result}'
            )
        return overall_result

    def add_monitoring_config(
        self,
        config_info: dict,
        project_id: Optional[str] = None,
        model_id: Optional[str] = None,
    ):
        """Adds a config for either an entire org, or project or a model.
        Here's a sample config:
        {
            'min_bin_value': 3600, # possible values 300, 3600, 7200, 43200, 86400, 604800 secs
            'time_ranges': ['Day', 'Week', 'Month', 'Quarter', 'Year'],
            'default_time_range': 7200,
            'tag': 'anything you want',
            ‘aggregation_config’: {
               ‘baseline’: {
                  ‘type’: ‘dataset’,
                  ‘dataset_name’: yyy
               }
            }
        }
        """
        # Type enforcement
        project_id = (
            type_enforce('project_id', project_id, str) if project_id else project_id
        )
        model_id = type_enforce('model_id', model_id, str) if model_id else model_id

        path = ['monitoring_setup', self.org_id]
        if project_id:
            path.append(project_id)
        if model_id:
            if not project_id:
                raise ValueError(
                    'We need to have a `project_id` when a model is specified'
                )
            path.append(model_id)

        result = self._call(path, config_info)
        self._dataset_baseline_display_message(result)
        return result

    def update_monitoring_config(
        self, config_info: dict, project_id: str, model_id: str
    ):
        """Only allows the users to update the aggregation config of the monitoring_config
        Here's a sample config:
        {
            ‘aggregation_config’: {
               ‘baseline’: {
                  ‘type’: ‘dataset’,
                  ‘dataset_name’: yyy
               }
            }
        }
        """
        # Type enforcement
        project_id = (
            type_enforce('project_id', project_id, str) if project_id else project_id
        )
        model_id = type_enforce('model_id', model_id, str) if model_id else model_id

        path = ['monitoring_update', self.org_id]
        if project_id:
            path.append(project_id)
        if model_id:
            if not project_id:
                raise ValueError(
                    'We need to have a `project_id` when a model is specified'
                )
            path.append(model_id)

        result = self._call(path, config_info)
        self._dataset_baseline_display_message(result['config_info'])
        return result

    def _dataset_baseline_display_message(self, config):
        try:
            aggregation_config_baseline = config['aggregation_config']['baseline']
            aggregation_config_baseline_type = aggregation_config_baseline['type']
            if aggregation_config_baseline_type == 'dataset':
                LOG.info(
                    'Dataset baseline will only be monitoring columns that are both present in the training data '
                    'and the specified dataset used as baseline'
                )
        except KeyError:
            pass

    ##### Start: Methods related to publishing event #####

    def _basic_drift_checks(self, project_id, model_info, model_id):
        # Lets make sure prediction table is created and has prediction data by
        # just running the slice query
        violations = []
        try:
            query_str = f'select * from "{model_info.datasets[0]}.{model_id}" limit 1'
            df = self.get_slice(
                query_str,
                project_id=project_id,
            )
            for index, row in df.iterrows():
                for out_col in model_info.outputs:
                    if out_col.name not in row:
                        msg = f'Drift error: {out_col.name} not in predictions table. Please delete and re-register your model.'
                        violations.append(
                            MonitoringViolation(MonitoringViolationType.WARNING, msg)
                        )
        except RuntimeError:
            msg = 'Drift error: Predictions table does not exists. Please run trigger_pre_computation for an existing model, or use register_model to register a new model.'
            violations.append(MonitoringViolation(MonitoringViolationType.WARNING, msg))
            return violations

        return violations

    def publish_event(
        self,
        project_id: str,
        model_id: str,
        event: dict,
        event_id: Optional[str] = None,
        update_event: Optional[bool] = None,
        event_timestamp: Optional[int] = None,
        timestamp_format: FiddlerTimestamp = FiddlerTimestamp.INFER,
        casting_type: Optional[bool] = False,
        dry_run: Optional[bool] = False,
    ):
        """
        Publishes an event to Fiddler Service.
        :param project_id: The project to which the model whose events are being published belongs
        :param model_id: The model whose events are being published
        :param dict event: Dictionary of event details, such as features and predictions.
        :param event_id: Unique str event id for the event
        :param update_event: Bool indicating if the event is an update to a previously published row
        :param event_timestamp: The UTC timestamp of the event in epoch milliseconds (e.g. 1609462800000)
        :param timestamp_format:   Format of timestamp within batch object. Can be one of:
                                - FiddlerTimestamp.INFER
                                - FiddlerTimestamp.EPOCH_MILLISECONDS
                                - FiddlerTimestamp.EPOCH_SECONDS
                                - FiddlerTimestamp.ISO_8601
        :param casting_type: Bool indicating if fiddler should try to cast the data in the event with
        the type referenced in model info. Default to False.
        :param dry_run: If true, the event isnt published and instead the user gets a report which shows
        IF the event along with the model would face any problems with respect to monitoring

        """
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)
        event = type_enforce('event', event, dict)
        if event_id:
            event_id = type_enforce('event_id', event_id, str)

        if casting_type:
            try:
                model_info = self.get_model_info(project_id, model_id)
            except RuntimeError:
                raise RuntimeError(
                    f'Did not find ModelInfo for project "{project_id}" and model "{model_id}".'
                )
            event = cast_input_data(event, model_info)

        if not timestamp_format or timestamp_format not in FiddlerTimestamp:
            raise ValueError('Please specify a valid timestamp_format')

        assert timestamp_format is not None, 'timestamp_format unexpectedly None'
        event['__timestamp_format'] = timestamp_format.value

        if update_event:
            event['__event_type'] = 'update_event'
            event['__updated_at'] = event_timestamp
            if event_id is None:
                raise ValueError('An update event needs an event_id')
        else:
            event['__event_type'] = 'execution_event'
            event['__occurred_at'] = event_timestamp

        if event_id is not None:
            event['__event_id'] = event_id

        if dry_run:
            violations = self._pre_flight_monitoring_check(project_id, model_id, event)
            violations_list = []
            print('\n****** publish_event dry_run report *****')
            print(f'Found {len(violations)} Violations:')
            for violation in violations:
                violations_list.append(
                    {'type': violation.type.value, 'desc': violation.desc}
                )
                print(f'Type: {violation.type.value: <11}{violation.desc}')
            result = json.dumps(violations_list)
        else:
            path = ['external_event', self.org_id, project_id, model_id]
            # The ._call uses `timeout` and `num_tries` logic due to an issue with Mac/Docker.
            # This is only enabled using the env variable `FIDDLER_RETRY_PUBLISH`; otherwise it
            # is a normal ._call function
            result = self._call(path, event, timeout=2, num_tries=5)

        return result

    def _pre_flight_monitoring_check(self, project_id, model_id, event):
        violations = []
        violations += self._basic_monitoring_tests(project_id, model_id)
        if len(violations) == 0:
            model_info = self.get_model_info(project_id, model_id)
            dataset_info = self.get_dataset_info(project_id, model_info.datasets[0])
            violations += self._basic_drift_checks(project_id, model_info, model_id)
            violations += self.monitoring_validator.pre_flight_monitoring_check(
                event, model_info, dataset_info
            )
        return violations

    def _basic_monitoring_tests(self, project_id, model_id):
        """ Basic checks which would prevent monitoring from working altogether. """
        violations = []
        try:
            model_info = self.get_model_info(project_id, model_id)
        except RuntimeError:
            msg = f'Error: Model:{model_id} in project:{project_id} does not exist'
            violations.append(MonitoringViolation(MonitoringViolationType.FATAL, msg))
            return violations

        try:
            _ = self.get_dataset_info(project_id, model_info.datasets[0])
        except RuntimeError:
            msg = f'Error: Dataset:{model_info.datasets[0]} does not exist'
            violations.append(MonitoringViolation(MonitoringViolationType.FATAL, msg))
            return violations

        return violations

    def publish_events_log(
        self,
        project_id: str,
        model_id: str,
        logs: pd.DataFrame,
        force_publish: Optional[bool] = None,
        ts_column: Optional[str] = None,
        default_ts: Optional[int] = None,
        num_threads: int = 1,
        batch_size: Optional[int] = None,
        casting_type: Optional[bool] = False,
    ):
        """
        [SOON TO BE DEPRECATED] Publishes prediction log to Fiddler Service.
        :param project_id:    The project to which the model whose events are being published belongs
        :param model_id:      The model whose events are being published
        :param logs:          Data frame of event details, such as features and predictions.
        :param force_publish: Continue with publish even if all input and output columns not in log.
        :param ts_column:     Column to extract timestamp value from.
                              Timestamp must be UTC in format: `%Y-%m-%d %H:%M:%S.%f` (e.g. 2020-01-01 00:00:00.000000)
                              or as the timestamp of the event in epoch milliseconds (e.g. 1609462800000)
        :param default_ts:    Default timestamp to use if ts_column not specified.
                              Must be given as the timestamp of the event in epoch milliseconds (e.g. 1609462800000)
        :param num_threads:   Number of threads to parallelize this function over. Dataset will be divided evenly
                              over the number of threads.
        :param batch_size:    Size of dataframe to publish in any given run.
        :param casting_type: Bool indicating if fiddler should try to cast the data in the event with
        the type referenced in model info. Default to False.

        """
        # Type enforcement
        print(
            'WARNING: This method will be deprecated in a future version. Please use the method `publish_events_batch` instead.'
        )
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)

        if num_threads < 1 or num_threads > 20:
            raise ValueError(
                'Please adjust parameter `num_threads` to be between 1 and 20.'
            )
        if batch_size and (batch_size < 1 or batch_size > 100000):
            raise ValueError(
                'Please adjust parameter `batch_size` to be between 1 and 100000, or type `None`.'
            )
        if default_ts and not isinstance(default_ts, int):
            raise ValueError(
                'Please adjust parameter `default_ts` to be of type `int` or type `None`.'
            )
        model_info = self.get_model_info(project_id, model_id)
        if casting_type:
            logs = cast_input_data(logs, model_info)

        log_columns = [c for c in list(logs.columns)]
        in_columns = [c.name for c in model_info.inputs]
        in_not_found = [c for c in in_columns if c not in log_columns]
        out_columns = [c.name for c in model_info.outputs]
        out_not_found = [c for c in out_columns if c not in log_columns]
        if (out_not_found or in_not_found) and not force_publish:
            raise ValueError(
                f'Model output columns "{out_not_found}" or input columns "{in_not_found}"'
                f'not found in logs. If this is expected try again with force_publish=True.'
            )

        payload: Dict[str, Any] = dict()
        if ts_column is not None:
            if ts_column not in log_columns:
                raise ValueError(f'Did not find {ts_column} in the logs columns.')
            payload['ts_column'] = ts_column
        else:
            if default_ts is None:
                default_ts = int(round(time.time() * 1000))
            payload['default_ts'] = default_ts
        include_index = logs.index.name is not None

        worker_lock = threading.Lock()
        workers_list = []

        class _PublishEventsLogWorker(threading.Thread):
            """
            Handles the call to `publish_events_log`
            """

            def __init__(
                self,
                thread_id,
                df,
                client,
                payload,
                org_id,
                project_id,
                model_id,
                include_index,
                batch_size,
                worker_lock,
                only_worker,
            ):
                threading.Thread.__init__(self)
                self.thread_id = thread_id
                self.df = df
                self.client = client
                self.payload = copy.deepcopy(payload)
                self.org_id = org_id
                self.project_id = project_id
                self.model_id = model_id
                self.include_index = include_index
                self.batch_size = batch_size
                self.worker_lock = worker_lock
                self.only_worker = only_worker
                self.path = [
                    'publish_events_log',
                    self.org_id,
                    self.project_id,
                    self.model_id,
                ]

            def run(self):
                df_batches = []
                if self.batch_size:
                    # Divide dataframe into size of self.batch_size
                    num_chunks = math.ceil(len(self.df) / self.batch_size)
                    for j in range(num_chunks):
                        df_batches.append(
                            self.df[j * self.batch_size : (j + 1) * self.batch_size]
                        )
                else:
                    df_batches.append(self.df)

                with tempfile.TemporaryDirectory() as tmp:
                    # To maintain the same data types during transportation from client
                    #  to server, we must explicitly send and recreate the data types through
                    #  a file. Otherwise, Pandas.from_csv() will convert quoted strings to integers.
                    #  See: https://github.com/pandas-dev/pandas/issues/35713
                    log_path = Path(tmp) / 'log.csv'
                    dtypes_path = Path(tmp) / 'dtypes.csv'
                    self.df.dtypes.to_frame('types').to_csv(dtypes_path)
                    csv_paths = [dtypes_path, log_path]

                    for curr_batch in df_batches:
                        # Overwrite CSV with current batch
                        curr_batch.to_csv(log_path, index=self.include_index)

                        result = self.client._call(
                            self.path, json_payload=self.payload, files=csv_paths
                        )

                        with self.worker_lock:
                            # Used to prevent printing clash
                            if self.only_worker:
                                print(result)
                            else:
                                print(f'thread_id {self.thread_id}: {result}')

        # Divide dataframe evenly amongst each thread
        df_split = np.array_split(logs, num_threads)

        for i in range(num_threads):
            workers_list.append(
                _PublishEventsLogWorker(
                    i,
                    df_split[i],
                    self,
                    payload,
                    self.org_id,
                    project_id,
                    model_id,
                    include_index,
                    batch_size,
                    worker_lock,
                    num_threads == 1,
                )
            )
            workers_list[i].start()

        for i in range(num_threads):
            workers_list[i].join()

    def publish_events_batch(  # noqa
        self,
        project_id: str,
        model_id: str,
        batch_source: Union[pd.DataFrame, str],
        id_field: Optional[str] = None,
        update_event: Optional[bool] = False,
        timestamp_field: Optional[str] = None,
        timestamp_format: FiddlerTimestamp = FiddlerTimestamp.INFER,
        data_source: Optional[BatchPublishType] = None,
        casting_type: Optional[bool] = False,
        credentials: Optional[dict] = None,
        group_by: Optional[str] = None,
    ):
        """
        Publishes a batch events object to Fiddler Service.
        :param project_id:    The project to which the model whose events are being published belongs.
        :param model_id:      The model whose events are being published.
        :param batch_source:  Batch object to be published. Can be one of: Pandas DataFrame, CSV file, PKL Pandas DataFrame, or Parquet file.
        :param id_field:  Column to extract id value from.
        :param update_event: Bool indicating if the events are updates to previously published rows
        :param timestamp_field:     Column to extract timestamp value from.
                              Timestamp must match the specified format in `timestamp_format`.
        :param timestamp_format:   Format of timestamp within batch object. Can be one of:
                                - FiddlerTimestamp.INFER
                                - FiddlerTimestamp.EPOCH_MILLISECONDS
                                - FiddlerTimestamp.EPOCH_SECONDS
                                - FiddlerTimestamp.ISO_8601
        :param data_source:   Source of batch object. In case of failed inference, can be one of:
                                - BatchPublishType.DATAFRAME
                                - BatchPublishType.LOCAL_DISK
                                - BatchPublishType.AWS_S3
                                - BatchPublishType.GCP_STORAGE
        :param casting_type: Bool indicating if fiddler should try to cast the data in the event with
                             the type referenced in model info. Default to False.
        :param credentials:  Dictionary containing authorization for AWS or GCP.

                             For AWS S3, list of expected keys are
                              ['aws_access_key_id', 'aws_secret_access_key', 'aws_session_token']
                              with 'aws_session_token' being applicable to the AWS account being used.

                             For GCP, list of expected keys are
                              ['gcs_access_key_id', 'gcs_secret_access_key', 'gcs_session_token']
                              with 'gcs_session_token' being applicable to the GCP account being used.
        :param group_by: Column to group events together for Model Performance metrics. For example,
                         in ranking models that column should be query_id or session_id, used to
                         compute NDCG and MAP. Be aware that the batch_source file/dataset provided should have
                         events belonging to the SAME query_id/session_id TOGETHER and cannot be mixed
                         in the file. For example, having a file with rows belonging to query_id 31,31,31,2,2,31,31,31
                         would not work. Please sort the file by group_by group first to have rows with
                         the following order: query_id 31,31,31,31,31,31,2,2.
        """

        if not timestamp_format or timestamp_format not in FiddlerTimestamp:
            raise ValueError('Please specify a valid timestamp_format')

        assert timestamp_format is not None, 'timestamp_format unexpectedly None'

        path = ['publish_events_batch', self.org_id, project_id, model_id]
        payload: Dict[str, Any] = {
            'casting_type': casting_type,
            'is_update_event': update_event,
            'timestamp_format': timestamp_format.value,
        }

        if id_field is not None:
            payload['id_field'] = id_field
        if timestamp_field is not None:
            payload['timestamp_field'] = timestamp_field
        if group_by is not None:
            payload['group_by'] = group_by

        # Default to current time for case when no timestamp field specified
        if timestamp_field is None:
            curr_timestamp = formatted_utcnow(
                milliseconds=int(round(time.time() * 1000))
            )
            LOG.info(
                f'`timestamp_field` not specified. Using current UTC time `{curr_timestamp}` as default'
            )
            payload['default_timestamp'] = curr_timestamp

        return self._publish_event_batch(
            req_path=path,
            req_payload=payload,
            batch_source=batch_source,
            data_source=data_source,
            credentials=credentials,
        )

    def publish_events_batch_schema(  # noqa
        self,
        batch_source: Union[pd.DataFrame, str],
        publish_schema: Dict[str, Any],
        data_source: Optional[BatchPublishType] = None,
        credentials: Optional[dict] = None,
        group_by: Optional[str] = None,
    ):
        """
        Publishes a batch events object to Fiddler Service.
        :param batch_source:  Batch object to be published. Can be one of: Pandas DataFrame, CSV file, PKL Pandas DataFrame, or Parquet file.
        :param publish_schema: Dict object specifying layout of data.
        :param data_source:   Source of batch object. In case of failed inference, can be one of:
                                - BatchPublishType.DATAFRAME
                                - BatchPublishType.LOCAL_DISK
                                - BatchPublishType.AWS_S3
                                - BatchPublishType.GCP_STORAGE
        :param credentials:  Dictionary containing authorization for AWS or GCP.

                             For AWS S3, list of expected keys are
                              ['aws_access_key_id', 'aws_secret_access_key', 'aws_session_token']
                              with 'aws_session_token' being applicable to the AWS account being used.

                             For GCP, list of expected keys are
                              ['gcs_access_key_id', 'gcs_secret_access_key', 'gcs_session_token']
                              with 'gcs_session_token' being applicable to the GCP account being used.
        :param group_by: Column to group events together for Model Performance metrics. For example,
                         in ranking models that column should be query_id or session_id, used to
                         compute NDCG and MAP.
        """

        path = ['publish_events_batch_schema', self.org_id]
        payload = {
            'publish_schema': publish_schema,
            'group_by': group_by,
        }

        return self._publish_event_batch(
            req_path=path,
            req_payload=payload,
            batch_source=batch_source,
            data_source=data_source,
            credentials=credentials,
        )

    def _publish_event_batch(
        self,
        req_path: List[str],
        req_payload: Dict[str, Any],
        batch_source: Union[pd.DataFrame, str],
        data_source: Optional[BatchPublishType] = None,
        credentials: Optional[dict] = None,
    ):
        if data_source is None:
            data_source = infer_data_source(source=batch_source)
            LOG.info(
                f'`data_source` not specified. Inferred `data_source` as '
                f'BatchPublishType.{BatchPublishType(data_source.value).name}'
            )

        if data_source not in BatchPublishType:
            raise ValueError('Please specify a valid batch_source')

        assert data_source is not None, 'data_source unexpectedly None'

        req_payload['data_source'] = data_source.value

        if data_source == BatchPublishType.DATAFRAME:
            # Converting dataframe to local disk format for transmission
            req_payload['data_source'] = BatchPublishType.LOCAL_DISK.value

            assert isinstance(
                batch_source, pd.DataFrame
            ), 'batch_source unexpectedly not a DataFrame'

            df = batch_source.copy()
            if df.index.name is not None:
                df.reset_index(inplace=True)

            clean_df_types(df)

            with tempfile.TemporaryDirectory() as tmp_dir:
                file_path = Path(tmp_dir) / f'log.{PARQUET_EXTENSION}'

                write_dataframe_to_parquet_file(df=df, file_path=file_path)

                result = self._call(
                    path=req_path,
                    json_payload=req_payload,
                    files=[file_path],
                    stream=True,
                )

        elif data_source == BatchPublishType.LOCAL_DISK:
            local_file_path = batch_source
            result = self._call(
                path=req_path,
                json_payload=req_payload,
                files=[Path(local_file_path)],
                stream=True,
            )

        elif data_source == BatchPublishType.AWS_S3:
            s3_uri = batch_source
            # Validate S3 credentials
            validate_s3_uri_access(s3_uri, credentials, throw_error=True)
            with tempfile.NamedTemporaryFile() as tmp:
                # tmp is a dummy file passed to BE for ease of API consolidation
                req_payload['file_path'] = s3_uri
                req_payload['credentials'] = credentials
                result = self._call(
                    path=req_path,
                    json_payload=req_payload,
                    files=[Path(tmp.name)],
                    stream=True,
                )

        elif data_source == BatchPublishType.GCP_STORAGE:
            gcp_uri = batch_source
            # Validate GCS credentials
            gcs_credentials: Optional[Dict[str, Any]] = None
            if credentials is not None:
                gcs_credentials = {}
                if 'gcs_access_key_id' in credentials:
                    gcs_credentials['aws_access_key_id'] = credentials[
                        'gcs_access_key_id'
                    ]
                if 'gcs_secret_access_key' in credentials:
                    gcs_credentials['aws_secret_access_key'] = credentials[
                        'gcs_secret_access_key'
                    ]
                if 'gcs_session_token' in credentials:
                    gcs_credentials['aws_session_token'] = credentials[
                        'gcs_session_token'
                    ]

            validate_gcp_uri_access(gcp_uri, gcs_credentials, throw_error=True)
            with tempfile.NamedTemporaryFile() as tmp:
                # tmp is a dummy file passed to BE for ease of API consolidation
                req_payload['file_path'] = gcp_uri
                req_payload['credentials'] = gcs_credentials
                result = self._call(
                    path=req_path,
                    json_payload=req_payload,
                    files=[Path(tmp.name)],
                    stream=True,
                )
        else:
            raise ValueError(f'Data source {data_source} not supported')

        final_return = None
        for res in result:
            print_streamed_result(res)
            final_return = res

        return final_return

    def publish_parquet_s3(
        self,
        project_id: str,
        model_id: str,
        parquet_file: str,
        auth_context: Optional[Dict[str, Any]] = None,
        ts_column: Optional[str] = None,
        default_ts: Optional[int] = None,
    ):
        """
        [SOON TO BE DEPRECATED] Publishes parquet events file from S3 to Fiddler instance. Experimental and may be expanded in the future.

        :param project_id:    The project to which the model whose events are being published belongs
        :param model_id:      The model whose events are being published
        :param parquet_file:  s3_uri for parquet file to be published
        :param auth_context:  Dictionary containing authorization for AWS. List of expected keys are
                              ['aws_access_key_id', 'aws_secret_access_key', 'aws_session_token']
                              with 'aws_session_token' being applicable to the AWS account being used.
        :param ts_column:     Column to extract time stamp value from.
                              Timestamp must be UTC in format: `%Y-%m-%d %H:%M:%S.%f` (e.g. 2020-01-01 00:00:00.000000)
                              or as the timestamp of the event in epoch milliseconds (e.g. 1609462800000)
        :param default_ts:    Default timestamp to use if ts_column not specified.
                              Must be given as the timestamp of the event in epoch milliseconds (e.g. 1609462800000)
        """
        # Type enforcement
        print(
            'WARNING: This method will be deprecated in a future version. Please use the method `publish_events_batch` instead.'
        )
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)

        payload: Dict[str, Any] = dict()
        payload['file_path'] = parquet_file
        payload['auth_context'] = auth_context

        # Validate S3 creds
        validate_s3_uri_access(parquet_file, auth_context, throw_error=True)

        if ts_column is not None:
            payload['ts_column'] = ts_column
        else:
            if default_ts is None:
                default_ts = int(round(time.time() * 1000))
            payload['default_ts'] = default_ts

        publish_path = ['publish_parquet_file', self.org_id, project_id, model_id]
        publish_result = self._call(publish_path, json_payload=payload, stream=True)
        for res in publish_result:
            print(res)

    ##### End: Methods related to publishing event #####

    def generate_sample_events(
        self,
        project_id: str,
        model_id: str,
        dataset_id: str,
        number_of_events: int = 100,
        time_range: int = 8,
    ):
        """
        Generate monitoring traffic for the given model. Traffic is generated
        by randomly sampling rows from the specified dataset.

        Note: This method can be used to generate monitoring traffic for
        testing purpose. In production, use publish_event or publish_events_logs
        to send model input and output to fiddler.

        :param project_id:
        :param model_id:
        :param dataset_id:
        :param number_of_events: number of prediction events to generate
        :param time_range: number of days. time_range is used
                to spread the traffic
        :return: sample events that can be published to fiddler
        """
        # Type enforcement
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)
        dataset_id = type_enforce('dataset_id', dataset_id, str)

        if number_of_events < 1 or number_of_events > 1000:
            raise ValueError('number_of_events must be between 1 and 1000')

        if time_range < 1 or time_range > 365:
            raise ValueError('time_range must be between 1 and 365 days')

        event_sample_df = self._get_dataset_sample(
            project_id, dataset_id, number_of_events
        )

        model_info = self.get_model_info(project_id, model_id)
        outputs_available = all(
            c in event_sample_df for c in model_info.get_output_names()
        )

        if outputs_available:
            result_df = event_sample_df
        else:
            # get prediction result
            result = self.run_model(
                project_id, model_id, event_sample_df, log_events=False
            )
            result_df = pd.concat([event_sample_df, result], axis=1)

        # create well distributed time stamps
        ONE_DAY_MS = 8.64e7
        event_time = round(time.time() * 1000) - (ONE_DAY_MS * time_range)
        interval = round((time.time() * 1000 - event_time) / number_of_events)
        time_stamp = []
        for i in range(0, len(result_df)):
            time_stamp.append(event_time)
            event_time = event_time + random.randint(1, interval * 2)
        result_df['__occurred_at'] = time_stamp

        return result_df

    def _get_dataset_sample(self, project_id, dataset_id, sample_size):
        dataset_dict = self.get_dataset(
            project_id, dataset_id, max_rows=sample_size, sampling=True
        )
        datasets = dataset_dict.values()
        for df in datasets:
            df.reset_index(inplace=True, drop=True)
        df = pd.concat(datasets, ignore_index=True)
        if len(df) > sample_size:
            df = df[:sample_size]
        # note: len(df) can be less than sample_size
        return df

    def get_model(self, project_id: str, model_id: str, output_dir: Path):
        """
        download the model binary, package.py and model.yaml to the given
        output dir.

        :param project_id: project id
        :param model_id: model id
        :param output_dir: output directory
        :return: model artifacts
        """
        return self.project(project_id).model(model_id).download(output_dir)

    def list_segments(
        self,
        project_id: str,
        model_id: str,
        activated: Optional[bool] = None,
        schema_version: Optional[float] = None,
    ):
        """
        List all segments currently associated with a model. Can filter by activated / schema_version if desired.

        activated = [None/True/False], for all, activated-only, deactivate-only, respectively
        schema_verios = [None/0.1] for all, 0.1 respectively
        """
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)
        res = None
        path = ['list_segments', self.org_id, project_id, model_id]
        payload: Dict[str, Any] = {}
        payload['activated'] = activated
        payload['schema_version'] = schema_version
        res = self._call(path, json_payload=payload)
        if res is None:
            print('Could not get segments for this model.')
        return res

    def upload_segment(
        self,
        project_id: str,
        model_id: str,
        segment_id: str,
        segment_info: SegmentInfo,
    ):
        """Validates and uploads an existing SegmentInfo object to Fiddler."""
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)
        segment_id = type_enforce('segment_id', segment_id, str)
        safe_name_check(segment_id, constants.MAX_ID_LEN, self.strict_mode)

        model_info = None
        try:
            model_info = self.get_model_info(project_id, model_id)
        except Exception as e:
            print(
                f'Did not find ModelInfo for project "{project_id}" and model "{model_id}".'
            )
            raise e

        try:
            assert _validate_segment(segment_id, segment_info, model_info)
        except MalformedSchemaException as mse:
            print(
                f'Could not validate SegmentInfo, does the object conform to schema version {CURRENT_SCHEMA_VERSION}?'
            )
            raise mse
        seg_info = segment_info.to_dict()

        res = None
        path = ['define_segment', self.org_id, project_id, model_id, segment_id]
        res = self._call(path, json_payload=seg_info)
        if res is None:
            print('Could not create segment.')
        return res

    def activate_segment(self, project_id: str, model_id: str, segment_id: str):
        """Activate an existing segment in Fiddler"""
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)
        segment_id = type_enforce('segment_id', segment_id, str)
        res = None
        path = ['activate_segment', self.org_id, project_id, model_id, segment_id]
        res = self._call(path)
        if res is None:
            print('Could not activate segment.')
        return res

    def deactivate_segment(self, project_id: str, model_id: str, segment_id: str):
        """Deactivate an existing segment in Fiddler"""
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)
        segment_id = type_enforce('segment_id', segment_id, str)
        res = None
        path = ['deactivate_segment', self.org_id, project_id, model_id, segment_id]
        res = self._call(path)
        if res is None:
            print('Could not deactivate segment.')
        return res

    def delete_segment(self, project_id: str, model_id: str, segment_id: str):
        """Deletes a deactivated segments from Fiddler"""
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)
        segment_id = type_enforce('segment_id', segment_id, str)
        res = None
        path = ['delete_segment', self.org_id, project_id, model_id, segment_id]
        res = self._call(path)
        if res is None:
            print('Could not delete segment.')
        return res

    def get_segment_info(self, project_id: str, model_id: str, segment_id: str):
        """Get the SegmentInfo specified from Fiddler"""
        project_id = type_enforce('project_id', project_id, str)
        model_id = type_enforce('model_id', model_id, str)
        segment_id = type_enforce('segment_id', segment_id, str)
        res = None
        path = ['get_segment', self.org_id, project_id, model_id, segment_id]
        res = self._call(path)
        if res is None:
            print('Could not get segment_info.')
            raise RuntimeError('res is unexpectedly None')
        if res['success']:
            return SegmentInfo.from_dict(res['segment_info'])
        else:
            return None


def _validate_segment(segment_id, segment_info, model_info):
    """helper to validate a segment"""
    if segment_info.segment_id != segment_id:
        raise MalformedSchemaException(
            f'Specified segment_id={segment_id} != segment_info.segment_id={segment_info.segment_id}.'
        )
    return segment_info.validate(model_info)

    # def get_segment_filter_labels(self, project_id, model_id, features=None):
    #     """Potentially for use in seg-monitoring v2: custom segments"""
    #     model_info = self.get_model_info(project_id, model_id)
    #     all_cols = []
    #     if model_info.inputs is not None:
    #         all_cols += model_info.inputs
    #     if model_info.outputs is not None:
    #         all_cols += model_info.outputs
    #     if model_info.targets is not None:
    #         all_cols += model_info.targets
    #     if model_info.decisions is not None:
    #         all_cols += model_info.decisions
    #     if model_info.metadata is not None:
    #         all_cols += model_info.metadata
    #     all_symbols = [col.name for col in all_cols]
    #     if features is None:
    #         features = all_symbols
    #     invalid_cols = [col for col in features if col not in all_symbols]
    #     if len(invalid_cols) > 0:
    #         raise ValueError(f'Cannot produce segment filter labels for features {invalid_cols}, as they could not be found in the model schema.')
    #     result_features = [col for col in features]
    #     return symbols(result_features), result_features
