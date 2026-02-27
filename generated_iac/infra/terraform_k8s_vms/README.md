Terraform templates for Kubernetes VMs on Proxmox

This directory contains template Terraform configurations to create Kubernetes control-plane and worker VMs on Proxmox.

Important:
- Do NOT include secrets in these files. Use environment variables (TF_VAR_pm_api_*) or a secrets manager to inject credentials.
- Ensure you have a management bridge vmbr-mgmt available before assigning control-plane NICs to it.
- The provider should be the bpg/proxmox provider version compatible with Proxmox VE 9.

Usage:
1. Review variables.tf and set values in an example.tfvars file.
2. Export TF_VAR_pm_api_token_id and TF_VAR_pm_api_token_secret or set them in your environment.
3. terraform init
4. terraform plan -var-file=example.tfvars

Do NOT terraform apply until you have completed witness/STONITH verification and have Security_Sentinel approval.
