from bs4 import BeautifulSoup as BS
import requests
import time
from pathlib import Path
import pickle
from os import getpid
import json
import argparse


# MULTITHREADING
from pebble import ProcessPool
from concurrent.futures import TimeoutError
from functools import partial


# VERBOSE
from collections import Counter


######## MAKE PROXY LIST ########
# Scrape free-proxy-list.net and use bs to parse html
# returns proxy list
#################################


def make_proxy_list(quality, connection, verbose):
    # making the request and getting the necessary info :
    url = "https://free-proxy-list.net/"
    req = requests.get(url)
    soup = BS(req.content, "html.parser")
    tbody = soup.find_all(lambda tag: tag.name == "tbody")
    rows = tbody[0].findAll(lambda tag: tag.name == "tr")

    # Creating the proxy list like [https, ip, port] or [http, ip, port]

    proxy_list = []
    for row in rows:
        td = row.find_all("td")
        if quality == "all":
            if (
                td[4].text == "anonymous"
                or td[4].text == "elite proxy"
                or td[4].text == "transparent"
            ):
                if connection == "all":
                    if td[6].text == "yes":
                        proxy = []
                        proxy.append("https")
                        proxy.append(td[0].text)  # ip
                        proxy.append(td[1].text)  # port
                        proxy_list.append(proxy)
                    else:
                        proxy = []
                        proxy.append("http")
                        proxy.append(td[0].text)  # ip
                        proxy.append(td[1].text)  # port
                        proxy_list.append(proxy)
                elif connection == "https":
                    if td[6].text == "yes":
                        proxy = []
                        proxy.append("https")
                        proxy.append(td[0].text)  # ip
                        proxy.append(td[1].text)  # port
                        proxy_list.append(proxy)
                elif connection == "http":
                    if td[6].text == "no":
                        proxy = []
                        proxy.append("http")
                        proxy.append(td[0].text)  # ip
                        proxy.append(td[1].text)  # port
                        proxy_list.append(proxy)
        elif quality == "elite":
            if td[4].text == "elite proxy":
                if connection == "all":
                    if td[6].text == "yes":
                        proxy = []
                        proxy.append("https")
                        proxy.append(td[0].text)  # ip
                        proxy.append(td[1].text)  # port
                        proxy_list.append(proxy)
                    else:
                        proxy = []
                        proxy.append("http")
                        proxy.append(td[0].text)  # ip
                        proxy.append(td[1].text)  # port
                elif connection == "https":
                    if td[6].text == "yes":
                        proxy = []
                        proxy.append("https")
                        proxy.append(td[0].text)  # ip
                        proxy.append(td[1].text)  # port
                        proxy_list.append(proxy)
                elif connection == "http":
                    if td[6].text == "no":
                        proxy = []
                        proxy.append("http")
                        proxy.append(td[0].text)  # ip
                        proxy.append(td[1].text)  # port
                        proxy_list.append(proxy)
    #################### VERBOSE/
    if verbose == 2:
        print("---------------------------------------")
        types = [i[0] for i in proxy_list]
        types = Counter(types)
        print(f"{len(proxy_list)} proxies fetched. \n")
        for typ in types:
            print(f">  {types[str(typ)]} {str(typ)} proxies")
        print("---------------------------------------")
    if verbose == 1:
        print("---------------------------------------")
        print(f"{len(proxy_list)} proxies fetched. \n")
        print("---------------------------------------")
    #################### \VERBOSE
    return proxy_list


######## PROXY CHECKER ########
# Tries to connect to the specified website using a proxy
# Returns proxy if the status code is 200
###############################


def proxy_checker(proxy, url, verbose):
    if verbose == 2:
        print(f">\tProcess n°{getpid()} started")
    proxies = {str(proxy[0]): str(proxy[1]) + ":" + str(proxy[2])}
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    }
    try:
        req = requests.get(
            url,
            proxies=proxies,
            headers=headers,
        )
        if req.status_code == 200:
            #################### VERBOSE/
            if verbose == 2:
                print("---------------------------------------")
                print(f"Found valid proxy : {proxy}")
                print("---------------------------------------")
            #################### \VERBOSE
            return proxy
        return ""
    except Exception as e:
        if verbose in [1,2] :
            print("PROXY FAILED!\n")
            if verbose == 2:
                print(e)
        return ""


######## GET PROXIES ########
# Checks multiple proxies' validity for the specified website
# Saves proxies list in a specified directory
# Returns a list of valid proxies
#############################


