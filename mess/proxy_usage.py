#-*-coding:utf-8-*-
import requests

def routine_00():
    print("routine_00")

    url = "https://www.google.com/"
    try:
        print("connect to {} directly".format(url))
        req = requests.get(url)
        if req.ok:
            with open("google.txt", "wb") as f:
                f.write(req._content)
        else:
            print("  direct connection failed with status code {}".format(req.status_code))
    except requests.exceptions.ConnectionError as err:
        print("  direct connection failed with description {}".format(err))

    proxies = {
        "http" : "socks5h://127.0.0.1:1080",
        "https" : "socks5h://127.0.0.1:1080"
    }
    try:
        print("connect to {} through proxy {}".format(url, proxies))
        req = requests.get(url, proxies=proxies, verify=False) # disable verification for quick start
        if req.ok:
            with open("google_proxy.txt", "wb") as f:
                f.write(req._content)
        else:
            print("  proxy connection failed with status code {}".format(req.status_code))
    except requests.exceptions.ConnectionError as err:
        print("  proxy connection failed with description {}".format(err))

    # example code
    #resp = requests.get('http://go.to', proxies=dict(http='socks5://user:pass@host:port',https='socks5://user:pass@host:port'))



def shell_entry():
    print("proxy_usage shell_entry")
    routine_00()