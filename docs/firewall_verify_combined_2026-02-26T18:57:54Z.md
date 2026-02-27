
PLAY [Verify firewall and management access] ***********************************

TASK [Generate ISO timestamp for report filenames] *****************************
ok: [192.168.10.202 -> localhost]
ok: [192.168.10.201 -> localhost]

TASK [Show nftables ruleset] ***************************************************
[WARNING]: Host '192.168.10.201' is using the discovered Python interpreter at '/usr/bin/python3.13', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.19/reference_appendices/interpreter_discovery.html for more information.
ok: [192.168.10.201]
[WARNING]: Host '192.168.10.202' is using the discovered Python interpreter at '/usr/bin/python3.13', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.19/reference_appendices/interpreter_discovery.html for more information.
ok: [192.168.10.202]

TASK [Capture pvecm status] ****************************************************
ok: [192.168.10.201]
ok: [192.168.10.202]

TASK [Capture corosync status] *************************************************
ok: [192.168.10.201]
ok: [192.168.10.202]

TASK [Attempt curl to Proxmox API from local host] *****************************
ok: [192.168.10.201]
ok: [192.168.10.202]

TASK [Gather verification report] **********************************************
changed: [192.168.10.201]
changed: [192.168.10.202]

TASK [Fetch verification report to controller] *********************************
ok: [192.168.10.201]
ok: [192.168.10.202]

TASK [Write report to controller] **********************************************
changed: [192.168.10.202 -> localhost]
changed: [192.168.10.201 -> localhost]

TASK [Ensure report permissions] ***********************************************
changed: [192.168.10.201 -> localhost]
changed: [192.168.10.202 -> localhost]

TASK [Report summary] **********************************************************
ok: [192.168.10.201] => {
    "msg": "Verification report saved for 192.168.10.201"
}
ok: [192.168.10.202] => {
    "msg": "Verification report saved for 192.168.10.202"
}

PLAY RECAP *********************************************************************
192.168.10.201             : ok=10   changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
192.168.10.202             : ok=10   changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

