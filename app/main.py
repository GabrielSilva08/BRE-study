import json
from fastapi import FastAPI, HTTPException, Body
from sqlalchemy.orm import Session
from models import Rule, DataEndpoint, RuleInput
from rules_engine import evaluate_rule
from database import SessionLocal, populate_initial_rules, cleanup_rules_on_shutdown

# Application lifespan behavior (startup/shutdown)
async def lifespan(app: FastAPI):
    populate_initial_rules()
    yield
    cleanup_rules_on_shutdown()

app = FastAPI(
    title="Bussiness Rule Engine API",
    description="Just an application of study in the BRE business-rules library",
    lifespan=lifespan
)

# Endpoint to evaluate a machine against all stored rules
@app.post("/evaluate_all")
def evaluate_all(endpoint: DataEndpoint):
    db: Session = SessionLocal()
    rules = db.query(Rule).all()

    if not rules:
        raise HTTPException(status_code=404, detail="No rules registered")

    results = []
    for rule in rules:
        rule_json = json.loads(rule.rule_json)
        result, triggered = evaluate_rule(rule_json, endpoint)
        results.append({
            "rule_name": rule.name,
            "activated": result,
            "triggered_action": triggered if triggered else None
        })

    return {"evaluations": results}

# Endpoint to evaluate a system with respect to a certain rule (rule_id)
@app.post("/evaluate/{rule_id}")
def evaluate(rule_id: int, endpoint: DataEndpoint):
    db: Session = SessionLocal()
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    try:
        rule_json = json.loads(rule.rule_json)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Corrupt or invalid rule")

    result, triggered = evaluate_rule(rule_json, endpoint)
    return {"endpoint": endpoint.endpoint_identifier, "result": result, "triggered_action": triggered}

# Endpoint to create a new rule
@app.post("/rules")
def create_rule(rule_input: RuleInput):
    db: Session = SessionLocal()
    rule = Rule(rule_json=json.dumps(rule_input.rule_json), name="Manuel rule")
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return {"message": "Rule added successfully", "rule_id": rule.id}

# Endpoint to list all rules
@app.get("/rules")
def list_rules():
    db: Session = SessionLocal()
    rules = db.query(Rule).all()
    return [{"id": rule.id, "rule_json": json.loads(rule.rule_json)} for rule in rules]

# Endpoint to update a rule by its ID
@app.put("/rules/{rule_id}")
def update_rule(rule_id: int, updated_rule: RuleInput = Body(...)):
    db: Session = SessionLocal()
    rule = db.query(Rule).filter(Rule.id == rule_id).first()

    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    rule.rule_json = json.dumps(updated_rule.rule_json)
    db.commit()
    return {"message": f"Rule with ID {rule_id} updated successfully"}

# Endpoint to delete a rule by its ID
@app.delete("/rules/{rule_id}")
def delete_rule(rule_id: int):
    db: Session = SessionLocal()
    rule = db.query(Rule).filter(Rule.id == rule_id).first()

    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    db.delete(rule)
    db.commit()
    return {"message": f"Rule with ID {rule_id} deleted successfully"}
