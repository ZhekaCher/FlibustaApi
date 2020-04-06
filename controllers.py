from flask_restful import Resource, request
import request_pages
import parsers.search_parser
import parsers.book_links_parser


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