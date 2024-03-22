import http.client
import json
import os
from datetime import datetime

def fetch_time_series_data(api_key, start_date, end_date, base_currency, target_currencies, resolution, amount, places, format_):
    conn = http.client.HTTPSConnection("api.fxratesapi.com")
    url = f"/timeseries?access_key={api_key}&start_date={start_date.strftime('%Y-%m-%d')}T00:00:00&end_date={end_date.strftime('%Y-%m-%d')}T00:00:00&base={base_currency}&currencies={target_currencies}&resolution={resolution}&amount={amount}&places={places}&format={format_}"
    conn.request("GET", url)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    conn.close()
    return json.loads(data)
def get_env_variable(var_name):
    value = os.environ.get(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' is not set.")
    return value
def get_user_input():
    api_key = os.environ.get("API_KEY")
    start_date_input = os.environ.get("START_DATE")
    end_date_input = os.environ.get("END_DATE")
    start_date = datetime.strptime(start_date_input, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_input, "%Y-%m-%d")
    base_currency = os.environ.get("BASE_CURRENCY")
    target_currencies = os.environ.get("TARGET_CURRENCIES")
    resolution = os.environ.get("RESOLUTION")
    amount = int(os.environ.get("AMOUNT"))
    places = int(os.environ.get("PLACES"))
    format_ = os.environ.get("FORMAT")
    return api_key, start_date, end_date, base_currency, target_currencies, resolution, amount, places, format_

def save_time_series_data(data, base_currency, target_currency, start_date, end_date):
    directory = f"time_series_data/{base_currency}"
    os.makedirs(directory, exist_ok=True)
    start_date_part = start_date.strftime("%Y-%m-%d")
    end_date_part = end_date.strftime("%Y-%m-%d")
    filename = f"{directory}/{base_currency}_{target_currency}_{start_date_part}_{end_date_part}.json"
    filename = filename.replace(':', '_').replace('T', '_').replace('Z', '')
    filename = filename.replace(' ', '_')
    data_str_keys = {str(key): value for key, value in data.items()}
    with open(filename, 'w') as file:
        json.dump(data_str_keys, file)

def parse_time_series_data(time_series_data, start_date, end_date):
    base_currency = time_series_data.get('base')
    rates = time_series_data.get('rates')

    if not base_currency or not rates:
        print("Unable to parse time series data.")
        return

    currency_data = {}
    for date, currencies in rates.items():
        for currency, rate in currencies.items():
            if currency not in currency_data:
                currency_data[currency] = {}
            date_time = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
            if start_date <= date_time <= end_date:
                currency_data[currency][date_time.date()] = rate

    for currency, data in currency_data.items():
        sorted_data = dict(sorted(data.items()))
        save_time_series_data(sorted_data, base_currency, currency, start_date, end_date)

if __name__ == "__main__":
    try:
        api_key = get_env_variable("API_KEY")
        start_date = get_env_variable("START_DATE")
        end_date = get_env_variable("END_DATE")
        base_currency = get_env_variable("BASE_CURRENCY")
        target_currencies = get_env_variable("TARGET_CURRENCIES")
        resolution = get_env_variable("RESOLUTION")
        amount = get_env_variable("AMOUNT")
        places = get_env_variable("PLACES")
        format_ = get_env_variable("FORMAT")

        print("API_KEY:", api_key)
        print("START_DATE:", start_date)
        print("END_DATE:", end_date)
        print("BASE_CURRENCY:", base_currency)
        print("TARGET_CURRENCIES:", target_currencies)
        print("RESOLUTION:", resolution)
        print("AMOUNT:", amount)
        print("PLACES:", places)
        print("FORMAT:", format_)

        api_key, start_date, end_date, base_currency, target_currencies, resolution, amount, places, format_ = get_user_input()
        if None in (api_key, start_date, end_date, base_currency, target_currencies, resolution, format_):
            raise ValueError("One or more environment variables are not set.")
        time_series_data = fetch_time_series_data(api_key, start_date, end_date, base_currency, target_currencies,
                                                  resolution, amount, places, format_)
        if time_series_data:
            parse_time_series_data(time_series_data, start_date, end_date)
            print("Time series data saved successfully.")
        else:
            print("Unable to fetch time series data.")
    except ValueError as e:
        print(e)
