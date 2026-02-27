User Requirements Log

- Entry 1:
  - Timestamp: 2026-02-26
  - User: Unnamed
  - Description: User has installed a Proxmox cluster with 2 nodes running Proxmox VE 9.
  - Notes: No additional details provided yet (network config, storage, VMs, backups, fencing, quorum expectations, etc.).

Action items for Architect_Zero:
- Collect missing details where necessary when required by plan phases, but proceed to create an implementation plan based on a common minimal production-ready setup for a 2-node Proxmox VE 9 cluster.

- Entry 2:
  - Timestamp: 2026-02-26T00:00:00Z
  - User: Provided IPs
  - Description: User supplied Proxmox node addresses for inventory collection.
  - Node addresses:
    - 192.168.10.201
    - 192.168.10.202
  - Notes: These IPs are to be used by the builder team to SSH and run the inventory/state collection commands. Inventory output must be consolidated into /app/docs/inventory_<ISO-8601-timestamp>.md with restrictive permissions and then reported back to Architect_Zero.

- Entry 3:
  - Timestamp: 2026-02-26T13:00:00Z
  - User instruction: "always run terraform in your local container, not on the remote servers trough ssh."
  - Notes: Architect_Zero and the builder team must ensure Terraform commands (init/plan/apply) are executed from the builder's local/container environment where provider plugins can be installed and network access to provider registries exists. Terraform must never be executed by remote SSH on the Proxmox nodes. This instruction is appended to the requirements and will be enforced in the execution runbook and README files for /app/infra and /app/config.

- Entry 4:
  - Timestamp: 2026-02-26T13:05:00Z
  - User: Provided environment note
  - Description: The Proxmox nodes are connected to a TP-Link AC2300 MU-MIMO Wi-Fi Router directly. The router does not support VLANs, and so creating a dedicated management VLAN on the physical network is not possible with current hardware.
  - Implications:
    - Cannot rely on switch/VLAN segmentation to isolate the Proxmox management plane from workload/ingress networks.
    - Security_Sentinel requirement to separate management and workload networks (vmbr-mgmt) cannot be implemented via VLANs on the current router.
  - Recommended mitigation options (operator must choose one):
    1) Deploy a small managed Ethernet switch or VLAN-capable router between the Proxmox nodes and the network (recommended). This enables proper VLANs and physical isolation for vmbr-mgmt.
    2) If new hardware is not immediately available, create a software-enforced management plane using one of these alternatives (short-term, risk-accepting):
       - Use host-level firewall rules (iptables/nftables) on each Proxmox node to restrict access to management services (API/UI/SSH/corosync ports) to a limited set of admin IPs. This reduces exposure but does not protect corosync from noisy workload traffic.
       - Create a secure overlay network for management (WireGuard or OpenVPN) between admin/jump host and the Proxmox nodes, put management services bound to the VPN interface, and restrict access otherwise. This provides logical isolation at the expense of complexity.
       - Place the witness (qdevice) offsite (cloud VM) reachable only via an encrypted tunnel (WireGuard) to provide the third quorum vote without changing local router/VLANs. Ensure firewall rules restrict it to management traffic only.
    3) Accept the risk and proceed using the existing flat network (vmbr0) with explicit acknowledgement—Security_Sentinel will flag this as elevated risk and will not approve enabling HA until compensating controls are documented and accepted.
  - Action required from the user (choose one option):
    - "PROVIDE_MANAGED_SWITCH" — you will procure and connect a VLAN-capable managed switch or router so we can create vmbr-mgmt properly. Provide confirmation when ready and we will prepare the Ansible play to create vmbr-mgmt and re-run preflight.
    - "USE_HOST_FIREWALL_AND_VPN" — you accept a software-only mitigation: we will implement strict host-level firewall rules and a WireGuard overlay for the management plane. This will be treated as a temporary mitigation until hardware isolation is available.
    - "WITNESS_OFFSITE_VPN" — you prefer to place the qdevice/witness in the cloud reachable only via WireGuard, to achieve quorum without local VLANs. This still requires host firewall restrictions and careful routing.
    - "ACCEPT_RISK_FLAT_NETWORK" — you explicitly accept the elevated risk and instruct us to continue using the existing flat network (we will record this as an accepted risk and implement other compensations such as strict host firewalls, reduced attack surface, and strict secrets handling).

  - Note: Choose one option above so the builder team can proceed. If you choose a temporary software mitigation or accept the risk, Security_Sentinel will need to explicitly acknowledge/approve the compensating controls. If you choose PROVIDE_MANAGED_SWITCH, we will wait for you to confirm when hardware is in place and then proceed.

