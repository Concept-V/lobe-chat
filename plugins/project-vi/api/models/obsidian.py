from flask_restx import fields
from .base import api


# Pattern Evolution models
pattern_register_model = api.model('PatternRegister', {
    'prefix': fields.String(
        required=True, 
        description='Pattern prefix identifier'
    ),
    'attributes': fields.Raw(
        description='Pattern attributes'
    ),
    'relationships': fields.List(
        fields.Raw(), 
        description='Pattern relationships'
    ),
    'contexts': fields.List(
        fields.String(), 
        description='Pattern contexts'
    )
})

pattern_evolve_model = api.model('PatternEvolve', {
    'original_pattern': fields.String(
        required=True, 
        description='Original pattern identifier'
    ),
    'new_attributes': fields.Raw(
        description='New attributes to add/update'
    ),
    'new_relationships': fields.List(
        fields.Raw(), 
        description='New relationships to add'
    ),
    'evolution_reason': fields.String(
        required=True, 
        description='Reason for evolution'
    )
})

pattern_match_model = api.model('PatternMatch', {
    'content': fields.String(
        required=True, 
        description='Content to match against patterns'
    ),
    'context': fields.String(
        description='Context for matching'
    ),
    'threshold': fields.Float(
        description='Matching threshold', 
        default=0.8
    )
})

# Memory models
memory_store_model = api.model('MemoryStore', {
    'content': fields.String(
        required=True, 
        description='Content to store in memory'
    ),
    'memory_type': fields.String(
        required=True, 
        enum=['short_term', 'long_term'], 
        description='Type of memory to store'
    ),
    'metadata': fields.Raw(
        description='Optional metadata for the memory'
    )
})

memory_query_model = api.model('MemoryQuery', {
    'query': fields.String(
        required=True, 
        description='Search term or phrase'
    ),
    'memory_type': fields.String(
        enum=['short_term', 'long_term', 'all'], 
        description='Type of memories to search'
    )
})

# Obsidian Models
obsidian_search_model = api.model('ObsidianSearch', {
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

obsidian_connections_model = api.model('ObsidianConnections', {
    'note_path': fields.String(
        required=True,
        description='Path to the note to analyze'
    ),
    'include_backlinks': fields.Boolean(
        description='Include notes that link to this note'
    )
})
