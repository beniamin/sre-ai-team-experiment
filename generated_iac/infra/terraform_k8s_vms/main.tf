// Terraform template for Kubernetes VMs on Proxmox (template only)
// Uses proxmox_vm_qemu resources to create control plane and worker VMs.

variable "control_plane_count" { default = 3 }

resource "proxmox_vm_qemu" "k8s_ctrl" {
  count = var.control_plane_count
  name = "k8s-ctrl-${count.index+1}"
  target_node = var.target_node
  cores = var.ctrl_cores
  memory = var.ctrl_memory_mb
  scsihw = "virtio-scsi-pci"
  network {
    model = "virtio"
    bridge = var.mgmt_bridge
  }
  disk {
    size = var.ctrl_disk_gb
    type = "scsi"
    storage = var.storage
  }
  cloud_init = true
  ciuser = var.cloud_init_user
  ssh_keys = [file(var.bootstrap_ssh_pubkey_path)]
}

resource "proxmox_vm_qemu" "k8s_worker" {
  count = var.worker_count
  name = "k8s-worker-${count.index+1}"
  target_node = var.target_node
  cores = var.worker_cores
  memory = var.worker_memory_mb
  scsihw = "virtio-scsi-pci"
  network {
    model = "virtio"
    bridge = var.workload_bridge
  }
  disk {
    size = var.worker_disk_gb
    type = "scsi"
    storage = var.storage
  }
  cloud_init = true
  ciuser = var.cloud_init_user
  ssh_keys = [file(var.bootstrap_ssh_pubkey_path)]
}
