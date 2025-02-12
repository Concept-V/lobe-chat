from flask_restx import Resource
from flask import jsonify
import os
import shutil
from datetime import datetime
from models import api, edit_file_model


@api.doc(
    methods=['POST'],
    description='This endpoint modify an existing files. (Optional) Saves a backup file.',
    params={
    'file_path': 'The path of the file to edit', 
    'content': 'The new content to write into the file', 
    'backup': 'Backup old file content to folder named `backup`'})
class EditFile(Resource):
    @api.expect(edit_file_model)
    @api.response(200, 'File edited successfully')
    @api.response(400, 'Invalid input')
    @api.response(404, 'File not found')
    @api.response(500, 'Internal Server Error')
    def post(self, file_path, new_content, backup=True):
        if not file_path or not new_content:
            return jsonify({"error": "Invalid input."}), 400
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found."}), 404
        
        try:
            if backup is True:
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                backup_directory = os.path.join("./backup", current_time)

                try:
                    os.makedirs(backup_directory, exist_ok=True)
                except Exception as e:
                    return jsonify({"error": f"Failed to create backup directory: {str(e)}"}), 500

                backup_file_path = os.path.join(backup_directory, file_path)
                print("backup_file_path: ", backup_file_path)

                try:
                    shutil.copy(file_path, backup_directory)
                except Exception as e:
                    print("Copy Error: ", e)
                    return jsonify({"error": f"Failed to back up the file: {str(e)}"}), 500
                
            # Write the new content to the file
            with open(file_path, 'w+') as file:
                file.write(new_content)
            
        except Exception as e:
            print("Error: ", e)
            return jsonify({"error": str(object=e)}), 500

        return jsonify({"message": "File edited successfully.", "backup": backup_file_path if backup_directory else None }), 200
