import requests
import sys


def get(country: str) -> None:
    url = f"https://corona-stats.online/{country}?minimal=true"
    response = requests.get(url, headers={'user-agent': 'curl'})
    print(response.text)

def show() -> None:
    country = sys.argv[1] if len(sys.argv) > 1 else ""
    print(get(country))
