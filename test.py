import os
import unittest
<<<<<<< HEAD
from app import *

class TestPPTXExtraction(unittest.TestCase):
    def setUp(self):
        # Path to the test PowerPoint file
        self.pptx_file_path = 'path_to_existing_or_new_test_pptx_file.pptx'

        # Check if the file exists
        if not os.path.exists(self.pptx_file_path):
            # Create a new test PowerPoint file
            self.create_test_pptx_file()

    def create_test_pptx_file(self):
        # Write your code here to create a new test PowerPoint file
        pass

    def test_image_saved_correctly(self):
        # Test whether images are extracted correctly from the PowerPoint file
        slides_content = extract_text_and_images_from_pptx(self.pptx_file_path, 'test_images_dir')
        # Write your assertions here

if __name__ == '__main__':
    unittest.main()
import os
import unittest
from app import extract_text_and_images_from_pptx

class TestPPTXExtraction(unittest.TestCase):
    def setUp(self):
        # Path to the test PowerPoint file
        self.pptx_file_path = 'path_to_existing_or_new_test_pptx_file.pptx'

        # Check if the file exists
        if not os.path.exists(self.pptx_file_path):
            # Create a new test PowerPoint file
            self.create_test_pptx_file()

    def create_test_pptx_file(self):
        # Write your code here to create a new test PowerPoint file
        pass

    def test_image_saved_correctly(self):
        # Test whether images are extracted correctly from the PowerPoint file
        slides_content = extract_text_and_images_from_pptx(self.pptx_file_path, 'test_images_dir')
        # Write your assertions here

=======
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

>>>>>>> main
if __name__ == '__main__':
    unittest.main()
