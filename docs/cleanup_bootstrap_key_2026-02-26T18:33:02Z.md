
PLAY [Remove bootstrap SSH key and rotate temporary automation keys] ***********

TASK [Read root authorized_keys if present] ************************************
[WARNING]: Host '192.168.10.201' is using the discovered Python interpreter at '/usr/bin/python3.13', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.19/reference_appendices/interpreter_discovery.html for more information.
ok: [192.168.10.201]
[WARNING]: Host '192.168.10.202' is using the discovered Python interpreter at '/usr/bin/python3.13', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.19/reference_appendices/interpreter_discovery.html for more information.
ok: [192.168.10.202]

TASK [Decode authorized_keys] **************************************************
ok: [192.168.10.201]
ok: [192.168.10.202]

TASK [Remove bootstrap key lines from authorized_keys] *************************
ok: [192.168.10.201]
ok: [192.168.10.202]

TASK [Ensure permissions on .ssh] **********************************************
ok: [192.168.10.201]
ok: [192.168.10.202]

TASK [Ensure authorized_keys permissions] **************************************
[ERROR]: Task failed: Module failed: chgrp failed
Origin: /app/config/ansible_proxmox_hardening/play_cleanup_bootstrap_key.yml:37:7

35       become: true
36
37     - name: Ensure authorized_keys permissions
         ^ column 7

fatal: [192.168.10.201]: FAILED! => {"changed": false, "gid": 33, "group": "www-data", "mode": "0600", "msg": "chgrp failed", "owner": "root", "path": "/etc/pve/priv/authorized_keys", "size": 2495, "state": "file", "uid": 0}
fatal: [192.168.10.202]: FAILED! => {"changed": false, "gid": 33, "group": "www-data", "mode": "0600", "msg": "chgrp failed", "owner": "root", "path": "/etc/pve/priv/authorized_keys", "size": 2495, "state": "file", "uid": 0}

PLAY RECAP *********************************************************************
192.168.10.201             : ok=4    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   
192.168.10.202             : ok=4    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   

