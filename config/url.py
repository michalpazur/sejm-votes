base_url = "https://api.sejm.gov.pl/sejm"

def term_url(term: int):
  return f"{base_url}/term{term}"