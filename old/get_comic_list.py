from bs4 import BeautifulSoup as bs
import requests
import re

url_xmen = "en.wikipedia.org/wiki/List_of_X-Men_comics"
url_avengers = "en.wikipedia.org/wiki/List_of_Avengers_titles"
url_spiderman = "en.wikipedia.org/wiki/List_of_Spider-Man_titles"

def get_comic_list(url, verbose=True):
    r = requests.get("http://" +url)
    data = r.text
    soup = bs(data)
    text = soup.get_text()
    mylist = []
    for line in text.splitlines():
        if "– )" in line or "present)" in line:
            mylist.append(line)
            if verbose:
                print(line)
    return mylist

def _find_title(mystr, line):
    x = 0
    for let in line:
        if len(mystr) > 1:
            if let == mystr[0] and line[x+1] == mystr[1] and line[x+2] == mystr[2]:
                break
            else:
                x += 1
        else:
            if let == mystr:
                break
            else:
                x += 1
    name = line[0:x]
    return name

def find_names(mylist):
    names = []
    for line in mylist:
        if "," in line:
            names.append(_find_title(",", line))
        elif "vol" in line:
            names.append(_find_title("vol", line))
        elif "(" in line:
            names.append(_find_title("(", line))
    return names

def find_latest(url):
    if url != None:
        r = requests.get(url)
        data = r.text
        soup = bs(data)
        text = soup.get_text()
        thenum = 0

        for line in text.splitlines():
            if "Issue" in line:
                for let in line:
                    if let == "#":
                        i = line.index("#")
                        num = line[i+1:]
                        if int(num) > thenum:
                            thenum = int(num)

        return thenum

def find_num(line):
    p = re.compile("\d+")
    numbers = p.findall(line)
    for num in numbers:
        if int(num) in range(1900, 2020):
            numbers.remove(num)
    if len(numbers) >= 1:
        return numbers[0]
    else:
        return 1

def pick_link(urls):
    newdict = {}
    counter = 0
    mycounter = 0
    for url in urls:
        if counter == 1:
            break
        else:
            counter = 1
        n = 0
        name = url.replace(" ", "")
        r = requests.get(urls[url])
        data = r.text
        soup = bs(data)
        text = soup.get_text()
        for line in text.splitlines():
            if name in line:
                print(line)
                num = find_num(line)
                num = int(num)
                if n < num:
                    n = num
                    counter += 1
                    if counter > 5:
                        break
        newdict[url] = n
    print(newdict)


def find_urls(mylist):
    siteurl = "http://thepiratebay.se/search/{}/0/7/602"

    thenames = find_names(mylist)

    urldict = {}
    for name in thenames:
        name = name.strip()
        url = name.replace(" ", "%20")
        url = siteurl.format(name)
        urldict[name] = url
    pick_link(urldict)


def find_page_old(mylist, myurl):
    siteurl = "http://www.comicvine.com/search/?q="
    searchurl = "&indices%5B%5D=arc&indices%5B%5D=character&indices%5B%5D=company&indices%5B%5D=concept&indices%5B%5D=episode&indices%5B%5D=issue&indices%5B%5D=location&indices%5B%5D=movie&indices%5B%5D=person&indices%5B%5D=series&indices%5B%5D=team&indices%5B%5D=thing&indices%5B%5D=volume"

    thenames = find_names(mylist)

    urllist = []
    for name in thenames:
        name = name.strip()
        named = name.replace(" ", "+")
        named = siteurl + named + searchurl
        urllist.append(named)
        newurl = pick_link(named, name)
        num = find_latest(newurl)
        if num != None:
            print(name)
            print(num)

url = url_xmen
xlist = get_comic_list(url, True)

find_urls(xlist)

