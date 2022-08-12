import json

import requests
from flask import Blueprint, request

from api_response.response import APIResponse
from order.models import Order, OrderItem, db

order_blueprint = Blueprint('order_api_routes', __name__, url_prefix='/api/orders')

USER_API_URL = 'http://127.0.0.1:5000/api/users/'


def get_user(api_key: str):
    headers = {"Authorization": api_key}
    user_response = requests.get(USER_API_URL, headers=headers)
    if user_response.json().get('code') != 200:
        return None
    return user_response.json()


@order_blueprint.route('/add-item', methods=['POST'])
def add_order_item():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return APIResponse.error_response('Not Authorized', 401)
    user = get_user(api_key)
    if not user:
        return APIResponse.error_response('Not Authorized', 401)
    try:
        json_body = json.loads(request.data)
    except Exception as ex1:
        print(ex1)
        return APIResponse.error_response('Invalid body', 400)

    user_id = user['data']['id']
    book_id = json_body.get('book_id')
    quantity = json_body.get('quantity')

    open_order = Order.query.filter_by(user_id=user_id, is_open=True).first()

    if not open_order:
        open_order = Order()
        open_order.user_id = user_id
        open_order.is_open = True

        order_item = OrderItem(book_id=book_id, quantity=quantity)

        open_order.order_items.append(order_item)

    else:
        book_found = False
        for item in open_order.order_items:
            if item.book_id == book_id:
                item.quantity += quantity
                book_found = True
        if not book_found:
            new_order_item = OrderItem(book_id=book_id, quantity=quantity)
            open_order.order_items.append(new_order_item)

    db.session.add(open_order)
    db.session.commit()

    return APIResponse.ok_response(open_order.serialize())


@order_blueprint.route('/', methods=['GET'])
def get_open_orders():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return APIResponse.error_response('Not Authorized', 401)
    user = get_user(api_key)
    if not user:
        return APIResponse.error_response('Not Authorized', 401)

    user_id = user['data']['id']

    user_open_order = Order.query.filter_by(user_id=user_id, is_open=True).first()
    if not user_open_order:
        return APIResponse.ok_response([])
    return APIResponse.ok_response(user_open_order.serialize())

@order_blueprint.route('/checkout', methods=['POST'])
def checkout():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return APIResponse.error_response('Not Authorized', 401)
    user = get_user(api_key)
    if not user:
        return APIResponse.error_response('Not Authorized', 401)

    user_id = user['data']['id']

    user_open_order = Order.query.filter_by(user_id=user_id, is_open=True).first()

    if not user_open_order:
        return APIResponse.error_response('No open orders!', 400)

    user_open_order.is_open = False
    db.session.add(user_open_order)
    db.session.commit()
    return APIResponse.ok_response(user_open_order.serialize())
