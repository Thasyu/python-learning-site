async function login() {
    const loginButton = document.getElementById("loginButton");
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    setMessage("message", "");
    setButtonLoading(loginButton, true, "Signing in...");

    try {
        const result = await loginUser(username, password);

        if (result.ok) {
            if (!result.data.token) {
                setMessage("message", "トークン取得に失敗しました。");
                return;
            }

            setToken(result.data.token);
            window.location.href = "dashboard.html";
        } else {
            setMessage("message", result.data.message);
        }
    } catch (error) {
        setMessage("message", "通信エラーが発生しました。");
    } finally {
        setButtonLoading(loginButton, false);
    }
}

const authExpiredMessage = sessionStorage.getItem("authExpiredMessage");
if (authExpiredMessage) {
    setMessage("message", authExpiredMessage);
    sessionStorage.removeItem("authExpiredMessage");
}

document.getElementById("loginButton").addEventListener("click", login);
document.getElementById("goRegisterButton").addEventListener("click", () => {
    window.location.href = "register.html";
});
document.getElementById("homeButton").addEventListener("click", () => {
    window.location.href = "index.html";
});