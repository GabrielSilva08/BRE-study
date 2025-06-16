import json
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from models import Rule, DataEndpoint, RuleInput
from rules_engine import evaluate_rule
from database import engine, SessionLocal, init_db

init_db()

app = FastAPI()

# Endpoint to evaluate a system with respect to a certain rule (rule_id)
@app.post("/evaluate/{rule_id}")
def evaluate(rule_id: int, endpoint: DataEndpoint):
    db: Session = SessionLocal()
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Regra não encontrada")
    
    rule_json = json.loads(rule.rule_json)
    result, triggered = evaluate_rule(rule_json, endpoint)
    return {"result": result, "triggered_action": triggered}

# Endpoint to create a new rule
@app.post("/rules")
def create_rule(rule_input: RuleInput):
    db: Session = SessionLocal()
    rule = Rule(rule_json=json.dumps(rule_input.rule_json))
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return {"message": "Regra adicionado com sucesso", "rule_id": rule.id}

# Endpoint to list all rules
@app.get("/rules")
def list_rules():
    db: Session = SessionLocal()
    rules = db.query(Rule).all()
    return [
        {"id": rule.id, "rule_json": json.loads(rule.rule_json)}
        for rule in rules
    ]
