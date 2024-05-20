import os
import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_upload(self):
        data = {
            'category': 'test_category',
            'file': (open('test.txt', 'rb'), 'test.txt')
        }
        response = self.app.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 302)  # Check for redirect after successful upload

    def test_open_file(self):
        # Assuming the file 'test.txt' exists in the UPLOAD_FOLDER
        response = self.app.get('/open/test_category/test.txt')
        self.assertEqual(response.status_code, 200)  # Check if file is found and rendered

    def tearDown(self):
        # Clean up any test files or directories if needed
        pass

if __name__ == '__main__':
    unittest.main()
