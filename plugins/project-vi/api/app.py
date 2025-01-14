from flask import Flask, send_from_directory
from flask_cors import CORS
from models import api
from test import HelloWorld
from file_management import *
from gateway.gateway import handle_gateway

app = Flask(__name__)
CORS(app)
api.init_app(app)

ns = api.namespace('api', description='File operations')

# Import all the resources and add them to the namespace
# Test
ns.add_resource(HelloWorld, '/hello', endpoint='get_hello_world')

# File management
ns.add_resource(ReadFile, '/read_file', endpoint='get_read_file')
ns.add_resource(WriteFile, '/write_file', endpoint='post_write_file')
ns.add_resource(ListFiles, '/list_files', endpoint='get_list_files')
ns.add_resource(EditFile, '/edit_file', endpoint='post_edit_file')
ns.add_resource(
    CreateDirectory,
    '/create_directory',
    endpoint='post_create_directory'
)
ns.add_resource(DeletePath, '/delete_path', endpoint='post_delete_path')
ns.add_resource(CopyPath, '/copy_path', endpoint='post_copy_path')
ns.add_resource(MovePath, '/move_path', endpoint='post_move_path')

# MCP extensions from Claude


# Serving static files
@app.route('/manifest.json', methods=['GET'])
def serve_manifest():
    return send_from_directory('../static', 'manifest.json')


# Gateway
@app.route('/api/gateway', methods=['GET', 'POST', 'PUT', 'DELETE'])
def serve_gateway():
    return handle_gateway()


if __name__ == '__main__':
    app.run(port=3400, debug=True)
