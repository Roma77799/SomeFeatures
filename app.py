# -*- coding: utf-8 -*-
import eventlet
eventlet.monkey_patch()

import sys
import logging
import threading
import time
from flask import Flask
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

# ── Логирование ──────────────────────────────────────────────────────────────

class ApiFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        blocked = ["/api/get_server_logs", "/api/get_clients",
                   "/api/get_hits", "/api/get_hits_logs"]
        return not any(b in msg for b in blocked)

class WebSocketLogHandler(logging.Handler):
    def emit(self, record):
        from state import server_logs
        log_entry = self.format(record)
        server_logs.append(log_entry)
        if len(server_logs) > 10000:
            server_logs.pop(0)

formatter = logging.Formatter('%(asctime)s | %(message)s', datefmt='%H:%M:%S')

log_handler = WebSocketLogHandler()
log_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(log_handler)
logger.addHandler(console_handler)

logging.getLogger('werkzeug').addFilter(ApiFilter())

# ── Фоновая очистка мёртвых клиентов ────────────────────────────────────────

def cleanup_dead_clients():
    from state import clients_db
    from config import CLIENT_TIMEOUT
    while True:
        time.sleep(30)
        now = time.time()
        dead = [cid for cid, d in list(clients_db.items())
                if now - d.get('last_seen', 0) > CLIENT_TIMEOUT]
        for cid in dead:
            logger.info(f"[CLEANUP] Removing dead client @{clients_db[cid]['name']}")
            del clients_db[cid]

threading.Thread(target=cleanup_dead_clients, daemon=True).start()

# ── Регистрация Blueprint'ов ─────────────────────────────────────────────────

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.ws import register_ws

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
register_ws(sock)

# ── Запуск ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    from config import PORT
    app.run(host='0.0.0.0', port=PORT)
