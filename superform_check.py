import requests
import pandas as pd

def parse_stats(wallet_address):
    url = f"https://api.superform.xyz/superrewards/tournamentXP/1?user={wallet_address}"
    try:
        response = requests.get(url)
        data = response.json()
        tournament_rank = data.get("current", {}).get("tournament_rank")
        tvl = data.get("current", {}).get("tvl")
        xp = data.get("current", {}).get("xp")
        boost = data.get("current", {}).get("boost")
        return tournament_rank, tvl, xp, boost
    except Exception as e:
        return None, None, None, None

def parse_nft(wallet_address):
    url = f"https://api.superform.xyz/superrewards/rewards/0/{wallet_address}"
    try:
        response = requests.get(url)
        data = response.json()
        superfren_values = []
        statuses = []
        if data:
            for item in data:
                superfren_value = item.get("tier")
                status = item.get("status")
                if superfren_value is not None:
                    superfren_values.append(superfren_value)
                    statuses.append(status)
        return superfren_values, statuses
    except Exception as e:
        return [], []

def main():
    print("Выберите режим:")
    print("1. Проверка статистики")
    print("2. Проверка NFT")
    choice = input("Введите номер режима: ")

    if choice == "1":
        mode = "stats"
    elif choice == "2":
        mode = "nft"
    else:
        print("Неверный выбор режима.")
        return

    # Reading wallet addresses from file
    with open("wallets.txt", "r") as file:
        wallets = file.read().splitlines()

    # Creating a list to store parsed data
    data_list = []

    # Parsing data for each wallet
    for wallet_address in wallets:
        if mode == "stats":
            tournament_rank, tvl, xp, boost = parse_stats(wallet_address)
            if tournament_rank is not None:
                data_list.append({
                    "Wallet Address": wallet_address,
                    "Tournament Rank": tournament_rank,
                    "TVL": tvl,
                    "XP": xp,
                    "Boost": boost
                })
        elif mode == "nft":
            superfren_values, statuses = parse_nft(wallet_address)
            print(f"Wallet Address: {wallet_address}")
            for superfren, status in zip(superfren_values, statuses):
                if status == "claimed":
                    print(f"Superfren: {superfren} - {status}")
            print("=" * 23)  # Print separator line

    # Saving DataFrame to CSV file
    if mode == "stats":
        df = pd.DataFrame(data_list)
        df.to_csv("superform_stats.csv", index=False)

if __name__ == "__main__":
    main()
