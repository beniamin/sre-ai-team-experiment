// Terraform template for Proxmox witness VM (template only)
// NOTE: Do NOT include secrets here. Inject PROXMOX API token via TF_VAR_pm_api_* environment variables.
// Use the bpg/proxmox provider which is compatible with Proxmox VE 9+.

terraform {
  required_providers {
    proxmox = {
      source = "bpg/proxmox"
      version = ">= 0.1, < 2.0"
    }
  }
}

provider "proxmox" {
  # The operator must set TF_VAR_pm_api_url, TF_VAR_pm_api_token_id, TF_VAR_pm_api_token_secret
  # or configure provider auth via environment before running terraform.
  # pm_api_url      = var.pm_api_url
  # pm_api_token_id = var.pm_api_token_id
  # pm_api_token_secret = var.pm_api_token_secret
}

resource "proxmox_vm_qemu" "witness" {
  name = var.witness_name
  target_node = var.target_node

  cores  = var.witness_cores
  sockets = 1
  memory = var.witness_memory_mb

  scsihw = "virtio-scsi-pci"

  network {
    model = "virtio"
    bridge = var.mgmt_bridge // e.g. "vmbr-mgmt"
  }

  disk {
    size = var.witness_disk_gb
    type = "scsi"
    storage = var.storage
  }

  cloud_init = true
  ciuser = var.cloud_init_user
  ssh_keys = [file(var.bootstrap_ssh_pubkey_path)]
  ipconfig0 = "ip=${var.witness_ip}/24,gw=${var.gateway}"
}
