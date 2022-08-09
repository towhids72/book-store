import json

from flask import Blueprint, request
from flask_login import current_user

from api_response.response import APIResponse
from book.models import Book, db

book_blueprint = Blueprint('book_api_routes', __name__, url_prefix='/api/books')


@book_blueprint.route('/all', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    return APIResponse.ok_response(data=[book.serialize() for book in books])


@book_blueprint.route('/create', methods=['POST'])
def create_book():
    if current_user.is_authenticated and current_user.is_admin:
        return APIResponse.error_response('Only admins can add books', 401)
    try:
        json_body = json.loads(request.data)
    except Exception as ex1:
        print(ex1)
        return APIResponse.error_response('Invalid body', 400)
    name = json_body.get('name', None)
    slug = json_body.get('slug', None)
    price = json_body.get('price', None)
    image = json_body.get('image', None)

    if name is None:
        return APIResponse.error_response('Book name must not be null', 400)
    if slug is None:
        return APIResponse.error_response('Book slug must not be null', 400)

    try:
        book = Book()
        book.name = name
        book.slug = slug
        book.price = price
        book.image = image

        db.session.add(book)
        db.session.commit()
        return APIResponse.ok_response(book.serialize())

    except Exception as ex:
        print(ex)
        return APIResponse.error_response('Can not save book right now', 400)


@book_blueprint.route('/<slug>', methods=['GET'])
def get_book_details(slug):
    book = Book.query.filter_by(slug=slug).first()
    if not book:
        return APIResponse.error_response('Book not found', 404)
    return APIResponse.ok_response(book.serialize())
