<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project-Int README</title>
    
</head>
<body>

<h1>Project-Int Flask Application</h1>

<h2>Overview</h2>
<p>This is a Flask-based web application designed for uploading, previewing, and searching files in multiple formats like <code>.txt</code>, <code>.pdf</code>, <code>.docx</code>, <code>.pptx</code>, and Jupyter notebooks (<code>.ipynb</code>). The app features content indexing and preview functionality for different file types.</p>

<h2>Features</h2>
<ul>
    <li>File Upload & Indexing: Upload files and index their content.</li>
    <li>Supported File Types: <code>.txt</code>, <code>.pdf</code>, <code>.docx</code>, <code>.pptx</code>, <code>.ipynb</code>.</li>
    <li>Search Functionality: Search through indexed files using keywords.</li>
    <li>File Preview: Preview PowerPoint slides, Jupyter notebooks, PDFs, text files, and images.</li>
</ul>

<h2>File Structure</h2>
<ul>
    <li><strong>app.py</strong>: Main application logic.</li>
    <li><strong>static/</strong>: Contains static assets (e.g., images).</li>
    <li><strong>templates/</strong>: HTML templates for rendering pages.</li>
    <li><strong>Dockerfile</strong>: Docker configuration file for containerizing the app.</li>
    <li><strong>Jenkinsfile</strong>: Jenkins pipeline for automating testing and deployment.</li>
    <li><strong>k8s/</strong>: Kubernetes manifests for deployment and service.</li>
</ul>

<h2>Installation</h2>

<h3>Docker Setup</h3>
<ol>
    <li><strong>Build the Docker image</strong>:
        <pre><code>docker build -t project-int-app .</code></pre>
    </li>
    <li><strong>Run the Docker container</strong>:
        <pre><code>docker run -p 5000:5000 -v $(pwd)/uploads:/app/uploads project-int-app</code></pre>
    </li>
</ol>

<h3>Kubernetes Setup</h3>
<ol>
    <li>Ensure <strong>Minikube</strong> or any Kubernetes cluster is running.</li>
    <li>Deploy the application:
        <pre><code>kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml</code></pre>
    </li>
    <li>Access the application by finding the service URL:
        <pre><code>minikube service project-int-service</code></pre>
    </li>
</ol>

<h2>CI/CD with Jenkins and ArgoCD</h2>
<ul>
    <li><strong>Jenkins Pipeline</strong>: The <code>Jenkinsfile</code> contains stages to build, test, and deploy the application in Kubernetes.</li>
    <li><strong>ArgoCD Integration</strong>: The app leverages ArgoCD for automated Kubernetes deployments. The <code>image-updater</code> updates app images based on changes in the container registry.</li>
</ul>

<h2>Usage</h2>
<ol>
    <li><strong>Upload Files:</strong> Use the homepage to upload supported files.</li>
    <li><strong>Search Files:</strong> Search through indexed files by keywords.</li>
    <li><strong>Preview Files:</strong> Preview uploaded files directly in the browser.</li>
</ol>

<h2>Branch-Specific Features</h2>
<ul>
    <li><strong>etcsys_test branch:</strong>
        <ul>
            <li>Kubernetes manifests for deployment.</li>
            <li>Integration with Jenkins and ArgoCD for automated CI/CD.</li>
            <li>Enhanced logging and error handling for file operations.</li>
        </ul>
    </li>
</ul>

<h2>Dependencies</h2>
<ul>
    <li>Flask</li>
    <li>python-pptx</li>
    <li>PyMuPDF (fitz)</li>
    <li>Mammoth</li>
    <li>nbformat</li>
    <li>Docker</li>
    <li>Kubernetes</li>
    <li>Jenkins</li>
    <li>ArgoCD</li>
</ul>

<h2>License</h2>
<p>This project is licensed under the MIT License.</p>

</body>
</html>
