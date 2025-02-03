from flask import Flask
from flask_cors import CORS
from models import api
from test.hello import Hello
from file_management import *
from user import *
from permissions import *
from mcp_tools import *
from static import *
from gateway.gateway import handle_gateway

app = Flask(__name__)
CORS(app)
api.init_app(app)

ns = api.namespace('api', description='File operations')

# Import all the resources and add them to the namespace
# Test
ns.add_resource(Hello, '/hello', endpoint='get_hello_world')

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

# User management & Permissions
ns.add_resource(GetUser, '/get_user', endpoint='get_user')
ns.add_resource(CreateUser, '/create_user', endpoint='create_user')
ns.add_resource(UpdateUser, '/update_user', endpoint='update_user')
ns.add_resource(DeleteUser, '/delete_user', endpoint='delete_user')
ns.add_resource(GetPermission, '/get_permission', endpoint='get_permission')

# MCP Tools
ns.add_resource(AddObservations, '/add_observations', endpoint='add_observations')
ns.add_resource(CreateEntities, '/create_entities', endpoint='create_entities')
ns.add_resource(CreateRelations, '/create_relations', endpoint='create_relations')
ns.add_resource(DeleteEntities, '/delete_entities', endpoint='delete_entities')
ns.add_resource(DeleteRelations, '/delete_relations', endpoint='delete_relations')
ns.add_resource(DeleteObservations, '/delete_observations', endpoint='delete_observations')
ns.add_resource(GetEntity, '/get_entity', endpoint='get_entity')
ns.add_resource(GetRelation, '/get_relation', endpoint='get_relation')
ns.add_resource(GetObservation, '/get_observation', endpoint='get_observation')
ns.add_resource(OpenNodes, '/open_nodes', endpoint='open_nodes')
ns.add_resource(SearchNodes, '/search_nodes', endpoint='search_nodes')
ns.add_resource(AdvancedSearch, '/advanced_search', endpoint='advanced_search')
ns.add_resource(AnalyzeConnections, '/analyze_connections', endpoint='analyze_connections')
ns.add_resource(RegisterPattern, '/register_pattern', endpoint='register_pattern')
ns.add_resource(MatchPattern, '/match_pattern', endpoint='match_pattern')
ns.add_resource(EvolvePattern, '/evolve_pattern', endpoint='evolve_pattern')
ns.add_resource(StoreMemory, '/store_memory', endpoint='store_memory')
ns.add_resource(QueryMemory, '/query_memory', endpoint='query_memory')
ns.add_resource(ExecuteQuery, '/execute_query', endpoint='execute_query')
ns.add_resource(ListTables, '/list_tables', endpoint='list_tables')
ns.add_resource(StoreData, '/store_data', endpoint='store_data')

# Serving static files
ns.add_resource(Logo, '/logo', endpoint='logo')
ns.add_resource(LogoBlack, '/logo_black', endpoint='logo_black')
ns.add_resource(Manifest, '/manifest', endpoint='manifest')
ns.add_resource(ManifestBeta, '/manifest_beta', endpoint='manifest_beta')


# Gateway
@app.route('/api/gateway', methods=['GET', 'POST', 'PUT', 'DELETE'])
def serve_gateway():
    return handle_gateway()


if __name__ == '__main__':
    app.run(port=3401, debug=True)
