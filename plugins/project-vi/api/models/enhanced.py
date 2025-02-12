from flask_restx import fields
from .base import api

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


semantic_search_model = api.model('SemanticSearch', {
    'query': fields.String(
        required=True,
        description='Search query'
    ),
    'limit': fields.Integer(
        description='Number of results to return',
        default=5
    )
})

store_concept_model = api.model('StoreConcept', {
    'content': fields.String(
        required=True,
        description='Content to store'
    ),
    'metadata': fields.Raw(
        description='Additional metadata',
        default={}
    )
})

query_concepts_model = api.model('QueryConcepts', {
    'query': fields.String(
        required=True,
        description='Query string'
    ),
    'limit': fields.Integer(
        description='Number of results to return',
        default=5
    )
})
