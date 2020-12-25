import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app, create_app
from models import setup_db, db, Actors, Movies
import random

casting_assistant_token = (os.environ.get('casting_assistant_token'))
casting_director_token = (os.environ.get('casting_director_token'))
executive_producer_token = (os.environ.get('executive_producer_token'))

database_path = (os.environ.get('DATABASE_URL_TEST'))


class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        self.casting_assistant_token = casting_assistant_token
        self.casting_director_token = casting_director_token
        self.executive_producer_token = executive_producer_token
        setup_db(self.app, self.database_path)

    def tearDown(self):
        # Executed after reach test
        pass

    '''
    post actor 200
    '''

    def test_success_200_post_actor(self):
        response_object = self.client().post(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(
                    self.executive_producer_token)},
            json={
                "name": "John",
                "age": "15",
                "gender": "male"})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['actors'])

    '''
    post actor 422
    '''

    def test_unprocessable_422_post_actor(self):

        response_object = self.client().post(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(
                    self.executive_producer_token)},
            json={
                "name": ""})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 422)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'unprocessable')

    '''
    post moive 200
    '''

    def test_success_200_post_movie(self):
        response_object = self.client().post(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(
                    self.executive_producer_token)},
            json={
                "title": "gratitude",
                "release_date": "2018-11-21 04:05:06"})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['movies'])

    '''
    post moive 422
    '''

    def test_unprocessable_422_post_movie(self):

        response_object = self.client().post(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(
                    self.executive_producer_token)},
            json={
                "title": "",
                "release_date": "21/11/2018"})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 422)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'unprocessable')

    '''
    get actors 200
    '''

    def test_success_200_get_actors(self):
        response_object = self.client().get(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_assistant_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['Actors'])

    '''
    get movies 200
    '''

    def test_success_200_get_movies(self):
        response_object = self.client().get(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_assistant_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['movies'])

    '''
    patch movie 200
    '''

    def test_success_200_patch_movie(self):
        random_id = random.choice([movie.id for movie in Movies.query.all()])
        response_object = self.client().patch(
            '/movies/' + str(random_id),
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_director_token)},
            json={
                "title": "live life"})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['movie'])

    '''
    patch movie 422
    '''

    def test_unprocessable_422_patch_movie(self):
        random_id = random.choice([movie.id for movie in Movies.query.all()])
        response_object = self.client().patch(
            '/movies/' + str(random_id),
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_director_token)},
            json={
                "title": ""})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 422)
        self.assertEqual(response_data['success'], False)

    '''
    patch actor 200
    '''

    def test_success_200_patch_actor(self):
        random_id = random.choice([actor.id for actor in Actors.query.all()])
        response_object = self.client().patch(
            '/actors/' + str(random_id),
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_director_token)},
            json={
                "name": "oliver"})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['actors'])

    '''
    patch actor 422
    '''

    def test_unprocessable_422_patch_actor(self):
        response_object = self.client().patch(
            '/actors/1',
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_director_token)},
            json={
                "name": ""})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 422)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'unprocessable')

    '''
    delete actor 200
    '''

    def test_success_200_delete_actor(self):
        random_id = random.choice([actor.id for actor in Actors.query.all()])
        response_object = self.client().delete("/actors/" + str(random_id),
        headers={"Authorization": "Bearer {}".format(
                self.executive_producer_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)

    '''
    delete actor 404
    '''

    def test_not_found_404_delete_actor(self):
        response_object = self.client().delete(
            "/actors/12345",
            headers={
                "Authorization": "Bearer {}".format(
                    self.executive_producer_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Not found')

    '''
    delete movie 200
    '''

    def test_success_200_delete_movie(self):
        random_id = random.choice([movie.id for movie in Movies.query.all()])
        response_object = self.client().delete("movies/" + str(random_id),
        headers={"Authorization": "Bearer {}".format(
                self.executive_producer_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)

    '''
    delete movie 404
    '''

    def test_not_found_404_delete_movie(self):
        response_object = self.client().delete(
            "/movies/12345",
            headers={
                "Authorization": "Bearer {}".format(
                    self.executive_producer_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
