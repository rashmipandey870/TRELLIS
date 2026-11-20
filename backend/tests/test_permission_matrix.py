"""Automated tests validating Role-Permission Matrix integrity and Default-Deny coverage."""

import json
from pathlib import Path


def get_matrix_path() -> Path:
    """Resolve path to PERMISSION_MATRIX.json regardless of execution root."""
    base = Path(__file__).resolve().parent.parent.parent
    return base / "docs" / "security" / "PERMISSION_MATRIX.json"


def test_permission_matrix_file_exists() -> None:
    """Verify that the permission matrix JSON artifact exists and is valid JSON."""
    matrix_path = get_matrix_path()
    assert matrix_path.exists(), f"Missing matrix file at {matrix_path}"

    with open(matrix_path, encoding="utf-8") as f:
        data = json.load(f)

    assert "active_roles" in data
    assert "future_roles_modeled" in data
    assert "resources" in data
    assert "actions" in data
    assert "rules" in data
    assert data.get("security_model", {}).get("default_policy") == "DENY"


def test_permission_matrix_dimensions_and_default_deny() -> None:
    """Verify collapsed 3-role matrix: 20 resources x 15 actions x 3 roles = 900 tuples under default-deny."""
    matrix_path = get_matrix_path()
    with open(matrix_path, encoding="utf-8") as f:
        data = json.load(f)

    active_roles = data["active_roles"]
    future_roles = data.get("future_roles_modeled", [])
    all_roles = active_roles + future_roles
    resources = data["resources"]
    actions = data["actions"]
    rules = data["rules"]

    assert set(all_roles) == {"ADMIN", "MENTOR", "LEARNER"}, f"Expected 3 collapsed roles, got {all_roles}"
    assert len(resources) == 20, f"Expected 20 resources, got {len(resources)}"
    assert len(actions) == 15, f"Expected 15 actions, got {len(actions)}"

    total_tuples = len(all_roles) * len(resources) * len(actions)
    assert total_tuples == 900

    explicit_grants = 0
    for res_rule in rules:
        resource = res_rule["resource"]
        assert resource in resources, f"Invalid resource: {resource}"
        for action, role_map in res_rule.get("actions", {}).items():
            assert action in actions, f"Invalid action: {action}"
            for role, grant in role_map.items():
                assert role in all_roles, f"Invalid role: {role}"
                assert "scope" in grant
                explicit_grants += 1

    assert explicit_grants == 90, f"Expected 90 explicit grants, got {explicit_grants}"
    default_denied = total_tuples - explicit_grants
    assert default_denied == 810, f"Expected 810 default-denied tuples, got {default_denied}"

    # Invariant: ADMIN cannot update/delete audit_log or evidence_ledger
    for res_rule in rules:
        if res_rule["resource"] in ["audit_log", "evidence_ledger"]:
            for action in ["update", "delete"]:
                action_grants = res_rule.get("actions", {}).get(action, {})
                admin_grant = action_grants.get("ADMIN", {})
                assert admin_grant.get("allowed") is not True, (
                    f"Forbidden: ADMIN must not have allowed {action} on {res_rule['resource']}"
                )
