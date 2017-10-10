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
#   last_name: string,
#   fb_token:  string
# }
#
@users.route(baseURI, methods=['POST'])
async def postUser(request):
    body = request.json

    if 'first_name' not in body and 'last_name' not in body and 'fb_token' not in body:
        return json_response({ 'error': Response.BadRequest }, status=400)

    user_id = db.insertUser(body)
    user = db.findUserById(user_id)

    return json_response({ 'user': user }, status=201)

#
# GET - /users/fb_token/:fb_token
#
@users.route(baseURI + '/fb_token/<fb_token>', methods=['GET'])
async def postUser(request, fb_token):

    user = db.findUserByFbToken(fb_token)
    if user == None:
        return json_response({ 'error': Response.NotFoundError }, status=404)

    return json_response({ 'user': user }, status=200)

#
# PATCH - /users/fb_token/:fb_token/sync_highscores
#
@users.route(baseURI + '/fb_token/<fb_token>', methods=['PATCH'])
async def postUser(request, fb_token):
    body = request.json

    if 'easy_highscores' not in body and 'hard_highscores' not in body:
        return json_response({ 'error': Response.BadRequest }, status=400)

    user = db.findUserByFbToken(fb_token)
    if user == None:
        return json_response({ 'error': Response.NotFoundError }, status=404)

    hardHS = sorted(user['hard_highscores'] + body['hard_highscores'], reversed=True)[:10]
    easyHS = sorted(user['easy_highscores'] + body['easy_highscores'], reversed=True)[:10]

    db.updateHighScores(user['_id'], easyHS, hardHS)
    user = db.findUserById(user['_id'])

    return json_response({ 'user': user }, status=200)
