```
.
├── app/
│   ├── main.py             # Entry point da API
│   ├── models.py           # Modelos do SQLAlchemy
│   ├── rules_engine.py     # Lógica de execução das regras
│   └── schemas.py          # Pydantic para entrada/saída
└── db/
    └── rules.db            # Banco de dados SQLite (pode ser outro)
```