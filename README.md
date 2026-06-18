# Python学習Webアプリ

## DB Migration

既存の `data/app.db` を使用している場合は、DB構造を最新化するために migration を実行してください。

実行方法:

```powershell
py -m backend.migrate
```

migration 完了後は通常通り次のコマンドで起動してください。

```powershell
py -m backend.api
```

## DB運用ルール

- 通常起動時は `init_db()` のみを実行します。
- `migrate_db()` は DB 構造変更時にのみ手動で実行します。
- `migrate_db()` を毎回の起動時に自動実行しない方針を採用します。

## Gmail SMTP 設定手順

パスワード再設定メール送信は Gmail SMTP を想定しています。

1. Google アカウントで 2 段階認証を有効化します。
2. Google アカウント管理画面で「アプリ パスワード」を作成します。
3. プロジェクトルートに `.env` ファイルを作成します。
4. `.env.example` を参考に、次の値を `.env` に設定します。

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=example@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=example@gmail.com
PASSWORD_RESET_PAGE_URL=http://127.0.0.1:5500/pages/reset-password.html
```

5. `SMTP_PASSWORD` には通常のGoogleログインパスワードではなく、必ずアプリパスワードを設定してください。
6. `.env` 変更後は backend を再起動してください。`load_dotenv()` は起動時に読み込まれます。

## セキュリティ注意点

- `.env` は Git 管理しないでください。
- SMTP の資格情報をソースコードへ直接書かないでください。
- `SMTP_PASSWORD` はログ出力しないでください。
- 本番では `.env` の代わりにシークレット管理サービスの利用を推奨します。

## GitHub Pages + Render 構成

フロントエンドは GitHub Pages、バックエンドAPIは Render で公開する想定です。

### 1. Render 側（Web Service）

- Runtime: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn --bind 0.0.0.0:$PORT backend.api:app`

Render の Environment Variables 例:

```env
FLASK_DEBUG=0
FRONTEND_ORIGINS=https://thasyu.github.io,http://127.0.0.1:5500,http://localhost:5500
PASSWORD_RESET_PAGE_URL=https://thasyu.github.io/python-learning-site/pages/reset-password.html
EMAIL_CHANGE_CONFIRM_PAGE_URL=https://thasyu.github.io/python-learning-site/pages/confirm-email-change.html
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=example@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=example@gmail.com
```

### 2. フロントエンドのAPI接続先

`frontend/utils/api.js` は以下の動作に変更済みです。

- ローカル表示 (`localhost` / `127.0.0.1`) では `http://127.0.0.1:5000`
- それ以外（GitHub Pages）では `https://python-learning-site-api.onrender.com`

Render で実際のサービスURLが異なる場合は、`frontend/utils/api.js` の
`DEFAULT_PRODUCTION_API_BASE_URL` を Render のURLに変更してください。

一時的にブラウザ側で変更したい場合は、開発者コンソールで次を実行できます。

```js
localStorage.setItem("apiBaseUrl", "https://<your-render-service>.onrender.com")
```

解除する場合:

```js
localStorage.removeItem("apiBaseUrl")
```
