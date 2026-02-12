from typing import List, Dict, Any, Callable
import logging

class PolicyEngine:
    """
    Policy-as-Code enforcement engine for Mahaakali agents.
    Evaluates actions against defined security policies.
    """
    def __init__(self):
        self.policies: List[Dict[str, Any]] = []
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("PolicyEngine")

    def add_policy(self, name: str, condition: Callable[[Dict[str, Any]], bool], action: str = "DENY"):
        self.policies.append({
            "name": name,
            "condition": condition,
            "action": action
        })
        self.logger.info(f"Policy added: {name}")

    def evaluate(self, agent_action: Dict[str, Any]) -> bool:
        """
        Returns True if the action is ALLOWED, False if DENIED.
        """
        for policy in self.policies:
            if policy["condition"](agent_action):
                if policy["action"] == "DENY":
                    self.logger.warning(f"ACTION DENIED by policy: {policy['name']} | Action: {agent_action}")
                    return False
        
        self.logger.info(f"Action allowed: {agent_action.get('type')}")
        return True

# Default Security Policies for the POC
def get_default_policies() -> PolicyEngine:
    engine = PolicyEngine()
    
    # Policy: Prevent access to sensitive files
    engine.add_policy(
        "NoSensitiveFiles",
        lambda a: a.get("type") == "file_read" and any(x in a.get("path", "").lower() for x in ["/etc/", "config.json", ".env"]),
        "DENY"
    )
    
    # Policy: Limit network access (simulated)
    engine.add_policy(
        "RestrictedNetwork",
        lambda a: a.get("type") == "network_request" and not a.get("destination", "").endswith(".gov"),
        "DENY"
    )
    
    # Policy: Prevent shell execution
    engine.add_policy(
        "NoShellExecution",
        lambda a: a.get("type") == "shell_exec",
        "DENY"
    )

    return engine

if __name__ == "__main__":
    # POC self-test
    engine = get_default_policies()
    
    test_actions = [
        {"type": "file_read", "path": "documents/report.txt"},
        {"type": "file_read", "path": "/etc/passwd"},
        {"type": "network_request", "destination": "api.github.com"},
        {"type": "network_request", "destination": "security.gov"},
        {"type": "shell_exec", "command": "ls -la"}
    ]
    
    for action in test_actions:
        allowed = engine.evaluate(action)
        print(f"Action: {action} -> {'ALLOWED' if allowed else 'DENIED'}")