- Entry 5:
  - Timestamp: 2026-02-26T13:50:00Z
  - User decision: ACCEPT_RISK_FLAT_NETWORK
  - Notes: User accepted operating Proxmox with management and workload traffic on a single flat network (vmbr0). Compensating controls to be implemented: host firewall hardening, bootstrap-key removal/rotation, tight admin IP ACLs, secrets management, monitoring and alerting. Security_Sentinel must re-approve compensating controls before any HA enablement.

- Entry 6:
  - Timestamp: 2026-02-26T14:10:00Z
  - User input: ADMIN_JUMP_HOST_IPS: 192.168.10.211; NO_WIREGUARD
  - Notes: User provided admin jump host IP and declined WireGuard. Use this IP in firewall playbooks to allow management ports only from this host. Playbooks will be prepared and run only after the user authorizes execution or chooses to run them locally.

- Entry 7:
  - Timestamp: 2026-02-26T14:30:00Z
  - User action: ADMIN_JUMP_HOST_IPS updated
  - Description: User corrected ADMIN_JUMP_HOST_IPS to include two IPs.
  - ADMIN_JUMP_HOST_IPS: 192.168.10.211, 192.168.10.10; NO_WIREGUARD

- Entry 8:
  - Timestamp: 2026-02-26T14:40:00Z
  - User OOB plan provided: "OOB_PLAN: local on-site keyboard/monitor access available for both hosts"
  - Notes: Operator confirmed local physical console access for emergency rollback if firewall rules block management traffic.
2026-02-26T16:58:00Z - USER action: nftables installed in builder environment. Operator authorized builder to locally validate rendered nft ruleset and proceed with safe apply after Security_Sentinel review. (Recorded by Architect_Zero)

- 2026-02-26T17:55:00Z - User instruction: Use escaped double quotes in the IP nodes list.
  - Details: The operator requests that when passing IP lists into Ansible/templating/extra-vars the IP addresses be represented with escaped double quotes (e.g., proxmox_node_ips=[\"192.168.10.201\",\"192.168.10.202\"]) to ensure they are interpreted as lists of strings and to avoid Jinja/Ansible treating them as single quoted strings that iterate as characters on-target.
  - Rationale: Prevents template rendering from iterating over string characters on-target and producing malformed nft lines; aligns variable passing between controller-local render and on-target copy.
  - Action: Builder must ensure extra-vars and playbook variable handling use escaped double quotes when invoked from shell contexts or where quoting could be lost.

- Entry: 2026-02-26T19:10:00Z — Operator token: PROCEED_WITH_ESCAPED_QUOTE_RUN
  - Actor: Operator
  - Action: Per operator instruction, proceed to re-run the controller-render + privileged validation and, on successful validation, execute the safe apply sequence using escaped double-quoted array extra-vars in all ansible invocations. The builder is authorized to run the sequence now, stop on first failure, and save all artifacts to /app/docs with chmod 600.
  - Required invocation example to use (exact):
    --extra-vars "proxmox_node_ips=[\"192.168.10.201\",\"192.168.10.202\"] admin_allowed_ips=[\"192.168.10.211\",\"192.168.10.10\"]"
  - Preconditions: BOOTSTRAP_SSH_KEY readable, controller/local render to /tmp must succeed, nft binary available for privileged validation (or admin-uploaded validation present), OOB_PLAN operator on-site present.
  - Deliverables (if success):
    - /app/docs/proposed_50-proxmox-mgmt.nft
    - /app/docs/proposed_50-proxmox-mgmt_validation_<TS>.md
    - /app/docs/playbook_fix_patch_<TS>.diff
    - /app/docs/firewall_apply_run_<TS>.md
    - /app/docs/cleanup_bootstrap_key_<TS>.md
    - /app/docs/firewall_verify_192.168.10.201_<TS>.md
    - /app/docs/firewall_verify_192.168.10.202_<TS>.md
    - /app/docs/verify_pvecm_<TS>.md
  - Failure handling: On first failure save full stdout/stderr to /app/docs/issue_report_compensations_<TS>.md (chmod 600) and STOP. Report only file paths back to Architect_Zero.
  - Reviewer: @Security_Sentinel (will be tagged after artifacts are uploaded)
  - Notes: This entry enforces the escaped double-quote extra-vars convention and documents operator authorization to proceed under that convention.
- Entry: 2026-02-26T20:50:00Z - Operator request: RUN_VERIFICATION_SUMMARY
  - The operator requested a verification summary run to collect per-node nft lists, pvecm/corosync status, ss outputs, https probes from admin and workload perspectives, and proof that bootstrap key was removed from /root/.ssh/authorized_keys. The Architect_Zero coordinated this and instructed @DevOps_Builder to execute. Artifacts must be saved under /app/docs with chmod 600.
