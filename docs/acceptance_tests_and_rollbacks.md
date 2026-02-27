Acceptance tests and rollback procedures

Witness / Quorum
- Acceptance:
  - pvecm status shows Expected votes: 3 and Quorate: Yes on both nodes.
  - corosync and qdevice logs show successful connection.
- Test:
  - Power off one node; verify cluster remains quorate and services continue.
- Rollback:
  - If witness fails, run pvecm delqdevice <ip:port> on a node and remove the witness VM.

STONITH
- Acceptance:
  - Fence operation can power-cycle a node via IPMI/BMC when invoked.
- Test:
  - Trigger fence for a node and verify cluster fences and moves HA resources as expected.
- Rollback:
  - Remove fence device from cluster and revert fencing configuration.

ZFS snapshot/replication or local-lvm backups
- Acceptance:
  - Successful vzdump backup of a VM to NFS and verified restore to a test VM.
- Test:
  - Run vzdump --dumpdir /mnt/backup --mode snapshot --compress lzo <vmid>
  - Restore on a test node and boot the test VM.
- Rollback:
  - Revert replication tasks or restore from backup.

Kubernetes
- Acceptance:
  - All control-plane nodes report Ready and kube-apiserver endpoints healthy.
  - MetalLB assigns an external IP from configured pool and the NGINX ingress is reachable from local network.
  - Hello-world service returns HTTP 200 from external IP.
- Test:
  - kubectl get nodes; kubectl get pods -A
  - curl -sS http://<metalLB-ip>/
- Rollback:
  - If control-plane bootstrap fails, destroy created control-plane VMs via Terraform state destroy and restore from VM template backups. Re-run provisioning after fixing root cause.

General notes
- Always snapshot or backup VMs before making disruptive changes.
- Document exact commands and store in /app/docs with restricted permissions.
