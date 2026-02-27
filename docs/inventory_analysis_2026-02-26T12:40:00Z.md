Inventory analysis generated from /app/docs/inventory_2026-02-26T12:35:02Z.md

Nodes
- proxmox1: 192.168.10.201 (hostname from inventory)
- proxmox2: 192.168.10.202
- Proxmox VE version: 9.x (both nodes)

Corosync/Quorum
- Cluster has 2 votes (no qdevice/witness). Quorum currently held but risk of split-brain exists.
- Recommendation: Deploy qdevice/witness VM as third vote before enabling HA. If BMC/IPMI is available, configure STONITH as alternate.

Storage
- No ZFS pools detected in inventory (zpool status returned no pools). Storage: local-lvm and local directory storage present.
- For Kubernetes persistent storage, decide between deploying ZFS on VMs or using local-lvm + backup strategy. Ceph is not recommended for 2-node cluster.

Network
- Single bridge vmbr0 on 192.168.10.0/24 for management and workload traffic.
- Recommend creating a management VLAN or separate bridge to isolate corosync and Proxmox API/UI traffic from workload network.

VMs/CTs
- 1 VM template found (VMID 9000: ubuntu-k8s-template-src)
- 0 CTs

Blockers / Missing Information
- No BMC/IPMI details collected; if available, STONITH would be preferred for automated fencing.
- Network switch VLAN capability confirmation required to implement mgmt VLAN isolation.
- Decision on storage backend (ZFS replication vs local-lvm) required for Kubernetes PV planning.

Conclusion
- Proceed to provision small witness VM (Ubuntu) for qdevice; do NOT enable HA until witness validated.
- After witness, run fencing tests and then proceed with VM provisioning and Kubernetes bootstrap.
