const SECTION_IDS = ["profile", "security", "appearance", "danger"];
const DEFAULT_PROFILE_AVATAR = "../image/main_bg_transparent.png";
const MAX_BIO_LENGTH = 160;
const MAX_AVATAR_FILE_SIZE = 2 * 1024 * 1024;
const ALLOWED_AVATAR_MIME_TYPES = new Set(["image/png", "image/jpeg", "image/webp"]);
const APPEARANCE_THEME_OPTIONS = new Set(["dark", "light", "system"]);
const APPEARANCE_ACCENT_OPTIONS = new Set(["cyan", "blue", "purple", "green", "pink"]);
const profileEditState = {
	isEditing: false,
	originalProfile: null,
	draftAvatarFile: null,
	draftAvatarPreviewUrl: null
};
const dangerDeleteState = {
	currentPassword: "",
	confirmation: ""
};

function getDeleteAccountModalInputs() {
	return {
		modalOverlay: document.getElementById("deleteAccountModal"),
		cancelButton: document.getElementById("cancelDeleteAccountModalButton"),
		confirmButton: document.getElementById("confirmDeleteAccountModalButton")
	};
}

function setSettingsMessage(text, type = "error") {
	setMessage("settingsMessage", text, type);
}

function setProfileMessage(text, type = "error") {
	setMessage("profileMessage", text, type);
}

function clearProfileMessage() {
	setProfileMessage("");
}

function getSectionFromHash() {
	const raw = window.location.hash.replace("#", "").trim();

	if (SECTION_IDS.includes(raw)) {
		return raw;
	}

	return "profile";
}

function switchSection(sectionId, shouldSyncHash = true) {
	const targetSection = SECTION_IDS.includes(sectionId) ? sectionId : "profile";

	document.querySelectorAll(".settings-nav-item").forEach((item) => {
		const isActive = item.dataset.section === targetSection;
		item.classList.toggle("is-active", isActive);
		item.setAttribute("aria-current", isActive ? "page" : "false");
	});

	document.querySelectorAll(".settings-section").forEach((section) => {
		const isActive = section.dataset.section === targetSection;
		section.classList.toggle("is-active", isActive);
	});

	if (shouldSyncHash) {
		window.location.hash = targetSection;
	}
}

function formatJoinedDate(value) {
	if (!value) {
		return "2026/01/01";
	}

	const date = new Date(value);

	if (Number.isNaN(date.getTime())) {
		return value;
	}

	return date.toLocaleDateString("ja-JP");
}

function resolveAvatarUrl(avatarUrl) {
	if (!avatarUrl) {
		return DEFAULT_PROFILE_AVATAR;
	}

	if (/^https?:\/\//i.test(avatarUrl)) {
		return avatarUrl;
	}

	if (avatarUrl.startsWith("/")) {
		return `${BASE_URL}${avatarUrl}`;
	}

	return avatarUrl;
}

function normalizeProfileValue(value) {
	return typeof value === "string" ? value.trim() : "";
}

function makeProfileSnapshot(profile) {
	return {
		display_name: normalizeProfileValue(profile.display_name || profile.username),
		bio: normalizeProfileValue(profile.bio || ""),
		avatar_url: profile.avatar_url || "",
		username: profile.username || "",
		created_at: profile.created_at || profile.registered_at || "",
		email: profile.email || ""
	};
}

function getProfileInputs() {
	return {
		avatarImage: document.getElementById("profileAvatarImage"),
		avatarFileInput: document.getElementById("avatarFileInput"),
		avatarButton: document.getElementById("changeAvatarButton"),
		displayNameInput: document.getElementById("profileDisplayName"),
		bioInput: document.getElementById("profileBio"),
		bioCounter: document.getElementById("profileBioCounter"),
		usernameInput: document.getElementById("profileUsername"),
		registeredAtInput: document.getElementById("profileRegisteredAt")
	};
}

