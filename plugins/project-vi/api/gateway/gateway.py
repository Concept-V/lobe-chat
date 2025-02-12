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
        "post_add_observations": lambda args: AddObservations.post(req, args.get('observations')),
        "post_create_entities": lambda args: CreateEntities.post(req, args.get('entities')),
        "post_create_relations": lambda args: CreateRelations.post(req, args.get('relations')),
        "post_delete_entities": lambda args: DeleteEntities.post(req, args.get('entityNames')),
        "post_delete_relations": lambda args: DeleteRelations.post(req, args.get('relations')),
        "post_delete_observations": lambda args: DeleteObservations.post(req, args.get('observations')),
        "get_entity": lambda args: Entity.get(req),
        "get_relation": lambda args: Relation.get(req),
        "get_observation": lambda args: Observation.get(req, args.get('entityName')),
        "post_open_nodes": lambda args: OpenNodes.post(req, args.get('names')),
        "post_search_nodes": lambda args: SearchNodes.post(req, args.get('query')),
        "get_read_graph": lambda args: ReadGraph.get(req),

        "post_advanced_search": lambda args: AdvancedSearch.post(req, args.get('vault_path'), args.get('query'), args.get('search_type', 'text'), args.get('include_metadata', False), args.get('follow_links', False), args.get('max_depth', 1)),
        "post_analyze_connections": lambda args: AnalyzeConnections.post(req, args.get('vault_path'), args.get('note_path'), args.get('include_backlinks', False)),
        "get_list_resources": lambda args: ListResources.get(req, args.get('vault_path')),
        "post_read_resource": lambda args: ReadResource.post(req, args.get('vault_path'), args.get('uri')),

        "post_register_pattern": lambda args: RegisterPattern.post(req),
        "post_evolve_pattern": lambda args: EvolvePattern.post(req),
        "post_match_pattern": lambda args: MatchPattern.post(req),

        "post_semantic_search": lambda args: SemanticSearch.post(req, args.get('query'), args.get('limit', 5)),
        "post_query_concepts": lambda args: QueryConcepts.post(req, args.get('query'), args.get('limit', 5)),
        "post_store_concept": lambda args: StoreConcept.post(req, args.get('content'), args.get('metadata', {})),

        "post_execute_query": lambda args: ExecuteQuery.post(req, args.get('query')),
        "get_list_tables": lambda args: ListTables.get(req),
        "post_store_data": lambda args: StoreData.post(req, args.get('category'), args.get('content'), args.get('metadata', {})),
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
        print(arguments)

        # Retrieve the API handlers and execute the matching function
        api_handlers = get_api_handlers(request)
        handler = api_handlers.get(apiName, lambda args: (jsonify({"error": "Method Not Allowed"}), 405))

        return handler(arguments)

    except (json.JSONDecodeError, KeyError):
        return jsonify({"error": "Invalid payload"}), 400
