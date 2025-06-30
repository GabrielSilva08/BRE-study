# BRE-study — Business Rules Engine for Resource Automation

## About this repository

Just an application of study in the BRE `business-rules` library.

## Some features

- 🔍 **Rule evaluation**: Check rules with respect to an `endpoint` dynamically;
- ⚙️ **Create new rules** via API
- 📤 **Simulated notifications** by e-mail

## How to run?

1. Clone the repository:

```bash
git clone https://github.com/your-user/BRE-study.git
cd BRE-study
```

2. Create and activate a virtual enviroment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the API:

```bash
uvicorn main:app --reload
```

## Available API's endpoints

| Method   | Route                       | Description                                            |
|----------|-----------------------------|------------------------------------------------------- |
| `POST`   | `/evaluate_all`             | Evaluate a machine against all stored rules            |
| `POST`   | `/evaluate/{rule_id}`       | Evaluate rules to a certain machine endpoint           |
| `POST`   | `/rules`                    | Add new rule in execution time                         |
| `GET`    | `/rules`                    | List current rules                                     |
| `PUT`    | `/rules/{rule_id}`          | Update a rule by its ID                                |
| `DELETE` | `/rules/{rule_id}`          | Delete a rule by its ID                                |

## 📄 Project Structure

```bash
BRE-study/
│
├── .gitignore
├── requirements.txt             # Project dependencies
├── README.md                    # This document
├── tests                        # Test scripts
│   ├── test_client.py              
│   └── test_client1.py
└── app
    ├── main.py                  # Main file which runs FastAPI
    ├── rules_engine.py          # Variables and actions used in the rules
    ├── models.py                # Models and types
    ├── database.py              # Database initialization
    └── db                       # Database folder
        └── rules.db             # Dataset with all rules
```
