Terraform witness VM module (template)

Purpose: create a small Ubuntu VM to act as a corosync qdevice (witness).

Notes:
- This is a template only. Do NOT apply without reviewing and injecting secrets.
- The Proxmox Terraform provider compatible with Proxmox VE 9 is bpg/proxmox. Use a recent provider version known to support PVE 9.
- Inject PROXMOX API credentials via TF_VAR_pm_api_* environment variables or use a secure mechanism (do not hardcode secrets).
- Provide the path to the bootstrap public SSH key via bootstrap_ssh_pubkey_path variable.
- The witness VM will attach its NIC to the management bridge (vmbr-mgmt). Ensure that bridge exists or create it via Ansible before applying.

Example usage:
terraform init
terraform plan -var-file=example.tfvars

Secrets required (do NOT store in repo):
- PROXMOX API token (TF_VAR_pm_api_token_id, TF_VAR_pm_api_token_secret)
- Bootstrapping SSH public key path

