from flask_restx import Resource
from flask import send_from_directory
from models import api, get_logo_black_model


@api.doc(
    methods=['GET'],
    description='This endpoint returns black logo.'
)
class GetLogoBlack(Resource):
    @api.expect(get_logo_black_model)
    def get(self):
        return send_from_directory('../static', 'logo_black.svg')
