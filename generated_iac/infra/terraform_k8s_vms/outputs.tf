output "control_plane_names" {
  value = [for vm in proxmox_vm_qemu.k8s_ctrl : vm.name]
}

output "worker_names" {
  value = [for vm in proxmox_vm_qemu.k8s_worker : vm.name]
}
