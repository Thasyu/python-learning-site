const LOCAL_API_BASE_URL = "http://127.0.0.1:5000";
const DEFAULT_PRODUCTION_API_BASE_URL = "https://python-learning-site-api.onrender.com";
const API_BASE_URL_OVERRIDE_KEY = "apiBaseUrl";

function normalizeBaseUrl(url) {
    if (!url || typeof url !== "string") {
        return "";
    }

    return url.trim().replace(/\/+$/, "");
}

function resolveBaseUrl() {
    const overrideBaseUrl = normalizeBaseUrl(localStorage.getItem(API_BASE_URL_OVERRIDE_KEY));
    if (overrideBaseUrl) {
        return overrideBaseUrl;
    }

    const hostName = window.location.hostname;
    const isLocalHost = hostName === "127.0.0.1" || hostName === "localhost";

    if (isLocalHost) {
        return LOCAL_API_BASE_URL;
    }

    return DEFAULT_PRODUCTION_API_BASE_URL;
}

//バックエンドAPIの基本URL
const BASE_URL = resolveBaseUrl();

//ログイン期限切れメッセージを保存するための共通キー名を定義しているコード
const AUTH_EXPIRED_MESSAGE_KEY = "authExpiredMessage";

//ログイン期限切れ時に表示するメッセージを管理するための定数
const AUTH_EXPIRED_MESSAGE = "ログイン期限が切れました。再ログインしてください。";

// 認証header取得関数
function getAuthHeaders() {
    const token = getToken();

    if (!token) {
        return {};
    }

    return {
        "Authorization": `Bearer ${token}`
    };
}

//API通信をまとめて管理するための関数
async function fetchJson(url, options = {}) {
    try {
        const response = await fetch(url, options);

        let data = {};
        try {
            data = await response.json();
        } catch (parseError) {
            data = {
                message: "レスポンスの解析に失敗しました。"
            };
        }

        if (response.status === 401 && getToken()) {
            clearToken();
            sessionStorage.setItem(AUTH_EXPIRED_MESSAGE_KEY, AUTH_EXPIRED_MESSAGE);
            window.location.href = "login.html";

            return {
                ok: false,
                status: response.status,
                data: data
            };
        }

        return {
            ok: response.ok,
            status: response.status,
            data: data
        };
    } catch (error) {
        return {
            ok: false,
            status: 0,
            data: {
                message: "通信エラーが発生しました。"
            }
        };
    }
}

//ログインAPIへユーザー名とパスワードを送信するための関数
async function loginUser(username, password) {
    return await fetchJson(`${BASE_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });
}

//新規ユーザー登録APIへ情報を送信するための関数
async function registerUser(username, email, password, displayName = "") {
    const payload = {
        username: username,
        email: email,
        password: password
    };

    if (displayName) {
        payload.display_name = displayName;
    }

    return await fetchJson(`${BASE_URL}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });
}

//パスワード再設定メールを送るAPIを呼び出す関数
async function requestPasswordReset(identifier) {
    return await fetchJson(`${BASE_URL}/password/request-reset`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            identifier: identifier
        })
    });
}

//新しいパスワードを確定するAPIを呼び出す関数
async function confirmPasswordReset(token, newPassword) {
    return await fetchJson(`${BASE_URL}/password/reset/confirm`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            token: token,
            new_password: newPassword
        })
    });
}

//学習進捗の概要データを取得するAPIを呼び出す関数
async function fetchProgressSummary() {
    return await fetchJson(`${BASE_URL}/progress/summary`, {
        headers: {
            ...getAuthHeaders()
        }
    });
}

//章ごとの学習統計を取得するAPIを呼び出す関数
async function fetchChapterStats() {
    return await fetchJson(`${BASE_URL}/progress/chapter`, {
        headers: {
            ...getAuthHeaders()
        }
    });
}

//難易度ごとの学習統計を取得するAPIを呼び出す関数
async function fetchDifficultyStats() {
    return await fetchJson(`${BASE_URL}/progress/difficulty`, {
        headers: {
            ...getAuthHeaders()
        }
    });
}

//現在ログインしているユーザー情報を取得するAPIを呼び出す関数
async function fetchMe() {
    return await fetchJson(`${BASE_URL}/me`, {
        headers: {
            ...getAuthHeaders()
        }
    });
}

