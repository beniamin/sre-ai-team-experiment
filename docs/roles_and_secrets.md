Roles and Secrets — 2026-02-26T13:30:00Z

Required service accounts and secrets (must be provisioned in secrets manager before running IaC/Ansible):

Secrets and where to store them
- PROXMOX_API_TOKEN -> secrets manager key: proxmox/api_token
- BOOTSTRAP_SSH_KEY -> secrets manager key: proxmox/bootstrap_ssh (playbooks expect the private key path supplied at runtime)
- BMC credentials (optional) -> secrets manager key: proxmox/bmc_creds (fields: host, user, password)
- CLOUD_INIT_SSH_PUBKEY -> secrets manager key: infra/cloud_init_pubkey

Service accounts and roles
- automation@pve (least-privilege API token): role -- Datacenter.Modify? limited to VM provisioning, storage query, and cluster query as needed. Create via Proxmox UI/API and store token in secrets manager.
- ansible-user on nodes: local user created by Ansible with NOPASSWD sudo restricted to required read-only/provisioning commands. Key installed from CLOUD_INIT_SSH_PUBKEY.

Rotation policy
- All bootstrap and initial credentials MUST be rotated within 48 hours of completion of initial deployment. Owner: infra-ops team (assign person/email). Record rotation events in centralized audit log.

Access rules for /app/docs
- Inventory and plan files under /app/docs are sensitive. File permissions must be set to 600 for inventory files and 644 for generic docs. TTL: inventory files older than 7 days must be archived to secure storage and removed from /app/docs unless explicitly retained by ops owner.
