Quorum & Fencing Plan — 2026-02-26T12:40:30Z

Executive summary
- Recommendation: Deploy an external QDevice/witness VM (preferred) to provide a third vote for corosync. This is the safest option when BMC/IPMI fencing is not available.
- Alternative: If reliable BMC/IPMI is available on both nodes, configure STONITH fencing agents and test them. Only enable HA after a successful STONITH acceptance test.
- Do NOT enable Proxmox HA (pve-ha-manager) or automatic failover until one of these is validated.

Preferred option — QDevice witness VM (recommended)
1) Witness VM placement options (choose one):
   - External cloud VM on a small instance (e.g., t2.nano/equivalent) reachable over management network
   - On-prem management host outside the two-node cluster (recommended separate physical host or a third node)
   - As a last resort, a small VM on the same Proxmox cluster (creates bootstrap dependency; acceptable for testing but not ideal for production)

2) Witness VM requirements
   - OS: Ubuntu 24.04 LTS or Debian 12/13
   - CPU: 1 vCPU
   - RAM: 256–512 MB
   - Disk: minimal (2 GB)
   - Network: management VLAN reachable by both Proxmox nodes

3) Terraform (witness) — high level
   - Use /app/infra/terraform_witness/ to provision VM (provider: bpg/proxmox if on-site, or cloud provider block if external)
   - Example variables: witness_name, vm_cpus, vm_memory, vm_disk_gb, network_bridge
   - After VM provision, run the qnetd service and register as corosync qdevice.

4) QDevice installation & registration (on witness VM)
   - Install qnetd (corosync-qnetd):
     sudo apt-get update && sudo apt-get install -y corosync-qnetd
   - Configure qnetd to listen on management IP (default port 5406)
   - Start qnetd service: sudo systemctl enable --now corosync-qnetd

5) Register QDevice on Proxmox cluster (run on one Proxmox node)
   - Install corosync-qdevice on cluster nodes if not present: apt-get install -y corosync-qdevice
   - Add the qdevice to the cluster:
     pvecm qdevice setup root@<QDEVICE_IP>
   - Verify qdevice status and quorum: pvecm status
   - Expected pvecm status shows Expected votes: 3 and Quorum: 2 (or Quorum reports 3 votes with highest expected 3)

6) Verification steps
   - Before enabling HA, confirm: pvecm status shows 3 expected votes and cluster is quorate with qdevice present.
   - Simulate network partition of one Proxmox node and verify cluster maintains quorum correctly (document test procedure in acceptance tests).

Alternative option — STONITH via BMC/IPMI
1) Pre-reqs
   - BMC (IPMI/iLO/iDRAC) reachable and credentials available for both nodes.
   - ipmitool available on an admin host or installed via Ansible.

2) Acceptance of STONITH requirement
   - Configure fencing agents in Proxmox and test by forcing a node to power off via IPMI and verifying that the other node fences it and recovers resources.

3) Example fencing test procedure
   - Use ipmitool to power-cycle the target node: ipmitool -I lanplus -H <bmc_ip> -U <user> -P <pass> chassis power cycle
   - Confirm Proxmox cluster notices the node is unreachable and that the fenced node is powered off via BMC.
   - Verify HA decisions and resource failover behavior.

Hard prohibition
- DO NOT enable automatic HA resource start or pve-ha-manager until either QDevice witness is validated OR STONITH tests pass successfully.

Next steps
- I will generate Terraform templates for the witness VM under /app/infra/terraform_witness/ and Ansible playbooks to register the qdevice or configure BMC fencing under /app/config/ansible_proxmox_hardening/.

Prepared-by: DevOps_Builder
