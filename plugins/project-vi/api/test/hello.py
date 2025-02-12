from flask_restx import Resource
from flask import Response, jsonify
from models import api, hello_model


@api.doc(
    methods=['GET'],
    description='This endpoint sends a hello message from API. Expects a GET request.'
)
class Hello(Resource):
    @api.expect(hello_model)
    def get(self):
        response = Response()
        response = jsonify({'message': 'Hello world from Flask API!'})
        response.status_code = 200
        return response
