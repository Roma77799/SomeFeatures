PASTES_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Pastes</title>
    {style_placeholder}
    <style>
        .pastes-toolbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 28px; }
        .pastes-count { font-family: 'JetBrains Mono'; font-size: 13px; color: var(--text-dim); }
        .pastes-count span { color: var(--accent); }
        .pastes-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 16px; }
        .paste-card { background: rgba(9,9,11,0.75); border: 1px solid #18181b; border-radius: 10px; display: flex; flex-direction: column; transition: border-color 0.2s, box-shadow 0.2s; overflow: hidden; backdrop-filter: blur(6px); }
        .paste-card:hover { border-color: #2a2a2a; box-shadow: 0 0 20px rgba(0,0,0,0.4); }
        .paste-card-head { display: flex; align-items: center; justify-content: space-between; padding: 14px 16px 12px; border-bottom: 1px solid #111; }
        .paste-nick { color: var(--accent); font-weight: 700; font-size: 14px; font-family: 'JetBrains Mono'; }
        .paste-id-badge { background: #0a0a0a; border: 1px solid #1a1a1a; color: #333; font-family: 'JetBrains Mono'; font-size: 10px; padding: 3px 8px; border-radius: 4px; }
        .paste-body { padding: 14px 16px; flex: 1; }
        .paste-preview { background: #050505; border: 1px solid #111; border-radius: 6px; padding: 12px 14px; color: #4a4a4a; font-size: 11px; font-family: 'JetBrains Mono'; white-space: pre-wrap; word-break: break-all; height: 72px; overflow: hidden; line-height: 1.7; position: relative; }
        .paste-preview::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 28px; background: linear-gradient(transparent, #050505); }
        .paste-meta { display: flex; gap: 16px; margin-top: 10px; }
        .paste-meta-item { font-family: 'JetBrains Mono'; font-size: 10px; color: #333; display: flex; align-items: center; gap: 5px; }
        .paste-meta-item svg { opacity: 0.4; }
        .paste-footer { display: flex; gap: 8px; padding: 12px 16px; border-top: 1px solid #0d0d0d; }
        .paste-btn-view { flex: 1; background: transparent; border: 1px solid #222; color: #888; text-align: center; text-decoration: none; padding: 8px 12px; border-radius: 5px; font-weight: 600; font-size: 10px; font-family: 'JetBrains Mono'; text-transform: uppercase; transition: 0.2s; display: flex; align-items: center; justify-content: center; gap: 6px; cursor: pointer; }
        .paste-btn-view:hover { border-color: var(--accent); color: var(--accent); }
        .paste-btn-delete { flex: 1; background: transparent; border: 1px solid #1a0808; color: #441111; padding: 8px 14px; border-radius: 5px; font-size: 10px; font-family: 'JetBrains Mono'; text-transform: uppercase; cursor: pointer; transition: 0.2s; display: flex; align-items: center; justify-content: center; }
        .paste-btn-delete:hover { border-color: var(--error); color: var(--error); }
        .pastes-empty { grid-column: 1 / -1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 100px 20px; border: 2px dashed rgba(251,189,5,0.15); border-radius: 16px; background: rgba(0,0,0,0.2); }
        .pastes-empty-title { color: var(--accent); font-family: 'JetBrains Mono'; font-size: 20px; font-weight: 800; letter-spacing: 4px; text-shadow: 0 0 20px rgba(251,189,5,0.4); animation: blink-slow 2s infinite ease-in-out; }
        @keyframes blink-slow { 0%,100%{opacity:1} 50%{opacity:0.5} }
        .pastes-empty-sub { color: #333; font-family: 'JetBrains Mono'; font-size: 11px; margin-top: 12px; }
    </style>
</head>
<body>
    {bg_placeholder}
    {sidebar_placeholder}
    <div class="main-content">
        <div id="toast-container"></div>
        <div class="pastes-toolbar">
            <div class="page-title" style="margin-bottom:0;">Saved <span>Pastes</span></div>
            <div class="pastes-count" id="pastes-count">- pastes</div>
        </div>
        <div class="pastes-grid" id="pastes-list"></div>
    </div>
    <script>
        (function(){
            const c = document.querySelector('.rain');
            if (!c || c.children.length > 0) return;
            for(let i=0;i<100;i++){
                const d=document.createElement('div'); d.className='drop';
                d.style.left=Math.random()*100+'vw';
                d.style.animationDuration=(Math.random()*.5+.5)+'s';
                d.style.animationDelay=Math.random()*2+'s';
                c.appendChild(d);
            }
        })();
        function showToast(text, type='success') {
            const container = document.getElementById('toast-container');
            if (container.children.length >= 5) container.removeChild(container.firstChild);
            const toast = document.createElement('div'); toast.className = 'toast-item';
            const iconClass = type === 'success' ? 'toast-success' : 'toast-error';
            const iconChar = type === 'success' ? 'Y' : 'X';
            toast.innerHTML = `<div class="toast-icon ${iconClass}">${iconChar}</div><div style="font-size:14px;color:#fff;">${text}</div>`;
            container.appendChild(toast);
            setTimeout(() => { toast.style.opacity='0'; toast.style.transition='0.3s'; setTimeout(()=>toast.remove(),300); }, 2500);
        }
        const MONTHS_P = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
        function formatPasteDate(ts) {
            const dt = new Date(ts * 1000);
            return `${dt.getDate()} ${MONTHS_P[dt.getMonth()]} ${dt.getFullYear()}, ${String(dt.getHours()).padStart(2,'0')}:${String(dt.getMinutes()).padStart(2,'0')}:${String(dt.getSeconds()).padStart(2,'0')}`;
        }
        async function deletePaste(id) {
            const r = await fetch(`/api/delete_paste/${id}`, { method: 'DELETE' });
            if (r.ok) {
                document.getElementById(`card-${id}`)?.remove();
                showToast('Paste deleted');
                const remaining = document.getElementById('pastes-list').querySelectorAll('.paste-card').length;
                document.getElementById('pastes-count').innerHTML = `<span>${remaining}</span> paste${remaining!==1?'s':''}`;
                if (remaining === 0) loadPastes();
            } else { showToast('Delete failed','error'); }
        }
        async function loadPastes() {
            const r = await fetch('/api/get_pastes');
            const data = await r.json();
            const list = document.getElementById('pastes-list');
            const entries = Object.entries(data);
            document.getElementById('pastes-count').innerHTML = `<span>${entries.length}</span> paste${entries.length!==1?'s':''}`;
            if (!entries.length) {
                list.innerHTML = `<div class="pastes-empty"><div class="pastes-empty-title">> NO PASTES _</div><div class="pastes-empty-sub">Pastes will appear here after hits are received</div></div>`;
                return;
            }
            entries.sort((a,b) => b[1].created_at - a[1].created_at);
            list.innerHTML = entries.map(([id, paste]) => {
                const lines = paste.content.split('\\n');
                const preview = lines.slice(0,4).join('\\n');
                const nick = paste.nick || '-';
                return `<div class="paste-card" id="card-${id}">
                    <div class="paste-card-head">
                        <span class="paste-nick">@${nick}</span>
                        <span class="paste-id-badge">${id}</span>
                    </div>
                    <div class="paste-body">
                        <div class="paste-preview">${escapeHtml(preview)}</div>
                        <div class="paste-meta">
                            <div class="paste-meta-item">
                                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
                                ${formatPasteDate(paste.created_at)}
                            </div>
                            <div class="paste-meta-item">
                                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                                ${paste.content.length} chars
                            </div>
                        </div>
                    </div>
                    <div class="paste-footer">
                        <a href="/pastes/${id}" target="_blank" class="paste-btn-view">
                            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg>VIEW
                        </a>
                        <button class="paste-btn-delete" onclick="deletePaste('${id}')">DELETE</button>
                    </div>
                </div>`;
            }).join('');
        }
        function escapeHtml(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
        setInterval(loadPastes, 5000); loadPastes();
    </script>
</body>
</html>
'''
