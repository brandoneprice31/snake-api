import asyncio
from sanic.response import json as json_response
from sanic import Blueprint

from db.db import db
from responses.response import Response

users = Blueprint('users')
baseURI = '/' + users.name

#
# POST - /users
# {
#   first_name: string,
#   last_name: string
# }
#
@users.route(baseURI, methods=['POST'])
async def postUser(request):
    body = request.json

    if 'first_name' not in body and 'last_name' not in body:
        return json_response({ 'error': Response.BadRequest }, status=400)

    user_id = db.insertUser(body)
    user = db.findUserById(user_id)

    return json_response({ 'user': user }, status=201)
