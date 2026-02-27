Render command executed on builder controller:
ansible localhost -m template -a "src=/app/config/ansible_proxmox_hardening/templates/50-proxmox-mgmt.nft.j2 dest=/tmp/50-proxmox-mgmt.nft" --extra-vars "admin_allowed_ips=['192.168.10.211','192.168.10.10'] node_ips=['192.168.10.201','192.168.10.202']"

Render result: /tmp/50-proxmox-mgmt.nft created and copied to /app/docs/proposed_50-proxmox-mgmt.nft

Validation command attempted:
nft -c -f /tmp/50-proxmox-mgmt.nft
Validation result: nft binary not found in this environment (exit code 127). See /app/docs/proposed_50-proxmox-mgmt_validation_2026-02-26T16:58:00Z.md for details.

Next steps: Operator must validate /app/docs/proposed_50-proxmox-mgmt.nft locally on a machine with nft present and upload the validation output and then authorize remote apply.
