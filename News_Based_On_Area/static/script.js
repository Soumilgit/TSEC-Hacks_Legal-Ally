document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded!");

    // Add smooth scroll effect when clicking a news item
    document.querySelectorAll(".news-item").forEach(item => {
        item.addEventListener("mouseenter", () => {
            item.style.transition = "transform 0.2s ease-in-out";
            item.style.transform = "scale(1.05)";
        });
        item.addEventListener("mouseleave", () => {
            item.style.transform = "scale(1)";
        });
    });
});
