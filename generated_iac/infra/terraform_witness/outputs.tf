output "witness_vm_id" {
  value = proxmox_vm_qemu.witness.id
}

output "witness_ip" {
  value = var.witness_ip
}