function setProfileEditable(isEditable) {
	const profileCard = document.getElementById("profileCard");
	const { displayNameInput, bioInput, avatarButton } = getProfileInputs();

	profileCard.classList.toggle("profile-edit-mode", isEditable);
	profileCard.classList.toggle("profile-readonly-mode", !isEditable);

	displayNameInput.readOnly = !isEditable;
	bioInput.readOnly = !isEditable;
	avatarButton.disabled = !isEditable;
}

function setEditButtonLabel() {
	const editProfileButton = document.getElementById("editProfileButton");
	editProfileButton.innerText = profileEditState.isEditing ? "編集をキャンセル" : "編集モード";
}

function hasProfileChanges() {
	if (!profileEditState.originalProfile) {
		return false;
	}

	const { displayNameInput, bioInput } = getProfileInputs();
	const displayNameChanged = normalizeProfileValue(displayNameInput.value) !== normalizeProfileValue(profileEditState.originalProfile.display_name);
	const bioChanged = normalizeProfileValue(bioInput.value) !== normalizeProfileValue(profileEditState.originalProfile.bio);
	const avatarChanged = profileEditState.draftAvatarFile !== null;

	return displayNameChanged || bioChanged || avatarChanged;
}

function updateProfileSaveVisibility() {
	const saveProfileButton = document.getElementById("saveProfileButton");
	const shouldShow = profileEditState.isEditing && hasProfileChanges();
	saveProfileButton.classList.toggle("is-hidden", !shouldShow);
}

function releaseDraftAvatarPreview() {
	if (profileEditState.draftAvatarPreviewUrl) {
		URL.revokeObjectURL(profileEditState.draftAvatarPreviewUrl);
		profileEditState.draftAvatarPreviewUrl = null;
	}
}

function setDraftAvatarPreview(file) {
	const { avatarImage } = getProfileInputs();
	releaseDraftAvatarPreview();
	profileEditState.draftAvatarPreviewUrl = URL.createObjectURL(file);
	avatarImage.src = profileEditState.draftAvatarPreviewUrl;
	avatarImage.classList.remove("is-default-avatar");
}

function syncAvatarPresentation(avatarSrc) {
	const { avatarImage } = getProfileInputs();
	const isDefaultAvatar = typeof avatarSrc === "string"
		&& /main_bg_transparent\.png(?:\?|$)/i.test(avatarSrc);

	avatarImage.classList.toggle("is-default-avatar", isDefaultAvatar);
}

function restoreProfileOriginalValues() {
	if (!profileEditState.originalProfile) {
		return;
	}

	const {
		avatarImage,
		avatarFileInput,
		displayNameInput,
		bioInput,
		usernameInput,
		registeredAtInput
	} = getProfileInputs();

	displayNameInput.value = profileEditState.originalProfile.display_name;
	bioInput.value = profileEditState.originalProfile.bio;
	usernameInput.value = profileEditState.originalProfile.username;
	registeredAtInput.value = formatJoinedDate(profileEditState.originalProfile.created_at);
	const resolvedAvatarUrl = resolveAvatarUrl(profileEditState.originalProfile.avatar_url);
	avatarImage.src = resolvedAvatarUrl;
	syncAvatarPresentation(resolvedAvatarUrl);
	avatarFileInput.value = "";

	releaseDraftAvatarPreview();
	profileEditState.draftAvatarFile = null;
	updateBioCounter();
	updateProfileSaveVisibility();
}

function enterProfileEditMode() {
	if (!profileEditState.originalProfile) {
		return;
	}

	profileEditState.isEditing = true;
	setProfileEditable(true);
	setEditButtonLabel();
	updateProfileSaveVisibility();
	setProfileMessage("ニックネーム・自己紹介・画像を編集できます。", "success");
}

