import pandas as pd
from analysis_utils import growth
import matplotlib.pyplot as plt
from typing import List

PLOT_FOLDER = "../plots"

instrument_name = "apple"
instrument_name = "SP500Info"

data_link_dict = {
    "apple": "../data/AAPL.csv",
    "SP500Info": "../data/QDVE.F.csv",
}


def plot_over_years(df: pd.DataFrame, instrument_name: str):
    years = [2021, 2020, 2019, 2018, 2017, 2016]
    plt.title(f"{instrument_name} stock price each year")

    for year in years:
        df_tmp = df[df["Date"].dt.year == year]
        # df_tmp["month_date"] = df_tmp["Date"].apply(lambda x: str(x.month) + "/" + str(x.day))
        # df_tmp["month_date"] =  list(df_tmp["Date"].dt.month.to_string()) + "/" + df_tmp["Date"].dt.day)
        plt.plot(df_tmp["Date"].dt.dayofyear, df_tmp["Open"])
        # plt.plot(df_tmp["month_date"], df_tmp["Open"])
    plt.xlabel("Day of year")
    plt.ylabel("Instrument price")
    plt.legend(years, loc="upper right", bbox_to_anchor=(1.2, 1))
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
    df_tmp = df.groupby(df.Date.dt.to_period("M"))

    df_tmp_2 = df_tmp.first()[["Open"]]
    df_tmp_2["Last"] = df_tmp.last()[["Open"]]
    df_tmp_2["mom_pct"] = (df_tmp_2["Last"]-df_tmp_2["Open"])/df_tmp_2["Open"] * 100
    df_tmp_2[["mom_pct"]].plot(marker=".", grid=True, title=f"{instrument_name}")
    # df_tmp_2[["mom_pct"]].plot(kind="hist", grid=True, title="S&P500 Inf.Tech.")

    plt.savefig(f"{PLOT_FOLDER}/mom_{instrument_name}.png")

    plt.show()

    print(df_tmp_2)


def clean_df_v1(df):
    # remove null
    df = df[~df["Open"].isnull()].copy()
    # df = clean_day(df)
    # reformate Date column
    df["Date"] = pd.to_datetime(df["Date"])
    return df


if __name__ == "__main__":
    data_filepath = data_link_dict[instrument_name]
    df = pd.read_csv(data_filepath)
    df = clean_df_v1(df)
    # print(dir(df.Date.dt))
    # print(df.Date.dt.dayofyear)
    # print(df.iloc[0].Date.day)
    plot_over_years(df, instrument_name)
    # plot_yoy_growth(df, instrument_name)
    # plot_mom_growth(df, instrument_name)

