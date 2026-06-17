const USERNAME_PATTERN = /^[A-Za-z0-9_]+$/;

function validateUsername(username) {
	if (username.length < 1 || username.length > 20) {
		return "ログインIDは1〜20文字で入力してください。";
	}

	if (/\s/.test(username)) {
		return "ログインIDに空白は使えません。";
	}

	if (!USERNAME_PATTERN.test(username)) {
		return "ログインIDは英数字と_のみ使用できます。";
	}

	return null;
}

function validateDisplayName(displayName) {
	if (!displayName) {
		return null;
	}

	if (!displayName.trim()) {
		return "ニックネームは空白のみでは登録できません。";
	}

	if (displayName !== displayName.trim()) {
		return "ニックネームの前後に空白は使えません。";
	}

	if (displayName.length > 30) {
		return "ニックネームは30文字以内で入力してください。";
	}

	if (/[\x00-\x1f\x7f]/.test(displayName) || displayName.includes("<") || displayName.includes(">")) {
		return "ニックネームに使用できない文字が含まれています。";
	}

	return null;
}

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

function validateEmail(email) {
	if (!email || !email.trim()) {
		return "メールアドレスを入力してください。";
	}

	if (email !== email.trim() || /\s/.test(email)) {
		return "メールアドレスに空白は使えません。";
	}

	if (!email.includes("@")) {
		return "メールアドレスの形式が正しくありません。";
	}

	return null;
}

async function register() {
	const registerButton = document.getElementById("registerButton");
	const username = document.getElementById("username").value;
	const displayName = document.getElementById("displayName").value;
	const email = document.getElementById("email").value;
	const password = document.getElementById("password").value;
	const confirmPassword = document.getElementById("confirmPassword").value;

	setMessage("message", "");

	const usernameError = validateUsername(username);
	if (usernameError) {
		setMessage("message", usernameError);
		return;
	}

	const displayNameError = validateDisplayName(displayName);
	if (displayNameError) {
		setMessage("message", displayNameError);
		return;
	}

	const passwordError = validatePassword(password);
	if (passwordError) {
		setMessage("message", passwordError);
		return;
	}

	if (!confirmPassword) {
		setMessage("message", "確認用パスワードを入力してください。");
		return;
	}

	if (password !== confirmPassword) {
		setMessage("message", "パスワードが一致しません。");
		return;
	}

	const emailError = validateEmail(email);
	if (emailError) {
		setMessage("message", emailError);
		return;
	}

	setButtonLoading(registerButton, true, "Creating account...");

	try {
		const result = await registerUser(username, email, password, displayName.trim());

		if (result.ok) {
			setMessage("message", "登録に成功しました", "success");
		} else {
			setMessage("message", result.data.message);
		}
	} catch (error) {
		setMessage("message", "通信エラーが発生しました。");
	} finally {
		setButtonLoading(registerButton, false);
	}
}

document.getElementById("registerButton").addEventListener("click", register);
document.getElementById("goLoginButton").addEventListener("click", () => {
	window.location.href = "login.html";
});
document.getElementById("homeButton").addEventListener("click", () => {
	window.location.href = "index.html";
});
