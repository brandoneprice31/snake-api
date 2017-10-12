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

    if 'first_name' not in body or 'last_name' not in body or 'fb_token' not in body:
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
@users.route(baseURI + '/fb_token/<fb_token>/sync_highscores', methods=['PATCH'])
async def postUser(request, fb_token):
    body = request.json

    if 'easy_highscores' not in body or 'hard_highscores' not in body:
        return json_response({ 'error': Response.BadRequest }, status=400)

    user = db.findUserByFbToken(fb_token)
    if user == None:
        return json_response({ 'error': Response.NotFoundError }, status=404)

    syncedHard = list(set(user['hard_highscores']) | set(body['hard_highscores']))
    hardHS = sorted(syncedHard, reverse=True)[:10]

    syncedEasy = list(set(user['easy_highscores']) | set(body['easy_highscores']))
    easyHS = sorted(syncedEasy, reverse=True)[:10]

    db.updateHighScores(user['_id'], easyHS, hardHS)

    return json_response({ 'easy_highscores': easyHS, 'hard_highscores': hardHS }, status=200)


#
# POST - /users/fb_token/:fb_token/sync_highscores
#
@users.route(baseURI + '/fb_token/<fb_token>/get_friends_highscores', methods=['POST'])
async def postUser(request, fb_token):
    body = request.json

    if 'fb_tokens' not in body:
        return json_response({ 'error': Response.BadRequest }, status=400)

    user = db.findUserByFbToken(fb_token)
    if user == None:
        return json_response({ 'error': Response.NotFoundError }, status=404)

    friends = db.getAllUsersByFBTokens(body['fb_tokens'])
    friendHighScores = []

    for friend in friends:
        maxEasy = 0
        if len(friend['easy_highscores']) > 0:
            maxEasy = max(friend['easy_highscores'])

        maxHard = 0
        if len(friend['hard_highscores']) > 0:
            maxHard = max(friend['hard_highscores'])

        friendHighScores.append({
            'first_name': friend['first_name'],
            'last_name': friend['last_name'],
            'fb_token': friend['fb_token'],
            'easy_highscore': maxEasy,
            'hard_highscore': maxHard
        })

    return json_response({ 'friends': friendHighScores}, status=200)

#
# DELETE - /users/fb_token/:fb_token/clear_highscores/:mode
#
@users.route(baseURI + '/fb_token/<fb_token>/clear_highscores/<mode>', methods=['DELETE'])
async def postUser(request, fb_token, mode):

    user = db.findUserByFbToken(fb_token)
    if user == None:
        return json_response({ 'error': Response.NotFoundError }, status=404)

    easyHS = [] if mode == "easy" else user['easy_highscores']
    hardHS = [] if mode == "hard" else user['hard_highscores']
    db.updateHighScores(user['_id'], easyHS, hardHS)

    return json_response({ 'success': 'removed ' + mode + ' highscores' }, status=201)

@users.route('/healthcheck', methods=['GET'])
async def healthcheck(request):
    return json_response({ 'success': 'yaayyayayay' }, status=200)
