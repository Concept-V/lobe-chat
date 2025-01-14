from flask import request, jsonify
from test import HelloWorld
from file_management import *
from mcp_tools import *
import json


def handle_gateway():
    data_bytes = request.get_data()
    try:
        payload = json.loads(data_bytes.decode('utf-8'))
        arguments = json.loads(payload.get('arguments', {}))
        apiName = payload.get('apiName')
    except (json.JSONDecodeError, KeyError):
        return jsonify({"error": "Invalid payload"}), 400

    if apiName == 'get_hello_world':
        return HelloWorld.get(request)

    elif apiName == 'get_read_file':
        file_path = arguments.get('file_path')
        return ReadFile.get(request, file_path)

    elif apiName == 'get_list_files':
        directory = arguments.get('directory', "../../../")
        return ListFiles.get(request, directory)

    elif apiName == 'post_write_file':
        file_path = arguments.get('file_path')
        content = arguments.get('content')
        return WriteFile.post(request, file_path, content)

    elif apiName == 'post_edit_file':
        file_path = arguments.get('file_path')
        new_content = arguments.get('content')
        backup = arguments.get('backup')  # Optional backup directory
        return EditFile.post(request, file_path, new_content, backup)

    elif apiName == 'post_create_directory':
        directory_path = arguments.get('directory_path')
        exist_ok = arguments.get('exist_ok', False)
        return CreateDirectory.post(request, directory_path, exist_ok)

    elif apiName == 'post_delete_path':
        path = arguments.get('path')
        recursive = arguments.get('recursive', False)
        return DeletePath.post(request, path, recursive)

    elif apiName == 'post_copy_path':
        source_path = arguments.get('source_path')
        destination_path = arguments.get('destination_path')
        recursive = arguments.get('recursive', False)
        return CopyPath.post(request, source_path, destination_path, recursive)

    elif apiName == 'post_move_path':
        source_path = arguments.get('source_path')
        destination_path = arguments.get('destination_path')
        return MovePath.post(request, source_path, destination_path)
    
    # MCP > obsidian
    elif apiName == 'post_advanced_search':
        query = arguments.get('query')
        search_type = arguments.get('search_type', 'text')
        include_metadata = arguments.get('include_metadata', False)
        follow_links = arguments.get('follow_links', False)
        max_depth = arguments.get('max_depth', 1)
        return AdvancedSearch.post(request, query, search_type, include_metadata, follow_links, max_depth)

    elif apiName == 'post_analyze_connections':
        note_path = arguments.get('note_path')
        include_backlinks = arguments.get('include_backlinks', False)
        return AnalyzeConnections.post(request, note_path, include_backlinks)

    elif apiName == 'get_list_resources':
        return ListResources.get(request)

    # MCP > sqlite
    elif apiName == 'post_execute_query':
        query = arguments.get('query')
        return ExecuteQuery.post(request, query)
        
    elif apiName == 'get_list_tables':
        return ListTables.get(request)
        
    elif apiName == 'post_store_data':
        category = arguments.get('category')
        content = arguments.get('content')
        metadata = arguments.get('metadata')
        return StoreData.post(request, category, content, metadata)

    else:
        return jsonify({"error": "Method Not Allowed"}), 405
