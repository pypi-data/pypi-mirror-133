"""
Fiddler Client Module
=====================

A Python client for Fiddler service.

TODO: Add Licence.
"""
from . import utils
from ._version import __version__
from .client import Fiddler, PredictionEventBundle
from .core_objects import (
    BatchPublishType,
    Column,
    DatasetInfo,
    DataType,
    ExplanationMethod,
    FiddlerPublishSchema,
    FiddlerTimestamp,
    MLFlowParams,
    ModelDeploymentParams,
    ModelInfo,
    ModelInputType,
    ModelTask,
)
from .fiddler_api import FiddlerApi
from .file_processor.src.constants import (
    CSV_EXTENSION,
    PARQUET_COMPRESSION,
    PARQUET_ENGINE,
    PARQUET_EXTENSION,
    PARQUET_ROW_GROUP_SIZE,
)
from .utils import ColorLogger
from .validator import PackageValidator, ValidationChainSettings, ValidationModule

__all__ = [
    '__version__',
    'BatchPublishType',
    'Column',
    'ColorLogger',
    'DatasetInfo',
    'DataType',
    'Fiddler',
    'FiddlerApi',
    'FiddlerTimestamp',
    'FiddlerPublishSchema',
    'MLFlowParams',
    'ModelDeploymentParams',
    'ModelInfo',
    'ModelInputType',
    'ModelTask',
    'ExplanationMethod',
    'PredictionEventBundle',
    'PackageValidator',
    'ValidationChainSettings',
    'ValidationModule',
    'utils',
    # Exposing constants
    'CSV_EXTENSION',
    'PARQUET_EXTENSION',
    'PARQUET_ROW_GROUP_SIZE',
    'PARQUET_ENGINE',
    'PARQUET_COMPRESSION',
]
