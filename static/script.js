document.addEventListener("DOMContentLoaded", () => {
    const consoleContainer = document.getElementById("console-container");
    const minimizeBtn = document.getElementById("minimize-btn");
    const maximizeBtn = document.getElementById("maximize-btn");

    // Function to update the position of the console window
    function updateConsolePosition() {
        const scrollY = window.scrollY || window.pageYOffset;
        const windowHeight = window.innerHeight;
        const consoleHeight = consoleContainer.offsetHeight;

        // Calculate the new top position based on scroll and window height
        let newTop = windowHeight - consoleHeight - 20; // Adjust as needed
        newTop += scrollY; // Add scroll position

        // Set the new top position
        consoleContainer.style.top = `${newTop}px`;
    }

    // Initial positioning
    updateConsolePosition();

    // Update position on scroll
    window.addEventListener("scroll", updateConsolePosition);

    // Function to minimize the console window
    function minimizeConsole() {
        consoleContainer.classList.add("minimized");
    }

    // Function to maximize the console window
    function maximizeConsole() {
        consoleContainer.classList.remove("minimized");
    }

    // Event listener for the minimize button
    minimizeBtn.addEventListener("click", minimizeConsole);

    // Event listener for the maximize button
    maximizeBtn.addEventListener("click", maximizeConsole);
});
