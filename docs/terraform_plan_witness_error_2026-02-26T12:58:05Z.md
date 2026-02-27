Terraform init/plan failed in this environment during provider discovery.

Error summary from terraform init/validate:

Error: Failed to query available provider packages
Could not retrieve the list of available versions for provider bpg/proxmox:
no available releases match the given constraints >= 1.0.0

And:
Error: Missing required provider registry.terraform.io/bpg/proxmox, but that provider isn't available. terraform init is required to fetch it.

Recommendation:
- Run terraform init/plan in a local/container environment with access to the Terraform provider registry, or upload an offline provider plugin package into this environment.
- Ensure provider block in main.tf references bpg/proxmox and the version constraint is compatible with your Terraform registry access.

Saved outputs of terraform init and validate to help debugging.

Saved at: /app/docs/terraform_plan_witness_error_2026-02-26T12:58:05Z.md
