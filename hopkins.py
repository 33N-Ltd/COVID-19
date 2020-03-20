import pandas as pd
import matplotlib.pyplot as plt

confirmed = pd.read_csv(
    "csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
)
deaths = pd.read_csv(
    "csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
)
recovered = pd.read_csv(
    "csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
)

frames = {"Confirmed": confirmed, "Deaths": deaths, "Recovered": recovered}

for key, frame in frames.items():
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
    frames[key] = frames[key].set_index("Date")

for key, frame in frames.items():
    frames[key].groupby("Date")[key].sum().plot()
    plt.legend()
plt.show()

for key, frame in frames.items():
    country_frame = frames[key][frames[key]["Country/Region"] == "United Kingdom"]
    country_frame.groupby("Date")[key].sum().plot()
    plt.legend()
plt.show()
