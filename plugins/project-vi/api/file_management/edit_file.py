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
    'backup': 'Backup old file content to folder named `backup`'}
)
class EditFile(Resource):
    @api.expect(edit_file_model)
    @api.response(200, 'File edited successfully')
    @api.response(400, 'Invalid input')
    @api.response(404, 'File not found')
    @api.response(500, 'Internal Server Error')
    def post(self, file_path, new_content, backup=True):
        # Debug prints
        print("\nDebug Info:")
        print(f"Backup parameter type: {type(backup)}, value: {backup}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Attempting to edit file: {file_path}")
        
        # Convert backup to boolean if it's a string
        if isinstance(backup, str):
            backup = backup.lower() == 'true'
        
        print(f"Converted backup value: {backup}")
        
        # Initialize variables used in return statement
        backup_directory = None
        backup_file_path = None
        
        if not file_path or not new_content:
            return jsonify({"error": "Invalid input."}), 400
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found."}), 404
        
        try:
            if backup:  # Now using the converted boolean value
                print("Backup is True, proceeding with backup...")
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                backup_directory = os.path.join("./backup", current_time)
                print(f"Created backup directory path: {backup_directory}")

                try:
                    os.makedirs(backup_directory, exist_ok=True)
                    print(f"Created backup directory at: {os.path.abspath(backup_directory)}")
                except Exception as e:
                    error_msg = f"Failed to create backup directory: {str(e)}"
                    print(error_msg)
                    return jsonify({"error": error_msg}), 500

                backup_file_path = os.path.join(backup_directory, os.path.basename(file_path))
                print(f"Backup file path: {backup_file_path}")

                try:
                    # Create the backup directory structure
                    os.makedirs(os.path.dirname(backup_file_path), exist_ok=True)
                    print(f"Created backup file directory structure")
                    # Copy the file with preserved metadata
                    shutil.copy2(file_path, backup_file_path)
                    print(f"Copied file to backup location")
                except Exception as e:
                    error_msg = f"Failed to back up the file: {str(e)}"
                    print(error_msg)
                    return jsonify({"error": error_msg}), 500
            else:
                print("Backup is False, skipping backup")
                
            # Write the new content with explicit UTF-8 encoding
            with open(file_path, 'w+', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Successfully wrote {len(new_content)} characters to file")
            
        except Exception as e:
            error_msg = f"Error editing file {file_path}: {str(e)}"
            print(error_msg)
            return jsonify({"error": error_msg}), 500

        return jsonify({
            "message": "File edited successfully.",
            "backup": backup_file_path if backup_directory else None
        }), 200
