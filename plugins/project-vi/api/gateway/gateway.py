from flask import request, jsonify
from test.hello import Hello
from file_management import *
from user import *
from static import *
from mcp_tools import *
import json

def get_api_handlers(req):
    return {
        # test
        "get_hello_world": lambda args: Hello.get(req),
        # file management
        "get_read_file": lambda args: ReadFile.get(req, args.get('file_path')),
        "get_list_files": lambda args: ListFiles.get(req, args.get('directory', "../../../")),
        "post_write_file": lambda args: WriteFile.post(req, args.get('file_path'), args.get('content')),
        "post_edit_file": lambda args: EditFile.post(req, args.get('file_path'), args.get('content'), args.get('backup')),
        "post_create_directory": lambda args: CreateDirectory.post(req, args.get('directory_path'), args.get('exist_ok', False)),
        "post_delete_path": lambda args: DeletePath.post(req, args.get('path'), args.get('recursive', False)),
        "post_copy_path": lambda args: CopyPath.post(req, args.get('source_path'), args.get('destination_path'), args.get('recursive', False)),
        "post_move_path": lambda args: MovePath.post(req, args.get('source_path'), args.get('destination_path')),
        # user & permissions
        "get_get_user": lambda args: GetUser.get(req, args.get('username'), args.get('password')),
        "post_create_user": lambda args: CreateUser.post(req, args.get('username'), args.get('password'), args.get('permissions'), args.get('state', 'active')),
        "post_update_user": lambda args: UpdateUser.post(req, args.get('username'), args.get('password'), args.get('permissions', None), args.get('state', None)),
        "delete_delete_user": lambda args: DeleteUser.delete(req, args.get('username')),
        "get_user_permission": lambda args: UserPermission.get(req, args.get('username')),
        # mcp tools
        "post_add_observations": lambda args: AddObservations.post(req),
        "post_create_entities": lambda args: CreateEntities.post(req),
        "post_create_relations": lambda args: CreateRelations.post(req),
        "post_delete_entities": lambda args: DeleteEntities.post(req),
        "post_delete_relations": lambda args: DeleteRelations.post(req),
        "post_delete_observations": lambda args: DeleteObservations.post(req),
        "get_get_entity": lambda args: GetEntity.get(req),
        "get_get_relation": lambda args: GetRelation.get(req),
        "get_get_observation": lambda args: GetObservation.get(req),
        "post_open_nodes": lambda args: OpenNodes.post(req),
        "post_search_nodes": lambda args: SearchNodes.post(req),
        "post_advanced_search": lambda args: AdvancedSearch.post(req),
        "post_analyze_connections": lambda args: AnalyzeConnections.post(req),
        "post_register_pattern": lambda args: RegisterPattern.post(req),
        "post_evolve_pattern": lambda args: EvolvePattern.post(req),
        "post_match_pattern": lambda args: MatchPattern.post(req),
        "post_query_memory": lambda args: QueryMemory.post(req),
        "post_store_memory": lambda args: StoreMemory.post(req),
        "post_execute_query": lambda args: ExecuteQuery.post(req),
        "get_list_tables": lambda args: ListTables.get(req),
        "post_store_data": lambda args: StoreData.post(req),
        # static
        "get_logo": lambda args: Logo.get(req),
        "get_logo_black": lambda args: LogoBlack.get(req),
        "get_manifest": lambda args: Manifest.get(req),
        "get_manifest_beta": lambda args: ManifestBeta.get(req),
    }


def handle_gateway():
    data_bytes = request.get_data()
    try:
        payload = json.loads(data_bytes.decode('utf-8'))
        arguments = json.loads(payload.get('arguments', {}))
        apiName = payload.get('apiName')
        print(apiName)

        # Retrieve the API handlers and execute the matching function
        api_handlers = get_api_handlers(request)
        handler = api_handlers.get(apiName, lambda args: (jsonify({"error": "Method Not Allowed"}), 405))

        return handler(arguments)

    except (json.JSONDecodeError, KeyError):
        return jsonify({"error": "Invalid payload"}), 400