function exitProfileEditMode() {
	profileEditState.isEditing = false;
	releaseDraftAvatarPreview();
	profileEditState.draftAvatarFile = null;
	setProfileEditable(false);
	setEditButtonLabel();
	updateProfileSaveVisibility();
}

function cancelProfileEditMode() {
	restoreProfileOriginalValues();
	exitProfileEditMode();
	clearProfileMessage();
}

function applyProfileSnapshot(snapshot) {
	profileEditState.originalProfile = {
		display_name: normalizeProfileValue(snapshot.display_name),
		bio: normalizeProfileValue(snapshot.bio),
		avatar_url: snapshot.avatar_url || "",
		username: snapshot.username || "",
		created_at: snapshot.created_at || "",
		email: snapshot.email || ""
	};

	restoreProfileOriginalValues();
	exitProfileEditMode();
}

function getSecurityInputs() {
	return {
		currentEmailInput: document.getElementById("profileCurrentEmail"),
		newEmailInput: document.getElementById("newEmailInput"),
		currentPasswordInput: document.getElementById("currentPasswordInput"),
		requestButton: document.getElementById("requestEmailChangeButton")
	};
}

function getPasswordInputs() {
	return {
		currentPasswordInput: document.getElementById("currentSecurityPassword"),
		newPasswordInput: document.getElementById("newSecurityPassword"),
		confirmPasswordInput: document.getElementById("confirmSecurityPassword"),
		changeButton: document.getElementById("changePasswordButton"),
		strengthText: document.getElementById("passwordStrengthText")
	};
}

function getAppearanceInputs() {
	return {
		themeInputs: document.querySelectorAll('input[name="appearanceTheme"]'),
		accentSwatches: document.querySelectorAll(".accent-swatch")
	};
}

function getDangerInputs() {
	return {
		logoutButton: document.getElementById("dangerLogoutButton"),
		currentPasswordInput: document.getElementById("dangerCurrentPassword"),
		confirmationInput: document.getElementById("dangerDeleteConfirmation"),
		deleteButton: document.getElementById("dangerDeleteAccountButton")
	};
}

function setDangerMessage(text, type = "error") {
	setMessage("dangerMessage", text, type);
}

function validateDeleteAccountInputs(currentPassword, confirmation) {
	if (!currentPassword) {
		return "現在のパスワードを入力してください。";
	}

	if (!confirmation) {
		return "確認文字列 DELETE を入力してください。";
	}

	if (confirmation !== "DELETE") {
		return "確認文字列は DELETE と完全一致で入力してください。";
	}

	return null;
}

function updateDangerDeleteButtonState() {
	const { currentPasswordInput, confirmationInput, deleteButton } = getDangerInputs();
	const canDelete = Boolean(currentPasswordInput.value) && confirmationInput.value === "DELETE";
	deleteButton.disabled = !canDelete;
}

async function handleDeleteAccount() {
	const { currentPasswordInput, confirmationInput } = getDangerInputs();
	const currentPassword = currentPasswordInput.value;
	const confirmation = confirmationInput.value;

	setDangerMessage("");

	const validationError = validateDeleteAccountInputs(currentPassword, confirmation);
	if (validationError) {
		setDangerMessage(validationError);
		return;
	}

	dangerDeleteState.currentPassword = currentPassword;
	dangerDeleteState.confirmation = confirmation;
	openDeleteAccountModal();
}

function openDeleteAccountModal() {
	const { modalOverlay } = getDeleteAccountModalInputs();

	if (!modalOverlay) {
		return;
	}

	modalOverlay.classList.add("is-open");
	modalOverlay.setAttribute("aria-hidden", "false");
	document.body.classList.add("is-modal-open");
}

function closeDeleteAccountModal() {
	const { modalOverlay, confirmButton } = getDeleteAccountModalInputs();

	if (!modalOverlay) {
		return;
	}

	modalOverlay.classList.remove("is-open");
	modalOverlay.setAttribute("aria-hidden", "true");
	document.body.classList.remove("is-modal-open");
	setButtonLoading(confirmButton, false);

	dangerDeleteState.currentPassword = "";
	dangerDeleteState.confirmation = "";
}

