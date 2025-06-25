import json
from fastapi import FastAPI, HTTPException, Body
from sqlalchemy.orm import Session
from models import Rule, DataEndpoint, RuleInput
from rules_engine import evaluate_rule
from database import SessionLocal, populate_initial_rules, cleanup_rules_on_shutdown
from contextlib import asynccontextmanager

# Application lifespan behavior (startup/shutdown)
async def lifespan(app: FastAPI):
    populate_initial_rules()
    yield
    cleanup_rules_on_shutdown()

app = FastAPI(lifespan=lifespan)

# Endpoint to evaluate a system with respect to a certain rule (rule_id)
@app.post("/evaluate/{rule_id}")
def evaluate(rule_id: int, endpoint: DataEndpoint):
    db: Session = SessionLocal()
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Regra não encontrada")
    
    try:
        rule_json = json.loads(rule.rule_json)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Regra corrompida ou inválida")

    result, triggered = evaluate_rule(rule_json, endpoint)
    return {"endpoint": endpoint.endpoint_identifier, "result": result, "triggered_action": triggered}

# Endpoint to create a new rule
@app.post("/rules")
def create_rule(rule_input: RuleInput):
    db: Session = SessionLocal()
    rule = Rule(rule_json=json.dumps(rule_input.rule_json), name="Regra Manual")
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return {"message": "Regra adicionado com sucesso", "rule_id": rule.id}

# Endpoint to list all rules
@app.get("/rules")
def list_rules():
    db: Session = SessionLocal()
    rules = db.query(Rule).all()
    return [{"id": rule.id, "rule_json": json.loads(rule.rule_json)} for rule in rules]

# Endpoint to update a rule by its name
@app.put("/rules/{rule_name}")
def update_rule(rule_name: str, updated_rule: RuleInput = Body(...)):
    db: Session = SessionLocal()
    rule = db.query(Rule).filter(Rule.name == rule_name).first()

    if not rule:
        raise HTTPException(status_code=404, detail="Regra não encontrada")

    rule.rule_json = json.dumps(updated_rule.rule_json)
    db.commit()
    return {"message": f"Regra '{rule_name}' atualizada com sucesso"}

# Endpoint to delete a rule by its name
@app.delete("/rules/{rule_name}")
def delete_rule(rule_name: str):
    db: Session = SessionLocal()
    rule = db.query(Rule).filter(Rule.name == rule_name).first()

    if not rule:
        raise HTTPException(status_code=404, detail="Regra não encontrada")

    db.delete(rule)
    db.commit()
    return {"message": f"Regra '{rule_name}' removida com sucesso"}
