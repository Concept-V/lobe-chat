from flask_restx import Resource
from flask import send_from_directory
from models import api, get_manifest_model


@api.doc(
    methods=['GET'],
    description='This endpoint returns manifest.json.'
)
class GetManifest(Resource):
    @api.expect(get_manifest_model)
    def get(self):
        return send_from_directory('../static', 'manifest.json')
