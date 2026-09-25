# Universal Modular AI Platform
Hexagonale Architektur, Pydantic v2, Python 3.12+.
## Sicherheit
- Default Deny Policy
- Kein Privilege Escalation via Header (Permissions kommen aus trusted IAM)
- Deterministische SHA-256 Audit Hashes
- FakeSandbox verweigert Code Execution strikt
## Start
pip install -r requirements.txt
pytest -q
uvicorn universal_ai.main:app --reload