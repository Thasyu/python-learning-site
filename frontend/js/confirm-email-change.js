function getTokenFromQuery() {
    const params = new URLSearchParams(window.location.search);
    return params.get("token") || "";
}

async function confirmEmailChangeByToken() {
    const confirmButton = document.getElementById("confirmEmailChangeButton");
    const token = getTokenFromQuery();

    setMessage("message", "");

    if (!token || /\s/.test(token)) {
        setMessage("message", "無効なリンクです。settings画面から再送信してください。");
        return;
    }

    setButtonLoading(confirmButton, true, "検証中...");

    try {
        const result = await confirmEmailChange(token);

        if (result.ok) {
            clearToken();
            setMessage("message", result.data.message || "メールアドレスを変更しました。再ログインしてください。", "success");
            return;
        }

        setMessage("message", result.data.message || "メールアドレス変更に失敗しました。リンクの有効期限を確認してください。");
    } catch (error) {
        setMessage("message", "通信エラーが発生しました。");
    } finally {
        setButtonLoading(confirmButton, false);
    }
}

document.getElementById("confirmEmailChangeButton").addEventListener("click", confirmEmailChangeByToken);
document.getElementById("goLoginButton").addEventListener("click", () => {
    window.location.href = "login.html";
});
document.getElementById("goHomeButton").addEventListener("click", () => {
    window.location.href = "index.html";
});