//表示名（ニックネーム）を更新するAPIを呼び出す関数
async function updateDisplayName(displayName) {
    return await fetchJson(`${BASE_URL}/profile/display-name`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            ...getAuthHeaders()
        },
        body: JSON.stringify({
            display_name: displayName
        })
    });
}

//自己紹介を更新するAPIを呼び出す関数
async function updateBio(bio) {
    return await fetchJson(`${BASE_URL}/profile/bio`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            ...getAuthHeaders()
        },
        body: JSON.stringify({
            bio: bio
        })
    });
}

//プロフィール画像をアップロードするAPIを呼び出す関数
async function uploadAvatar(file) {
    const formData = new FormData();
    formData.append("avatar", file);

    return await fetchJson(`${BASE_URL}/profile/avatar`, {
        method: "POST",
        headers: {
            ...getAuthHeaders()
        },
        body: formData
    });
}

//パスワード変更APIを呼び出す関数
async function changePassword(currentPassword, newPassword, confirmPassword) {
    return await fetchJson(`${BASE_URL}/password/change`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            ...getAuthHeaders()
        },
        body: JSON.stringify({
            current_password: currentPassword,
            new_password: newPassword,
            confirm_password: confirmPassword
        })
    });
}

//指定した章の問題一覧を取得するAPIを呼び出す関数
async function fetchQuestionsByChapter(chapter, mode = "recommended") {
    return await fetchJson(
        `${BASE_URL}/questions/chapter?chapter=${chapter}&mode=${encodeURIComponent(mode)}`,
        {
            headers: {
                ...getAuthHeaders()
            }
        }
    );
}

//ユーザーの回答コードをサーバーへ送信して採点してもらう関数
async function submitAnswer(questionId, userCode) {
    return await fetchJson(`${BASE_URL}/submit`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            ...getAuthHeaders()
        },
        body: JSON.stringify({
            question_id: questionId,
            user_code: userCode
        })
    });
}

//Practice用にコードを安全実行するAPIを呼び出す関数
async function runPracticeCodeApi(code) {
    return await fetchJson(`${BASE_URL}/practice/run`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            ...getAuthHeaders()
        },
        body: JSON.stringify({
            code: code
        })
    });
}

//復習対象の問題一覧を取得するAPIを呼び出す関数
async function fetchReviewQuestions() {
    return await fetchJson(`${BASE_URL}/questions/review`, {
        headers: {
            ...getAuthHeaders()
        }
    });
}

//現在の学習状態をサーバーへ保存する関数（question_snapshotを含む）
async function saveStudySession(payload) {
    return await fetchJson(`${BASE_URL}/study-session/save`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            ...getAuthHeaders()
        },
        body: JSON.stringify(payload)
    });
}

//最後に保存された学習状態を取得する関数
async function fetchLatestStudySession() {
    return await fetchJson(`${BASE_URL}/study-session/latest`, {
        headers: {
            ...getAuthHeaders()
        }
    });
}

//保存されている学習セッションを削除する関数
async function deleteStudySession() {
    return await fetchJson(`${BASE_URL}/study-session`, {
        method: "DELETE",
        headers: {
            ...getAuthHeaders()
        }
    });
}

//現在ログイン中のユーザーアカウントをソフト削除するAPIを呼び出す関数
async function deleteAccount(currentPassword, confirmation) {
    return await fetchJson(`${BASE_URL}/account/delete`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            ...getAuthHeaders()
        },
        body: JSON.stringify({
            current_password: currentPassword,
            confirmation: confirmation
        })
    });
}

//ログアウトAPIを呼び出す関数
async function logoutUser() {
    return await fetchJson(`${BASE_URL}/logout`, {
        method: "POST",
        headers: {
            ...getAuthHeaders()
        }
    });
}

//メールアドレス変更の確認メールを送信するAPIを呼び出す関数
async function requestEmailChange(newEmail, currentPassword) {
    return await fetchJson(`${BASE_URL}/email-change/request`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            ...getAuthHeaders()
        },
        body: JSON.stringify({
            new_email: newEmail,
            current_password: currentPassword
        })
    });
}

//メールアドレス変更を確定するAPIを呼び出す関数
async function confirmEmailChange(token) {
    return await fetchJson(`${BASE_URL}/email-change/confirm`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            token: token
        })
    });
}