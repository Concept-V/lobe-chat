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
