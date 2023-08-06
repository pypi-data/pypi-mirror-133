import importlib
import pickle

import numpy
import pandas
import seaborn
import tqdm

from sumdf import custom
from sumdf.Logging import setup_logger
from sumdf.Dataset import Dataset
from sumdf.DatasUtility import ParamSet, tie
from sumdf.Plots import *

logger = setup_logger(name=__name__)


class Database:
    """Dataset Manager

    Attributes
    ----------
    datasets : dict of Dataset
    params : set of Param
    iter_wrapper : function
    processes : int
    """

    def __init__(self, datasets=None):
        if datasets is None:
            self.datasets = dict()
        else:
            self.datasets = datasets
        self.params = ParamSet(self.datasets.keys())
        self.iter_wrapper = lambda x, *args, **kwargs: x
        self.processes = 1
        self.__columns = set()
        for dataset in self.datasets:
            self.__columns |= dataset.columns()

    def columns(self):
        return self.__columns

    def set_processes(self, processes):
        """
        Parameters
        ----------
        processes : int
            number of processes
        """
        assert isinstance(processes, int)
        self.processes = processes
        return self

    def set_tqdm(self):
        """set tqdm wrapper of getitem"""
        self.iter_wrapper = tqdm.tqdm
        return self

    def unset_tqdm(self):
        """set non-display wrapper of getitem"""
        self.iter_wrapper = lambda x, *args, **kwargs: x
        return self

    def add_dataset(self, dataset, param=None):
        """
        Parameters
        ----------
        dataset : Dataset
        param : Param
        """
        assert param is not None or dataset.param is not None
        assert (param is None or dataset.param is None) or param == dataset.param
        if param is None:
            param = dataset.param
        self.datasets[param] = dataset
        self.__columns |= dataset.columns()
        self.params.add(param)
        return self

    def add_dataframe(self, dataframe, param):
        """
        Parameters
        ----------
        dataframe : pandas.Dataframe
        param : Param
        """
        return self.add_dataset(Dataset(dataframe, param))

    def to_dataset(self):
        """
        Returns
        -------
        Dataset
        """
        if len(self) > 1:
            print("donot output Dataset because this includes multi datasets")
            return None
        return list(self.datasets.values())[0]

    def sub(self, param=None, **kwargs):
        """create sub-Database

        Parameters
        ----------
        param : None or Param
        """
        assert param is None or (isinstance(param, tuple) and not kwargs)
        assert (
            len(set(kwargs.keys()) - set(custom.param_names)) == 0
        ), f"invalid param is included in {set(kwargs.keys())}"
        item_list = ["*"] * len(custom.param_names)
        if param is not None:
            for i, value in enumerate(param):
                item_list[i] = value
        else:
            for i, param in enumerate(custom.param_names):
                if param in kwargs:
                    item_list[i] = kwargs[param]
        return self[item_list]

    def clone(self):
        """clone this Database"""
        item_list = ["*"] * len(custom.param_names)
        return self[item_list]

    def min(self, item):
        """get minimum value of item"""
        return min(dataset.min(item) for dataset in self)

    def max(self, item):
        """get maximum value of item"""
        return max(dataset.max(item) for dataset in self)

    def reduce(
        self,
        key,
        items=None,
        reduce_func=numpy.mean,
        lim=None,
        num=100,
        overwrap=0.0,
        extend=True,
    ):
        """Reduce all datasets to create a single dataset

        Parameters
        ----------
        key : str
            reduce key
        items : list of str
            items
        reduce_func : func
            argument is list of values -> value
        lim : limit of key
            e.g.) (-1, 4)
        num : None or int
            split number of key
        overwrap : float
            plot only if at least a percentage x of the dataset holds the x-data
        extend : bool
            if it is true, extend and describe the data at the end of the x-axis for each dataset
        """
        assert callable(reduce_func)
        assert 0.0 <= overwrap <= 1.0
        assert lim is None or len(lim) == 2

        if lim is None:
            min_key = self.min(key)
            max_key = self.max(key)
        else:
            min_key = lim[0]
            max_key = lim[1]
        if items is None:
            items = self.keys() - {key}
        key_vals = numpy.linspace(min_key, max_key, num)
        key_vals = numpy.append(key_vals, max_key + 1e-5)
        data_dict = {key_val: {key: key_val} for key_val in key_vals[:-1]}

        for item in items:
            data_generators = [
                dataset.sort(key=key).data_generator(key, key_vals, extend)
                for dataset in self
            ]
            for key_min, key_max in zip(key_vals, key_vals[1:]):
                values = list()
                for data_generator in data_generators:
                    data = next(data_generator)
                    if data is not None:
                        values.append(data[item])
                if len(values) >= overwrap * len(data_generators):
                    data_dict[key_min][item] = reduce_func(values)
                else:
                    del data_dict[key_min]

        return Dataset(data=pandas.DataFrame(data_dict.values())).sort(key=key)

    def lineplot(
        self,
        xitem,
        yitem,
        xlim=None,
        xnum=100,
        custom_operator_x=lambda x: x,
        custom_operator_y=lambda y: y,
        reduce_func=numpy.mean,
        overwrap=0.0,
        extend=True,
        ci=None,
        ax=None,
        *args,
        **kwargs,
    ):
        """line plot

        See Also
        --------
        lineplot and lineplot_with_ci of Plots.py
        """
        if ci is not None:
            reduce_func = lambda x: x

        dataset = self.reduce(xitem, [yitem], reduce_func, xlim, xnum, overwrap, extend)
        return dataset.lineplot(
            xitem,
            yitem,
            custom_operator_x,
            custom_operator_y,
            ci,
            ax=ax,
            *args,
            **kwargs,
        )

    def scatterplot(
        self,
        xitem,
        yitem,
        custom_operator_x=lambda x: x,
        custom_operator_y=lambda y: y,
        ax=None,
        *args,
        **kwargs,
    ):
        """scatter plot

        See Also
        --------
        scatterplot in Plots.py
        """
        return scatterplot(
            self,
            xitem,
            yitem,
            custom_operator_x,
            custom_operator_y,
            ax,
            *args,
            **kwargs,
        )

    def histplot(self, item, ax=None, *args, **kwargs):
        """create histgram

        See Also
        --------
        histplot in Plots.py
        """
        return histplot(self, item, ax, *args, **kwargs)

    def tableplot(self, columns=None, param=True, *args, **kwargs):
        dataframe = self.toDataFrame(columns=columns, param=param)
        return render_mpl_table(dataframe, *args, **kwargs)

    def iter_items(self, item_or_items, remove_none=True):
        """iterator of items

        Parameters
        ----------
        item : str or list of str
            item name(s)

        Yield
        -----
        item(s) of each data
        """
        for dataset in self:
            for value in dataset.iter_items(item_or_items, remove_none):
                yield value

    def loadedParams(self):
        """
        Returns
        -------
        list of Param
        """
        return list(self.datasets)

    def to_dataframe(self, columns=None, param=True):
        """
        Parameters
        ----------
        columns : None or list of str
        param : bool
            if it is true, then param columns is added

        Returns
        -------
        pandas.core.frame.DataFrame
        """
        dataframe = None
        for dataset in self:
            if dataframe is None:
                dataframe = dataset.to_dataframe(columns, param)
            else:
                dataframe = pandas.concat(
                    [dataframe, dataset.to_dataframe(columns, param)]
                )
        return dataframe

    def __add__(self, other):
        new_database = Database(self.datasets)
        new_database.datasets.update(other.datasets)
        new_database.params = self.params | other.params
        return new_database

    def __iadd__(self, other):
        self.datasets.update(other.datasets)
        self.params |= other.params
        return self

    def __sub__(self, other):
        new_database = Database(self.datasets)
        new_database.datasets = dict(self.datasets.items() - other.datasets.items())
        new_database.params = self.params - other.params
        return new_database

    def __isub__(self, other):
        self.datasets = dict(self.datasets.items() - other.datasets.items())
        self.params -= other.params
        return self

    def __getitem__(self, item_iter):
        """
        Parameters
        ----------
        iterm_iter : list of parameters or Param

        Returns
        -------
        Dataset or Database
        if item_iter is Param, then return Dataset whose param is Param.
        if item_iter is list of parameters, then return Database which has all data

        Notes
        -----
        database[paramA, paramB, '*', paramC]
        or database[paramA, paramB, '-', paramC]
        """
        logger.debug(f"item_iter={item_iter}")

        if isinstance(item_iter, tuple):
            return self.datasets[item_iter]

        # get parameters will be loaded
        fixed_params = dict()
        for ix, item in enumerate(item_iter):
            if item not in {"*", "-", "--", None}:
                fixed_params[ix] = item

        logger.debug(f"fixed_params={fixed_params}")
        load_params = list()
        for log_param in self.params:
            for ix, fix_item in fixed_params.items():
                if log_param[ix] != fix_item:
                    break
            else:
                load_params.append(log_param)

        # create new database
        new_database = Database()
        for param in load_params:
            new_database.add_dataset(self.datasets[param], param)
        logger.debug(f"generate database size {len(new_database)}")
        return new_database

    def __len__(self):
        return len(self.datasets)

    def __iter__(self):
        return iter(self.datasets.values())

    def __contains__(self, dataset):
        return dataset in self.datasets.values()

    def __str__(self):
        s = "Database\n"
        s += f"  size: {len(self)}\n"
        s += tie(self.params)
        return s