async function confirmDeleteAccountFromModal() {
	const { deleteButton } = getDangerInputs();
	const { confirmButton } = getDeleteAccountModalInputs();

	if (!dangerDeleteState.currentPassword || dangerDeleteState.confirmation !== "DELETE") {
		setDangerMessage("削除条件の入力値が不足しています。もう一度やり直してください。", "error");
		closeDeleteAccountModal();
		updateDangerDeleteButtonState();
		return;
	}

	setButtonLoading(confirmButton, true, "削除中...");
	setButtonLoading(deleteButton, true, "削除中...");


	try {
		const result = await deleteAccount(dangerDeleteState.currentPassword, dangerDeleteState.confirmation);

		if (result.ok) {
			closeDeleteAccountModal();
			setDangerMessage(result.data.message || "アカウントを削除しました。", "success");
			clearToken();
			sessionStorage.setItem("authExpiredMessage", result.data.message || "アカウントを削除しました。");
			setTimeout(() => {
				window.location.replace("login.html");
			}, 900);
			return;
		}

		setDangerMessage(result.data?.message || "アカウント削除に失敗しました。");
	} catch (error) {
		setDangerMessage("通信エラーが発生しました。");
	} finally {
		setButtonLoading(confirmButton, false);
		setButtonLoading(deleteButton, false);
		updateDangerDeleteButtonState();
	}
}

async function handleLogoutFromDangerZone() {
	const { logoutButton } = getDangerInputs();

	setButtonLoading(logoutButton, true, "ログアウト中...");
	await logout();
}

function updateAccentSwatchSelection(accent) {
	const { accentSwatches } = getAppearanceInputs();

	accentSwatches.forEach((swatch) => {
		const isSelected = swatch.dataset.accent === accent;
		swatch.classList.toggle("is-selected", isSelected);
		swatch.setAttribute("aria-pressed", String(isSelected));
	});
}

function syncAppearanceControls() {
	const defaultSettings = { theme: "dark", accent: "cyan" };
	const settings = typeof window.getAppearanceSettings === "function" ? window.getAppearanceSettings() : defaultSettings;
	const normalizedTheme = APPEARANCE_THEME_OPTIONS.has(settings.theme) ? settings.theme : "dark";
	const normalizedAccent = APPEARANCE_ACCENT_OPTIONS.has(settings.accent) ? settings.accent : "cyan";
	const { themeInputs } = getAppearanceInputs();

	themeInputs.forEach((input) => {
		input.checked = input.value === normalizedTheme;
	});

	updateAccentSwatchSelection(normalizedAccent);
}

function applyThemeSetting(theme) {
	if (!APPEARANCE_THEME_OPTIONS.has(theme)) {
		return;
	}

	if (typeof window.applyTheme === "function") {
		window.applyTheme(theme, true);
	}
}

function applyAccentSetting(accent) {
	if (!APPEARANCE_ACCENT_OPTIONS.has(accent)) {
		return;
	}

	if (typeof window.applyAccentColor === "function") {
		window.applyAccentColor(accent, true);
	}

	updateAccentSwatchSelection(accent);
}

function validatePasswordCandidate(password, requiredMessage) {
	if (!password) {
		return requiredMessage;
	}

	if (password !== password.trim()) {
		return "パスワードの前後に空白は使えません。";
	}

	if (password.length < 4 || password.length > 32) {
		return "パスワードは4〜32文字で入力してください。";
	}

	if (/\s/.test(password)) {
		return "パスワードに空白は使えません。";
	}

	if (!/[A-Za-z]/.test(password) || !/\d/.test(password)) {
		return "パスワードには英字と数字を両方含めてください。";
	}

	return null;
}

