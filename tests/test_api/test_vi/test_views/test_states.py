from api.v1.app import app
from api.v1.views import *
from models import storage
from models.state import State
import json
import unittest


class TestState(unittest.TestCase):
    """ testing the routes of state """


    def test_get_status(self):
        with app.test_client().get('/api/v1/states') as res:
            self.assertEqual(res.status_code, 200)

    def test_get_response_data(self):
        with app.test_client().get('/api/v1/states') as res:
            states = [state.to_dict() for state in storage.all(State).values()]
            self.assertEqual(states, res.get_json())

    def test_delete_state(self):
        with app.test_client().delete('/api/v1/states/1234567') as res:
            self.assertEqual(res.status_code, 404)

        states_id = [state.id for state in storage.all(State).values()]
        delete_id = states_id[0]
        with app.test_client().delete('/api/v1/states/{}'.format(delete_id)) as res:
            states_id = [state.id for state in storage.all(State).values()]
            self.assertEqual(200, res.status_code)
            self.assertTrue(delete_id not in states_id)

    def test_post_state(self):
        number_of_states = len([state for state in storage.all(State).values()])

        with app.test_client().post('/api/v1/states',
                                     data=json.dumps({"name": "Test"}),
                                     content_type="application/json") as res:
            number_of_states2 = len([state for state in storage.all(State).values()])
            self.assertEqual(number_of_states, number_of_states2 - 1)
            self.assertEqual(res.status_code, 201)

    def test_put_city(self):
        states = [state.to_dict() for state in storage.all(State).values()]

        for state in states:
            name = state.get('name')
            if name is not None:
                a_state = state
                break
        test_name = 'test' if a_state['name'] != 'test' else 'tset'
        with app.test_client().put('/api/v1/states/{}'.format(a_state.get('id')),
                                    data=json.dumps({'name': test_name}),
                                    content_type='application/json') as res:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.get_json()['name'], test_name)
            self.assertNotEqual(name, res.get_json()['name'])


if __name__ == "__main__":
    unittest.main()
