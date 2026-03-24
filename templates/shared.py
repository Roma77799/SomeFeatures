STYLE = '''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono&display=swap');

    :root {
        --bg: #000000;
        --panel: rgba(9, 9, 11, 0.85);
        --border: #18181b;
        --accent: #fbbd05;
        --error: #ff4b4b;
        --text-main: #ffffff;
        --text-dim: #71717a;
        --sidebar-width: 230px;
    }

    body {
        background: var(--bg);
        color: var(--text-main);
        font-family: 'Inter', sans-serif;
        margin: 0;
        display: flex;
        height: 100vh;
        overflow: hidden;
    }
    .main-content {
        flex: 1;
        margin-left: var(--sidebar-width);
        padding: 40px;
        position: relative;
        box-sizing: border-box;
        width: calc(100% - var(--sidebar-width));
        height: 100vh;
        overflow-y: auto;
    }
    .sidebar {
        width: var(--sidebar-width);
        background: var(--panel);
        border-right: 1px solid var(--border);
        height: 100vh;
        position: fixed;
        left: 0; top: 0;
        z-index: 100;
        display: flex;
        flex-direction: column;
        padding-top: 20px;
        backdrop-filter: blur(10px);
    }
    .sidebar-item {
        padding: 12px 25px;
        color: var(--text-dim);
        text-decoration: none;
        font-family: 'JetBrains Mono';
        font-size: 13px;
        transition: 0.2s;
        display: flex;
        align-items: center;
        gap: 10px;
        border-left: 3px solid transparent;
    }
    .sidebar-item:hover, .sidebar-item.active {
        color: var(--accent);
        background: rgba(251, 189, 5, 0.05);
        border-left: 3px solid var(--accent);
    }
    .sidebar-logo {
        padding: 0 20px 20px 20px;
        color: var(--accent);
        font-weight: 800;
        font-size: 18px;
        font-family: 'JetBrains Mono';
    }
    .sidebar-logout {
        padding: 12px 25px;
        color: var(--error) !important;
        text-decoration: none;
        font-family: 'JetBrains Mono';
        font-size: 13px;
        border-top: 1px solid var(--border);
        border-left: 3px solid transparent;
        display: flex;
        align-items: center;
        gap: 10px;
        transition: 0.2s;
        margin-top: auto;
    }
    .sidebar-logout:hover {
        background: rgba(255,75,75,0.05) !important;
        border-left-color: var(--error) !important;
    }
    @media (max-width: 900px) {
        .sidebar { transform: translateX(-100%); transition: 0.3s; }
        .sidebar.open { transform: translateX(0); }
        .main-content { margin-left: 0; padding: 20px; }
        .menu-btn { display: block !important; }
    }
    .menu-btn {
        display: none;
        position: fixed;
        top: 20px; left: 20px;
        z-index: 101;
        background: var(--accent);
        border: none; padding: 8px; border-radius: 5px;
    }
    .bg-gif {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: url('https://wallpapercave.com/wp/wp9637442.gif') no-repeat center center;
        background-size: cover;
        z-index: -10;
    }
    .bg-overlay {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.6);
        z-index: -9;
    }
    .rain {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        z-index: -5;
        pointer-events: none;
    }
    .drop {
        position: absolute;
        bottom: 100%;
        width: 2px;
        height: 80px;
        background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0.25));
        animation: fall linear infinite;
    }
    @keyframes fall { to { transform: translateY(110vh); } }
    .container { width: 100%; max-width: 1000px; position: relative; z-index: 1; }
    .login-box {
        background: var(--panel);
        border: 1px solid var(--border);
        padding: 40px;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        text-align: center;
        width: 300px;
        z-index: 10;
    }
    .login-box input {
        width: 100%;
        background: #000;
        border: 1px solid var(--border);
        color: #fff;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-sizing: border-box;
        outline: none;
        text-align: center;
    }
    .btn-login {
        width: 100%;
        background: var(--accent);
        color: #000;
        border: none;
        padding: 12px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        text-transform: uppercase;
        font-family: 'JetBrains Mono';
        transition: 0.3s;
    }
    .btn-login:hover { opacity: 0.8; transform: translateY(-2px); }
    .lock-timer { font-family: 'JetBrains Mono'; color: var(--error); font-size: 14px; margin-top: 10px; line-height: 1.6; }
    .page-title { font-family: 'JetBrains Mono'; font-size: 22px; font-weight: 700; margin-bottom: 30px; color: var(--text-main); }
    .page-title span { color: var(--accent); }
    .title-group { display: flex; align-items: center; gap: 12px; margin-bottom: 40px; }
    .target-icon { border: 1px solid var(--border); padding: 8px; border-radius: 8px; display: flex; align-items: center; background: var(--panel); }
    .title-text h1 { font-size: 20px; font-weight: 500; margin: 0; }
    .title-text p { font-size: 11px; color: var(--text-dim); font-family: 'JetBrains Mono'; margin: 4px 0 0 0; }
    .hit-row { background: var(--panel); border: 1px solid #151515; border-radius: 8px; display: flex; align-items: center; padding: 15px 20px; margin-bottom: 8px; backdrop-filter: blur(5px); }
    .cell.nick { color: var(--accent); font-weight: 600; width: 190px; font-size: 13px; }
    .cell.info { flex: 1; color: #444; font-size: 13px; display: flex; align-items: center; }
    .cell.info b { color: #888; font-weight: 500; }
    .exe-tag { border: 1px solid #222; background: #0a0a0a; padding: 2px 5px; border-radius: 4px; color: #71717a; font-size: 10px; margin-right: 10px; }
    .device-icon { font-size: 16px; margin-right: 10px; }
    .copy-btn { cursor: pointer; margin-left: 5px; color: var(--accent); opacity: 0.6; }
    .actions { display: flex; gap: 8px; align-items: center; }
    .btn { background: #111; border: 1px solid #222; color: #888; padding: 6px 12px; border-radius: 4px; font-size: 11px; cursor: pointer; font-family: 'JetBrains Mono'; text-transform: uppercase; }
    .btn:hover { border-color: #444; color: #fff; }
    .btn-all { border-color: var(--accent); color: var(--accent); margin-left: 8px; }
    .btn-join { background: #fff; color: #000; padding: 6px 15px; text-decoration: none; border-radius: 4px; font-size: 12px; font-weight: 600; }
    .overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: none; align-items: center; justify-content: center; z-index: 1000; backdrop-filter: blur(4px); }
    .modal-main { background: #09090b; border: 1px solid var(--border); padding: 25px; border-radius: 12px; width: 440px; z-index: 1001; }
    .modal-main.wide { width: 700px; }
    .modal-main textarea, .modal-main input[type="text"] { width: 100%; background: #000; border: 1px solid var(--border); color: #fff; padding: 12px; border-radius: 8px; outline: none; margin: 15px 0 20px 0; font-family: 'Inter'; box-sizing: border-box; display: block; }
    .modal-main textarea { resize: vertical; max-height: 50vh; min-height: 100px; overflow-y: auto; }
    .btn-download-logs { background: #fff !important; color: #000 !important; border: 1px solid transparent !important; transition: 0.2s ease; }
    .btn-download-logs:hover { border-color: var(--accent) !important; box-shadow: 0 0 10px rgba(251, 189, 5, 0.3); }
    .command-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 20px 0; }
    .btn-cmd-item { background: #000; border: 1px solid var(--border); color: var(--text-dim); padding: 12px; border-radius: 8px; cursor: pointer; font-family: 'JetBrains Mono'; font-size: 11px; transition: 0.2s; text-align: center; user-select: none; }
    .btn-cmd-item:hover { border-color: #333; }
    .btn-cmd-item.selected { border-color: var(--accent); color: var(--accent); background: rgba(251, 189, 5, 0.05); }
    .console-stream { height: 350px; background: #000; border: 1px solid var(--border); border-radius: 8px; overflow-y: auto; padding: 15px; margin: 15px 0 20px 0; font-family: 'JetBrains Mono'; font-size: 12px; line-height: 1.6; }
    .log-line { display: flex; gap: 12px; margin-bottom: 2px; border-bottom: 1px solid #0a0a0a; }
    .line-text { color: #d4d4d8; word-break: break-all; }
    .btn-send { flex: 1; background: #fff; color: #000; border: none; padding: 10px; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 12px; }
    .btn-abort { flex: 1; background: #18181b; color: #a1a1aa; border: 1px solid #27272a; padding: 10px; border-radius: 6px; cursor: pointer; font-size: 12px; }
    .server-console-container { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); width: 95%; max-width: 1000px; z-index: 9999; pointer-events: none; }
    .server-console { background: rgba(5,5,5,0.6); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; height: 150px; overflow-y: auto; padding: 12px; font-family: 'JetBrains Mono', monospace; font-size: 11px; pointer-events: all; box-shadow: 0 -10px 30px rgba(0,0,0,0.5); }
    .server-console::-webkit-scrollbar { width: 4px; }
    .server-console::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 10px; }
    .log-line-item { color: #ffffff; margin-bottom: 4px; text-shadow: 1px 1px 2px #000; }
    .log-line-item.warn { color: var(--accent); }
    .log-line-item.err { color: var(--error); }
    .console-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
    .btn-toggle { background: none; border: 1px solid var(--accent); color: var(--accent); font-family: 'JetBrains Mono'; font-size: 10px; cursor: pointer; padding: 2px 8px; border-radius: 4px; pointer-events: all; }
    .server-console.hidden { display: none; }
    #toast-container { position: fixed; bottom: 30px; right: 30px; display: flex; flex-direction: column-reverse; gap: 10px; z-index: 2000; }
    .toast-item { background: #000; border: 1px solid #222; padding: 12px 20px; border-radius: 10px; display: flex; align-items: center; gap: 12px; animation: toast-in 0.3s ease-out forwards; min-width: 200px; }
    @keyframes toast-in { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
    .toast-icon { width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; }
    .toast-success { border: 2px solid #4ade80; color: #4ade80; }
    .toast-error { border: 2px solid var(--error); color: var(--error); }
</style>
'''

