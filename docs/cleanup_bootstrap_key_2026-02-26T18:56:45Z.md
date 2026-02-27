
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

TASK [Ensure authorized_keys permissions (avoid chgrp to prevent failures on constrained FS)] ***
ok: [192.168.10.201]
ok: [192.168.10.202]

TASK [Touch cleanup marker] ****************************************************
changed: [192.168.10.201]
changed: [192.168.10.202]

PLAY RECAP *********************************************************************
192.168.10.201             : ok=6    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
192.168.10.202             : ok=6    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

