from flask_restx import fields
from .base import api


advanced_search_model = api.model('AdvancedSearch', {
    'query': fields.String(
        required=True,
        description='Search term'
    ),
    'search_type': fields.String(
        description='Type of search to perform',
        enum=['text', 'semantic', 'tag', 'path'],
        default='text'
    ),
    'include_metadata': fields.Boolean(
        description='Include note metadata in results',
        default=False
    ),
    'follow_links': fields.Boolean(
        description='Include linked notes in results',
        default=False
    ),
    'max_depth': fields.Integer(
        description='How many levels of links to follow',
        default=1
    )
})

analyze_connections_model = api.model('AnalyzeConnections', {
    'note_path': fields.String(
        required=True,
        description='Path to the note to analyze'
    ),
    'include_backlinks': fields.Boolean(
        description='Include notes that link to this note',
        default=False
    )
})

list_resource_model = api.model('Resource', {
    'uri': fields.String(description='Resource URI'),
    'name': fields.String(description='Resource name'),
    'mimeType': fields.String(description='MIME type of the resource'),
    'description': fields.String(description='Resource description')
})

read_resource_model = api.model('ReadResource', {
    'uri': fields.String(
        required=True,
        description='URI of the resource to read'
    )
})
