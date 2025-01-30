from flask_restx import fields
from .base import api

get_user_model = api.model('GetUser', {
    'username': fields.String(
        required=True,
        description='Username'
    ),
    'password': fields.String(
        required=True,
        description='Password'
    )
})

create_user_model = api.model('CreateUser', {
    'username': fields.String(
        required=True,
        description='Username'
    ),
    'password': fields.String(
        required=True,
        description='Password'
    ),
    'permissions': fields.Integer(
        required=True,
        description='User permissions as integer'
    ),
    'state': fields.String(
        description='Account state',
        enum=['active', 'suspended'],
        default='active'
    )
})

update_user_model = api.model('UpdateUser', {
    'username': fields.String(
        required=True,
        description='Username'
    ),
    'permissions': fields.Integer(
        description='User permissions as integer'
    ),
    'state': fields.String(
        description='Account state',
        enum=['active', 'suspended']
    )
})

delete_user_model = api.model('DeleteUser', {
    'username': fields.String(
        required=True,
        description='Username to delete'
    )
})
