from flask import request, jsonify
from test import HelloWorld
from file_management import ReadFile, WriteFile, ListFiles, EditFile
import json

def handle_gateway():
    data_bytes = request.get_data()
    try:
        payload = json.loads(data_bytes.decode('utf-8'))
        # print(payload)
        arguments = json.loads(payload.get('arguments', {}))
        apiName = payload.get('apiName')
        # print("apiName: ", apiName)
        # print("arguments: ", arguments)
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
        
    else:
        return jsonify({"error": "Method Not Allowed"}), 405
    