RAIN_JS = '''
<script>
    function createRain() {
        const rainContainer = document.querySelector('.rain');
        if (!rainContainer || rainContainer.children.length > 0) return;
        for (let i = 0; i < 100; i++) {
            const drop = document.createElement('div');
            drop.className = 'drop';
            drop.style.left = Math.random() * 100 + 'vw';
            drop.style.animationDuration = (Math.random() * 0.5 + 0.5) + 's';
            drop.style.animationDelay = Math.random() * 2 + 's';
            rainContainer.appendChild(drop);
        }
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createRain);
    } else {
        createRain();
    }
</script>
'''

BG_HTML = '''
<div class="bg-gif"></div>
<div class="bg-overlay"></div>
<div class="rain"></div>
'''

SIDEBAR_HTML = '''
<div class="sidebar" id="sidebar">
    <div class="sidebar-logo">THUNDERHUBs</div>
    <a href="/admin" class="sidebar-item {active_dashboard}">LIVECAST</a>
    <a href="/hits" class="sidebar-item {active_hits}">HITS</a>
    <a href="/pastes" class="sidebar-item {active_pastes}">PASTES</a>
    <a href="/logout" class="sidebar-logout">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>
        </svg>
        LOGOUT
    </a>
</div>
<button class="menu-btn" onclick="document.getElementById('sidebar').classList.toggle('open')">OP</button>
'''
