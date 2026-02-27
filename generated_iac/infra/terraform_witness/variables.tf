variable "pm_api_url" {}
variable "pm_api_token_id" {}
variable "pm_api_token_secret" {}

variable "target_node" { default = "192.168.10.201" }
variable "witness_name" { default = "proxmox-witness" }
variable "witness_cores" { default = 1 }
variable "witness_memory_mb" { default = 512 }
variable "witness_disk_gb" { default = 4 }
variable "storage" { default = "local" }
variable "mgmt_bridge" { default = "vmbr-mgmt" }
variable "cloud_init_user" { default = "ubuntu" }
variable "bootstrap_ssh_pubkey_path" { default = "/path/to/bootstrap.pub" }
variable "witness_ip" { default = "192.168.10.210" }
variable "gateway" { default = "192.168.10.1" }
