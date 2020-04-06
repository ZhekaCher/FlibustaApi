from bs4 import BeautifulSoup


def parse(content):
    soup = BeautifulSoup(content, 'lxml')
    result = []
    try:
        next_page = soup.find("li", class_="pager-next").find_next("a").get("href")
    except AttributeError:
        next_page = None

    main_divs = soup.find("form", {'name': 'bk'}).findChildren("div")
    for div in main_divs:
        element = {}
        all_a = div.findChildren("a")
        book_data = list(filter(lambda x: "/b/" in x["href"], all_a))[0]
        element['book_id'] = int(book_data["href"].split("/")[2])
        element['book_title'] = book_data.text

        try:
            element['rating'] = div.findChild("img").get("title")
        except AttributeError:
            element['rating'] = 'нет данных'

        try:
            genres_p = div.findChild("p")
            genres_a = genres_p.findChildren("a")
            genres = []
            for genre in genres_a:
                genre_id = genre["href"].split("/")[2]
                genre_name = genre.text
                genre_code = genre['name']
                genres.append({'genre_id': genre_id, 'genre_title': genre_name, 'genre_code': genre_code})
            if not genres:
                genres = None
            element['genres'] = genres
            print(div)
        except AttributeError:
            element['genres'] = None

        try:
            translators_a = []
            for a in all_a:
                if "(fb2)" in a.text:
                    break
                elif "/a/" in a['href']:
                    translators_a.append(a)
            translators = []
            for translator in translators_a:
                translator_id = translator["href"].split("/")[2]
                translator_name = translator.text
                translators.append({'translator_id': translator_id, 'translator_name': translator_name})
            if not translators:
                translators = None
                element['translators'] = translators
        except AttributeError:
            element['translators'] = None

        try:
            authors_a = []
            flag = False
            for a in all_a:
                if "(fb2)" in a.text:
                    flag = True
                elif "/a/" in a['href'] and flag:
                    authors_a.append(a)
            authors = []
            for author in authors_a:
                author_id = author["href"].split("/")[2]
                author_name = author.text
                authors.append({'author_id': author_id, 'author_name': author_name})
            if not authors:
                authors = None
            element['authors'] = authors
        except AttributeError:
            element['authors'] = None

        try:
            series_a = list(filter(lambda x: "/s/" in x["href"], all_a))
            series = []
            for s in series_a:
                s_id = s["href"].split("/")[2]
                s_name = s.text
                series.append({'series_id': s_id, 'series_name': s_name})
            if not series:
                series = None
            element['series'] = series
        except AttributeError:
            element['series'] = None

        try:
            element['size'] = div.findChild("span", {'style': 'size'}).text
        except AttributeError:
            element['size'] = None
        result.append(element)
    return result, next_page
