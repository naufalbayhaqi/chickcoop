import os
import requests
import time
import json
from colorama import init, Fore, Style
import random
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)


# Function to get random color
def get_random_color():
    colors = [Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    return random.choice(colors)

# Read and parse the query.txt file
with open('query.txt', 'r') as file:
    lines = file.readlines()

# Extract authorization data from each line
authorizations = [line.strip() for line in lines]

# Store previous results
previous_results = {}

def claim_gift(auth):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': auth,
        'cache-control': 'no-cache',
        'content-length': '0',
        'content-type': 'application/octet-stream',
        'origin': 'https://game.chickcoop.io',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://game.chickcoop.io/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    response = requests.post('https://api.chickcoop.io/gift/claim', headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            return True
    return False

def upgrade_laboratory(auth, research_type):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': auth,
        'cache-control': 'no-cache',
        'content-type': 'application/octet-stream',
        'origin': 'https://game.chickcoop.io',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://game.chickcoop.io/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    data = json.dumps({"researchType": research_type})
    response = requests.post('https://api.chickcoop.io/laboratory/research', headers=headers, data=data)
    return response.json()


# Function to sell eggs
def sell_eggs(auth, number_of_eggs):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': auth,
        'cache-control': 'no-cache',
        'content-type': 'application/octet-stream',
        'origin': 'https://game.chickcoop.io',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://game.chickcoop.io/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    data = json.dumps({"numberOfEggs": number_of_eggs})
    response = requests.post('https://api.chickcoop.io/user/sell-eggs', headers=headers, data=data)
    return response.status_code == 200

# Store previous results and upgrade counts
previous_results = {}
upgrade_counts = {
    "egg_value": 0,
    "laying_rate": 0
}

def fetch_and_print_user_data(auth, index):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': auth,
        'cache-control': 'no-cache',
        'content-length': '0',
        'content-type': 'application/octet-stream',
        'origin': 'https://game.chickcoop.io',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://game.chickcoop.io/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    
    while True:
        try:
            time.sleep(2)
            response = requests.post('https://api.chickcoop.io/hatch/manual', headers=headers)
            
            if response.status_code == 401:
                return Fore.RED + f"Authorization failed for Akun {index + 1}"

            data = response.json()

            profile = data['data']['profile']
            chickens = data['data']['chickens']
            eggs = data['data']['eggs']
            cash = data['data']['cash']
            gem = data['data']['gem']
            level = data['data']['discovery']['level']
  

            if claim_gift(auth):
                chest_count = previous_results.get('chest_count', 0) + 1
                previous_results['chest_count'] = chest_count
            else:
                chest_count = previous_results.get('chest_count', 0)
          
            color = get_random_color()
            formatted_cash = f"{cash:,.0f}".replace(",", ".")
            
            # Upgrade laboratory after hatching
            egg_value_upgrade = upgrade_laboratory(auth, "laboratory.regular.eggValue")
            laying_rate_upgrade = upgrade_laboratory(auth, "laboratory.regular.layingRate")
            
            if egg_value_upgrade['ok']:
                upgrade_counts["egg_value"] += 1
            if laying_rate_upgrade['ok']:
                upgrade_counts["laying_rate"] += 1
            
            upgrade_result = (
                f"Egg {Style.BRIGHT}{color}{upgrade_counts['egg_value']}, "
                f"Laying {Style.BRIGHT}{color}{upgrade_counts['laying_rate']}"
            )
            
            result = (
                f"Akun {Style.BRIGHT}{color}{index + 1}{Style.RESET_ALL} | "
                f"Ayam {Style.BRIGHT}{color}{int(chickens['quantity'])}{Style.RESET_ALL} | "
                f"Lvl {Style.BRIGHT}{color}{level}{Style.RESET_ALL} | "
                f"Telur {Style.BRIGHT}{color}{int(eggs['quantity'])}{Style.RESET_ALL} | "
                f"Cash {Style.BRIGHT}{color}{formatted_cash}{Style.RESET_ALL} | "
                f"Gems {Style.BRIGHT}{color}{gem}{Style.RESET_ALL} | "
                f"Gift: {Style.BRIGHT}{color}{chest_count} | "
                f"Up: {Style.BRIGHT}{color}{upgrade_result} |{Style.RESET_ALL} "
                f"Name: {Style.BRIGHT}{color}{profile['username']}{Style.RESET_ALL}"
            )
            
            # Check if the result is different from the previous one
            if previous_results.get(index) != result:
                previous_results[index] = result
                # Sell eggs only if the quantity is more than 1000
                if int(eggs['quantity']) > 100:
                    sell_eggs(auth, int(eggs['quantity']))
                return result
            return None
        except Exception as e:
            print(Fore.RED + f"Error fetching data for Akun {index + 1}: {e}")
            time.sleep(5)  # Wait before retrying


while True:
    results = []
    # Use ThreadPoolExecutor to make requests concurrently
    with ThreadPoolExecutor(max_workers=len(authorizations)) as executor:
        futures = [executor.submit(fetch_and_print_user_data, auth, index) for index, auth in enumerate(authorizations)]
        for future in futures:
            result = future.result()  # Wait for all threads to complete
            if result:
                results.append(result)
    
    if results:
        # Clear the previous output
        print("\033c", end="")  # ANSI escape code to clear the screen
        # Print all results at once
        print("\n".join(results), end="\r", flush=True)