# Based on Quantadre blog: https://quantdare.com/will-the-fed-ruin-my-sp500-investments/
# FOMC Calendar: https://www.federalreserve.gov/newsevents/calendar.htm

from mizani.formatters import *
from plotnine import *
import yfinance as yf
import pandas as pd
import numpy as np

fomc_meetings = ["2023-02-01", "2023-03-22", "2023-05-03", "2023-06-14", "2023-07-26", "2023-09-20",
                 "2022-01-26", "2022-03-16", "2022-05-04", "2022-06-15", "2022-07-27", "2022-09-21", "2022-11-02", "2022-12-14",
                 "2021-01-27", "2021-03-17", "2021-04-28", "2021-06-16", "2021-07-28", "2021-09-22", "2021-11-03", "2021-12-15",
                 "2020-01-29", "2020-03-03", "2020-03-19", "2020-04-29", "2020-06-10", "2020-07-29", "2020-09-16", "2020-11-05", "2020-12-16",
                 "2019-01-30", "2019-03-20", "2019-05-01", "2019-06-19", "2019-09-18", "2019-10-30", "2019-12-11", "2018-01-31",
                 "2018-03-21", "2018-05-02", "2018-06-13", "2018-08-01", "2018-09-26", "2018-11-08", "2018-12-19",
                 "2017-02-01", "2017-03-15", "2017-05-03", "2017-06-14", "2017-07-26", "2017-09-20", "2017-11-01", "2017-12-13"]

fomc_meetings = pd.to_datetime(fomc_meetings)

INI_DATE = "2016-12-30"
END_DATE = "2023-09-25"

df_date = pd.date_range(start=INI_DATE, end=END_DATE, freq="D")
df_date = pd.DataFrame({"Date": df_date})

df = yf.download("SPY", start=INI_DATE, end=END_DATE)
df = pd.merge(df_date, df, on="Date", how="left")[["Date", "Close"]]

df["Close"].fillna(method="ffill", inplace=True)
df["Daily Returns"] = df["Close"].pct_change()

df = df[df["Date"] >= "2017-01-01"]

df["Cumulative Returns"] = np.cumprod(1 + df["Daily Returns"].values) - 1
df["Meeting"] = df["Date"].apply(lambda date: 1 if date in fomc_meetings else 0)
df["Dot Meeting"] = np.where(df["Meeting"] != 0, df["Cumulative Returns"], np.nan)


plot1 = (ggplot(df)
        + geom_line(aes(x="Date", y="Cumulative Returns", color='"1"'))
        + geom_point(aes(x="Date", y="Dot Meeting", color='"2"'))

        + scale_x_date(date_breaks="6 months",
                       expand=(0, 0),
                       labels=date_format("%Y-%m"),
                       limits=pd.to_datetime(["2017-01-01", "2023-09-30"]))
        + scale_y_continuous(expand=(0, 0),
                             breaks=np.arange(0, 1.3, 0.25),
                             labels=percent_format(),
                             limits=(0.0, 1.25))

        + scale_color_manual(values={"1": "#003299", "2": "#fe4b01"}, labels=[" Cumulative Returns", " FOMC Meeting"])

        + labs(title="Will the Fed ruin my S&P500 investments?",
               subtitle="",
               x="", y="Cumulative Returns",
               caption="Own elaboration. Source: S&P 500 (SPY) from Yahoo Finance. Created by @jaldeko.")

        + theme_minimal()
        + theme(
            plot_title=element_text(face="bold", hjust=0.5, size=16),
            plot_subtitle=element_text(face="bold", hjust=0, size=12),
            plot_caption=element_text(size=8, face="italic"),
            panel_grid_major=element_line(linetype="solid", linewidth=0.5, color="#C0C0C0"),
            panel_grid_minor=element_blank(),
            axis_line=element_line(colour="#000000"),
            axis_ticks=element_line(colour="#000000"),
            axis_text=element_text(face="bold", color="#000000"),
            legend_title=element_blank(),
            legend_position="top",
            legend_box_just="left",
            legend_box="horizontal",
            legend_text=element_text(size=12, colour="#000000")
            )
        )

plot1.save(filename="Plot 1 125.jpg", format="jpg", width=1280/125, height=720/125, dpi=125)


strategy = pd.concat([pd.Series(fomc_meetings + pd.offsets.Day(-1)),
                      pd.Series(fomc_meetings),
                      pd.Series(fomc_meetings + pd.offsets.Day(1)),
                      pd.Series(fomc_meetings + pd.offsets.Day(2))])
strategy = pd.DatetimeIndex(strategy)

df["Strategy"] = df["Date"].apply(lambda date: 1 if date in strategy else 0)
df["Daily Strat Returns"] = df.apply(lambda row: row["Daily Returns"] if row["Strategy"] == 0 else 0, axis=1)
df["Cumulative Strat Returns"] = np.cumprod(1 + df["Daily Strat Returns"].values) - 1


plot2 = (ggplot(df)
         + geom_line(aes(x="Date", y="Cumulative Returns", color='"1"'))
         + geom_line(aes(x="Date", y="Cumulative Strat Returns", color='"2"'))

         + scale_x_date(date_breaks="6 months",
                        expand=(0, 0),
                        labels=date_format("%Y-%m"),
                        limits=pd.to_datetime(["2017-01-01", "2023-09-30"]))
         + scale_y_continuous(expand=(0, 0),
                              breaks=np.arange(0, 1.8, 0.25),
                              labels=percent_format(),
                              limits=(0.0, 1.75))

         + scale_color_manual(values={"1": "#003299", "2": "#fe4b01"}, labels=[" S&P 500", " Portfolio"])

         + labs(title="Will the Fed ruin my S&P500 investments?",
                subtitle="",
                x="", y="Cumulative Returns",
                caption="Own elaboration. Source: S&P 500 (SPY) from Yahoo Finance. Created by @jaldeko.")

         + theme_minimal()
         + theme(
             plot_title=element_text(face="bold", hjust=0.5, size=16),
             plot_subtitle=element_text(face="bold", hjust=0, size=12),
             plot_caption=element_text(size=8, face="italic"),
             panel_grid_major=element_line(linetype="solid", linewidth=0.5, color="#C0C0C0"),
             panel_grid_minor=element_blank(),
             axis_line=element_line(colour="#000000"),
             axis_ticks=element_line(colour="#000000"),
             axis_text=element_text(face="bold", color="#000000"),
             legend_title=element_blank(),
             legend_position="top",
             legend_box_just="left",
             legend_box="horizontal",
             legend_text=element_text(size=12, colour="#000000")
            )
         )

plot2.save(filename="Plot 2 125.jpg", format="jpg", width=1280/125, height=720/125, dpi=125)
