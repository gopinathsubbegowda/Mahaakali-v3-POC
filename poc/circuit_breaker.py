import logging
import time
from typing import Dict, Any, List

class CircuitBreaker:
    """
    Safety mechanism for Agentic AI.
    Monitors agent behavior and triggers a 'kill switch' if thresholds are exceeded.
    """
    def __init__(self, failure_threshold: int = 3, reset_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.last_failure_time = 0
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("CircuitBreaker")

    def record_failure(self, reason: str):
        self.failures += 1
        self.last_failure_time = time.time()
        self.logger.warning(f"Failure recorded: {reason}. Total failures: {self.failures}")
        
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"
            self.logger.critical(f"CIRCUIT BREAKER OPENED: Agent execution halted for {self.reset_timeout}s")

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def can_execute(self) -> bool:
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = "HALF_OPEN"
                self.logger.info("Circuit Breaker state: HALF_OPEN. Probing for recovery.")
                return True
            return False
        return True

class BehavioralDriftMonitor:
    """
    Monitors agent behavior for drift or anomalies.
    """
    def __init__(self, token_limit: int = 2000):
        self.token_limit = token_limit
        self.token_usage_history: List[int] = []
        self.logger = logging.getLogger("DriftMonitor")

    def track_usage(self, tokens: int):
        self.token_usage_history.append(tokens)
        total_usage = sum(self.token_usage_history)
        if total_usage > self.token_limit:
            self.logger.error(f"Quota exceeded: {total_usage} > {self.token_limit}. Triggering safety protocol.")
            return False
        return True

if __name__ == "__main__":
    # POC self-test
    cb = CircuitBreaker(failure_threshold=2)
    
    print(f"Initial State: {cb.state}")
    cb.record_failure("Policy violation 1")
    print(f"Can execute? {cb.can_execute()}")
    cb.record_failure("Policy violation 2")
    print(f"Can execute? {cb.can_execute()}")
    print(f"Final State: {cb.state}")
