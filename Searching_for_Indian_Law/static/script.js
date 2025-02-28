document.addEventListener("DOMContentLoaded", function() {
    const themeToggle = document.querySelector(".theme-toggle");
    const body = document.body;

    // Load theme preference
    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark-mode");
    }

    themeToggle.addEventListener("click", function() {
        body.classList.toggle("dark-mode");
        if (body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.setItem("theme", "light");
        }
    });
});

async function searchLaws() {
    let keyword = document.getElementById('keyword').value;
    let sort_by = document.getElementById('sort_by').value;
    let order = document.getElementById('order').value;
    let limit = document.getElementById('limit').value;

    let response = await fetch('/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ keyword, sort_by, order, limit })
    });

    let results = await response.json();
    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    if (results.length === 0) {
        resultsDiv.innerHTML = "<p>No matching laws found.</p>";
        return;
    }

    results.forEach(async (law) => {
        let lawElement = document.createElement('div');
        lawElement.classList.add("fade-in");
        lawElement.innerHTML = `
            <h3>${law.title}</h3>
            <p><b>${sort_by === "P" ? "Published Date" : "Commencement Date"}:</b> ${law.published_date || law.commencement_date}</p>
            <a href="${law.url}" target="_blank">View Law</a>
            <button onclick="summarizeLaw('${law.title}')" class="animated-button">Summarize</button>
            <p id="summary-${law.title}"></p>
        `;
        resultsDiv.appendChild(lawElement);
    });
}

async function summarizeLaw(title) {
    let response = await fetch('/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
    });

    let data = await response.json();
    document.getElementById(`summary-${title}`).innerText = data.summary;
}
