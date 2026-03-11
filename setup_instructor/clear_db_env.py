"""Temporary script to clear Databricks env vars set by VS Code extension.
Run this before connecting via Databricks Connect if the extension is
pointing to a different workspace than your target profile.

Delete this file once the VS Code Databricks extension is reconfigured.
"""
import os

DB_ENV_VARS = [
    "DATABRICKS_HOST",
    "DATABRICKS_AUTH_TYPE",
    "DATABRICKS_SERVERLESS_COMPUTE_ID",
    "DATABRICKS_METADATA_SERVICE_URL",
]

for var in DB_ENV_VARS:
    val = os.environ.pop(var, None)
    if val:
        print(f"Cleared {var}")

print("Done - Databricks env vars cleared.")
