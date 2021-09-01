import pandas as pd
from typing import Union


def growth_by_time(df: pd.DataFrame,
                   price_col: str = "Open",
                   date_col: str = "Date",
                   year: Union[str, int] = None,
                   return_type: str = "percentage") -> float:
    """

    :param df: data frame. Assume that it has some basic columns:
        - price_col: containing price
        - date_col: containing dates
    :param price_col (str): the name of the column that has prices
    :param year: to filter
    :param return_type (str): either "percentage" or "absolute"
    :return: float
    """
    df_tmp = df.copy()

    if year is not None:
        year = str(year)
        df_tmp = df_tmp[df_tmp[date_col].apply(lambda x: year in x)].copy()
    df_tmp.sort_values(by=date_col, inplace=True)
    # df is ascending, going up
    if return_type == "percentage":
        return (df_tmp.iloc[0][price_col] - df_tmp.iloc[-1][price_col]) / df_tmp.iloc[-1][price_col]
    elif return_type == "absolute":
        return (df_tmp.iloc[0][price_col] - df_tmp.iloc[-1][price_col])
    else:
        raise ValueError(f"dont recognize return_type = {return_type}")
