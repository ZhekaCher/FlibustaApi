from flask_restful import Resource, request
import request_pages
import parsers.search_parser
import parsers.book_links_parser
import parsers.widesearch_parser


class Search(Resource):
    def get(self):
        search_string = request.args.get('search_string')

        route = "/booksearch?ask=" + search_string
        response = request_pages.get_search(route)
        parsed = parsers.search_parser.parse(response.content)
        result = parsed[0]
        while parsed[1] is not None:
            response = request_pages.get_search(parsed[1])
            parsed = parsers.search_parser.parse(response.content)
            for x in parsed[0]:
                result[x].extend(parsed[0][x])
        return result, 200


class Downloads(Resource):
    def get(self):
        route = request.args.get('route')
        response = request_pages.get_book_page(route)
        parsed = parsers.book_links_parser.parse(response.content)
        result = parsed
        return result, 200


class WideSearch(Resource):
    def get(self):
        author_fname = request.args.get('author_fname')
        author_lname = request.args.get('author_lname')
        book_title = request.args.get('book_title')
        genres = request.args.get('genres')
        patronymic = request.args.get('patronymic')
        language = request.args.get('language')
        sort = request.args.get('sort')
        route = '/makebooklist?ab=ab1&sort=st1'
        if book_title is not None:
            route += '&t=' + book_title
        if author_lname is not None:
            route += '&ln=' + author_lname
        if author_fname is not None:
            route += '&fn=' + author_fname
        if genres is not None:
            route += '&g=' + genres
        if patronymic is not None:
            route += '&mn=' + patronymic
        if sort is not None:
            route += '&sort=' + sort
        if language is not None:
            route += '&lng=' + language
        response = request_pages.get_widesearch(route)
        parsed = parsers.widesearch_parser.parse(response.content)
        result = parsed[0]
        i = 0
        while parsed[1] is not None:
            i += 1
            response = request_pages.get_widesearch(route + '&page=' + str(i))
            parsed = parsers.widesearch_parser.parse(response.content)
            result.extend(parsed[0])

        return {"books":result}, 200
