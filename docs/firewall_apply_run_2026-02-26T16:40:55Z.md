
PLAY [Apply host-level firewall compensations on Proxmox nodes] ****************

TASK [Ensure nftables present] *************************************************
[WARNING]: Host '192.168.10.201' is using the discovered Python interpreter at '/usr/bin/python3.13', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.19/reference_appendices/interpreter_discovery.html for more information.
ok: [192.168.10.201]
[WARNING]: Host '192.168.10.202' is using the discovered Python interpreter at '/usr/bin/python3.13', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.19/reference_appendices/interpreter_discovery.html for more information.
ok: [192.168.10.202]

TASK [Ensure nftables service enabled and started] *****************************
ok: [192.168.10.201]
ok: [192.168.10.202]

TASK [Ensure /etc/nftables.d exists] *******************************************
ok: [192.168.10.201]
ok: [192.168.10.202]

TASK [Render nftables management table from template] **************************
changed: [192.168.10.201]
changed: [192.168.10.202]

TASK [Validate rendered nft file syntax on controller] *************************
[ERROR]: Task failed: Module failed: Error executing command: [Errno 2] No such file or directory: b'nft'
Origin: /app/config/ansible_proxmox_hardening/play_host_firewall_compensations.yml:38:7

36       become: true
37
38     - name: Validate rendered nft file syntax on controller
         ^ column 7

fatal: [192.168.10.202 -> localhost]: FAILED! => {"changed": false, "cmd": "nft -c -f /etc/nftables.d/50-proxmox-mgmt.nft", "failed_when_result": true, "msg": "Error executing command.", "rc": 2, "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}
fatal: [192.168.10.201 -> localhost]: FAILED! => {"changed": false, "cmd": "nft -c -f /etc/nftables.d/50-proxmox-mgmt.nft", "failed_when_result": true, "msg": "Error executing command.", "rc": 2, "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}

PLAY RECAP *********************************************************************
192.168.10.201             : ok=4    changed=1    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   
192.168.10.202             : ok=4    changed=1    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   

