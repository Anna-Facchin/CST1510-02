
from pathlib import Path

import pandas as pd
import requests

# ---- Settings: the only part you change for your own data ----------------

URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
PARAMS = {"format": "geojson", "minmagnitude": 2.5, "limit": 500}
RECORDS_KEY = "features"                # the key that holds the list of records (None if the reply is already a list)

RENAME = {
	"properties_mag": "mag",
	"properties_place": "place",
	"properties_time": "time",
	"properties_magType": "mag_type",
	"properties_sig": "significance",
	"properties_tsunami": "tsunami",      # ugly column name -> short column name
}
KEEP = ["time", "place", "mag", "mag_type", "significance", "tsunami"]   # the columns you want, e.g. ["country", "continent", "cases"]
MUST_HAVE = ["mag"]                  # drop any row that is empty in these columns                        

RAW_FILE = Path(__file__).parent / "DATA" / "raw.csv"

# ---- The functions ----------------------------------------------------------


def get_data(url, params):
    """Ask the API for data. Returns the JSON reply, or None if something went wrong."""
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()          # turns 404, 500 ... into an error
        return response.json()
    except requests.RequestException as error:
        print("Could not get the data:", error)
        return None


def make_table(data, records_key):
    """Turn the JSON reply into a pandas table."""
    records = data[records_key] if records_key else data
    return pd.json_normalize(records, sep="_")      # nested {"a": {"b": 1}} becomes column a_b


def tidy_data(df):
    """Rename, keep and clean the columns."""
    df = df.rename(columns=RENAME)
    # Extra cleaning for your own data can go here (the earthquake example in Step 5 shows two lines).
    df = df[KEEP]
    df = df.dropna(subset=MUST_HAVE)
    return df


def save_data(df, path):
    """Save the table as a CSV file."""
    path.parent.mkdir(exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")


if __name__ == "__main__":
    data = get_data(URL, PARAMS)
    if data is not None:
        table = make_table(data, RECORDS_KEY)
        table = tidy_data(table)
        print(table.head())
        save_data(table, RAW_FILE)


def show_checks(checks):
    """Print the results of the data validation checks."""
    for passed, message in checks:
        print(f"{'PASS' if passed else 'FAIL'}: {message}")


raw = RAW_FILE
df = pd.read_csv(raw) if raw.exists() else pd.DataFrame()

numbers = df.select_dtypes("number").columns.tolist()
texts = df.select_dtypes(exclude="number").columns.tolist()
good_names = all(c.islower() and " " not in c and "." not in c for c in df.columns)

show_checks([
    (raw.exists(),          "DATA/raw.csv exists"),
    (len(df) >= 50,         f"{len(df)} rows (need 50 or more)"),
    (len(numbers) >= 1,     f"number columns: {numbers}"),
    (len(texts) >= 1,       f"text columns: {texts}"),
    (df.shape[1] <= 12,     f"{df.shape[1]} columns (keep it to 12 or fewer)"),
    (good_names,            "column names are lower case, with no spaces or dots"),
])
df.head()