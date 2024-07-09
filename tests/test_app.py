import os
import io
import pytest
from app import app, extract_text_from_txt, extract_text_from_pdf, extract_text_from_docx, extract_text_from_ipynb, search_files

SAMPLE_FILES_DIR = os.path.join(os.path.dirname(__file__), 'sample_files')

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload(client):
    data = {
        'category': 'test_category'
    }
    file_data = {
        'file': (io.BytesIO(b"Sample text content"), 'sample.txt')
    }
    response = client.post('/upload', data=file_data, content_type='multipart/form-data', follow_redirects=True)
    assert response.status_code == 200
    assert b'File successfully uploaded' in response.data

def test_extract_text_from_txt():
    content = extract_text_from_txt(os.path.join(SAMPLE_FILES_DIR, 'sample.txt'))
    assert content == 'This is a sample text file.\nIt contains some text for testing purposes.'

def test_extract_text_from_pdf():
    content = extract_text_from_pdf(os.path.join(SAMPLE_FILES_DIR, 'sample.pdf'))
    assert 'This is a sample PDF file.\nIt contains some text for testing purposes.' in content

def test_extract_text_from_docx():
    content = extract_text_from_docx(os.path.join(SAMPLE_FILES_DIR, 'sample.docx'))
    assert 'This is a sample DOCX file.\nIt contains some text for testing purposes.' in content

def test_extract_text_from_ipynb():
    content = extract_text_from_ipynb(os.path.join(SAMPLE_FILES_DIR, 'sample.ipynb'))
    assert '# Sample Notebook\n\nThis is a sample notebook.' in content

def test_search_files():
    results = search_files('sample')
    assert 'sample.txt' in results
    assert 'sample.pdf' in results

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data

def test_search_endpoint(client):
    data = {
        'query': 'sample'
    }
    response = client.post('/search', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'["sample.txt", "sample.pdf"]' in response.data

def test_pptx_preview(client):
    response = client.get('/pptx_preview')
    assert response.status_code == 200
    assert b'Slides Content' in response.data