function validateBioText(bio) {
	if (bio.length > MAX_BIO_LENGTH) {
		return `自己紹介は${MAX_BIO_LENGTH}文字以内で入力してください。`;
	}

	if (/[\x00-\x1f\x7f]/.test(bio)) {
		return "自己紹介に制御文字は使えません。";
	}

	if (bio.includes("<") || bio.includes(">")) {
		return "自己紹介に使用できない文字が含まれています。";
	}

	return null;
}

function updateBioCounter() {
	const { bioInput, bioCounter } = getProfileInputs();

	if (!bioInput || !bioCounter) {
		return;
	}

	const length = bioInput.value.length;
	bioCounter.innerText = `${length} / ${MAX_BIO_LENGTH}`;
	bioCounter.classList.toggle("is-limit", length > MAX_BIO_LENGTH * 0.9);
}

function renderPasswordStrength(password) {
	const { strengthText } = getPasswordInputs();

	if (!strengthText) {
		return;
	}

	if (!password) {
		strengthText.innerText = "8文字以上、英字と数字を組み合わせると安全性が上がります。";
		return;
	}

	const hasLetters = /[A-Za-z]/.test(password);
	const hasNumbers = /\d/.test(password);
	const hasSymbols = /[^A-Za-z0-9]/.test(password);

	if (password.length >= 12 && hasLetters && hasNumbers && hasSymbols) {
		strengthText.innerText = "強いパスワードです。";
		return;
	}

	if (password.length >= 8 && hasLetters && hasNumbers) {
		strengthText.innerText = "十分に強い候補です。記号を加えるとさらに安全です。";
		return;
	}

	strengthText.innerText = "英字と数字を両方含めると安全性が上がります。";
}

function renderProfile(profile) {
	applyProfileSnapshot(makeProfileSnapshot(profile));
}

function loadSecurity(profile) {
	const { currentEmailInput } = getSecurityInputs();
	currentEmailInput.value = profile.email || "";
}

async function loadProfile() {
	const userStatus = document.getElementById("settingsUserStatus");

	userStatus.innerText = "プロフィールを読み込み中...";
	const result = await fetchMe();

	if (result.ok && result.data) {
		renderProfile(result.data);
		loadSecurity(result.data);
		userStatus.innerText = `${result.data.display_name || result.data.username || "ユーザー"} としてログイン中`;
		setSettingsMessage("", "success");
		setProfileMessage("", "success");
		return;
	}

	userStatus.innerText = "プロフィール取得に失敗しました";
	setSettingsMessage(result.data?.message || "プロフィール取得に失敗しました。", "error");
}

function handleAvatarSelection(file) {
	const { avatarFileInput } = getProfileInputs();

	if (!profileEditState.isEditing) {
		avatarFileInput.value = "";
		return;
	}

	if (!file) {
		return;
	}

	if (!ALLOWED_AVATAR_MIME_TYPES.has(file.type)) {
		setProfileMessage("対応していない画像形式です。png/jpg/jpeg/webp を使用してください。", "error");
		avatarFileInput.value = "";
		return;
	}

	if (file.size <= 0) {
		setProfileMessage("空のファイルはアップロードできません。", "error");
		avatarFileInput.value = "";
		return;
	}

	if (file.size > MAX_AVATAR_FILE_SIZE) {
		setProfileMessage("画像サイズが大きすぎます。2MB以下にしてください。", "error");
		avatarFileInput.value = "";
		return;
	}

	profileEditState.draftAvatarFile = file;
	setDraftAvatarPreview(file);
	setProfileMessage("新しい画像を選択しました。保存すると反映されます。", "success");
	updateProfileSaveVisibility();
}

