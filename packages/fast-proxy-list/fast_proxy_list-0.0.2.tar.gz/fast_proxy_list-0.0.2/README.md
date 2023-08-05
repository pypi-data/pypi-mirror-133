# Fast Proxy List
v 0.0.1
python >= 3.6.8

With this python library, you can easily get working proxies for any project. 
It does the following things :
- Finding proxies (around 300 proxies, 50% usually being https)
- Testing those proxies on an URL you provide (multi-threading makes that super fast)
- Returns the working ones
- Returns only proxies that are faster than the timeout limit (which you can set to any value)


## what's to come (soon-ish):
- auto formating url / making sure that any valid URL is formated properly 
- adding more sources to get free proxies - for now proxies are all from free-proxy-list.net
- code visibility changes
- adding proxy speed info

## How to install it?

```pip install fast-proxy-list```

## What are the other packages it requires ?

```pip install -r requirements.txt```

BeautifulSoup4 == 4.10.0
Pebble == 4.6.3
requests == 2.26.0


## How to run it?

If you've imported the library in a python file, you can run it through the command line in case you just need a proxy really fast, just like that :
Let's say your file is called ```proxies.py```

```python3 proxies.py --url https://github.com```

Will return a  list of  proxies that can be used to scrape github.com

### What are the arguments?
Required arguments:

--url : the url of the page you want to scrape. the two valid formats are : https://YOURSITE or https://www.YOURSITE

Optional arguments:

--timeout  : Time in seconds before requests times out (the lower, the faster are the returned proxies)
--nbr-workers : number of thread workers for a faster execution
--save : select the file format the proxy list will be saved to. you can chose pickle or txt.
--savedir : path to where the file will be saved

For the detailed argument list, try --help

###

## Python package usage

### Code

The following code does the same thing as above

```
from fast-proxy-list import proxies

url = "https//:www.github.com"
proxies.get_proxies(url)
````

By default, files are saved in the current directory, use the ```savedir``` argument to change the save path.
You can specify any path, if it doesn't exist, it will kindly be created for you.
