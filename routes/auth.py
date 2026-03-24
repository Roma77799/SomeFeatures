# -*- coding: utf-8 -*-
import time
import logging
from flask import Blueprint, request, redirect, make_response, render_template_string, Response
from config import SECRET_ACCESS_KEY
from state import failed_attempts
from templates.shared import STYLE, BG_HTML, RAIN_JS

logger = logging.getLogger()
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    ip = request.remote_addr
    now = time.time()

    if ip in failed_attempts:
        attempts, lock_time = failed_attempts[ip]
        if attempts >= 8:
            elapsed = now - lock_time
            if elapsed < 300:
                remaining = int(300 - elapsed)
                return render_template_string(f"""
                    <html><head>{STYLE}</head>
                    <body style='display:flex;align-items:center;justify-content:center;'>
                    {BG_HTML}
                    <div class='login-box'>
                        <div class='lock-timer'>SYSTEM LOCKED<br>
                        <span style='font-size:28px;' id='timer'>{remaining}</span>s</div>
                        <script>
                            let sec = {remaining};
                            setInterval(() => {{
                                sec--;
                                document.getElementById('timer').innerText = sec;
                                if(sec <= 0) location.reload();
                            }}, 1000);
                        </script>
                    </div>
                    {RAIN_JS}
                    </body></html>
                """)
            else:
                failed_attempts[ip] = [0, 0]

    err_msg = ""
    if request.method == 'POST':
        key_input = request.form.get('key', '').strip()
        if not key_input:
            err_msg = "Field cannot be empty"
        elif key_input == SECRET_ACCESS_KEY:
            logger.info(f"[AUTH] Successful login! IP: {ip}")
            failed_attempts[ip] = [0, 0]
            res = make_response(redirect('/admin'))
            res.set_cookie('access_token', 'validated_user_session')
            return res
        else:
            logger.info(f"[AUTH] Hack attempt! Key: '{key_input}' IP: {ip}")
            if ip not in failed_attempts:
                failed_attempts[ip] = [0, 0]
            failed_attempts[ip][0] += 1
            if failed_attempts[ip][0] >= 8:
                failed_attempts[ip][1] = now
            return redirect('/')

    attempt_count = failed_attempts.get(ip, [0])[0] if ip in failed_attempts else 0
    return render_template_string(f"""
        <html><head>{STYLE}</head>
        <body style='display:flex;align-items:center;justify-content:center;'>
        {BG_HTML}
        <div class='login-box'>
            <form method='POST'>
                <input type='password' name='key' placeholder='ACCESS KEY' autofocus required>
                {f'<div style="color:var(--error);font-size:11px;margin-bottom:10px;font-family:JetBrains Mono;">{err_msg}</div>' if err_msg else ''}
                <button type='submit' class='btn-login'>Sign In</button>
            </form>
            <div style='font-size:10px;color:#444;margin-top:15px;font-family:JetBrains Mono;'>
                ATTEMPT: {attempt_count} / 8
            </div>
        </div>
        {RAIN_JS}
        </body></html>
    """)


@auth_bp.route('/logout')
def logout():
    res = make_response(redirect('/'))
    res.set_cookie('access_token', '', expires=0)
    logger.info(f"[AUTH] User logged out. IP: {request.remote_addr}")
    return res