async function saveProfileChanges() {
	if (!profileEditState.originalProfile || !profileEditState.isEditing) {
		return;
	}

	const { displayNameInput, bioInput, usernameInput } = getProfileInputs();
	const saveButton = document.getElementById("saveProfileButton");
	const userStatus = document.getElementById("settingsUserStatus");

	const displayName = normalizeProfileValue(displayNameInput.value);
	const bio = normalizeProfileValue(bioInput.value);
	const displayNameChanged = displayName !== normalizeProfileValue(profileEditState.originalProfile.display_name);
	const bioChanged = bio !== normalizeProfileValue(profileEditState.originalProfile.bio);
	const avatarChanged = profileEditState.draftAvatarFile !== null;

	if (!displayNameChanged && !bioChanged && !avatarChanged) {
		exitProfileEditMode();
		clearProfileMessage();
		return;
	}

	if (!displayName) {
		setProfileMessage("ニックネームを入力してください。", "error");
		return;
	}

	const bioError = validateBioText(bio);
	if (bioError) {
		setProfileMessage(bioError, "error");
		return;
	}

	setButtonLoading(saveButton, true, "保存中...");

	try {
		if (displayNameChanged) {
			const displayNameResult = await updateDisplayName(displayName);
			if (!displayNameResult.ok) {
				setProfileMessage(displayNameResult.data.message || "ニックネームの保存に失敗しました。", "error");
				updateProfileSaveVisibility();
				return;
			}

			displayNameInput.value = normalizeProfileValue(displayNameResult.data.display_name || displayName);
			profileEditState.originalProfile.display_name = displayNameInput.value;
		}

		if (bioChanged) {
			const bioResult = await updateBio(bio);
			if (!bioResult.ok) {
				setProfileMessage(bioResult.data.message || "自己紹介の保存に失敗しました。", "error");
				updateProfileSaveVisibility();
				return;
			}

			bioInput.value = normalizeProfileValue(bioResult.data.bio || "");
			profileEditState.originalProfile.bio = bioInput.value;
		}

		if (avatarChanged) {
			const avatarResult = await uploadAvatar(profileEditState.draftAvatarFile);
			if (!avatarResult.ok) {
				setProfileMessage(avatarResult.data.message || "画像アップロードに失敗しました。", "error");
				updateProfileSaveVisibility();
				return;
			}

			profileEditState.originalProfile.avatar_url = avatarResult.data.avatar_url || profileEditState.originalProfile.avatar_url;
			const { avatarImage, avatarFileInput } = getProfileInputs();
			const resolvedAvatarUrl = resolveAvatarUrl(profileEditState.originalProfile.avatar_url);
			avatarImage.src = `${resolvedAvatarUrl}?v=${Date.now()}`;
			syncAvatarPresentation(resolvedAvatarUrl);
			avatarFileInput.value = "";
		}

		updateBioCounter();

		userStatus.innerText = `${displayNameInput.value || usernameInput.value || "ユーザー"} としてログイン中`;
		setProfileMessage("Identity情報を保存しました。", "success");
		setSettingsMessage("", "success");
		exitProfileEditMode();
	} catch (error) {
		setProfileMessage("通信エラーが発生しました。", "error");
	} finally {
		setButtonLoading(saveButton, false);
	}
}

