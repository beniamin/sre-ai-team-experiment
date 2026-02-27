Quorum & Fencing Plan (generated)

Summary
- Preferred: QDevice / witness VM (lightweight Ubuntu VM running corosync-qnetd) acting as external third vote for a 2-node cluster. This avoids requiring BMC access.
- Alternative: STONITH via BMC/IPMI if BMC credentials are available for both nodes.

Preferred option: QDevice (witness VM)
- Provision a small Ubuntu 22.04/24.04 VM (512MB RAM, 1 vCPU, 8GB disk) on the management network, e.g., 192.168.10.210.
- Install corosync-qnetd on the witness and start the service.
- On each Proxmox node, run: pvecm addqdevice 192.168.10.210:5402
- Verify: pvecm status should show 3 votes and qdevice registered.

Detailed steps (witness)
1) Provision witness VM (Terraform module in /app/infra/terraform_witness). Assign static IP on management network.
2) Install corosync-qnetd (via cloud-init or Ansible). Ensure TCP port 5402 is open between nodes and witness.
3) On each proxmox node, run: pvecm addqdevice 192.168.10.210:5402
4) Verify: pvecm status
   Expected: "Quorum information
   Node ID: 1
   Expected votes: 3
   Quorate: Yes"
5) Do not enable HA until verification steps pass on both nodes.

Alternative: STONITH via BMC
- If BMC credentials exist for both nodes, configure fence agents and add fence devices to cluster.
- Use fence_ipmilan or other appropriate fence agent and test with fence-plugins.
- Acceptance test: simulate host power off; cluster should fence and release resources.

Acceptance criteria
- pvecm status reports 3 votes and quorate.
- Fencing test (stonith) simulates failure and cluster recovers as expected.
- Only after above are validated may HA be enabled.

Notes
- Do NOT enable HA or automatic failover until witness or STONITH is validated.
- Witness VM should be hosted outside the two-node cluster if possible (e.g., management host, cloud, or another network segment) to avoid simultaneous failures.
