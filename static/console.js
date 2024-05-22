document.addEventListener("DOMContentLoaded", async () => {
    const inputElement = document.getElementById("input");
    const outputElement = document.getElementById("output");
    const consoleElement = document.getElementById("console");
    const minimizeButton = document.getElementById("minimize-button");
    const maximizeButton = document.getElementById("maximize-button");
    const clearButton = document.getElementById("clear-button"); // Add clear button

    // Load Pyodide with the correct indexURL
    let pyodide;
    try {
        pyodide = await loadPyodide({
            indexURL: "https://cdn.jsdelivr.net/pyodide/v0.18.1/full/"
        });
    } catch (error) {
        console.error("Error loading Pyodide:", error);
        outputElement.innerHTML += `<div style="color: red;">Error loading Pyodide: ${error.message}</div>`;
        return;
    }

    minimizeButton.addEventListener("click", () => {
        consoleElement.style.height = "40px"; // Set the height of the console to a small value
        maximizeButton.style.display = "block"; // Show the maximize button
        minimizeButton.style.display = "none"; // Hide the minimize button
    });

    maximizeButton.addEventListener("click", () => {
        consoleElement.style.height = "auto"; // Set the height of the console back to auto
        maximizeButton.style.display = "none"; // Hide the maximize button
        minimizeButton.style.display = "block"; // Show the minimize button
    });

    clearButton.addEventListener("click", () => {
        outputElement.innerHTML = ""; // Clear the output
    });

    inputElement.addEventListener("keydown", async (event) => {
        if (event.key === "Enter" && !event.shiftKey) { // Check for Enter key without Shift
            event.preventDefault(); // Prevent default Enter behavior (line break)

            const code = inputElement.value;
            inputElement.value = "";

            // Display the input code
            outputElement.innerHTML += `<div>> ${code}</div>`;
            outputElement.scrollTop = outputElement.scrollHeight;

            try {
                // Capture the standard output from Python
                let result = await pyodide.runPythonAsync(`
import io
import sys
from contextlib import redirect_stdout, redirect_stderr

f = io.StringIO()
with redirect_stdout(f), redirect_stderr(f):
${code}

f.getvalue()
                `);

                // Display the captured output
                outputElement.innerHTML += `<div>${result}</div>`;
            } catch (err) {
                let errorMessage = err.toString();

                // Check for common Python 2 to 3 syntax error
                if (errorMessage.includes("SyntaxError: Missing parentheses in call to 'print'")) {
                    errorMessage += "<br>Hint: In Python 3, use print('Hello World') instead of print 'Hello World'.";
                }

                outputElement.innerHTML += `<div style="color: red;">${errorMessage}</div>`;
            }

            outputElement.scrollTop = outputElement.scrollHeight;
        }
    });
});
