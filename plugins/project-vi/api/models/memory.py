from flask_restx import fields
from .base import api

# Knowledge Graph Models
entity_model = api.model('Entity', {
    'name': fields.String(
        required=True,
        description='The name of the entity'
    ),
    'entityType': fields.String(
        required=True,
        description='The type of the entity'
    ),
    'observations': fields.List(
        fields.String(),
        required=True,
        description='An array of observation contents associated with the entity'
    )
})

create_entities_model = api.model('CreateEntities', {
    'entities': fields.List(
        fields.Nested(entity_model),
        required=True,
        description='Array of entities to create'
    )
})

delete_entities_model = api.model('DeleteEntities', {
    'entityNames': fields.List(
        fields.String(),
        required=True,
        description='Array of entity names to delete'
    )
})

relation_model = api.model('Relation', {
    'from': fields.String(
        required=True,
        description='The name of the entity where the relation starts'
    ),
    'to': fields.String(
        required=True,
        description='The name of the entity where the relation ends'
    ),
    'relationType': fields.String(
        required=True,
        description='The type of the relation'
    )
})

create_relations_model = api.model('CreateRelations', {
    'relations': fields.List(
        fields.Nested(relation_model),
        required=True,
        description='Array of relations to create'
    )
})

delete_relations_model = api.model('DeleteRelations', {
    'relations': fields.List(
        fields.Nested(relation_model),
        required=True,
        description='Array of relations to delete'
    )
})

observation_model = api.model('Observation', {
    'entityName': fields.String(
        required=True,
        description='The name of the entity to add the observations to'
    ),
    'contents': fields.List(
        fields.String(),
        required=True,
        description='An array of observation contents to add'
    )
})

add_observations_model = api.model('AddObservations', {
    'observations': fields.List(
        fields.Nested(observation_model),
        required=True,
        description='Array of observations to add'
    )
})

delete_observations_model = api.model('DeleteObservations', {
    'deletions': fields.List(
        fields.Nested(observation_model),
        required=True,
        description='Array of observations to delete'
    )
})

search_nodes_model = api.model('SearchNodes', {
    'query': fields.String(
        required=True,
        description='The search query to match against entity names, types, and observation content'
    )
})

open_nodes_model = api.model('OpenNodes', {
    'names': fields.List(
        fields.String(),
        required=True,
        description='Array of entity names to retrieve'
    )
})
