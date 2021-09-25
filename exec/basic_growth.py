import pandas as pd
from analysis_utils import growth
import matplotlib.pyplot as plt
from typing import List
from analysis_utils.calculations import closest_behavior

PLOT_FOLDER = "../plots"
APPLE = "apple"
SP500Info = "SP500Info"
instrument_name = "apple"
instrument_name = SP500Info

data_link_dict = {
    APPLE: "../data/AAPL.csv",
    SP500Info: "../data/QDVE.F.csv",
}


def plot_over_years(df: pd.DataFrame, instrument_name: str):
    years = [2021, 2020, 2019, 2018, 2017, 2016, 2015]
    plt.title(f"{instrument_name} stock price each year")

    for year in years:
        df_tmp = df[df["Date"].dt.year == year].copy()
        # TODO: think of a way to plot with Month-Day also.
        # lunar year will give problem
        plt.plot(df_tmp["Date"].dt.dayofyear, df_tmp["Open"])

    plt.xlabel("Day of year")
    plt.ylabel("Instrument price")
    plt.legend(years, loc="upper right", bbox_to_anchor=(1.15, 1))
    plt.savefig(f"{PLOT_FOLDER}/plot_over_years_{instrument_name}.png")

    plt.show()


def plot_yoy_growth(df: pd.DataFrame, instrument_name: str, years: List[int] = None):
    if years is None:
        # assume df has colume Date of pd.datetime Series
        years = list(set(df.Date.dt.year))

    growth_pcts = []
    for year in years:
        growth_pcts.append(growth.growth_by_time(df, year=year))

    print(growth_pcts)
    plt.bar(years, growth_pcts)
    plt.title(f"yoy% growth of {instrument_name}")
    plt.savefig(f"{PLOT_FOLDER}/yoy_{instrument_name}.png")

    plt.show()


def plot_mom_growth(df: pd.DataFrame, instrument_name: str):
    """
    We use groupby method here
    :param df:
    :return:
    """
    df_tmp = df.groupby(df.Date.dt.to_period("1M"))

    df_tmp_2 = df_tmp.first()[["Open"]]
    df_tmp_2["Last"] = df_tmp.last()[["Open"]]
    df_tmp_2["mom_pct"] = (df_tmp_2["Last"] - df_tmp_2["Open"]) / df_tmp_2["Open"] * 100
    # df_tmp_2[["mom_pct"]].plot(marker=".", grid=True, title=f"{instrument_name}")
    # plt.bar(df_tmp_2[["mom_pct"]])
    # df_tmp_2[["mom_pct"]].plot.bar(grid=True, title=f"{instrument_name}")
    ax = plt.subplot(111)
    df_tmp_2[["mom_pct"]].plot(use_index=True, kind="bar", title=f"{instrument_name}")
    ax.xaxis_date()
    plt.xticks()
    # df_tmp_2[["mom_pct"]].plot(kind="hist", grid=True, title="S&P500 Inf.Tech.")

    plt.savefig(f"{PLOT_FOLDER}/mom_{instrument_name}.png")

    plt.show()

    print(df_tmp_2)


def remove_bad_days_with_price(df: pd.DataFrame, instrument_name: str):
    if instrument_name == SP500Info:
        df_tmp = df[df["Date"] != "2018-05-21"].copy()
    return df_tmp


def remove_null_value_rows(df: pd.DataFrame, col_name: str):
    return df[~df["Open"].isnull()].copy()


def clean_df_v1(df: pd.DataFrame, instrument_name: str):
    # remove null
    df_tmp = remove_null_value_rows(df, col_name="Open")
    # df = clean_day(df)

    # reformat Date column
    df_tmp["Date"] = pd.to_datetime(df_tmp["Date"])

    df_tmp = remove_bad_days_with_price(df_tmp, instrument_name)
    return df_tmp


def EDA(df: pd.DataFrame):
    # for any adhoc analysis
    n = 3
    df = df.iloc[:10].copy()
    base_vector = base_vector = list(df.iloc[-n:]["Open"])
    print(f"most recent {n} Open price: {base_vector}")
    (ind, distance) = closest_behavior(base_vector=base_vector, vector=list(df["Open"]))
    print(ind, distance)
    print(f"Closest distance is {df.iloc[ind:ind+n]}")


if __name__ == "__main__":
    data_filepath = data_link_dict[instrument_name]
    df = pd.read_csv(data_filepath)
    df = clean_df_v1(df, instrument_name)
    EDA(df)

    # plot_over_years(df, instrument_name)
    # plot_yoy_growth(df, instrument_name)
    # plot_mom_growth(df, instrument_name)
