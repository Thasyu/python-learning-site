import os
import smtplib
import logging
from html import escape
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


logger = logging.getLogger(__name__)


SERVICE_NAME = "Python Learning Cloud"
PASSWORD_RESET_SUBJECT = "【Python Learning Cloud】パスワード再設定のご案内"
EMAIL_CHANGE_SUBJECT = "【Python Learning Cloud】メールアドレス変更の確認"


def build_password_reset_email_text(reset_url):
    return (
        f"{SERVICE_NAME}\n"
        "=================================\n\n"
        "平素よりご利用いただきありがとうございます。\n"
        "パスワード再設定のリクエストを受け付けました。\n\n"
        "以下のURLから、パスワードの再設定を行ってください。\n"
        f"{reset_url}\n\n"
        "このリンクの有効期限は30分です。\n"
        "このリンクは1回のみ利用可能です。\n"
        "本メールに心当たりがない場合は、何もせず破棄してください。\n"
        "パスワードは第三者に共有しないでください。\n\n"
        "ボタンが開けない場合は、上記URLをブラウザに貼り付けてアクセスしてください。\n\n"
        "---------------------------------\n"
        f"{SERVICE_NAME} サポートチーム"
    )


def build_password_reset_email_html(reset_url):
        app_public_url = os.getenv("APP_PUBLIC_URL", "").rstrip("/")
        if app_public_url:
            logo_block = (
                f'<img src="{app_public_url}/image/main.png" alt="Python Learning Cloud" '
                'width="48" height="48" style="display:block;border-radius:10px;object-fit:contain;" />'
            )
        else:
            logo_block = ""

        return f"""<!doctype html>
<html lang=\"ja\">
    <head>
        <meta charset=\"utf-8\" />
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
        <title>{PASSWORD_RESET_SUBJECT}</title>
    </head>
    <body style=\"margin:0;padding:0;background-color:#050816;color:#e5e7eb;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Hiragino Kaku Gothic ProN','Yu Gothic UI','Yu Gothic',Meiryo,sans-serif;\">
        <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"100%\" style=\"background-color:#050816;background-image:radial-gradient(circle at 15% 15%, #0b1020 0%, #050816 55%);\">
            <tr>
                <td align=\"center\" style=\"padding:28px 14px;\">
                    <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"100%\" style=\"max-width:620px;\">
                        <tr>
                            <td align=\"center\" style=\"padding-bottom:18px;\">
                                <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">
                                    <tr>
                                        <td align=\"center\" style=\"padding-bottom:10px;\">{logo_block}</td>
                                    </tr>
                                    <tr>
                                        <td align=\"center\">
                                            <div style=\"display:inline-block;padding:8px 14px;border:1px solid #1e293b;border-radius:999px;background-color:#0b1224;color:#67e8f9;font-size:13px;letter-spacing:0.08em;text-transform:uppercase;font-weight:700;\">Python Learning Cloud</div>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style=\"background-color:#0f172a;border:1px solid #1e293b;border-radius:16px;padding:28px 24px;\">
                                <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"100%\">
                                    <tr>
                                        <td style=\"font-size:26px;line-height:1.4;font-weight:700;color:#e5e7eb;padding-bottom:12px;\">パスワード再設定のご案内</td>
                                    </tr>
                                    <tr>
                                        <td style=\"font-size:15px;line-height:1.8;color:#cbd5e1;padding-bottom:10px;\">平素より <span style=\"color:#e5e7eb;font-weight:600;\">{SERVICE_NAME}</span> をご利用いただき、ありがとうございます。</td>
                                    </tr>
                                    <tr>
                                        <td style=\"font-size:15px;line-height:1.8;color:#cbd5e1;padding-bottom:24px;\">パスワード再設定のリクエストを受け付けました。以下のボタンから、パスワードを再設定してください。</td>
                                    </tr>
                                    <tr>
                                        <td align=\"center\" style=\"padding:0 0 8px;\">
                                            <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">
                                                <tr>
                                                    <td align=\"center\" bgcolor=\"#06b6d4\" style=\"border-radius:10px;background:#06b6d4;background-image:linear-gradient(90deg,#06b6d4 0%,#3b82f6 55%,#8b5cf6 100%);\">
                                                        <a href=\"{reset_url}\" style=\"display:inline-block;padding:14px 30px;font-size:15px;line-height:1.2;font-weight:700;color:#ffffff;text-decoration:none;\">Reset Password</a>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style=\"font-size:13px;line-height:1.7;color:#94a3b8;padding-top:12px;padding-bottom:8px;\">ボタンが開けない場合は、以下のURLをブラウザに貼り付けてください。</td>
                                    </tr>
                                    <tr>
                                        <td style=\"word-break:break-all;font-size:13px;line-height:1.7;color:#67e8f9;background-color:#0b1224;border:1px solid #1e293b;border-radius:10px;padding:12px;\">{reset_url}</td>
                                    </tr>
                                    <tr>
                                        <td style=\"padding-top:22px;\">
                                            <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"100%\" style=\"border-collapse:separate;\">
                                                <tr>
                                                    <td style=\"font-size:13px;line-height:1.8;color:#94a3b8;padding:14px;border:1px solid #243147;border-radius:10px;background-color:#0b1224;\">
                                                        <div style=\"padding-bottom:3px;\">このリンクの有効期限は30分です。</div>
                                                        <div style=\"padding-bottom:3px;\">このリンクは1回のみ利用可能です。</div>
                                                        <div style=\"padding-bottom:3px;\">本メールに心当たりがない場合は、何もせず破棄してください。</div>
                                                        <div>パスワードは第三者に共有しないでください。</div>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style=\"padding:16px 8px 4px;font-size:12px;line-height:1.7;color:#94a3b8;text-align:center;\">{SERVICE_NAME} サポートチーム</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
</html>
"""


