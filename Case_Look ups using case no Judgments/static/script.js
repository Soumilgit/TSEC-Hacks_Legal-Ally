// Function to toggle Light/Dark Mode
function toggleTheme() {
    let body = document.body;
    let button = document.getElementById("theme-toggle");

    // Toggle dark mode class
    body.classList.toggle("dark-mode");

    // Store user preference in localStorage
    if (body.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
        button.textContent = "☀️ Light Mode";
    } else {
        localStorage.setItem("theme", "light");
        button.textContent = "🌙 Dark Mode";
    }
}

// Load the saved theme preference on page load
window.onload = function() {
    let savedTheme = localStorage.getItem("theme");
    let body = document.body;
    let button = document.getElementById("theme-toggle");

    if (savedTheme === "dark") {
        body.classList.add("dark-mode");
        button.textContent = "☀️ Light Mode";
    }
};

// Add event listener to the theme toggle button
document.getElementById("theme-toggle").addEventListener("click", toggleTheme);

// Function to search for a case with proper error handling
function searchCase() {
    let caseNumber = document.getElementById("case_number").value.trim();

    if (caseNumber === "") {
        alert("Please enter a case number.");
        return;
    }

    fetch("/search", {
        method: "POST",
        body: new URLSearchParams({ case_number: caseNumber }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.getElementById("result");

        if (data.error) {
            resultDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
        } else {
            resultDiv.innerHTML = `
                <p><strong>Case Number:</strong> ${data.case_no}</p>
                <p><strong>Petitioner:</strong> ${data.pet}</p>
                <p><strong>Respondent:</strong> ${data.res}</p>
                <p><strong>Petitioner Advocate:</strong> ${data.pet_adv}</p>
                <p><strong>Respondent Advocate:</strong> ${data.res_adv}</p>
                <p><strong>Bench:</strong> ${data.bench}</p>
                <p><strong>Judgement By:</strong> ${data.judgement_by}</p>
                <p><strong>Judgement Date:</strong> ${data.judgment_date}</p>
                <p><strong>PDF Link:</strong> <a href="${data.pdf_link}" target="_blank">View Judgment</a></p>
            `;
        }

        // Apply fade-in animation
        resultDiv.style.animation = "fadeIn 0.5s ease-in-out";
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("result").innerHTML = `<p style="color: red;">Error fetching data. Please try again.</p>`;
    });
}

// Attach event listener to the search button
document.getElementById("search-button").addEventListener("click", searchCase);
