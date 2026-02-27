Ansible playbooks for Proxmox hardening and fencing

Playbooks:
- play_create_automation_user.yml: creates a least-privilege automation user and installs a placeholder for authorized_keys. It also disables root password login and restarts sshd.
- play_qdevice_register.yml: idempotent registration of a corosync qdevice (witness). Verifies pvecm votes == 3 before succeeding.
- play_stonith_setup.yml: templated STONITH setup; gated by stonith_enabled variable. Includes dry-run and operator-confirmed destructive test.

Gating variables (defaults are safe):
- enable_ha: false
- stonith_enabled: false
- fence_test_confirm: false

Secrets and vaults:
- Do not store plaintext credentials in the repo. Use Ansible Vault or an external secrets manager. Variables noted as <BMC_USER>, <BMC_PASS>, <BOOTSTRAP_SSH_PUBKEY> are placeholders and must be injected from secure storage.

Execution order recommendation:
1) Ensure management bridge (vmbr-mgmt) exists and is reachable from your control host.
2) Run play_create_automation_user.yml to create automation user and place SSH key.
3) Provision witness VM (via Terraform) and ensure its cloud-init installs qnetd.
4) Run play_qdevice_register.yml to add qdevice and verify pvecm votes.
5) If BMC available and you choose STONITH path, configure play_stonith_setup.yml with stonith_enabled: true and run dry-run; only run destructive test in a controlled maintenance window and set fence_test_confirm: true.

Safety:
- All plays will fail fast if gating variables are not set.
- Do not run destructive fence tests without approval and maintenance windows.
