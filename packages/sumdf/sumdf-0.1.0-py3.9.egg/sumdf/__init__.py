import collections

import attrdict

custom = attrdict.AttrDict()


def set_param_names(param_names):
    global custom
    custom["param_names"] = param_names


def get_param_namedtuple():
    return collections.namedtuple("Param", custom.param_names)


def get_param(params):
    """
    Parameters
    ----------
    params : iterator of parameter
    """
    return get_param_namedtuple()(*params)


from sumdf.Logging import setup_logger, get_root_logger, set_log_level

logger = get_root_logger()

from sumdf.Dataset import Dataset
from sumdf.Database import Database
from sumdf.DatasUtility import tie
