import logging
from aibom import AIBOM
from policies import get_default_policies
from circuit_breaker import CircuitBreaker, BehavioralDriftMonitor
from typing import Dict, Any

class TrustPlane:
    """
    Mahaakali v3 Core Orchestrator.
    Integrates all trust layers to provide a secure execution environment for agents.
    """
    def __init__(self, agent_id: str, version: str):
        self.agent_id = agent_id
        self.version = version
        self.aibom = AIBOM(agent_id, version)
        self.policy_engine = get_default_policies()
        self.circuit_breaker = CircuitBreaker()
        self.drift_monitor = BehavioralDriftMonitor()
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"TrustPlane-{agent_id}")

    def initialize_agent(self, config: Dict[str, Any], models: list):
        """Register agent components in AIBOM."""
        self.aibom.set_config(config)
        for m in models:
            self.aibom.add_model(m["name"], m["version"], m["hash"])
        self.logger.info("Agent initialized and AIBOM generated.")

    def execute_action(self, action: Dict[str, Any]) -> bool:
        """
        The central gateway for all agent actions.
        Ensures safety, policy compliance, and resource isolation.
        """
        # 1. Check Circuit Breaker
        if not self.circuit_breaker.can_execute():
            self.logger.error("EXECUTION BLOCKED: Circuit breaker is OPEN.")
            return False

        # 2. Track Drift/Usage
        tokens = action.get("tokens", 0)
        if not self.drift_monitor.track_usage(tokens):
            self.circuit_breaker.record_failure("Resource quota exceeded")
            return False

        # 3. Policy Enforcement
        if not self.policy_engine.evaluate(action):
            self.circuit_breaker.record_failure(f"Policy violation: {action.get('type')}")
            return False

        # 4. Success path
        self.circuit_breaker.record_success()
        self.logger.info(f"Action '{action.get('type')}' successfully validated and executed.")
        return True

    def shutdown(self, report_path: str = "aibom_final.json"):
        """Save final attestation report."""
        self.aibom.save_to_file(report_path)
        self.logger.info(f"Trust Plane shutdown. AIBOM saved to {report_path}")

if __name__ == "__main__":
    # Integration test
    tp = TrustPlane("test-agent-01", "1.0.0-poc")
    tp.initialize_agent({"temp": 0.5}, [{"name": "Llama3", "version": "1.0", "hash": "h123"}])
    
    # Safe action
    tp.execute_action({"type": "file_read", "path": "plans/project.md", "tokens": 100})
    
    # Unsafe action (policy violation)
    tp.execute_action({"type": "file_read", "path": "/etc/shadow", "tokens": 50})
    
    # Unsafe action (shell)
    tp.execute_action({"type": "shell_exec", "command": "rm -rf /", "tokens": 10})
    
    # Check circuit breaker
    tp.execute_action({"type": "file_read", "path": "logs.txt", "tokens": 20})
    
    tp.shutdown()
