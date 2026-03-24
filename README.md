# ThunderHubs

## Установка на VPS

```bash
git clone https://github.com/ТЫ/thunderhubs.git
cd thunderhubs
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Создать .env из примера и вставить свой ключ
cp .env.example .env
nano .env
```

## Запуск

```bash
source venv/bin/activate
python app.py
```

## Автозапуск через systemd

```bash
nano /etc/systemd/system/thunderhubs.service
```

```ini
[Unit]
Description=ThunderHubs
After=network.target

[Service]
User=root
WorkingDirectory=/root/thunderhubs
ExecStart=/root/thunderhubs/venv/bin/python app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable thunderhubs
systemctl start thunderhubs
```

## Обновление

```bash
cd /root/thunderhubs
git pull
systemctl restart thunderhubs
```

## Структура

```
thunderhubs/
├── app.py              # точка входа
├── config.py           # настройки из .env
├── state.py            # глобальные переменные
├── requirements.txt
├── .env                # секреты (не в репо!)
├── .env.example        # шаблон для .env
├── routes/
│   ├── auth.py         # /  /logout
│   ├── admin.py        # /admin /hits /pastes + /api/
│   └── ws.py           # /ws  /forhits
└── templates/
    ├── shared.py       # STYLE, BG_HTML, RAIN_JS, SIDEBAR
    ├── admin_html.py
    ├── hits_html.py
    └── pastes_html.py
```
