function getToken() {
    return localStorage.getItem("token");
}

const APPEARANCE_THEME_KEY = "appearance_theme";
const APPEARANCE_ACCENT_COLOR_KEY = "appearance_accent_color";
const DEFAULT_THEME = "dark";
const DEFAULT_ACCENT = "cyan";
const APPEARANCE_THEME_MEDIA_QUERY = window.matchMedia("(prefers-color-scheme: dark)");

let appearanceSystemListenerAttached = false;

const ACCENT_PRESETS = {
    cyan: {
        accentColor: "#6ee4ff",
        accentHover: "#9eedff",
        accentSoft: "rgba(110, 228, 255, 0.2)",
        accentBorder: "rgba(110, 228, 255, 0.34)",
        accentGlow: "rgba(110, 228, 255, 0.36)",
        accentRing: "rgba(110, 228, 255, 0.16)",
        accentGradientMid: "#88ebff",
        accentGradientEnd: "#b6f3ff",
        accentButtonGlow: "rgba(78, 196, 255, 0.32)",
        secondaryColor: "#7b61ff",
        secondaryGlow: "rgba(123, 97, 255, 0.24)"
    },
    blue: {
        accentColor: "#4f8cff",
        accentHover: "#78a9ff",
        accentSoft: "rgba(79, 140, 255, 0.2)",
        accentBorder: "rgba(79, 140, 255, 0.34)",
        accentGlow: "rgba(79, 140, 255, 0.36)",
        accentRing: "rgba(79, 140, 255, 0.16)",
        accentGradientMid: "#73a4ff",
        accentGradientEnd: "#9ec1ff",
        accentButtonGlow: "rgba(79, 140, 255, 0.3)",
        secondaryColor: "#6a7dff",
        secondaryGlow: "rgba(106, 125, 255, 0.24)"
    },
    purple: {
        accentColor: "#b084ff",
        accentHover: "#c5a4ff",
        accentSoft: "rgba(176, 132, 255, 0.22)",
        accentBorder: "rgba(176, 132, 255, 0.34)",
        accentGlow: "rgba(176, 132, 255, 0.36)",
        accentRing: "rgba(176, 132, 255, 0.18)",
        accentGradientMid: "#c19bff",
        accentGradientEnd: "#d7bfff",
        accentButtonGlow: "rgba(176, 132, 255, 0.3)",
        secondaryColor: "#7f93ff",
        secondaryGlow: "rgba(127, 147, 255, 0.24)"
    },
    green: {
        accentColor: "#2fd7a8",
        accentHover: "#56e2bd",
        accentSoft: "rgba(47, 215, 168, 0.22)",
        accentBorder: "rgba(47, 215, 168, 0.34)",
        accentGlow: "rgba(47, 215, 168, 0.34)",
        accentRing: "rgba(47, 215, 168, 0.16)",
        accentGradientMid: "#5de5bf",
        accentGradientEnd: "#96f0d8",
        accentButtonGlow: "rgba(47, 215, 168, 0.28)",
        secondaryColor: "#4fb6ff",
        secondaryGlow: "rgba(79, 182, 255, 0.24)"
    },
    pink: {
        accentColor: "#ff4fd8",
        accentHover: "#ff7be6",
        accentSoft: "rgba(255, 79, 216, 0.22)",
        accentBorder: "rgba(255, 79, 216, 0.38)",
        accentGlow: "rgba(255, 79, 216, 0.4)",
        accentRing: "rgba(255, 79, 216, 0.18)",
        accentGradientMid: "#ff5ce1",
        accentGradientEnd: "#ff91ee",
        accentButtonGlow: "rgba(255, 79, 216, 0.34)",
        secondaryColor: "#57b3ff",
        secondaryGlow: "rgba(87, 179, 255, 0.24)"
    }
};

function normalizeTheme(theme) {
    if (theme === "light" || theme === "system") {
        return theme;
    }

    return "dark";
}

function normalizeAccent(accent) {
    return Object.prototype.hasOwnProperty.call(ACCENT_PRESETS, accent) ? accent : DEFAULT_ACCENT;
}

function getAppearanceSettings() {
    return {
        theme: normalizeTheme(localStorage.getItem(APPEARANCE_THEME_KEY) || DEFAULT_THEME),
        accent: normalizeAccent(localStorage.getItem(APPEARANCE_ACCENT_COLOR_KEY) || DEFAULT_ACCENT)
    };
}

function getResolvedTheme(themePreference) {
    if (themePreference === "system") {
        return APPEARANCE_THEME_MEDIA_QUERY.matches ? "dark" : "light";
    }

    return themePreference;
}

