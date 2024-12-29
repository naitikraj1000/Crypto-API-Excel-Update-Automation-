import requests
import pandas as pd

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
headers = {
    'X-CMC_PRO_API_KEY': '42cbb389-b6a1-4fa5-9fe4-47b72054fcb8'
}

def extract_info(crypto):
    data = {}
    data["name"] = crypto["name"]
    data["symbol"] = crypto["symbol"]
    data["price"] = crypto["quote"]["USD"]["price"]
    data["market_cap"] = crypto["quote"]["USD"]["market_cap"]
    data["volume_24h"] = crypto["quote"]["USD"]["volume_24h"]
    data["percent_change_24hh"] = crypto["quote"]["USD"]["percent_change_24h"]
    return data

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    
    crypto_list_all_info = data["data"][0:50]
    crypto_list_our_info = []
    for i in range(0, min(50, len(crypto_list_all_info))):
        temp_data = extract_info(crypto_list_all_info[i])
        crypto_list_our_info.append(temp_data)

    df = pd.DataFrame(crypto_list_our_info)

    df["price"] = df["price"].astype(float)
    df["market_cap"] = df["market_cap"].astype(float)
    df["volume_24h"] = df["volume_24h"].astype(float)
    df["percent_change_24hh"] = df["percent_change_24hh"].astype(float)

    top_5_by_market_cap = df.nlargest(5, "market_cap")
    avg_price = df["price"].mean()
    highest_change_row = df.loc[df["percent_change_24hh"].idxmax()]
    lowest_change_row = df.loc[df["percent_change_24hh"].idxmin()]

    df["price"] = df["price"].apply(lambda x: f"{x:,.6f}")
    df["market_cap"] = df["market_cap"].apply(lambda x: f"{x:,.0f}")
    df["volume_24h"] = df["volume_24h"].apply(lambda x: f"{x:,.0f}")
    df["percent_change_24hh"] = df["percent_change_24hh"].apply(lambda x: f"{x:,.6f}")
    print("Top 50 Cryptocurrencies:")
    print(df)

    print("\nTop 5 Cryptocurrencies by Market Cap:")
    top_5_by_market_cap["market_cap"] = top_5_by_market_cap["market_cap"].apply(lambda x: f"{x:,.0f}")
    top_5_by_market_cap["volume_24h"] = top_5_by_market_cap["volume_24h"].apply(lambda x: f"{x:,.0f}")
    print(top_5_by_market_cap)

    print(f"\nAverage Price of Top 50 Cryptocurrencies: {avg_price:,.6f}")
    print(f"Highest 24-hour Percentage Change: {highest_change_row['name']} ({highest_change_row['symbol']}) : {highest_change_row['percent_change_24hh']}%")
    print(f"Lowest 24-hour Percentage Change: {lowest_change_row['name']} ({lowest_change_row['symbol']}) : {lowest_change_row['percent_change_24hh']}%")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
