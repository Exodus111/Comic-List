from bs4 import BeautifulSoup as bs
import requests
import re

marvel_comics = {}
comic_title = "Marvel_Comics"

pattern = re.compile(r"MARVEL COMICS(.+?)\s*#(\d+)")

year = "2014"
urlcode = "/doku.php?id=comiclists_for_"
siteurl = "http://www.comiclistdatabase.com"
myurl = "{}{}{}".format(siteurl, urlcode, year)


def get_http(url):
    r = requests.get(url)
    data = r.text
    soup = bs(data)
    return soup

def find_latest():
    soup = get_http(myurl)
    top_ten = []
    for link in soup.find_all(class_="wikilink1"):
        top_ten.append(link.get("href"))
        if "comiclists_for_2014" in top_ten[-1]:
            del top_ten[-1:-3:-1]
            break
    return top_ten

def add_to_database(name, num):
    if name in marvel_comics.keys():
        if marvel_comics[name] < num:
            marvel_comics[name] = num
    else:
        marvel_comics[name] = num

def search_for_titles():
    sitelist = find_latest()
    for site in sitelist:
        url = "{}{}".format(siteurl, site)
        soup = get_http(url)
        text = soup.get_text()
        if "This topic does not exist yet" not in text:
            for row in soup.select("div.table tr")[1:]:
                print(".")
                publisher = row.find("td", class_="col1").text
                title = row.find("td", class_="col2").text
                price = row.find("td", class_="col3").text
                if publisher == "MARVEL COMICS":
                    if "$" in price:
                        p = re.search(r"[$](\d+.\d+)", price)
                        p = p.group(1)
                        p = float(p)
                        if p < 5.0:
                            searched = re.search(r"(.+?)#(\d+)", title)
                            title = searched.group(1)
                            title = title.strip()
                            num = searched.group(2)
                            if num.isdigit():
                                num = int(num)
                                add_to_database(title, num)

def save_and_load():
    global marvel_comics
    filename = comic_title + ".txt"
    f = open(filename, "r+")
    if marvel_comics == {}:
        s = f.read()
        if s:
            marvel_comics = eval(s)
    else:
        f.write(str(marvel_comics))
    f.close()

save_and_load()
search_for_titles()
save_and_load()




