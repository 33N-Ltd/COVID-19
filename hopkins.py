import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Read in data
confirmed = pd.read_csv(
    "csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
)
deaths = pd.read_csv(
    "csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
)
recovered = pd.read_csv(
    "csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
)

# Dictionary of frames
frames = {"Confirmed": confirmed, "Deaths": deaths, "Recovered": recovered}

# Process data into standard form for plotting/analysis
for key in frames.keys():
    frames[key] = (
        frames[key]
        .drop(columns=["Province/State", "Lat", "Long"], axis=1)
        .groupby("Country/Region")
        .sum()
        .reset_index()
    )
    frames[key] = (
        frames[key]
        .melt(id_vars="Country/Region", var_name="Date")
        .rename(columns={"value": key})
    )
    frames[key]["Date"] = pd.to_datetime(frames[key]["Date"])

# Plot total global values for each of confirmed, deaths and recovered
for key in frames.keys():
    frames[key].set_index("Date").groupby("Date")[key].sum().plot()
    plt.legend()
plt.show()

# Plot total UK values for each of confirmed, deaths and recovered
for key in frames.keys():
    country_frame = frames[key][frames[key]["Country/Region"] == "United Kingdom"]
    country_frame.set_index("Date").groupby("Date")[key].sum().plot()
    plt.legend()
plt.show()

# Create single frame of all data
full_frame = (
    frames["Confirmed"]
    .merge(frames["Deaths"], on=["Country/Region", "Date"])
    .merge(frames["Recovered"], on=["Country/Region", "Date"])
).set_index("Date")

# General estimate of discharges and mean discharge rate
full_frame["Est_Discharge"] = full_frame["Recovered"] + full_frame["Deaths"]
full_frame["Est_Discharge_Rate"] = full_frame["Est_Discharge"] / full_frame["Confirmed"]
full_frame["Est_Discharge_Rate"].groupby("Date").mean().plot()
# plt.show()


# General estimate of discharges and mean discharge rate
full_frame["Est_Discharge_Rate"].groupby("Date").mean().plot()
full_frame[full_frame["Country/Region"] == "China"]["Est_Discharge_Rate"].groupby(
    "Date"
).mean().plot()
full_frame[full_frame["Country/Region"] != "China"]["Est_Discharge_Rate"].groupby(
    "Date"
).mean().plot()
full_frame[full_frame["Country/Region"] == "United Kingdom"][
    "Est_Discharge_Rate"
].groupby("Date").mean().plot()
plt.show()


# General estimate of discharges and mean discharge rate China & global
full_frame["Est_Discharge"].groupby("Date").mean().plot()
full_frame[full_frame["Country/Region"] == "China"]["Est_Discharge"].groupby(
    "Date"
).mean().plot()
full_frame[full_frame["Country/Region"] != "China"]["Est_Discharge"].groupby(
    "Date"
).sum().plot()
plt.show()


# Simple analysis of confirmed-recovery lag
disch = full_frame["Recovered"].groupby("Date").sum().reset_index(drop=True)
conf = full_frame["Confirmed"].groupby("Date").sum().reset_index(drop=True)
lag_corr = pd.Series([disch.corr(conf.shift(lag)) for lag in range(0, len(conf) - 2)])
lag_corr.plot()
plt.show()


# Simple analysis of est_discharge-recovery lag for China
disch_ch = (
    full_frame[full_frame["Country/Region"] == "China"]["Est_Discharge"]
    .groupby("Date")
    .sum()
    .reset_index(drop=True)
)
conf_ch = (
    full_frame[full_frame["Country/Region"] == "China"]["Confirmed"]
    .groupby("Date")
    .sum()
    .reset_index(drop=True)
)
lag_corr_ch = pd.Series(
    [disch_ch.corr(conf_ch.shift(lag)) for lag in range(0, len(conf_ch) - 2)]
)
disch_ch.plot()
conf_ch.plot()
plt.show()
lag_corr_ch.plot()
plt.show()
