Validation attempted on builder controller, but nft binary not present in this environment.
Command run: nft -c -f /tmp/50-proxmox-mgmt.nft
Result: nft: not found (exit code 127)

Because the builder/container has no nft utility, local validation could not be performed here. The rendered file is saved as /app/docs/proposed_50-proxmox-mgmt.nft for offline/local validation by the operator in an environment with nft available.

Next steps:
- Please copy /app/docs/proposed_50-proxmox-mgmt.nft to a machine with nft installed and run:
  nft -c -f /path/to/proposed_50-proxmox-mgmt.nft
- If validation succeeds, save the validation output to /app/docs/proposed_50-proxmox-mgmt_validation_<TS>.md (chmod 600) and upload. Then I will proceed with apply steps under Authorization.
