#!/usr/bin/env python3
"""Grant catalog access and inspect workspace users/permissions.

Designed to be %run from a notebook where a DatabricksSession (spark) is already connected.
"""

# --- Grant USE CATALOG to all account users ---
# The "account users" group includes every user in the workspace.
# Granting at the group level is the simplest way to give everyone catalog access
# without needing to iterate through individual users.
catalog_name = "main"
spark.sql(f"GRANT USE CATALOG ON CATALOG {catalog_name} TO `account users`")
print(f"Granted USE CATALOG on {catalog_name} to `account users`")


# ============================================================================
# The sections below are commented out but useful for debugging and auditing.
# Uncomment as needed.
# ============================================================================

# --- Grant schema-level permissions ---
# Unity Catalog uses a hierarchical permission model:
#   USE CATALOG -> USE SCHEMA -> SELECT (read tables/views)
# After granting USE CATALOG above, you can grant schema access like this:
#
# schema_name = "my_schema"
# spark.sql(f"GRANT USE SCHEMA ON SCHEMA {catalog_name}.{schema_name} TO `account users`")
# spark.sql(f"GRANT SELECT ON SCHEMA {catalog_name}.{schema_name} TO `account users`")
# print(f"Granted USE SCHEMA + SELECT on {catalog_name}.{schema_name} to `account users`")

# --- Grant permissions to an individual user ---
#
# grant_user = "user@company.com"
# spark.sql(f"GRANT USE CATALOG ON CATALOG {catalog_name} TO `{grant_user}`")
# spark.sql(f"GRANT USE SCHEMA ON SCHEMA {catalog_name}.{schema_name} TO `{grant_user}`")
# spark.sql(f"GRANT SELECT ON SCHEMA {catalog_name}.{schema_name} TO `{grant_user}`")
# print(f"Granted USE CATALOG, USE SCHEMA, and SELECT to {grant_user}")

# --- List all workspace users via SCIM API ---
# Derives the host from the active spark session so we don't need to hardcode a profile.
# The WorkspaceClient uses the CLI auth tokens cached for this host.
#
# from databricks.sdk import WorkspaceClient
# host = f"https://{spark._client._builder.host}"
# w = WorkspaceClient(host=host)
#
# users = list(w.users.list())
# print(f"Found {len(users)} user(s):\n")
# print(f"{'Username':<45} {'Display Name':<30} {'Active'}")
# print("-" * 85)
# for user in sorted(users, key=lambda u: (u.user_name or "")):
#     print(f"{user.user_name or '':<45} {user.display_name or '':<30} {user.active}")

# --- Show Unity Catalog permissions ---
# Shows GRANTS on the catalog and each schema underneath it.
# Note: can be slow on workspaces with many schemas.
#
# catalog_grants = spark.sql(f"SHOW GRANTS ON CATALOG {catalog_name}").collect()
# if catalog_grants:
#     print(f"{'Principal':<45} {'Privilege':<25} {'Type'}")
#     print("-" * 85)
#     for row in sorted(catalog_grants, key=lambda r: r.Principal):
#         print(f"{row.Principal:<45} {row.ActionType:<25} {row.ObjectType}")
#
# schemas = [row.databaseName for row in spark.sql(f"SHOW SCHEMAS IN {catalog_name}").collect()]
# for schema_name in sorted(schemas):
#     schema_grants = spark.sql(f"SHOW GRANTS ON SCHEMA {catalog_name}.{schema_name}").collect()
#     if schema_grants:
#         print(f"\nPermissions on {catalog_name}.{schema_name}:")
#         for row in sorted(schema_grants, key=lambda r: r.Principal):
#             print(f"  {row.Principal:<45} {row.ActionType:<25} {row.ObjectType}")