async function handlePasswordChange() {
	const { currentPasswordInput, newPasswordInput, confirmPasswordInput, changeButton } = getPasswordInputs();
	const currentPassword = currentPasswordInput.value;
	const newPassword = newPasswordInput.value;
	const confirmPassword = confirmPasswordInput.value;

	setMessage("passwordChangeMessage", "");

	const currentPasswordError = validatePasswordCandidate(currentPassword, "現在のパスワードを入力してください。");
	if (currentPasswordError) {
		setMessage("passwordChangeMessage", currentPasswordError);
		return;
	}

	const newPasswordError = validatePasswordCandidate(newPassword, "新しいパスワードを入力してください。");
	if (newPasswordError) {
		setMessage("passwordChangeMessage", newPasswordError);
		return;
	}

	if (!confirmPassword) {
		setMessage("passwordChangeMessage", "確認用パスワードを入力してください。");
		return;
	}

	if (confirmPassword !== confirmPassword.trim()) {
		setMessage("passwordChangeMessage", "確認用パスワードの前後に空白は使えません。");
		return;
	}

	if (newPassword !== confirmPassword) {
		setMessage("passwordChangeMessage", "新しいパスワードが一致しません。");
		return;
	}

	if (currentPassword === newPassword) {
		setMessage("passwordChangeMessage", "新しいパスワードは現在のパスワードと同じにできません。");
		return;
	}

	setButtonLoading(changeButton, true, "変更中...");

	try {
		const result = await changePassword(currentPassword, newPassword, confirmPassword);

		if (result.ok && result.data) {
			setMessage("passwordChangeMessage", result.data.message || "パスワードを変更しました。ログイン状態は維持されています。", "success");
			currentPasswordInput.value = "";
			newPasswordInput.value = "";
			confirmPasswordInput.value = "";
			renderPasswordStrength("");
			return;
		}

		setMessage("passwordChangeMessage", result.data?.message || "パスワードの変更に失敗しました。");
	} catch (error) {
		setMessage("passwordChangeMessage", "通信エラーが発生しました。");
	} finally {
		setButtonLoading(changeButton, false);
	}
}

async function sendEmailChangeRequest() {
	const { requestButton, newEmailInput, currentPasswordInput } = getSecurityInputs();
	const newEmail = newEmailInput.value.trim();
	const currentPassword = currentPasswordInput.value;

	if (!newEmail) {
		setSettingsMessage("新しいメールアドレスを入力してください。", "error");
		return;
	}

	if (!currentPassword) {
		setSettingsMessage("現在のパスワードを入力してください。", "error");
		return;
	}

	setButtonLoading(requestButton, true, "送信中...");

	try {
		const result = await requestEmailChange(newEmail, currentPassword);

		if (result.ok) {
			setSettingsMessage(result.data.message || "確認メールを送信しました。", "success");
			currentPasswordInput.value = "";
			return;
		}

		setSettingsMessage(result.data.message || "確認メールの送信に失敗しました。", "error");
	} catch (error) {
		setSettingsMessage("通信エラーが発生しました。", "error");
	} finally {
		setButtonLoading(requestButton, false);
	}
}

function toggleSidebar() {
	const sidebar = document.getElementById("settingsSidebar");
	const toggleButton = document.getElementById("sidebarToggle");
	const willOpen = !sidebar.classList.contains("is-open");

	sidebar.classList.toggle("is-open", willOpen);
	toggleButton.setAttribute("aria-expanded", String(willOpen));
	toggleButton.innerText = willOpen ? "セクションを隠す" : "セクション表示";
}

function initializeSettingsNavigation() {
	document.querySelectorAll(".settings-nav-item").forEach((item) => {
		item.addEventListener("click", () => {
			switchSection(item.dataset.section);
		});
	});

	window.addEventListener("hashchange", () => {
		switchSection(getSectionFromHash(), false);
	});

	switchSection(getSectionFromHash(), false);
}

function bindTopbarActions() {
	document.getElementById("homeButton").addEventListener("click", () => {
		window.location.href = "index.html";
	});

	document.getElementById("dashboardButton").addEventListener("click", () => {
		window.location.href = "dashboard.html";
	});
}