def get_proxies(
    url,
    nbr_workers=20,
    quality="all",
    connection="all",
    timeout=20,
    save="pickle",
    savedir="",
    verbose=0,
):
    proxy_list = make_proxy_list(quality, connection, verbose)
    #################### VERBOSE/
    if verbose == 2:
        time.sleep(3)
        print("---------------------------------------")
        print(f"Initiliazing pool with {nbr_workers}.\n")
        if save == "pickle" or save == "txt":
            print(
                f"The {save} file will be saved in {'current directory' if savedir=='' else savedir}.\n"
            )
        time.sleep(2)
        print("---------------------------------------")
    if verbose == 1:
        time.sleep(3)
        print("---------------------------------------")
        print(
            f"The {save} file will be saved in {'current directory' if savedir=='' else savedir}.\n"
        )
        print("---------------------------------------")
    #################### \VERBOSE
    start = time.time()
    with ProcessPool(max_workers=nbr_workers) as pool:
        check_url = partial(proxy_checker, url=url, verbose=verbose)
        # partial allows to iterate on the same url with all proxies
        future = pool.map(check_url, proxy_list, timeout=timeout)
        iterator = future.result()
        results = []
        while True:
            try:
                result = next(iterator)
                results.append(result)
            except StopIteration:
                break
            except TimeoutError as error:
                if verbose == 2:
                    print(
                        "/!\ function took longer than %d seconds /!\ \n"
                        % error.args[1]
                    )
    end = time.time()
    proxies = [x for x in results if x != ""]
    types = [i[0] for i in proxies]
    types = Counter(types)
    #################### VERBOSE/
    if verbose == 2:
        print("---------------------------------------")
        print(f"for url : {url} : ")
        print(f">\t{len(proxies)} working proxies found. \n")
        for typ in types:
            print(f"> {types[str(typ)]} {str(typ)} proxies")
        print(f"Time take : {end-start}")
        print("---------------------------------------")
    if verbose == 1:
        print("---------------------------------------")
        print(f">\t{len(proxies)} working proxies found. \n")
        print("---------------------------------------")
    if len(proxies) < 1:
        print("---------------------------------------")
        print("No valid proxy availabe right now ! \n")
        print("---------------------------------------")
    #################### \VERBOSE
    else:
        Path(f"{savedir}").mkdir(parents=True, exist_ok=True)
        if save == "pickle":
            with open(f"{savedir}/proxies.pickle", "wb") as fp:
                pickle.dump(proxies, fp)
        if save == "txt":
            with open("{savedir}/proxies.txt", "w") as f:
                f.write(json.dumps(proxies))

    return proxies



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--url",
        dest="url",
        type=str,
        metavar="<str>",
        required=True,
        help="Url to the page you want to scrape",
    )
    parser.add_argument(
        "-n",
        "--nbr-workers",
        dest="nbr_workers",
        type=int,
        metavar="<int>",
        default=10,
        help="Number of thread workers (default=10)",
    )
    parser.add_argument(
        "-q",
        "--quality",
        dest="quality",
        type=str,
        metavar="<str>",
        default="all",
        help="'elite' or 'all' (default='all')",
    )
    parser.add_argument(
        "-c",
        "--connection",
        dest="connection",
        type=str,
        metavar="<str>",
        default="all",
        help="'http', 'https' or 'all' (default='all')",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        dest="timeout",
        type=float,
        metavar="<float>",
        default=5,
        help="'Time in sec. before connection times out. A lower timeout will show less results but faster proxies. (default=5)",
    )
    parser.add_argument(
        "-s",
        "--save",
        dest="save_type",
        type=str,
        metavar="<str>",
        default="pickle",
        help="'pickle' or 'txt' as the output format (default='pickle')",
    )
    parser.add_argument(
        "--savedir",
        dest="save_dir",
        type=str,
        metavar="<str>",
        default="data",
        help="Path to where output will be saved (default='data/')",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        type=int,
        metavar="<int>",
        default=0,
        help="'0', '1' or '2' as verbose level (default=0)",
    )

    args = parser.parse_args()

    url = args.url
    nbr_workers = args.nbr_workers
    quality = args.quality
    connection = args.connection
    timeout = args.timeout
    save = args.save_type
    savedir = args.save_dir
    verbose = args.verbose

    # print(get_proxies(url, verbose=0, timeout=5, savedir="data"))
    get_proxies(
        url,
        nbr_workers=nbr_workers,
        quality=quality,
        connection=connection,
        timeout=timeout,
        save=save,
        savedir=savedir,
        verbose=verbose,
    )
    """
    Usage example :

    url = "github.com"
    get_proxies(url, 20, 'elite', 'https', 20, 'pickle', savedir="data", verbose=2)

    """
    # get_proxies($url, $nbr_workers, $quality, $connection, $timeout, $save, $savedir $verbose)

    """ Args Types and Values"""

    # url          : [String]  (NA)                        // url
    # nbr_workers   : [int]     (1-30)                      // number of threads
    # quality       : [String]  ('elite' or 'all')          // all includes transparent proxies
    # connection    : [String]  ('http', 'https', 'all')    // self-explainatory
    # timeout       : [int]     (1+)                        // time in seconds before thread timeout, low timeout == faster proxies
    # save          : [String]  ('pickle', 'txt')           // defines the type of the file in order to save the proxy list
    # savedir       : [String]  (NA)                        // path to where you want the file to be saved
    # verbose       : [int]     (1,2)                       // get some written feed back in order to grasp better what's working or what's not
    #                                                       // Setting verbose to 2 gives more info than setting it to 1
