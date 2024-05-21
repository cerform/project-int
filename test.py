import os
import unittest
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

if __name__ == '__main__':
    unittest.main()
