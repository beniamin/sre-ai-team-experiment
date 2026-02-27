Execution Instructions — Compensating Hardening Fix & Retry
Timestamp: 2026-02-26T13:40:00Z UTC
Author: Architect_Zero

Context:
- User authorized FIX_AND_RETRY_COMPENSATIONS_CONTINUE and explicitly permitted the builder to fix and retry compensating hardening actions without further permission prompts.
- Security_Sentinel previously approved compensating controls but required verification artifacts before any witness/HA actions.
- vmbr-mgmt is NOT available on the physical network; we are enforcing host-firewall compensations.

Mandatory constraints (do NOT bypass):
1) Do NOT provision witness VMs, enable HA, perform STONITH tests, or run terraform apply.
2) Do NOT write plaintext secrets into any files under /app/docs or /app/infra or /app/config. Use BOOTSTRAP_SSH_KEY only for SSH connections; other secrets must be provided via env vars or the secrets manager and never persisted.
3) Stop immediately on any failure in any play; capture full stdout/stderr and save to /app/docs with chmod 600.
4) All saved outputs produced by the builder must be chmod 600.

Developer instruction (exact steps for @DevOps_Builder — implement now):
A) Fix Ansible template rendering for firewall rules
  1) Open /app/config/ansible_proxmox_hardening/tasks/firewall.yml (or included task file) and remove raw Jinja blocks that inject admin_allowed_ips directly into YAML.
  2) Create a proper Jinja2 template at /app/config/ansible_proxmox_hardening/templates/50-proxmox-mgmt.nft.j2 that loops over admin_allowed_ips and renders one nft rule per admin IP and required ports.
  3) Update /app/config/ansible_proxmox_hardening/play_host_firewall_compensations.yml to use the template module to deploy the rendered NFT file to /etc/nftables.d/50-proxmox-mgmt.nft and then run 'nft -f /etc/nftables.d/50-proxmox-mgmt.nft' to load rules.
  4) Save a patch diff for the change to /app/docs/playbook_fix_patch_<ISO-TS>.diff before running any playbooks.

B) Run the compensating sequence (execute these ansible-playbook commands in order)
  1) Apply firewall rules (capture output):
     ansible-playbook -i "192.168.10.201,192.168.10.202," /app/config/ansible_proxmox_hardening/play_host_firewall_compensations.yml -u root --private-key="$BOOTSTRAP_SSH_KEY" --extra-vars "admin_allowed_ips=['192.168.10.211','192.168.10.10']" 2>&1 | tee /tmp/firewall_apply_run.txt
     cp /tmp/firewall_apply_run.txt /app/docs/firewall_apply_run_<ISO-TS>.md && chmod 600 /app/docs/firewall_apply_run_<ISO-TS>.md
  2) Remove/rotate bootstrap key (capture output):
     ansible-playbook -i "192.168.10.201,192.168.10.202," /app/config/ansible_proxmox_hardening/play_cleanup_bootstrap_key.yml -u root --private-key="$BOOTSTRAP_SSH_KEY" 2>&1 | tee /tmp/cleanup_bootstrap_key.txt
     cp /tmp/cleanup_bootstrap_key.txt /app/docs/cleanup_bootstrap_key_<ISO-TS>.md && chmod 600 /app/docs/cleanup_bootstrap_key_<ISO-TS>.md
  3) Verification play (capture output and per-node verify files):
     ansible-playbook -i "192.168.10.201,192.168.10.202," /app/config/ansible_proxmox_hardening/play_verify_firewall.yml -u root --private-key="$BOOTSTRAP_SSH_KEY" --extra-vars "admin_allowed_ips=['192.168.10.211','192.168.10.10']" 2>&1 | tee /tmp/firewall_verify_combined.txt
     cp /tmp/firewall_verify_combined.txt /app/docs/firewall_verify_combined_<ISO-TS>.md && chmod 600 /app/docs/firewall_verify_combined_<ISO-TS>.md
     Also ensure the play writes per-node verify files: /app/docs/firewall_verify_192.168.10.201_<ISO-TS>.md and /app/docs/firewall_verify_192.168.10.202_<ISO-TS>.md (chmod 600)

C) On any failure
  - Immediately stop further steps.
  - Save full stdout/stderr to /app/docs/issue_report_compensations_<ISO-TS>.md (chmod 600).
  - Notify Architect_Zero here with the path to the issue report.

D) After successful completion
  - Post the exact created file paths here (one per line):
    - /app/docs/playbook_fix_patch_<ISO-TS>.diff
    - /app/docs/firewall_apply_run_<ISO-TS>.md
    - /app/docs/cleanup_bootstrap_key_<ISO-TS>.md
    - /app/docs/firewall_verify_192.168.10.201_<ISO-TS>.md
    - /app/docs/firewall_verify_192.168.10.202_<ISO-TS>.md
  - Provide a 1–2 line summary: Preflight SSH: OK/FAILED; Firewall apply: OK/FAILED; Bootstrap cleanup: OK/FAILED; pvecm/corosync health: OK/FAILED; Any blockers.
  - Architect_Zero will then tag Security_Sentinel for re-review of the artifacts.

Important: This document is the single source of truth for the compensating operation authorized by the operator. Execute exactly and stop on first error.
