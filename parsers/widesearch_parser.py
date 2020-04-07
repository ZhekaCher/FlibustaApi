from bs4 import BeautifulSoup


def parse(content):
    soup = BeautifulSoup(content, 'lxml')
    result = []
    try:
        next_page = soup.find("li", class_="pager-next").find_next("a").get("href")
    except AttributeError:
        next_page = None

    try:
        main_divs = soup.find("form", {'name': 'bk'}).findChildren("div")
    except AttributeError:
        return None, next_page
    for div in main_divs:
        element = {}
        all_a = div.findChildren("a")
        book_data = list(filter(lambda x: "/b/" in x["href"], all_a))[0]
        element['book_id'] = int(book_data["href"].split("/")[2])
        element['book_title'] = book_data.text

        try:
            element['rating'] = div.findChild("img").get("title")
        except AttributeError:
            pass

        try:
            genres_p = div.findChild("p")
            genres_a = genres_p.findChildren("a")
            genres = []
            for genre in genres_a:
                genre_id = int(genre["href"].split("/")[2])
                genre_name = genre.text
                genre_code = genre['name']
                genres.append({'genre_id': genre_id, 'genre_title': genre_name, 'genre_code': genre_code})
            if genres:
                element['genres'] = genres
        except AttributeError:
            pass

        try:
            translators_a = []
            for a in all_a:
                if "(fb2)" in a.text:
                    break
                elif "/a/" in a['href']:
                    translators_a.append(a)
            translators = []
            for translator in translators_a:
                translator_id = int(translator["href"].split("/")[2])
                translator_fullname = translator.text
                translators.append({'translator_id': translator_id, 'translator_fullname': translator_fullname})
            if translators:
                element['translators'] = translators
        except AttributeError:
            pass

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
                author_id = int(author["href"].split("/")[2])
                author_fullname = author.text
                authors.append({'author_id': author_id, 'author_fullname': author_fullname})
            if authors:
                element['authors'] = authors
        except AttributeError:
            pass

        try:
            series_a = list(filter(lambda x: "/s/" in x["href"], all_a))
            series = []
            for s in series_a:
                s_id = int(s["href"].split("/")[2])
                s_name = s.text
                series.append({'series_id': s_id, 'series_name': s_name})
            if series:
                element['series'] = series
        except AttributeError:
            pass

        try:
            element['size'] = div.findChild("span", {'style': 'size'}).text
        except AttributeError:
            pass
        result.append(element)
    return result, next_page
