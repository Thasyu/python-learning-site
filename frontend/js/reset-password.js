function validatePassword(password) {
    if (password.length < 4 || password.length > 32) {
        return "パスワードは4〜32文字で入力してください。";
    }

    if (/\s/.test(password)) {
        return "パスワードに空白は使えません。";
    }

    const hasLetter = /[A-Za-z]/.test(password);
    const hasDigit = /\d/.test(password);

    if (!hasLetter || !hasDigit) {
        return "パスワードには英字と数字を両方含めてください。";
    }

    return null;
}

function getTokenFromQuery() {
    const params = new URLSearchParams(window.location.search);
    return params.get("token") || "";
}

async function resetPassword() {
    const resetButton = document.getElementById("resetPasswordButton");
    const token = getTokenFromQuery();
    const newPassword = document.getElementById("newPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    setMessage("message", "");

    if (!token || /\s/.test(token)) {
        setMessage("message", "無効なリンクです。再度メール送信を行ってください。");
        return;
    }

    const passwordError = validatePassword(newPassword);
    if (passwordError) {
        setMessage("message", passwordError);
        return;
    }

    if (newPassword !== confirmPassword) {
        setMessage("message", "確認用パスワードが一致しません。");
        return;
    }

    setButtonLoading(resetButton, true, "Updating password...");

    try {
        const result = await confirmPasswordReset(token, newPassword);

        if (result.ok) {
            setMessage("message", "パスワードを再設定しました。ログインしてください。", "success");
            return;
        }

        setMessage("message", result.data.message || "パスワード再設定に失敗しました。");
    } catch (error) {
        setMessage("message", "通信エラーが発生しました。");
    } finally {
        setButtonLoading(resetButton, false);
    }
}

document.getElementById("resetPasswordButton").addEventListener("click", resetPassword);
document.getElementById("goLoginButton").addEventListener("click", () => {
    window.location.href = "login.html";
});
