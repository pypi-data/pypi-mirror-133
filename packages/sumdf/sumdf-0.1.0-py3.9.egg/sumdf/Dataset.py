import copy
import importlib
import os
import pickle

import attrdict
import pandas

from sumdf.Logging import setup_logger
from sumdf.Plots import histplot, lineplot, scatterplot

logger = setup_logger(name=__name__)


class Dataset:
    """Data Manager

    Parameters
    ----------
    data : parandas.Dataframe

    Attributes
    ----------
    data : parandas.Dataframe
        keys includes any data in data
    globals : list of dictionary
    param: Param
    """

    def __init__(self, data, param=None):
        self.data = data
        self.globals = attrdict.AttrDict()
        self.param = param

    def add_global(self, global_dict):
        """update globals

        Parameters
        ----------
        global_dict : dict
        """
        self.globals.update(global_dict)
        return self

    def columns(self):
        return set(self.data.columns)

    def iter_items(self, item_or_items, remove_none=True):
        """iterator of item

        Parameters
        ----------
        item_or_items : iterator of str
            item name
        remove_none : bool
            if it is true, then any data that has none is not yield

        Yield
        -----
        item of each data
        """
        if isinstance(item_or_items, (list, tuple)):
            iter_type = type(item_or_items)
            items = item_or_items
        else:
            iter_type = lambda x: x[0]
            items = [item_or_items]

        for data in self:
            if remove_none and any(
                item not in data or data[item] is None for item in items
            ):
                continue
            yield iter_type([data[item] for item in items])

    def clone(self):
        """clone this dataset

        Returns
        -------
        Dataset
        """
        data = copy.deepcopy(self.data)
        return Dataset(data=data)

    def sort(self, key):
        """sort datas

        Parameters
        ----------
        key: str or function that argument is data
        """
        self.data.sort_values(key)
        return self

    def min(self, item):
        """get minimum value of item"""
        return self.data[item].min()

    def max(self, item):
        """get maximum value of item"""
        return self.data[item].max()

    def data_generator(self, item, items, extend):
        """
        generate D = (None, None, ..., d1, d2, d3, ..., dN, ..., dN)
        such that Di[item] > items[i]
        where self data is (d1, ..., dN) and length of D is equal to one of items

        Parameters
        ----------
        item : str
            item name
        itmes : list of (int or float)
            list of values of item
        extend : bool
            if it is true, extend and describe the data at the end of the item

        Yield
        -----
        dict

        """
        item_ix = 0
        pre_data = None
        for data in self:
            while data[item] > items[item_ix]:
                yield pre_data
                item_ix += 1
            pre_data = data
        yield self.tail()

        while True:
            yield self.tail() if extend else None

    def lineplot(
        self,
        xitem,
        yitem,
        custom_operator_x=lambda x: x,
        custom_operator_y=lambda y: y,
        ci=None,
        ax=None,
        *args,
        **kwargs,
    ):
        """line plot

        See Also
        --------
        lineplot of Plots.py
        """
        return lineplot(
            self,
            xitem,
            yitem,
            custom_operator_x,
            custom_operator_y,
            ci,
            ax,
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

    def save(self, cache_path):
        directory = os.path.dirname(cache_path)
        os.makedirs(directory, exist_ok=True)
        with open(cache_path, "wb") as f:
            pickle.dump(self, file=f)

    def load(self, cache_path):
        with open(cache_path, "rb") as f:
            try:
                self = pickle.load(f)
            except ModuleNotFoundError as e:
                import sys

                sys.exit(
                    f"{e} -- "
                    + f"You may need to create a dummy module"
                    + f"that cannot be found."
                )
            except Exception as e:
                logger.error(e)
        return self

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
        dataframe = pandas.DataFrame(self.data)
        if columns is not None:
            try:
                dataframe = dataframe[columns]
            except:
                import traceback

                traceback.print_exc()
                logger.error(f"param = {self.param}, load_set = {self.load_set}")
                exit(1)

        if param and self.param is not None:
            param_dataframe = None
            for name, value in self.param._asdict().items():
                dataframe[name] = value
                if param_dataframe is None:
                    param_dataframe = dataframe[name].astype(str)
                else:
                    param_dataframe += "_" + dataframe[name].astype(str)
            dataframe["param"] = param_dataframe
        for name, value in self.globals.items():
            dataframe[name] = value
        return dataframe

    def keys(self):
        return set(self.data.columns)

    def tail(self):
        return dict(zip(self.data.tail(1).columns, self.data.tail(1).to_numpy()[0]))

    def __getitem__(self, item):
        return [data[item] for data in self]

    def __eq__(self, other):
        return self.load_set == other.load_set

    def __hash__(self):
        return hash(self.load_set)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for row in self.data.itertuples():
            yield row._asdict()

    def __str__(self):
        if self.datas:
            s += f"size {len(self.data)}\n"
            return s
        else:
            return "empty dataset"