def build_email_change_email_text(confirm_url, new_email, expires_minutes):
    return (
        f"{SERVICE_NAME}\n"
        "=================================\n\n"
        "登録メールアドレス変更のリクエストを受け付けました。\n"
        "以下のURLを開いて、メールアドレス変更を確定してください。\n\n"
        f"{confirm_url}\n\n"
        f"変更先メールアドレス: {new_email}\n"
        f"このリンクの有効期限は{expires_minutes}分です。\n"
        "このリンクは1回のみ利用可能です。\n"
        "本メールに心当たりがない場合は、何もせず破棄してください。\n\n"
        "---------------------------------\n"
        f"{SERVICE_NAME} セキュリティチーム"
    )


def build_email_change_email_html(confirm_url, new_email, expires_minutes, username=None):
    app_public_url = os.getenv("APP_PUBLIC_URL", "").rstrip("/")
    if app_public_url:
        logo_block = (
            f'<img src="{app_public_url}/image/main.png" alt="Python Learning Cloud" '
            'width="48" height="48" style="display:block;border-radius:10px;object-fit:contain;" />'
        )
    else:
        logo_block = ""

    safe_email = escape(new_email)
    safe_confirm_url = escape(confirm_url)
    safe_username = escape(username or "ユーザー")

    return f"""<!doctype html>
<html lang=\"ja\">
    <head>
        <meta charset=\"utf-8\" />
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
        <title>{EMAIL_CHANGE_SUBJECT}</title>
    </head>
    <body style=\"margin:0;padding:0;background-color:#050816;color:#e5e7eb;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Hiragino Kaku Gothic ProN','Yu Gothic UI','Yu Gothic',Meiryo,sans-serif;\">
        <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"100%\" style=\"background-color:#050816;background-image:radial-gradient(circle at 15% 15%, #0b1020 0%, #050816 55%);\">
            <tr>
                <td align=\"center\" style=\"padding:28px 14px;\">
                    <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"100%\" style=\"max-width:620px;\">
                        <tr>
                            <td align=\"center\" style=\"padding-bottom:18px;\">
                                <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">
                                    <tr>
                                        <td align=\"center\" style=\"padding-bottom:10px;\">{logo_block}</td>
                                    </tr>
                                    <tr>
                                        <td align=\"center\">
                                            <div style=\"display:inline-block;padding:8px 14px;border:1px solid #1e293b;border-radius:999px;background-color:#0b1224;color:#67e8f9;font-size:13px;letter-spacing:0.08em;text-transform:uppercase;font-weight:700;\">Security Console</div>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style=\"background-color:#0f172a;border:1px solid #1e293b;border-radius:16px;padding:28px 24px;\">
                                <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"100%\">
                                    <tr>
                                        <td style=\"font-size:26px;line-height:1.4;font-weight:700;color:#e5e7eb;padding-bottom:12px;\">メールアドレス変更の確認</td>
                                    </tr>
                                    <tr>
                                        <td style=\"font-size:15px;line-height:1.8;color:#cbd5e1;padding-bottom:10px;\">{safe_username} さん、メールアドレス変更リクエストを受け付けました。</td>
                                    </tr>
                                    <tr>
                                        <td style=\"font-size:15px;line-height:1.8;color:#cbd5e1;padding-bottom:24px;\">以下のボタンをクリックすると、変更先メールアドレスへの更新が確定します。</td>
                                    </tr>
                                    <tr>
                                        <td align=\"center\" style=\"padding:0 0 8px;\">
                                            <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">
                                                <tr>
                                                    <td align=\"center\" bgcolor=\"#06b6d4\" style=\"border-radius:10px;background:#06b6d4;background-image:linear-gradient(90deg,#06b6d4 0%,#3b82f6 55%,#8b5cf6 100%);\">
                                                        <a href=\"{safe_confirm_url}\" style=\"display:inline-block;padding:14px 30px;font-size:15px;line-height:1.2;font-weight:700;color:#ffffff;text-decoration:none;\">メールアドレスを変更する</a>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style=\"padding-top:10px;font-size:13px;color:#94a3b8;\">変更先メールアドレス: <span style=\"color:#67e8f9;\">{safe_email}</span></td>
                                    </tr>
                                    <tr>
                                        <td style=\"font-size:13px;line-height:1.7;color:#94a3b8;padding-top:12px;padding-bottom:8px;\">ボタンが開けない場合は、以下のURLをブラウザに貼り付けてください。</td>
                                    </tr>
                                    <tr>
                                        <td style=\"word-break:break-all;font-size:13px;line-height:1.7;color:#67e8f9;background-color:#0b1224;border:1px solid #1e293b;border-radius:10px;padding:12px;\">{safe_confirm_url}</td>
                                    </tr>
                                    <tr>
                                        <td style=\"padding-top:22px;\">
                                            <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"100%\" style=\"border-collapse:separate;\">
                                                <tr>
                                                    <td style=\"font-size:13px;line-height:1.8;color:#94a3b8;padding:14px;border:1px solid #243147;border-radius:10px;background-color:#0b1224;\">
                                                        <div style=\"padding-bottom:3px;\">このリンクの有効期限は{expires_minutes}分です。</div>
                                                        <div style=\"padding-bottom:3px;\">このリンクは1回のみ利用可能です。</div>
                                                        <div style=\"padding-bottom:3px;\">本メールに心当たりがない場合は、何もせず破棄してください。</div>
                                                        <div>第三者にリンクを共有しないでください。</div>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style=\"padding:16px 8px 4px;font-size:12px;line-height:1.7;color:#94a3b8;text-align:center;\">{SERVICE_NAME} セキュリティチーム</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
</html>
"""


