import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from models import Base, Rule

DATABASE_URL = "sqlite:///./db/rules.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def populate_initial_rules():
    """
    Insert default rules into the database at app startup.
    This only inserts them if they are not already present.
    """
    db: Session = SessionLocal()

    INITIAL_RULES = [
        {
            "name": "Under Usage Rule",
            "rule_json": {
                "conditions": {
                    "any": [
                        {"name": "current_usage_percentage", "operator": "less_than_or_equal_to", "value": 20}
                    ]
                },
                "actions": [
                    {"name": "under_usage_resource"}
                ]
            }
        },
        {
            "name": "Inactive Access Rule",
            "rule_json": {
                "conditions": {
                    "any": [
                        {"name": "days_since_last_access", "operator": "greater_than_or_equal_to", "value": 90}
                    ]
                },
                "actions": [
                    {"name": "inactive_resource", "params": {"inactive_days": 90}}
                ]
            }
        }
    ]

    for rule in INITIAL_RULES:
        existing = db.query(Rule).filter(Rule.name == rule["name"]).first()
        if not existing:
            new_rule = Rule(name=rule["name"], rule_json=json.dumps(rule["rule_json"]))
            db.add(new_rule)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
    finally:
        db.close()

def cleanup_rules_on_shutdown():
    """
    Clear all rules from the database on shutdown (testing mode only).
    """
    db: Session = SessionLocal()
    db.query(Rule).delete()
    db.commit()
    db.close()