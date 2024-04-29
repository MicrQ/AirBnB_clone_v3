from api.v1.app import app
from api.v1.views import *
import json
import unittest


class TestIndex(unittest.TestCase):
    """ testing the index(/stats and /status routes) """

    def test_stats(self):
        with app.test_client().get('/api/v1/stats') as res:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(json.loads(res.data)), 6)

        with app.test_client().get('/api/v1/stats/') as res:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(json.loads(res.data)), 6)

    def test_status(self):
        with app.test_client().get('/api/v1/status') as res:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(json.loads(res.data)), 1)

        with app.test_client().get('/api/v1/status/') as res:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(json.loads(res.data)), 1)


if __name__ == '__main__':
    unittest.main()