function applyResolvedThemeToDocument(themePreference) {
    const resolvedTheme = getResolvedTheme(themePreference);
    const root = document.documentElement;

    root.dataset.theme = resolvedTheme;
    root.dataset.themePreference = themePreference;
    root.style.colorScheme = resolvedTheme;

    return resolvedTheme;
}

function updateAppearanceForSystemPreference() {
    const currentPreference = normalizeTheme(localStorage.getItem(APPEARANCE_THEME_KEY) || DEFAULT_THEME);

    if (currentPreference !== "system") {
        return;
    }

    applyResolvedThemeToDocument(currentPreference);
}

function ensureSystemThemeListener() {
    if (appearanceSystemListenerAttached) {
        return;
    }

    APPEARANCE_THEME_MEDIA_QUERY.addEventListener("change", updateAppearanceForSystemPreference);
    appearanceSystemListenerAttached = true;
}

function applyTheme(theme, shouldPersist = true) {
    const normalizedTheme = normalizeTheme(theme);
    applyResolvedThemeToDocument(normalizedTheme);
    ensureSystemThemeListener();

    if (shouldPersist) {
        localStorage.setItem(APPEARANCE_THEME_KEY, normalizedTheme);
    }
}

function applyAccentColor(accent, shouldPersist = true) {
    const normalizedAccent = normalizeAccent(accent);
    const preset = ACCENT_PRESETS[normalizedAccent];
    const root = document.documentElement;

    root.dataset.accent = normalizedAccent;
    root.style.setProperty("--accent-color", preset.accentColor);
    root.style.setProperty("--accent-hover", preset.accentHover);
    root.style.setProperty("--accent-soft", preset.accentSoft);
    root.style.setProperty("--accent-border", preset.accentBorder);
    root.style.setProperty("--accent-glow", preset.accentGlow);
    root.style.setProperty("--accent-ring", preset.accentRing);
    root.style.setProperty("--accent-gradient-mid", preset.accentGradientMid);
    root.style.setProperty("--accent-gradient-end", preset.accentGradientEnd);
    root.style.setProperty("--accent-button-glow", preset.accentButtonGlow);
    root.style.setProperty("--color-primary", preset.accentColor);
    root.style.setProperty("--color-primary-hover", preset.accentHover);
    root.style.setProperty("--color-border-strong", preset.accentBorder);
    root.style.setProperty("--color-glow-cyan", preset.accentGlow);
    root.style.setProperty("--color-secondary", preset.secondaryColor);
    root.style.setProperty("--color-glow-purple", preset.secondaryGlow);

    if (shouldPersist) {
        localStorage.setItem(APPEARANCE_ACCENT_COLOR_KEY, normalizedAccent);
    }
}

function loadAppearanceSettings() {
    const settings = getAppearanceSettings();
    applyTheme(settings.theme, false);
    applyAccentColor(settings.accent, false);
    return settings;
}

function setToken(token) {
    localStorage.setItem("token", token);
}

function clearToken() {
    localStorage.removeItem("token");
}

function isLoggedIn() {
    return !!getToken();
}

function requireLogin() {
    if (!isLoggedIn()) {
        window.location.href = "login.html";
        return false;
    }
    return true;
}

async function logout() {
    try {
        await logoutUser();
    } catch (error) {
        // 通信失敗時でもローカルトークンは確実に削除する
    }

    clearToken();
    window.location.href = "login.html";
}

function setMessage(elementId, text, type = "error") {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerText = text;

        if (element.classList) {
            element.classList.remove("is-success");

            if (text && type === "success") {
                element.classList.add("is-success");
            }
        }
    }
}

function setButtonLoading(button, isLoading, loadingText) {
    if (!button) {
        return;
    }

    if (!button.dataset.originalText) {
        button.dataset.originalText = button.innerText;
    }

    button.disabled = isLoading;
    button.dataset.loading = isLoading ? "true" : "false";
    button.innerText = isLoading ? (loadingText || button.dataset.originalText) : button.dataset.originalText;
}

function initializePasswordToggles() {
    const toggles = document.querySelectorAll("[data-password-toggle]");

    toggles.forEach((toggleButton) => {
        toggleButton.addEventListener("click", () => {
            const targetId = toggleButton.getAttribute("data-password-toggle");
            const input = document.getElementById(targetId);

            if (!input) {
                return;
            }

            const isPassword = input.type === "password";
            input.type = isPassword ? "text" : "password";
            toggleButton.setAttribute("aria-pressed", String(isPassword));
            toggleButton.innerText = isPassword ? "HIDE" : "SHOW";
        });
    });
}

window.applyTheme = applyTheme;
window.applyAccentColor = applyAccentColor;
window.loadAppearanceSettings = loadAppearanceSettings;
window.getAppearanceSettings = getAppearanceSettings;

document.addEventListener("DOMContentLoaded", () => {
    loadAppearanceSettings();
    initializePasswordToggles();
});