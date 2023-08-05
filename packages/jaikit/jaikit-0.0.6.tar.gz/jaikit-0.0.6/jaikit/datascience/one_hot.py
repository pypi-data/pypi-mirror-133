import re
from typing import Optional

import pandas as pd
from pandas import Series, DataFrame


def series_onehot_converter(
    series: Series, dimension: Optional[int] = None
) -> DataFrame:
    """
    将DataFrame的一个整数值列（即Series）转为N维的one-hot表示，返回N列的DataFrame
    这是为了增强pandas.get_dummies的功能，因为get_dummies只能按照所有出现过的值种类数作为one-hot的dimension，不能自由设定
    注意必须符合以下两个条件，否则会报错：
    （1）如指定参数dimension，其必须要大于series中的最大值
    （2）series中的数值类型必须为整数型
    例如：
    > import pandas as pd
    > series_onehot_converter(series=pd.Series([2, 4]))  # 不指定dimension，默认取series最大值+1
    Out:
           0  1  2  3  4
        0  0  0  1  0  0
        1  0  0  0  0  1

    > series_onehot_converter(series=pd.Series([2, 4]), dimension=6)
    Out:
       0  1  2  3  4  5
    0  0  0  1  0  0  0
    1  0  0  0  0  1  0
    """
    if dimension is None:
        dimension = series.max() + 1
    elif dimension <= series.max():
        raise ValueError("Dimension must be more than the maximum value in the series.")
    if not re.match(r"int|uint", series.dtypes.name):
        raise TypeError("Values in the series must be in the type of int.")
    return pd.get_dummies(
        series.append(pd.DataFrame(data=range(dimension))[0], ignore_index=True,)
    )[:-dimension]
