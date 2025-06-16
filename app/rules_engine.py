from datetime import datetime
from business_rules.engine import run_all
from business_rules.variables import BaseVariables, numeric_rule_variable
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC
from models import DataEndpoint

# Define available variables to be used in the rules
class InputVariables(BaseVariables):
    def __init__(self, data_endpoint: DataEndpoint):
        self.endpoint = data_endpoint

    @numeric_rule_variable
    def current_usage_percentage(self) -> float:
        return (self.endpoint.space_used * 100) / self.endpoint.space_quota
    
    @numeric_rule_variable
    def days_since_last_access(self) -> int:
        return (datetime.now() - self.endpoint.last_acess).days

# Define the actions to be executed if some is triggered
class OutputActions(BaseActions):
    def __init__(self, endpoint_identifier: str):
        self.cis_storage_email = "team_member@email.com"
        self.endpoint = endpoint_identifier
        self.triggered_actions = [] # Keep track to return actions that were executed

    def send_email_notification(self, destination, message) -> None:
        notification = f"[EMAIL to {destination}]: {message}"
        print(notification)
        self.triggered_actions.append(notification)

    @rule_action()
    def under_usage_resource(self) -> None:
        self.send_email_notification("team_member", f'Under usage detected for endpoint "{self.endpoint}"')
    
    @rule_action(params={"inactive_days": FIELD_NUMERIC})
    def inactive_resource(self, inactive_days) -> None:
        self.send_email_notification("user", f'Endpoint "{self.endpoint}" has not been accessed in the last {inactive_days} days')
    
def evaluate_rule(rule_json, data_endpoint):
    variables = InputVariables(data_endpoint)
    actions = OutputActions(data_endpoint.endpoint_identifier)
    result = run_all(rule_list=rule_json, defined_variables=variables, defined_actions=actions)
    return result, actions.triggered_actions
