document.addEventListener("DOMContentLoaded", () => {
    
    // Feature 1: Local Time Greeting Routine
    const greetingElement = document.getElementById("greeting");
    if (greetingElement) {
        const currentHour = new Date().getHours();
        if (currentHour < 12) greetingElement.innerText = "Good Morning! Welcome.";
        else if (currentHour < 18) greetingElement.innerText = "Good Afternoon! Welcome.";
        else greetingElement.innerText = "Good Evening! Welcome.";
    }

    // Feature 2: Smart Navigation State Highlight Tracker
    const currentPage = window.location.pathname.split("/").pop() || "index.html";
    const navButtons = document.querySelectorAll(".btn-custom-nav");
    
    navButtons.forEach(btn => {
        if (btn.getAttribute("data-page") === currentPage) {
            btn.classList.add("active");
        }
    });

    // Feature 3: Single Word Class Swapper (Light/Dark Scene)
    const themeToggle = document.getElementById("themeToggle");
    const body = document.body;
    const themeStatus = document.getElementById("themeStatus");

    function updateThemeStatus() {
        themeStatus.innerText = `Current Theme: ${body.classList.contains("light") ? "Light" : "Dark"}`;
    }

    // Load initial preference or default to light scene
    const preservedTheme = localStorage.getItem("theme") || "light";
    body.classList.add(preservedTheme);
    updateThemeStatus();

    themeToggle.addEventListener("click", () => {
        if (body.classList.contains("light")) {
            body.classList.replace("light", "dark");
            localStorage.setItem("theme", "dark");
        } else {
            body.classList.replace("dark", "light");
            localStorage.setItem("theme", "light");
        }
        updateThemeStatus();
    });
});