def send_email_message(to_email, subject, text_body, html_body):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port_raw = os.getenv("SMTP_PORT")
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM")

    logger.info("[mail] SMTP_HOST=%s", smtp_host)
    logger.info("[mail] SMTP_PORT=%s", smtp_port_raw)
    logger.info("[mail] SMTP_USERNAME=%s", smtp_username)
    logger.info("[mail] SMTP_FROM=%s", smtp_from)

    required_settings = {
        "SMTP_HOST": smtp_host,
        "SMTP_PORT": smtp_port_raw,
        "SMTP_USERNAME": smtp_username,
        "SMTP_PASSWORD": smtp_password,
        "SMTP_FROM": smtp_from
    }
    missing_keys = [key for key, value in required_settings.items() if not value]

    if missing_keys:
        missing_text = ", ".join(missing_keys)
        raise RuntimeError(f"SMTP設定が不足しています: {missing_text}")

    try:
        smtp_port = int(smtp_port_raw)
    except ValueError as error:
        raise RuntimeError("SMTP_PORT は数値で指定してください。") from error

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = smtp_from
    message["To"] = to_email
    message.attach(MIMEText(text_body, "plain", "utf-8"))
    message.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as smtp:
            smtp.ehlo()

            if smtp_port == 587:
                smtp.starttls()
                smtp.ehlo()

            smtp.login(smtp_username, smtp_password)

            smtp.send_message(message)

    except Exception:
        logger.exception("[mail] failed to send email")
        raise


def send_password_reset_email(to_email, reset_url):
    text_body = build_password_reset_email_text(reset_url)
    html_body = build_password_reset_email_html(reset_url)
    send_email_message(to_email, PASSWORD_RESET_SUBJECT, text_body, html_body)


def send_email_change_confirmation(to_email, username, confirm_url, expires_minutes):
    text_body = build_email_change_email_text(confirm_url, to_email, expires_minutes)
    html_body = build_email_change_email_html(confirm_url, to_email, expires_minutes, username=username)
    send_email_message(to_email, EMAIL_CHANGE_SUBJECT, text_body, html_body)
