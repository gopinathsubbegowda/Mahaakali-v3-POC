import json
import hashlib
import datetime
from typing import List, Dict, Any

class AIBOM:
    """
    Agentic AI Bill of Materials (AIBOM) implementation.
    Tracks models, tools, datasets, and configurations used by an agent.
    """
    def __init__(self, agent_id: str, version: str):
        self.agent_id = agent_id
        self.version = version
        self.timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.models: List[Dict[str, str]] = []
        self.tools: List[Dict[str, str]] = []
        self.datasets: List[Dict[str, str]] = []
        self.config_hash: str = ""

    def add_model(self, name: str, version: str, hash_val: str):
        self.models.append({
            "name": name,
            "version": version,
            "hash": hash_val
        })

    def add_tool(self, name: str, description: str, access_level: str):
        self.tools.append({
            "name": name,
            "description": description,
            "access_level": access_level
        })

    def set_config(self, config_dict: Dict[str, Any]):
        config_str = json.dumps(config_dict, sort_keys=True)
        self.config_hash = hashlib.sha256(config_str.encode()).hexdigest()

    def generate_report(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "version": self.version,
            "timestamp": self.timestamp,
            "components": {
                "models": self.models,
                "tools": self.tools,
                "datasets": self.datasets
            },
            "integrity": {
                "config_hash": self.config_hash
            }
        }

    def save_to_file(self, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(self.generate_report(), f, indent=4)

if __name__ == "__main__":
    # POC self-test
    aibom = AIBOM("mahaakali-proto-agent", "1.0.0-poc")
    aibom.add_model("Llama-3-8B-Instruct", "v1.0", "sha256:abcd...")
    aibom.add_tool("file_reader", "Read files from sandbox", "RESTRICTED")
    aibom.set_config({"temperature": 0.7, "max_tokens": 512})
    
    print(json.dumps(aibom.generate_report(), indent=2))
