import flask
import unittest
from api.v1.app import app


class AppTestCase(unittest.TestCase):
    '''test for app'''

    def test_create_app(self):
        with app.test_client() as test:
            self.assertIsInstance(test, flask.testing.FlaskClient)


if __name__ == '__main__':
    unittest.main()
