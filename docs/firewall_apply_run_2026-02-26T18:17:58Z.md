
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
ok: [192.168.10.201]
ok: [192.168.10.202]

TASK [Validate rendered nft file syntax on target] *****************************
changed: [192.168.10.201]
changed: [192.168.10.202]

TASK [Ensure nftables includes proxmox-mgmt table (load rules)] ****************
changed: [192.168.10.201]
changed: [192.168.10.202]

TASK [Save nftables rules] *****************************************************
changed: [192.168.10.201]
changed: [192.168.10.202]

TASK [Reload nftables] *********************************************************
changed: [192.168.10.201]
changed: [192.168.10.202]

TASK [Verify management ports are only accessible from admin IPs (local check)] ***
ok: [192.168.10.201]
ok: [192.168.10.202]

TASK [Output local port listeners] *********************************************
ok: [192.168.10.201] => {
    "ss_out.stdout_lines": [
        "LISTEN 0      128          0.0.0.0:22        0.0.0.0:*    users:((\"sshd\",pid=885,fd=6))                                                                                                                    ",
        "LISTEN 0      128             [::]:22           [::]:*    users:((\"sshd\",pid=885,fd=7))                                                                                                                    ",
        "LISTEN 0      4096               *:8006            *:*    users:((\"pveproxy worker\",pid=1712600,fd=6),(\"pveproxy worker\",pid=1712599,fd=6),(\"pveproxy worker\",pid=1712598,fd=6),(\"pveproxy\",pid=1101,fd=6))"
    ]
}
ok: [192.168.10.202] => {
    "ss_out.stdout_lines": [
        "LISTEN 0      128           0.0.0.0:22        0.0.0.0:*    users:((\"sshd\",pid=820,fd=6))                                                                                                                    ",
        "LISTEN 0      128              [::]:22           [::]:*    users:((\"sshd\",pid=820,fd=7))                                                                                                                    ",
        "LISTEN 0      4096                *:8006            *:*    users:((\"pveproxy worker\",pid=1476621,fd=6),(\"pveproxy worker\",pid=1476620,fd=6),(\"pveproxy worker\",pid=1476618,fd=6),(\"pveproxy\",pid=1101,fd=6))"
    ]
}

TASK [Report firewall applied marker] ******************************************
changed: [192.168.10.201]
changed: [192.168.10.202]

PLAY RECAP *********************************************************************
192.168.10.201             : ok=11   changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
192.168.10.202             : ok=11   changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

