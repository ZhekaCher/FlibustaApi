from bs4 import BeautifulSoup


def parse(content):
    soup = BeautifulSoup(content, 'lxml')
    json = {}
    try:
        next_page = soup.find("li", class_="pager-next").find_next("a").get("href")
    except:
        next_page = None

    main_divs = soup.find("form", {'name': 'bk'}).findChildren("div")
    for div in main_divs:
        print(div)
    return "Done", next_page
