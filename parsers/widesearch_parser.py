from bs4 import BeautifulSoup


def parse(content):
    soup = BeautifulSoup(content, 'lxml')
    json = {}
    try:
        next_page = soup.find("li", class_="pager-next").find_next("a").get("href")
    except:
        next_page = None
