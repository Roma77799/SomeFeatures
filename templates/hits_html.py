HITS_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Hits</title>
    {style_placeholder}
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono&display=swap');
        * { box-sizing: border-box; }
        body { background: var(--bg); color: var(--text-main); font-family: 'Inter', sans-serif; margin: 0; display: flex; height: 100vh; overflow: hidden; }
        .main-content { flex: 1; margin-left: var(--sidebar-width); padding: 40px; width: calc(100% - var(--sidebar-width)); box-sizing: border-box; height: 100vh; overflow-y: auto; }
        .hits-list { display: flex; flex-direction: column; gap: 8px; }
        .hit-row { background: rgba(9,9,11,0.7); border: 1px solid #151515; border-radius: 8px; display: grid; grid-template-columns: 140px 120px 80px 1fr 80px 100px 210px; align-items: center; padding: 14px 18px; backdrop-filter: blur(5px); transition: border-color 0.2s; gap: 12px; }
        .hit-row:hover { border-color: #2a2a2a; }
        .col-time { font-family: 'JetBrains Mono'; font-size: 11px; color: #444; line-height: 1.6; }
        .col-nick { color: var(--accent); font-weight: 700; font-size: 13px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .col-place { font-family: 'JetBrains Mono'; font-size: 11px; color: #555; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .col-exe { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; row-gap: 4px; }
        .exe-badge { border: 1px solid #222; padding: 3px 8px; border-radius: 4px; color: #666; font-size: 10px; font-family: 'JetBrains Mono'; text-transform: uppercase; white-space: nowrap; }
        .items-count { color: #444; font-size: 11px; font-family: 'JetBrains Mono'; white-space: nowrap; }
        .col-value { color: #4ade80; font-weight: 800; font-size: 16px; font-family: 'JetBrains Mono'; text-align: right; white-space: nowrap; }
        .col-status { text-align: center; padding: 0 5px; }
        .status-badge { border: 1px solid #222; padding: 4px 0; width: 80px; text-align: center; border-radius: 4px; font-size: 10px; font-family: 'JetBrains Mono'; text-transform: uppercase; display: inline-block; white-space: nowrap; }
        .col-actions { display: flex; gap: 8px; justify-content: flex-end; align-items: center; min-width: 220px; }
        .btn-details { border: 1px solid #222; background: transparent; color: #888; padding: 6px 12px; border-radius: 4px; font-size: 10px; font-family: 'JetBrains Mono'; text-transform: uppercase; cursor: pointer; transition: 0.2s; display: inline-flex; align-items: center; text-decoration: none; }
        .btn-details:hover { border-color: var(--accent); color: var(--accent); }
        .btn-join-sm { background: #fff; color: #000; padding: 6px 12px; border-radius: 4px; font-size: 11px; font-weight: 600; text-decoration: none; white-space: nowrap; display: inline-flex; align-items: center; }
        .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.85); display: none; align-items: center; justify-content: center; z-index: 1000; backdrop-filter: blur(4px); }
        .modal-card { background: #0c0c0e; border: 1px solid #1a1a1a; width: 540px; max-width: 95vw; padding: 28px; border-radius: 12px; max-height: 90vh; overflow-y: auto; }
        .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .modal-time { font-family: 'JetBrains Mono'; color: #333; font-size: 11px; }
        .modal-close { cursor: pointer; color: #555; font-size: 18px; background: none; border: none; }
        .modal-close:hover { color: #fff; }
        .modal-grid { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 16px; margin-bottom: 20px; }
        .modal-field span { font-size: 10px; color: #444; text-transform: uppercase; font-family: 'JetBrains Mono'; display: block; margin-bottom: 4px; }
        .modal-field b { display: block; font-size: 13px; color: #eee; font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .modal-field b.accent { color: var(--accent); }
        .items-box { background: #060606; border: 1px solid #111; border-radius: 8px; max-height: 320px; overflow-y: auto; margin-bottom: 20px; }
        .items-box::-webkit-scrollbar { width: 4px; }
        .items-box::-webkit-scrollbar-thumb { background: #222; border-radius: 4px; }
        .item-card { display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; border-bottom: 1px solid #0d0d0d; }
        .item-card:last-child { border-bottom: none; }
        .item-left { display: flex; align-items: center; gap: 10px; }
        .item-name { color: #aaa; font-size: 12px; }
        .item-amount { color: #333; font-size: 11px; font-family: 'JetBrains Mono'; }
        .item-val { color: #4ade80; font-weight: 700; font-family: 'JetBrains Mono'; font-size: 12px; }
        .modal-footer { display: flex; align-items: center; border-top: 1px solid #1a1a1a; padding-top: 16px; }
        .total-label { color: #444; font-size: 11px; font-family: 'JetBrains Mono'; text-transform: uppercase; margin-right: 8px; }
        .total-value { color: #4ade80; font-weight: 800; font-size: 24px; font-family: 'JetBrains Mono'; }
        .modal-footer .btn-join-sm { margin-left: 10px; display: inline-flex; align-items: center; justify-content: center; }
    </style>
</head>
<body>
    {bg_placeholder}
    {sidebar_placeholder}
    <div class="main-content" style="padding-bottom: 200px;">
        <div class="page-title">Loot <span>History</span></div>
        <div class="hits-list" id="hits-list"></div>
    </div>
    <div id="modal" class="modal-overlay" onclick="if(event.target===this)closeModal()">
        <div class="modal-card">
            <div class="modal-header">
                <span class="modal-time" id="m-time"></span>
                <button class="modal-close" onclick="closeModal()">X</button>
            </div>
            <div class="modal-grid">
                <div class="modal-field"><span>Username</span><b class="accent" id="m-nick"></b></div>
                <div class="modal-field"><span>Place ID</span><b id="m-place"></b></div>
                <div class="modal-field"><span>Job ID</span><b id="m-job" style="color:#555;font-size:11px;"></b></div>
                <div class="modal-field"><span>Items</span><b id="m-count"></b></div>
            </div>
            <div class="items-box" id="m-items"></div>
            <div class="modal-footer">
                <span class="total-label">Total Value</span>
                <span class="total-value" id="m-total"></span>
                <div style="margin-left: auto;"></div>
                <a id="m-join" href="#" target="_blank" class="btn-join-sm">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="vertical-align:middle;margin-right:4px;">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/>
                    </svg>Join
                </a>
                <a id="m-paste" href="#" target="_blank" class="btn-join-sm" style="background:#4ade80;display:none;margin-left:8px;">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="vertical-align:middle;margin-right:4px;">
                        <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2"/>
                    </svg>Paste
                </a>
            </div>
        </div>
    </div>
    <script>
        (function(){
            const c = document.querySelector('.rain');
            for(let i=0;i<100;i++){
                const d=document.createElement('div');
                d.className='drop';
                d.style.left=Math.random()*100+'vw';
                d.style.animationDuration=(Math.random()*.5+.5)+'s';
                d.style.animationDelay=Math.random()*2+'s';
                c.appendChild(d);
            }
        })();
        const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
        function formatDate(str) {
            const [datePart, timePart] = str.split(' ');
            const [y,m,d] = datePart.split('-');
            return `${parseInt(d)} ${MONTHS[parseInt(m)-1]} ${y}, ${timePart}`;
        }
        let hitsData = [];
        function renderHits(data) {
            hitsData = data;
            const list = document.getElementById('hits-list');
            if (!data.length) {
                list.innerHTML = `<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:100px 20px;margin-top:30px;border:2px dashed rgba(251,189,5,0.15);border-radius:16px;background:rgba(0,0,0,0.2);">
                    <div style="color:#fbbd05;font-family:'JetBrains Mono',monospace;font-size:20px;font-weight:800;text-transform:uppercase;letter-spacing:5px;text-shadow:0 0 20px rgba(251,189,5,0.4);animation:blink-slow 2s infinite ease-in-out;">NO HITS YET _</div>
                    <div style="color:#333;font-family:'JetBrains Mono';font-size:11px;margin-top:12px;">WAITING FOR INCOMING LOOT DATA...</div>
                    </div><style>@keyframes blink-slow{0%,100%{opacity:1}50%{opacity:0.5}}</style>`;
                return;
            }
            list.innerHTML = data.map((h, i) => {
                const statusColor = h.is_online ? '#eee' : '#ff4b4b';
                const statusBorder = h.is_online ? '#222' : '#411';
                return `<div class="hit-row">
                    <div class="col-time">${formatDate(h.time)}</div>
                    <div class="col-nick">@${h.name}</div>
                    <div class="col-place" title="${h.placeId}">${h.placeId}</div>
                    <div class="col-exe">
                        <span class="exe-badge">${h.exe}</span>
                        <span class="items-count">${h.total_count} items</span>
                        <span class="items-count" style="color:#333;">${h.location || '-'}</span>
                    </div>
                    <div class="col-value">${h.total_price}</div>
                    <div class="col-status"><span class="status-badge" style="color:${statusColor};border-color:${statusBorder};">${h.status || (h.is_online ? 'online' : 'offline')}</span></div>
                    <div class="col-actions">
                        <button class="btn-details" onclick="showDetails(${i})">DETAILS</button>
                        ${h.paste_id ? `<a href="/pastes/${h.paste_id}" target="_blank" class="btn-details" style="border-color:#4ade80;color:#4ade80;">PASTE</a>` : ''}
                        <a href="https://www.roblox.com/games/start?placeId=${h.placeId}&gameId=${h.jobId}" target="_blank" class="btn-join-sm">JOIN</a>
                    </div>
                </div>`;
            }).join('');
        }
        function showDetails(i) {
            const h = hitsData[i];
            document.getElementById('m-time').innerText = formatDate(h.time);
            document.getElementById('m-nick').innerText = '@' + h.name;
            document.getElementById('m-place').innerText = h.placeId;
            document.getElementById('m-job').innerText = h.jobId ? h.jobId.substring(0,16)+'...' : '-';
            document.getElementById('m-count').innerText = h.total_count;
            document.getElementById('m-total').innerText = h.total_price;
            document.getElementById('m-join').href = `https://www.roblox.com/games/start?placeId=${h.placeId}&gameId=${h.jobId}`;
            const pasteBtn = document.getElementById('m-paste');
            if (h.paste_id) { pasteBtn.href = `/pastes/${h.paste_id}`; pasteBtn.style.display = 'inline-flex'; }
            else { pasteBtn.style.display = 'none'; }
            const container = document.getElementById('m-items');
            if (!h.items || !h.items.length) {
                container.innerHTML = '<div style="color:#222;text-align:center;padding:20px;font-family:JetBrains Mono;font-size:12px;">EMPTY</div>';
            } else {
                container.innerHTML = h.items.map(it => `<div class="item-card"><div class="item-left"><span class="item-name">${it.name}</span><span class="item-amount">x${it.amount}</span></div><span class="item-val">${it.value}</span></div>`).join('');
            }
            document.getElementById('modal').style.display = 'flex';
        }
        function closeModal() { document.getElementById('modal').style.display = 'none'; }
        async function loadHits() {
            try { const r = await fetch('/api/get_hits'); const data = await r.json(); renderHits(data); } catch(e) {}
        }
        setInterval(loadHits, 3000); loadHits();
        function toggleHitlog() {
            const box = document.getElementById('hitlog-box');
            const btn = document.getElementById('hitlog-toggle-btn');
            if (box.classList.contains('hidden')) { box.classList.remove('hidden'); btn.innerText = 'HIDE'; }
            else { box.classList.add('hidden'); btn.innerText = 'SHOW'; }
        }
        function downloadHitlog() {
            const text = document.getElementById('hitlog-box').innerText;
            const blob = new Blob([text], { type: 'text/plain' });
            const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'hitlog.txt'; a.click();
        }
        async function updateHitlog() {
            try {
                const r = await fetch('/api/get_hits_logs');
                const logs = await r.json();
                const box = document.getElementById('hitlog-box');
                const isAtBottom = box.scrollHeight - box.clientHeight <= box.scrollTop + 2;
                box.innerHTML = logs.map(log => {
                    let cls = '';
                    if (log.includes('[HIT]')) cls = 'warn';
                    if (log.includes('[CONNECT]')) cls = 'warn';
                    if (log.includes('[DISCONNECT]')) cls = 'err';
                    if (log.includes('[TIMEOUT]')) cls = 'err';
                    if (log.includes('[WARN]')) cls = 'err';
                    return `<div class="log-line-item ${cls}">${log}</div>`;
                }).join('');
                if (isAtBottom) box.scrollTop = box.scrollHeight;
            } catch(e) {}
        }
        setInterval(updateHitlog, 1500); updateHitlog();
    </script>
    <div class="server-console-container">
        <div class="console-header">
            <div style="font-family:'JetBrains Mono';font-size:10px;color:var(--accent);opacity:0.8;">[ HITLOG_STREAM ]</div>
            <div style="display:flex;gap:8px;align-items:center;">
                <button class="btn-toggle" onclick="downloadHitlog()">DL .TXT</button>
                <button class="btn-toggle" onclick="toggleHitlog()" id="hitlog-toggle-btn">HIDE</button>
            </div>
        </div>
        <div class="server-console" id="hitlog-box"></div>
    </div>
</body>
</html>
'''
