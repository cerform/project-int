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

    def test_open_file_route_nonexistent(self):
        response = self.app.get('/open/nonexistent_file.txt')
        self.assertEqual(response.status_code, 404)
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

        response = self.app.get('/open/pdf_file.pdf')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'%PDF' in response.data)  # Checking if the response contains PDF header

    def test_open_file_route_docx(self):
        response = self.app.get('/open/docx_file.docx')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Preview Docx' in response.data)

    def test_open_file_route_pptx(self):
        response = self.app.get('/open/pptx_file.pptx')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Preview Pptx' in response.data)

    def test_upload_route(self):
        # You can test the file upload route by sending a POST request with a file
        data = {
            'category': 'test_category',
            'file': (open('test_file.txt', 'rb'), 'test_file.txt')
        }
        response = self.app.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 302)  # Redirect after successful upload


if __name__ == '__main__':
    unittest.main()
