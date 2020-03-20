import pandas as pd
import matplotlib.pyplot as plt


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
plt.show()
