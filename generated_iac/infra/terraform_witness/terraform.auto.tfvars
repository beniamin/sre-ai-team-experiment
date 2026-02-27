name = "qdevice-witness"
target_node = "192.168.10.201"
cores = 1
memory = 512
disk_gb = 4
storage = "local"
network_bridge = "vmbr0"
iso = "local:iso/ubuntu-24.04-server.iso"
# witness_ip_placeholder should be updated after provisioning or use cloud-init to obtain IP
