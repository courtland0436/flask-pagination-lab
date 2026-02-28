#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

class Books(Resource):
    def get(self):
        # 1. Extract query parameters with defaults
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        # 2. Use .paginate() instead of .all()
        pagination_obj = Book.query.paginate(page=page, per_page=per_page, error_out=False)

        # 3. Serialize the items (the books for the current page)
        books_schema = BookSchema(many=True)
        books_data = books_schema.dump(pagination_obj.items)

        # 4. Build the structured response required by the tests
        response_dict = {
            "page": pagination_obj.page,
            "per_page": pagination_obj.per_page,
            "total": pagination_obj.total,
            "total_pages": pagination_obj.pages,
            "items": books_data
        }

        return make_response(jsonify(response_dict), 200)


api.add_resource(Books, '/books', endpoint='books')


if __name__ == '__main__':
    app.run(port=5555, debug=True)