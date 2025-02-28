/* script.js */

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-checker");
    const resultDiv = document.getElementById("result");
    const darkModeToggle = document.getElementById("dark-mode-toggle");
    
    // Handle form submission
    form.addEventListener("submit", function (event) {
        event.preventDefault();  // Prevent page reload
        
        let formData = new FormData(form);
        
        fetch("/compare", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = ""; // Clear previous results
            
            if (data.error) {
                resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
            } else if (data.missing_fields) {
                resultDiv.innerHTML = `<p style="color: red;">Missing Fields:</p><ul>`;
                data.missing_fields.forEach(field => {
                    resultDiv.innerHTML += `<li>${field}</li>`;
                });
                resultDiv.innerHTML += `</ul>`;
            } else {
                resultDiv.innerHTML = `<p style="color: green;">✅ The form is correctly formatted. No missing fields!</p>`;
            }
            resultDiv.classList.add("fade-in");
        })
        .catch(error => console.error("Error:", error));
    });
    
    // Dark Mode Toggle with Local Storage
    darkModeToggle.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
        const isDarkMode = document.body.classList.contains("dark-mode");
        localStorage.setItem("darkMode", isDarkMode);
        darkModeToggle.textContent = isDarkMode ? "☀️" : "🌙";
    });

    // Load Dark Mode preference from Local Storage
    if (localStorage.getItem("darkMode") === "true") {
        document.body.classList.add("dark-mode");
        darkModeToggle.textContent = "☀️";
    }
});
