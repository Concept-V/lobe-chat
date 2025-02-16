from flask_restx import fields
from .base import api

read_file_model = api.model('FileRead', {
    'file_path': fields.String(
        required=True,
        description='The path of the file to read'
    )
})

write_file_model = api.model('FileWrite', {
    'file_path': fields.String(
        required=True,
        description='The path of the file to write'
    ),
    'content': fields.String(
        required=True,
        description='The content to write into the file'
    )
})

edit_file_model = api.model('EditFile', {
    'file_path': fields.String(
        required=True,
        description='The path of the file to edit'
    ),
    'content': fields.String(
        required=True,
        description='New content to write into the file'
    ),
    'backup': fields.Boolean(
        description='Backup old file content to folder named `backup`'
    ),
})

list_files_model = api.model('ListFiles', {
    'directory': fields.String(
        description='The directory to list files from. By default, it lists files in the current directory.',
    )
})

create_directory_model = api.model('CreateDirectory', {
    'directory_path': fields.String(
        required=True,
        description='The path of the directory to create'
    ),
    'exist_ok': fields.Boolean(
        description='Do not raise an error if the directory already exists',
        default=False
    ),
})

delete_model = api.model('Delete', {
    'path': fields.String(
        required=True,
        description='The path of the file or directory to delete'
    ),
    'recursive': fields.Boolean(
        description='Recursively delete directories',
        default=False
    ),
})

copy_model = api.model('Copy', {
    'source_path': fields.String(
        required=True,
        description='The path of the source file or directory'
    ),
    'destination_path': fields.String(
        required=True,
        description='The destination path'
    ),
    'recursive': fields.Boolean(
        description='Recursively copy directories',
        default=False
    ),
})

move_model = api.model('Move', {
    'source_path': fields.String(
        required=True,
        description='The path of the source file or directory'
    ),
    'destination_path': fields.String(
        required=True,
        description='The destination path'
    ),
})
