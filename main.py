import controllers

from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

api.add_resource(controllers.Search, "/api/search")
api.add_resource(controllers.WideSearch, "/api/widesearch")
api.add_resource(controllers.Downloads, "/api/downlods")
if __name__ == '__main__':
    app.run(debug=True)
