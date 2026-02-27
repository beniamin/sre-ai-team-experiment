Ansible playbook run output (firewall apply) captured at 2026-02-26T13:12:02Z

Output:

PLAY [Apply host-level firewall compensations on Proxmox nodes] ****************

TASK [Ensure nftables present] *************************************************
ok: [192.168.10.201]
ok: [192.168.10.202]

TASK [Ensure nftables service enabled and started] *****************************
changed: [192.168.10.201]
changed: [192.168.10.202]

TASK [Render nftables management table from template] **************************
[ERROR]: Task failed: Module failed: Destination directory /etc/nftables.d does not exist

fatal: [192.168.10.201]: FAILED! => {"changed": false, "checksum": "4314d0ccb182a634d284a48b7f18279855866ac8", "msg": "Destination directory /etc/nftables.d does not exist"}
fatal: [192.168.10.202]: FAILED! => {"changed": false, "checksum": "4314d0ccb182a634d284a48b7f18279855866ac8", "msg": "Destination directory /etc/nftables.d does not exist"}

PLAY RECAP *********************************************************************
192.168.10.201             : ok=2    changed=1    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   
192.168.10.202             : ok=2    changed=1    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   
