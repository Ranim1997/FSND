import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db, Actors, Movies
from auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    Actors end-points
    '''

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            actors = Actors.query.all()
            if actors:
                return jsonify({'success': True,
                                'Actors': [{'id': actor.id,
                                            'age': actor.age,
                                            'name': actor.name}
                                           for actor in actors]}), 200
            else:
                return jsonify({'success': True, 'Actors': "No Actors"}), 200
        except Exception as ex:
            return jsonify({'success': False}), 404

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(payload):
        try:
            if request.data is not None:

                json_body = request.get_json()
                get_name = json_body.get('name', None)
                get_age = json_body.get('age', None)
                get_gender = json_body.get('gender', None)

                actor = Actors(name=get_name, age=get_age, gender=get_gender)
                Actors.insert(actor)

                actor_posted = Actors.query.filter_by(id=actor.id).first()

                return jsonify({
                    'success': True,
                    'actors': actor_posted.name
                }), 200
            else:
                abort(400)
        except Exception as ex:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actors(payload, id):
        try:
            actor_to_edit = Actors.query.get(id)
            if actor_to_edit:
                try:
                    get_body = request.get_json()
                    get_name = get_body.get('name')
                    get_age = get_body.get('age')
                    get_gender = get_body.get('gender')

                    if get_name == "" and get_age == "" and get_gender == "":
                        abort(400)

                    if get_name:
                        actor_to_edit.name = get_name
                    if get_age:
                        actor_to_edit.age = get_age
                    if get_gender:
                        actor_to_edit.gender = get_gender
                    actor_to_edit.update()
                    return jsonify({
                        'success': True,
                        'actors': actor_to_edit.name
                    }), 200
                except Exception as ex:
                    db.session.rollback()
                    abort(422)
            else:
                abort(404)
        except BaseException:
            abort(422)

    @app.route('/actors/<id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, id):
        actor_to_be_deleted = Actors.query.get(id)
        if actor_to_be_deleted:
            try:
                actor_to_be_deleted.delete()
                return jsonify({
                    'success': True,
                    'delete': id
                }), 200
            except Exception as ex:
                abort(422)
        else:
            abort(404)

    '''
    Movies end-points
    '''
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movies.query.all()
            if movies:
                return jsonify({'success': True,
                                'movies': [{
                                    "id": movie.id, 'title': movie.title,
                                    'releas date': movie.release_date}
                                    for movie in movies]}), 200
            else:
                return jsonify({'success': True, 'movies': "No Movies"}), 200
        except Exception as ex:
            return jsonify({'success': False}), 404

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(payload):
        try:
            if request.data:
                json_body = request.get_json()
                get_title = json_body.get('title', "")
                get_release_date = json_body.get('release_date', "")

                if get_title == "" or get_release_date == "":
                    abort(400)

                movie = Movies(title=get_title, release_date=get_release_date)
                Movies.insert(movie)

                movies_posted = Movies.query.filter_by(id=movie.id).first()

                return jsonify({
                    'success': True,
                    'movies': movies_posted.title
                }), 200
            else:
                abort(400)
        except Exception as ex:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movies(payload, id):
        movie_to_edit = Movies.query.get(id)
        if movie_to_edit:
            try:
                json_body = request.get_json()
                get_title = json_body.get('title', "")
                get_release_date = json_body.get('release_date', "")

                if get_title == "" and get_release_date == "":
                    abort(422)

                if get_title:
                    movie_to_edit.title = get_title
                if get_release_date:
                    movie_to_edit.release_date = get_release_date
                movie_to_edit.update()
                return jsonify({
                    'success': True,
                    'movie': movie_to_edit.title
                }), 200
            except Exception as ex:
                db.session.rollback()
                abort(422)
        else:
            abort(404)

    @app.route('/movies/<id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, id):
        movie_to_be_deleted = Movies.query.get(id)
        if movie_to_be_deleted:
            try:
                movie_to_be_deleted.delete()
                return jsonify({
                    'success': True,
                    'delete': id
                }), 200
            except Exception as ex:
                abort(422)
        else:
            abort(404)

    '''
    Error handlers
    '''

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(400)
    def Bad_Request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(500)
    def Internal_Server_Error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(405)
    def Method_Not_Allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(AuthError)
    def handle_auth_error(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            'message': e.error
        }), 401

    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
