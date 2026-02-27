variable "pm_api_url" {}
variable "pm_api_token_id" {}
variable "pm_api_token_secret" {}

variable "target_node" { default = "192.168.10.201" }
variable "ctrl_cores" { default = 2 }
variable "ctrl_memory_mb" { default = 2048 }
variable "ctrl_disk_gb" { default = 16 }
variable "worker_count" { default = 2 }
variable "worker_cores" { default = 2 }
variable "worker_memory_mb" { default = 2048 }
variable "worker_disk_gb" { default = 16 }
variable "storage" { default = "local-lvm" }
variable "bootstrap_ssh_pubkey_path" { default = "/path/to/bootstrap.pub" }
variable "cloud_init_user" { default = "ubuntu" }
variable "mgmt_bridge" { default = "vmbr-mgmt" }
variable "workload_bridge" { default = "vmbr0" }
