from bs4 import BeautifulSoup


def parse(content):
    soup = BeautifulSoup(content, 'lxml')
    json = {}
    links = soup.find_all("a")
    json['fb2'] = next(x for x in links if x.text == "(fb2)").get('href')
    json['epub'] = next(x for x in links if x.text == "(epub)").get('href')
    json['mobi'] = next(x for x in links if x.text == "(mobi)").get('href')
    return json
