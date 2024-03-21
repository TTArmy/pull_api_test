import http.client
import json
import os

def fetch_time_series_data(api_key, start_date, end_date, base_currency='USD', target_currencies='EUR,GBP', resolution='1d', amount=1, places=7, format_='json'):
    conn = http.client.HTTPSConnection("api.fxratesapi.com")
    url = f"/timeseries?access_key={api_key}&start_date={start_date}&end_date={end_date}&base={base_currency}&currencies={target_currencies}&resolution={resolution}&amount={amount}&places={places}&format={format_}"
    conn.request("GET", url)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    conn.close()
    return json.loads(data)

def get_user_input():
    api_key = input("Enter API key: ")
    start_date_input = input("Enter start date (YYYY-MM-DD) or (YYYY-MM-DDTHH:MM:SSZ): ")
    end_date_input = input("Enter end date (YYYY-MM-DD) or (YYYY-MM-DDTHH:MM:SSZ): ")

    start_date = start_date_input + 'T00:00:00Z' if 'T' not in start_date_input else start_date_input
    end_date = end_date_input + 'T00:00:00Z' if 'T' not in end_date_input else end_date_input

    base_currency = input("Enter base currency (default: USD): ") or 'USD'
    target_currencies = input("Enter target currencies (default: EUR,GBP): ") or 'EUR,GBP'
    resolution = input("Enter resolution (default: 1d): ") or '1d'
    amount = int(input("Enter amount (default: 1): ") or 1)
    places = int(input("Enter decimal places (default: 7): ") or 7)
    format_ = input("Enter format (default: json): ") or 'json'
    return api_key, start_date, end_date, base_currency, target_currencies, resolution, amount, places, format_

def save_time_series_data(data, base_currency, target_currency, start_date, end_date):
    directory = f"time_series_data/{base_currency}"
    os.makedirs(directory, exist_ok=True)
    start_date_part = start_date.split('T')[0]
    end_date_part = end_date.split('T')[0]
    filename = f"{directory}/{base_currency}_{target_currency}_{start_date_part}_{end_date_part}.json"
    filename = filename.replace(':', '_').replace('T', '_').replace('Z', '')
    filename = filename.replace(' ', '_')
    with open(filename, 'w') as file:
        json.dump(data, file)

def parse_time_series_data(time_series_data, start_date, end_date):
    base_currency = time_series_data['base']
    rates = time_series_data['rates']

    currency_data = {}
    for date, currencies in rates.items():
        for currency, rate in currencies.items():
            if currency not in currency_data:
                currency_data[currency] = {}
            currency_data[currency][date] = rate

    for currency, data in currency_data.items():
        save_time_series_data(data, base_currency, currency, start_date, end_date)


if __name__ == "__main__":
    api_key, start_date, end_date, base_currency, target_currencies, resolution, amount, places, format_ = get_user_input()
    time_series_data = fetch_time_series_data(api_key, start_date, end_date, base_currency, target_currencies,
                                              resolution, amount, places, format_)
    if time_series_data:
        parse_time_series_data(time_series_data, start_date, end_date)
        print("Time series data saved successfully.")
    else:
        print("Unable to fetch time series data.")
