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
        return (datetime.now() - self.endpoint.last_access).days

# Define the actions to be executed if some is triggered
class OutputActions(BaseActions):
    def __init__(self, endpoint: DataEndpoint):
        self.cis_storage_email = "team_member@email.com"
        self.endpoint = endpoint
        self.triggered_actions = [] # Keep track to return actions that were executed

    def send_email_notification(self, destination, message) -> None:
        notification = f"[EMAIL to {destination}]: {message}"
        print(notification)
        self.triggered_actions.append(notification)

    @rule_action()
    def under_usage_resource(self) -> None:
        self.send_email_notification("team_member", f'Under usage detected of {(self.endpoint.space_used * 100) / self.endpoint.space_quota} for endpoint "{self.endpoint.endpoint_identifier}"')
    
    @rule_action()
    def over_usage_resource(self) -> None:
        self.send_email_notification("team_member", f'Over usage detected of {(self.endpoint.space_used * 100) / self.endpoint.space_quota} for endpoint "{self.endpoint.endpoint_identifier}"')
    
    @rule_action()
    def inactive_resource(self) -> None:
        self.send_email_notification("user", f'Endpoint "{self.endpoint.endpoint_identifier}" has not been accessed in the last {(datetime.now() - self.endpoint.last_access).days} days')

    @rule_action()
    def inactive_under_usage_resource(self) -> None:
        self.send_email_notification("user", f'Endpoint "{self.endpoint.endpoint_identifier}" has not been accessed in the last {(datetime.now() - self.endpoint.last_access).days} days and use {(self.endpoint.space_used * 100) / self.endpoint.space_quota} of available memory')
    
    @rule_action()
    def excessive_usage(self) -> None:
        self.send_email_notification("team_member", f'Endpoint "{self.endpoint.endpoint_identifier}" last access was {(datetime.now() - self.endpoint.last_access).days} and it is using {(self.endpoint.space_used * 100) / self.endpoint.space_quota} of available memory')

def evaluate_rule(rule_json, data_endpoint):
    variables = InputVariables(data_endpoint)
    actions = OutputActions(data_endpoint)

    result = run_all(rule_list=[rule_json], defined_variables=variables, defined_actions=actions)

    triggered_action = None
    if actions.triggered_actions:
        triggered_action = rule_json["actions"][0]["name"]

    return result, triggered_action
