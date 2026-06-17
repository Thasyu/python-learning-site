const loginButton = document.getElementById("loginButton");
const dashboardButton = document.getElementById("dashboardButton");
const startButton = document.getElementById("startButton");
const textbookButton = document.getElementById("textbookButton");
const settingsButton = document.getElementById("settingsButton");
const message = document.getElementById("message");

loginButton.addEventListener("click", () => {
    window.location.href = "login.html";
});

dashboardButton.addEventListener("click", () => {
    if (isLoggedIn()) {
        window.location.href = "dashboard.html";
    } else {
        message.innerText = "先にログインしてください。";
    }
});

startButton.addEventListener("click", () => {
    if (isLoggedIn()) {
        window.location.href = "study.html";
    } else {
        message.innerText = "先にログインしてください。";
    }
});

textbookButton.addEventListener("click", () => {
    if (isLoggedIn()) {
        window.location.href = "../textbook/textbook.html";
    } else {
        message.innerText = "先にログインしてください。";
    }
});

settingsButton.addEventListener("click", () => {
    if (isLoggedIn()) {
        window.location.href = "settings.html";
    } else {
        message.innerText = "先にログインしてください。";
    }
});