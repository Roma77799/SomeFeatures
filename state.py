# -*- coding: utf-8 -*-
# Все глобальные переменные состояния сервера

clients_db = {}     # активные WS клиенты /ws
hits_db = []        # история хитов
pastes_db = {}      # { paste_id: { "content": "...", "nick": "...", "created_at": timestamp } }
hits_logs = []      # логи /forhits
server_logs = []    # системные логи
failed_attempts = {}  # неудачные попытки логина { ip: [count, lock_time] }
