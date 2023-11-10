import sys
import unittest
from flask.testing import FlaskClient

# 현재 작업 디렉토리에 apiend 모듈이 있다고 가정
sys.path.append('.')

from apiend import create_app

class TestMyApp(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)

    def test_app(self):
        app = create_app()
        client = app.test_client()

        response = client.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
