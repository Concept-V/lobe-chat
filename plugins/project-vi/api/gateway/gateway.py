from flask import request, jsonify
from test.hello import Hello
from file_management import *
from user import *
from permissions import *
from static import *
# from mcp_tools import *
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
        return Hello.get(request)

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
    
    elif apiName == 'get_user':
        username = arguments.get('username')
        return GetUser.get(request, username)
    
    elif apiName == 'post_create_user':
        username = arguments.get('username')
        password = arguments.get('password')
        permissions = arguments.get('permissions')
        state = arguments.get('state', 'active')
        return CreateUser.post(request, username, password, permissions, state)
    
    elif apiName == 'post_update_user':
        username = arguments.get('username')
        permissions = arguments.get('permissions')
        return UpdateUser.post(request, username, permissions)
    
    elif apiName == 'post_delete_user':
        username = arguments.get('username')
        return DeleteUser.post(request, username)
    
    elif apiName == 'get_permission':
        username = arguments.get('username')
        return GetPermission.get(request, username)
    
    elif apiName == 'get_logo':
        return GetLogo.get(request)
    
    elif apiName == 'get_logo_black':
        return GetLogoBlack.get(request)
    
    elif apiName == 'get_manifest':
        return GetManifest.get(request)

    else:
        return jsonify({"error": "Method Not Allowed"}), 405
