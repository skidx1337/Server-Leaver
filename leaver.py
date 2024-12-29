import requests
import time
from colorama import Fore
import pyfiglet
import os
from colorama import Fore, Style


author = "skidxjija"

ravan = pyfiglet.figlet_format("SERVER LEAVER", font="bloody")
made_by = f"[ Made By {author} ]"
centered_made_by = made_by.center(len(ravan))
console_width = 120
centered_ascii_art = "\n".join(line.center(console_width) for line in ravan.split("\n"))
output = centered_ascii_art + f"{centered_made_by}\n"


menu = f"""{Style.BRIGHT}{Fore.RED} {output}\n"""
os.system("clear")
print(menu)


def validate_token(token):
    headers = {'Authorization': token}
    response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    if response.status_code == 200:
        print(f"{Fore.GREEN}Token is valid!{Fore.RESET}")
        return True
    else:
        print(f"{Fore.RED}Invalid token! Status Code: {response.status_code}{Fore.RESET}")
        return False


def fetch_servers(token):
    headers = {'Authorization': token}
    response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
    if response.status_code == 200:
        guilds = response.json()
        print(f"{Fore.GREEN}Fetched {len(guilds)} servers.{Fore.RESET}")
        return guilds
    else:
        print(f"{Fore.RED}Failed to fetch servers. Status Code: {response.status_code}{Fore.RESET}")
        return []


def leave_server(token, guild_id, guild_name):
    headers = {'Authorization': token}
    payload = {}
    while True:
        response = requests.delete(f'https://discord.com/api/v9/users/@me/guilds/{guild_id}', headers=headers, json=payload)

        if response.status_code == 204:
            print(f"{Fore.GREEN}[SUCCESS] Left server '{guild_name}' successfully!{Fore.RESET}")
            break
        elif response.status_code == 429:
            retry_after = response.json().get("retry_after", 1)
            print(f"{Fore.YELLOW}[RATE LIMITED] Retrying in {retry_after} seconds...{Fore.RESET}")
            time.sleep(retry_after)
        else:
            print(f"{Fore.RED}[ERROR] Failed to leave server '{guild_name}'. Status Code: {response.status_code}{Fore.RESET}")
            break


def main():
    token = input("{Fore.RED} Enter Your account Token")
    if not validate_token(token):
        return

    
    servers = fetch_servers(token)
    if not servers:
        print(f"{Fore.RED}No servers found or failed to fetch servers.{Fore.RESET}")
        return

    print(f"{Fore.YELLOW}You are part of {len(servers)} server(s):{Fore.RESET}")
    for idx, guild in enumerate(servers):
        print(f"{Fore.CYAN}{idx + 1}. {guild['name']} (ID: {guild['id']}){Fore.RESET}")

    
    confirmation = input(f"{Fore.RED}Are you sure you want to leave all servers? (y/n): {Fore.RESET}")
    if confirmation.lower() != 'y':
        print(f"{Fore.RED}Process canceled.{Fore.RESET}")
        return


    
    for guild in servers:
        leave_server(token, guild["id"], guild["name"])
        time.sleep(1)  

if __name__ == "__main__":
    main()
    