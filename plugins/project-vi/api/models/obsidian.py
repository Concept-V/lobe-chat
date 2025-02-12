from flask_restx import fields
from .base import api


# Obsidian Models
advanced_search_model = api.model('ObsidianSearch', {
    'vault_path': fields.String(
        required=True,
        description='Path to the Obsidian vault'
    ),
    'query': fields.String(
        required=True,
        description='Search term'
    ),
    'search_type': fields.String(
        enum=['text', 'semantic', 'tag', 'path'],
        description='Type of search to perform'
    ),
    'include_metadata': fields.Boolean(
        description='Include note metadata in results'
    ),
    'follow_links': fields.Boolean(
        description='Include linked notes in results'
    ),
    'max_depth': fields.Integer(
        description='How many levels of links to follow'
    )
})

analyze_connections_model = api.model('ObsidianConnections', {
    'vault_path': fields.String(
        required=True,
        description='Path to the Obsidian vault'
    ),
    'note_path': fields.String(
        required=True,
        description='Path to the note to analyze'
    ),
    'include_backlinks': fields.Boolean(
        description='Include notes that link to this note'
    )
})

list_resources_model = api.model('ListResources', {
    'vault_path': fields.String(
        required=True,
        description='Path to Obsidian vault'
    )
})

read_resource_model = api.model('ReadResource', {
    'vault_path': fields.String(
        required=True,
        description='Path to Obsidian vault'
    ),
    'uri': fields.String(
        required=True,
        description='Resource URI'
    )
})
