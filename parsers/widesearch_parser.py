from bs4 import BeautifulSoup


def parse(content):
    soup = BeautifulSoup(content, 'lxml')
    result = []
    try:
        next_page = soup.find("li", class_="pager-next").find_next("a").get("href")
    except:
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
                genres.append({'genre_id': genre_id, 'genre_title': genre_name})
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
                author_id = translator["href"].split("/")[2]
                author_name = translator.text
                translators.append({'translator_id': author_id, 'translator_name': author_name})
            element['translators'] = translators

        except AttributeError:
            element['authors_a'] = None
        result.append(element)
    return result, next_page
