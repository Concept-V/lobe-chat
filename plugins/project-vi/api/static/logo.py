from flask_restx import Resource
from flask import send_from_directory
from models import api, get_logo_model


@api.doc(
    methods=['GET'],
    description='This endpoint returns white logo.'
)
class Logo(Resource):
    @api.expect(get_logo_model)
    def get(self):
        return send_from_directory('../static', 'logo.png')
