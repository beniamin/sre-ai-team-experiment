Attempting to render NFT template to /tmp/50-proxmox-mgmt.nft and validate locally

Command: nft -c -f /tmp/50-proxmox-mgmt.nft

Result: Validation failed

stderr:
/tmp/50-proxmox-mgmt.nft:7:20-20: Error: syntax error, unexpected token
/tmp/50-proxmox-mgmt.nft:12:18-18: Error: syntax error, unexpected '['
/tmp/50-proxmox-mgmt.nft:15:5-5: Error: syntax error, unexpected '}'

Action: Aborting play to avoid loading invalid nft rules on nodes. No firewall changes applied.

Saved: /app/docs/firewall_apply_run_2026-02-26T16:56:10Z.md (chmod 600)
