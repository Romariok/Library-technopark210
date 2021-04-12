from flasgger import Swagger
from flask import request
from flask import Flask
app = Flask(__name__)
swagger = Swagger(app)

class Author:
    name = ''
    comment = ''
    books =[]

    def __init__(self, name, comment=None):
        self.name = name
        self.comment = "" if comment is None else comment


class Publisher:
    name = ''
    comment = ''
    works = []

    def __init__(self, name, comment=None):
        self.name = name
        self.comment = "" if comment is None else comment


class Book:
    name = ''
    publisher = None
    publishing_year = None
    availability = True
    e_link = ''
    comment = ''
    works = []

    def __init__(self, name, publisher, publishing_year, availability=True, e_link=None, comment=None):
        self.name = name
        self.publisher = publisher
        self.publishing_year = publishing_year
        self.availability = availability
        self.e_link = "" if e_link is None else e_link
        self.comment = "" if comment is None else comment


class Work:
    name = ''
    author = None
    inside_period = ''
    e_link = ''
    comment = ''
    book = None

    def __init__(self, name, author, inside_period=None, e_link=None, comment=None):
        self.name = name
        self.author = author
        self.inside_period = "" if inside_period is None else inside_period
        self.e_link = "" if e_link is None else e_link
        self.comment = "" if comment is None else comment


from flask_marshmallow import Marshmallow
from marshmallow import fields
ma = Marshmallow()


class AuthorSchema(ma.Schema):
    name = fields.String()
    comment = fields.String()


class CollectionSchema(ma.Schema):
    name = fields.String()
    comment = fields.String()


class PublisherSchema(ma.Schema):
    name = fields.String()
    comment = fields.String()

authors = [Author('Джон Ронал Руел Толкин', 'создатель властелин колец'), Author('Брэм Стокер', 'Создатель Дракулы'), Author('Говард Филлипс Лавкрафт', 'Создатель Некрономикона, да, это вымышленная книга')]


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/authors')
def get_authors():
    """Example endpoint returning a list of colors by palette
        This is using docstrings for specifications.
        ---
        definitions:
            Authors:
              type: array
              items:
                name:
                  type: string
                comment:
                  type: string
        responses:
          200:
            description: Get all authors
    """
    return AuthorSchema(many=True).dumps(authors)

@app.route('/author/<string:name>')
def get_author(name):
    """Example endpoint returning a list of colors by palette
    This is using docstrings for specifications.
    ---
    parameters:
    - in: "path"
      name: "name"
      required: true
      type: string
      description: "Name of author"
    definitions:
      Author:
        type: object
        properties:
          name:
            type: string
          comment:
            type: string
    responses:
      200:
        description: Author got
    """
    for elem in authors:
        if name in elem.name:
            return AuthorSchema().dumps(elem)
    # TODO если автора нет в массиве, return {message: "Not found"}, 404
    return {'message': "Not found"}

@app.route('/author', methods=['POST'])
def add_author():
    """Example endpoint returning a list of colors by palette
        This is using docstrings for specifications.
        ---
        parameters:
        - in: "body"
          name: "body"
          required: true
          schema:
            required:
              - name
            properties:
              name:
                type: string
                description: "Name of author"
              comment:
                type: string
                description: "Some comment"

        definitions:
          Author:
            type: object
            properties:
              name:
                type: string
              comment:
                type: string
        responses:
          200:
            description: Author created
        """
    # TODO если пользователь не передал name и comment вернуть return {"message": "ЧТО_ТО_ТАМ is required"}, 400
    author = Author(request.json.get('name'), request.json.get('comment'))
    authors.append(author)
    return AuthorSchema().dumps(author)
@app.route('/author/<string:name>', methods=['DELETE'])
def delete_author(name):
    author = None
    for elem in authors:
        if name in elem.name:
            author = elem
            break
    # TODO если автора нет в массиве, return {message: "Not found"}, 404
    # TODO удалить автора из массива
    authors.remove(author)
    return AuthorSchema().dumps(author)


# TODO сделать роут на изменение (PATCH) автора

app.run()
