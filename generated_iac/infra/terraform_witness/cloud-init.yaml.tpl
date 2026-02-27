#cloud-config
packages:
  - corosync
  - corosync-qnetd
runcmd:
  - systemctl enable --now corosync-qnetd || true
  - echo "qnetd started" > /var/log/qnetd-install.log
# Users and ssh keys will be templated by Terraform/Ansible when rendering cloud-init
