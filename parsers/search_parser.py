from bs4 import BeautifulSoup

ul_titles_dict = {'серии': 'series',
                  'писатели': 'writers',
                  'книги': 'books'}


def parse(content):
    soup = BeautifulSoup(content, 'lxml')
    json = {}
    try:
        next_page = soup.find("li", class_="pager-next").find_next("a").get("href")
    except:
        next_page = None

    main_div = soup.find("div", id="main")
    names = main_div.findChildren("h3")
    ul_titles = []
    for name in names:
        for ul_title in ul_titles_dict:
            if ul_title in name.text:
                json[ul_titles_dict[ul_title]] = []
                ul_titles.append(ul_titles_dict[ul_title])

    elements = list(filter(lambda x: not x.has_attr('class'), main_div.findChildren("ul")))
    i = 0
    for element in elements:
        for child_element in element.findChildren("li"):
            json[ul_titles[i]].append({'element': child_element.text,
                                       'link': child_element.findChild('a').get('href')})
        i = i + 1
    return json, next_page
