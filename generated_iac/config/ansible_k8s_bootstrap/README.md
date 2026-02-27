Ansible playbooks to bootstrap Kubernetes HA cluster

Prerequisites:
- Control-plane and worker VMs provisioned and reachable.
- Management network (vmbr-mgmt) configured for control-plane NICs.
- Secrets (kubeadm cert key, tokens) stored in Vault/Ansible Vault.

Important gating variables:
- enable_ha: false (must be set true to perform HA bootstrap)

MetalLB:
- Provide a metallb_ip_pool variable that is on the workload network and not overlapping the mgmt VLAN or Proxmox management IPs.

PV strategy:
- This playbook currently contains a placeholder. Decide on a PV strategy (ZFS CSI on node pools, NFS, or local path) and update the playbooks accordingly.

Execution:
1) Run play_os_prep.yml against all k8s hosts.
2) Once OS prep done and images are ready, set enable_ha: true and run play_kube_bootstrap.yml from control host with required secrets injected.
3) Verify nodes with kubectl get nodes and MetalLB by assigning a service of type LoadBalancer and testing ingress.

Secrets management:
- Do not store tokens/certs in repository. Use Ansible Vault or external secrets manager and reference variables in the playbooks.
