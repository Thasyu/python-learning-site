function validateIdentifier(identifier) {
    if (!identifier || !identifier.trim()) {
        return "ユーザー名またはメールアドレスを入力してください。";
    }

    if (/\s/.test(identifier)) {
        return "空白は使えません。";
    }

    return null;
}

async function sendResetMail() {
    const sendButton = document.getElementById("sendResetMailButton");
    const identifier = document.getElementById("identifier").value.trim();

    setMessage("message", "");

    const identifierError = validateIdentifier(identifier);
    if (identifierError) {
        setMessage("message", identifierError);
        return;
    }

    setButtonLoading(sendButton, true, "Sending link...");

    try {
        const result = await requestPasswordReset(identifier);

        if (result.ok) {
            setMessage("message", "該当するアカウントが存在する場合、再設定メールを送信しました。", "success");
            return;
        }

        setMessage("message", "再設定メールの送信に失敗しました。");
    } catch (error) {
        setMessage("message", "通信エラーが発生しました。");
    } finally {
        setButtonLoading(sendButton, false);
    }
}

document.getElementById("sendResetMailButton").addEventListener("click", sendResetMail);
document.getElementById("goLoginButton").addEventListener("click", () => {
    window.location.href = "login.html";
});
