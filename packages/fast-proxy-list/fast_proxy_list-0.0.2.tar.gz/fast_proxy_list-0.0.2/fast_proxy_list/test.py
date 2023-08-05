import proxies
from proxies import get_proxies

url = "https//:www.sephora.fr"
print(get_proxies(url, 20, timeout=20, verbose=2))
