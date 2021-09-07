import pandas as pd
from analysis_utils import growth
import matplotlib.pyplot as plt

PLOT_FOLDER = "../plots"


def plot_yoy_growth(df: pd.DataFrame):
    years = [2015, 2016, 2017, 2018, 2019, 2020, 2021]
    growth_pcts = []
    for year in years:
        growth_pcts.append(growth.growth_by_time(df, year=year))

    print(growth_pcts)
    plt.bar(years, growth_pcts)
    plt.title(f"yoy% growth")
    plt.show()
    plt.savefig(f"{PLOT_FOLDER}/yoy_ETF.png")


def plot_mom_growth(df: pd.DataFrame):
    """
    We use groupby method here
    :param df:
    :return:
    """
    df_tmp = df.groupby(df.Date.dt.to_period("M"))

    df_tmp_2 = df_tmp.first()[["Open"]]
    df_tmp_2["Last"] = df_tmp.last()[["Open"]]
    df_tmp_2["mom_pct"] = (df_tmp_2["Last"]-df_tmp_2["Open"])/df_tmp_2["Open"] * 100
    df_tmp_2[["mom_pct"]].plot(marker="o")
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
    data_filepath = "../data/QDVE.F.csv"
    df = pd.read_csv(data_filepath)
    df = clean_df_v1(df)
    # print(df)
    # plot_yoy_growth(df)
    plot_mom_growth(df)
