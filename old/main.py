from bs4 import BeautifulSoup as bs
import requests

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

xlist = get_comic_list(url_xmen)
print("")
alist = get_comic_list(url_avengers)
print("")
slist = get_comic_list(url_spiderman)

thenames = find_names(xlist)
print(thenames)