function bindProfileActions() {
	const { avatarImage, avatarFileInput, avatarButton, displayNameInput, bioInput } = getProfileInputs();
	const editProfileButton = document.getElementById("editProfileButton");
	const saveProfileButton = document.getElementById("saveProfileButton");

	avatarImage.addEventListener("error", () => {
		avatarImage.src = DEFAULT_PROFILE_AVATAR;
		syncAvatarPresentation(DEFAULT_PROFILE_AVATAR);
	});

	syncAvatarPresentation(avatarImage.src);

	avatarButton.addEventListener("click", () => {
		if (!profileEditState.isEditing) {
			return;
		}
		avatarFileInput.click();
	});

	avatarFileInput.addEventListener("change", () => {
		handleAvatarSelection(avatarFileInput.files[0]);
	});

	displayNameInput.addEventListener("input", () => {
		updateProfileSaveVisibility();
	});

	bioInput.addEventListener("input", () => {
		updateBioCounter();
		updateProfileSaveVisibility();
	});

	editProfileButton.addEventListener("click", () => {
		if (profileEditState.isEditing) {
			cancelProfileEditMode();
			return;
		}

		enterProfileEditMode();
		displayNameInput.focus();
	});

	saveProfileButton.addEventListener("click", () => {
		saveProfileChanges();
	});

	setProfileEditable(false);
	setEditButtonLabel();
	updateProfileSaveVisibility();
	updateBioCounter();
}

function bindSecurityActions() {
	const { requestButton, currentEmailInput } = getSecurityInputs();
	const { changeButton, newPasswordInput } = getPasswordInputs();

	requestButton.addEventListener("click", () => {
		sendEmailChangeRequest();
	});

	changeButton.addEventListener("click", () => {
		handlePasswordChange();
	});

	newPasswordInput.addEventListener("input", () => {
		renderPasswordStrength(newPasswordInput.value);
	});

	currentEmailInput.addEventListener("focus", () => {
		setSettingsMessage("現在のメールアドレスは確認専用です。Security セクションで変更できます。", "success");
	});

	renderPasswordStrength("");
}

function bindAppearanceActions() {
	const { themeInputs, accentSwatches } = getAppearanceInputs();

	themeInputs.forEach((input) => {
		input.addEventListener("change", () => {
			if (input.checked) {
				applyThemeSetting(input.value);
			}
		});
	});

	accentSwatches.forEach((swatch) => {
		swatch.addEventListener("click", () => {
			applyAccentSetting(swatch.dataset.accent || "cyan");
		});
	});

	syncAppearanceControls();
}

function bindDangerActions() {
	const { logoutButton, currentPasswordInput, confirmationInput, deleteButton } = getDangerInputs();

	logoutButton.addEventListener("click", () => {
		handleLogoutFromDangerZone();
	});

	currentPasswordInput.addEventListener("input", () => {
		setDangerMessage("");
		updateDangerDeleteButtonState();
	});

	confirmationInput.addEventListener("input", () => {
		setDangerMessage("");
		updateDangerDeleteButtonState();
	});

	deleteButton.addEventListener("click", () => {
		handleDeleteAccount();
	});

	updateDangerDeleteButtonState();
}

function bindDeleteAccountModalActions() {
	const { modalOverlay, cancelButton, confirmButton } = getDeleteAccountModalInputs();

	cancelButton.addEventListener("click", () => {
		closeDeleteAccountModal();
	});

	confirmButton.addEventListener("click", () => {
		confirmDeleteAccountFromModal();
	});

	modalOverlay.addEventListener("click", (event) => {
		if (event.target === modalOverlay) {
			closeDeleteAccountModal();
		}
	});

	document.addEventListener("keydown", (event) => {
		if (event.key !== "Escape" || !modalOverlay.classList.contains("is-open")) {
			return;
		}

		event.preventDefault();
		closeDeleteAccountModal();
	});
}

function initializeResponsiveSidebar() {
	const sidebarToggle = document.getElementById("sidebarToggle");

	sidebarToggle.addEventListener("click", () => {
		toggleSidebar();
	});
}

document.addEventListener("DOMContentLoaded", async () => {
	if (!requireLogin()) {
		return;
	}

	bindTopbarActions();
	initializeSettingsNavigation();
	initializeResponsiveSidebar();
	bindProfileActions();
	bindSecurityActions();
	bindAppearanceActions();
	bindDangerActions();
	bindDeleteAccountModalActions();

	await loadProfile();
});
