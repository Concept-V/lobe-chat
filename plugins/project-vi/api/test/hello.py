from flask_restx import Resource
from flask import jsonify
from model import api, hello_model


@api.doc(
    methods=['GET'],
    description='This endpoint sends a hello message from API.'
)
class HelloWorld(Resource):
    @api.expect(hello_model)
    def get(self):
        response = jsonify({'message': 'Hello world from Flask API!'})
        response.status_code = 200
        return response
        # deprecated way of returning response
        # jsonify({'message': 'Hello world from Flask API!'}), 200
