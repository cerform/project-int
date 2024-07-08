import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Expected Content', result.data)

    def test_upload(self):
        with open('test_file.txt', 'rb') as test_file:
            data = {
                'file': (test_file, 'test_file.txt'),
                'category': 'test'
            }
            result = self.app.post('/upload', data=data, follow_redirects=True)
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'File successfully uploaded', result.data)

if __name__ == '__main__':
    unittest.main()
