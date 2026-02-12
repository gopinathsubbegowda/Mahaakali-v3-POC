from trust_plane import TrustPlane
import time

class MockAgent:
    """
    Simulates an AI Agent interacting with the Trust Plane.
    """
    def __init__(self, trust_plane: TrustPlane):
        self.trust_plane = trust_plane

    def run_simulation(self):
        print("--- Starting Agent Simulation ---")
        
        actions = [
            {"type": "file_read", "path": "instructions.txt", "tokens": 100},
            {"type": "network_request", "destination": "docs.gov", "tokens": 200},
            {"type": "file_read", "path": ".env", "tokens": 50},  # Violation
            {"type": "network_request", "destination": "malicious.com", "tokens": 1000}, # Violation
            {"type": "file_read", "path": "success_report.txt", "tokens": 50} # Should be blocked if breaker is OPEN
        ]

        for action in actions:
            print(f"\nAgent attempting: {action['type']} on {action.get('path') or action.get('destination')}")
            allowed = self.trust_plane.execute_action(action)
            if allowed:
                print(">>> Action executed successfully.")
            else:
                print(">>> Action BLOCKED by Trust Plane.")
            time.sleep(1)

        print("\n--- Simulation Finished ---")
        self.trust_plane.shutdown("simulation_aibom.json")

if __name__ == "__main__":
    tp = TrustPlane("mahaakali-poc-agent", "v3.0-poc")
    tp.initialize_agent(
        config={"max_iterations": 10, "security_level": "MAX"},
        models=[{"name": "Mistral-7B", "version": "v3", "hash": "sha-5678"}]
    )
    
    agent = MockAgent(tp)
    agent.run_simulation()
