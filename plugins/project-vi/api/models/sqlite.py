from flask_restx import fields
from .base import api

execute_query_model = api.model('ExecuteQuery', {
    'query': fields.String(
        required=True,
        description='SQL query to execute'
    )
})

store_data_model = api.model('StoreData', {
    'category': fields.String(
        required=True,
        description='Category of the data'
    ),
    'content': fields.String(
        required=True,
        description='Content to store'
    ),
    'metadata': fields.Raw(
        description='Additional metadata as JSON',
        default={}
    )
})

# list table doesn't need a model, just a response
list_tables_response = api.model('ListTablesResponse', {
    'tables': fields.List(
        fields.String,
        description='List of table names in the database'
    )
})
