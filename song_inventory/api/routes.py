from flask import Blueprint, request, jsonify
from song_inventory.helpers import token_required
from song_inventory.models import db, Song, song_schema, songs_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return{ 'some' : 'value' }

@api.route('/songs', methods = ['POST'])
@token_required
def create_song(current_user_token):
    album_name = request.json['album_name']
    song_name= request.json['song_name']
    artist = request.json['artist']
    lyrics = request.json['lyrics']
    user_token = current_user_token.token

    print(f"User Token: {current_user_token.token}")

    song = Song(album_name, song_name, artist, lyrics, user_token = user_token)

    db.session.add(song)
    db.session.commit()

    response = song_schema.dump(song)
    print(response)

    return jsonify(response)

@api.route('/songs', methods = ['GET'])
@token_required
def get_songs(current_user_token):
    owner = current_user_token.token
    songs = Song.query.filter_by(user_token=owner).all()
    response = songs_schema.dump(songs)
    return jsonify(response)

@api.route('/songs/<id>', methods = ['GET'])
@token_required
def get_song(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        song = Song.query.get(id)
        response = song_schema.dump(song)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401

@api.route('/songs/<id>', methods = ['POST', 'PUT'])
@token_required
def update_song(current_user_token, id):
    song = Song.query.get(id)
    song.album_name = request.json['album_name']
    song.song_name = request.json['song_name']
    song.artist = request.json['artist']
    song.lyrics = request.json['lyrics']
    song.user_token = current_user_token.token

    db.session.commit()
    response = song_schema.dump(song)
    return jsonify(response)

@api.route('/songs/<id>', methods = ['DELETE'])
@token_required
def delete_song(current_user_token, id):
    song = Song.query.get(id)
    db.session.delete(song)
    db.session.commit()
    response = song_schema.dump(song)
    return jsonify(response)