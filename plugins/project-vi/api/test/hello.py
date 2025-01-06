from flask_restx import Resource
from flask import jsonify
from model import api, hello_model

@api.doc(
    methods=['GET'],
    description='This endpoint sends a hello message from API. Expects a GET request.'
)
class HelloWorld(Resource):
    @api.expect(hello_model)
    def get(self):
        return jsonify({'message': 'Hello world from Flask API!'}), 200 # The dictionary is automatically JSONified
