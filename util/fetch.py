import requests

def get(url: str):
  res = requests.get(url)
  if (res.ok):
    return res.json()
  else:
    raise RuntimeError(f"Request for URL {url} failed with status code {res.status_code}.")
