
function runPythonCode() {
    const input = document.getElementById("pythonInput").value;
    const output = document.getElementById("pythonOutput");

    // Make an AJAX request to the server to execute the Python code
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/run_python", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            output.innerHTML = `<pre>${response.output}</pre>`;
        }
    };
    xhr.send(JSON.stringify({ code: input }));
}
