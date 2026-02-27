Quorum & Fencing Plan — 2026-02-26T13:30:00Z

Summary
- Based on inventory, no BMC details were found. Preferred quorum approach: provision a QDevice/witness VM on a dedicated management VLAN. If BMC/IPMI access is provided later, STONITH playbooks are available as an alternative.

Mandatory controls (enforced in artifacts)
1) Management network: witness VM and corosync traffic MUST be on a dedicated management VLAN/bridge (vmbr-mgmt). All artifacts create/configure vmbr-mgmt or document how to tag the witness VM to the mgmt VLAN.
2) HA gating: All automation/playbooks include a gating variable `enable_ha` (default: false). Any task that would enable HA will check:
   - Either: qdevice registered AND `pvecm status` shows 3 votes, OR
   - STONITH configured and fencing test passed.
   If neither condition is true, the playbook will fail and not enable HA.
3) STONITH: If BMC creds are provided, the STONITH playbook (templated) will configure fence-agents on both nodes and run an idempotent dry-run followed by an operator-confirmed destructive test (with explicit confirmation prompt).

QDevice (preferred) provisioning steps (high level)
- Provision a small Ubuntu 22.04/24.04 VM on mgmt VLAN (1 vCPU, 512–1024MB RAM, 4GB disk), IP reserved from mgmt network (example: 192.168.20.210).
- cloud-init: install corosync-qnetd and enable service. Use the provided cloud-init template in /app/infra/terraform_witness/cloud-init.yaml.
- Register qnetd with corosync-qdevice on the cluster nodes using `pvecm qdevice setup ...` steps included in the play_qdevice_register.yml.

Verification commands (must succeed before enabling HA)
- pvecm status
  - Expected: Quorum: 3 nodes
  - corosync-cmapctl or corosync-cfgtool -s to show qdevice status
- Example: pvecm status | grep -A2 'Quorum' should show vote count 3.

STONITH (if BMC present)
- Playbook will install fence-agents and configure /etc/fence.d/ scripts. Requires BMC IP/user/credential in secrets manager. Includes idempotent verify_fence action that queries power status, and an operator-only `perform_fence` action that will power-cycle a node when confirmed.
- Acceptance test: in a maintenance window, trigger `perform_fence` against one node and verify cluster correctly fences and VMs failover according to HA policies.

Network and firewall notes
- Witness VM must be reachable from both nodes over mgmt VLAN for corosync-qnetd (TCP/5405 or as configured).
- Update Ansible to create vmbr-mgmt and apply firewall rules restricting Proxmox ports (8006, 22, corosync ports) to admin IP range only.

Secrets
- PROXMOX_API_TOKEN, BOOTSTRAP_SSH_KEY (path), BMC credentials (if used) must be stored in the secrets manager. Playbooks reference these via vault variables; they MUST NOT be committed in plaintext.

DO NOT enable HA until verification commands above pass.
