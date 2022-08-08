from typing import List, Dict, Union, Optional

from flask import jsonify


class APIResponse:
    @staticmethod
    def ok_response(data: Union[Dict, List], message: str = 'OK'):
        return jsonify(
            {
                "code": 200,
                "message": message,
                "data": data
            }
        )

    @staticmethod
    def error_response(message: str, code: int = 400):
        return jsonify(
            {
                "code": code,
                "message": message
            }
        )
