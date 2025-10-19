
```
taro/
├── src/
│   ├── tg_bot/
│   │   ├── __init__.py
│   │   ├── handlers/
│   │   │   ├── __init__.py
│   │   │   ├── start.py
│   │   │   ├── commands.py
│   │   │   └── callbacks.py
│   │   ├── keyboards/
│   │   │   ├── __init__.py
│   │   │   ├── main_menu.py
│   │   │   └── inline.py
│   │   ├── middlewares/
│   │   │   ├── __init__.py
│   │   │   └── throttling.py
│   │   └── filters/
│   │       ├── __init__.py
│   │       └── custom_filters.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── crud.py
│   │   └── connection.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── api_client.py
│   │   ├── payment.py
│   │   └── notifications.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   └── validators.py
│   └── config.py
├── data/
│   ├── temp/
│   └── logs/
├── locales/ (для мультиязычности)
│   ├── ru.json
│   └── en.json
├── tests/
│   ├── __init__.py
│   ├── test_handlers.py
│   └── test_services.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── main.py
```