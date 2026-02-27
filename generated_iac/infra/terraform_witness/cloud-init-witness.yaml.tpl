#cloud-config
users:
  - name: ${cloud_init_user}
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    ssh_authorized_keys:
      - ${ssh_key}
packages:
  - corosync-qnetd
runcmd:
  - [ systemctl, enable, --now, corosync-qnetd ]
  - [ mkdir, -p, /etc/corosync/qdevice.d ]
# qnetd will be used as the external qdevice daemon
