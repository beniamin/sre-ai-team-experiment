
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

TASK [Validate rendered nft file syntax on target] *****************************
changed: [192.168.10.201]
changed: [192.168.10.202]

TASK [Ensure nftables includes proxmox-mgmt table (load rules)] ****************
changed: [192.168.10.201]
changed: [192.168.10.202]

TASK [Save nftables rules] *****************************************************
[ERROR]: Task failed: Module failed: non-zero return code
Origin: /app/config/ansible_proxmox_hardening/play_host_firewall_compensations.yml:51:7

49       when: nft_check.rc == 0
50
51     - name: Save nftables rules
         ^ column 7

fatal: [192.168.10.201]: FAILED! => {"changed": true, "cmd": ["nft", "list", "ruleset", ">", "/etc/nftables.conf", "||", "true"], "delta": "0:00:00.006619", "end": "2026-02-26 20:13:47.345730", "msg": "non-zero return code", "rc": 1, "start": "2026-02-26 20:13:47.339111", "stderr": "Error: syntax error, unexpected >, expecting end of file or newline or semicolon\nlist ruleset > /etc/nftables.conf || true\n             ^", "stderr_lines": ["Error: syntax error, unexpected >, expecting end of file or newline or semicolon", "list ruleset > /etc/nftables.conf || true", "             ^"], "stdout": "", "stdout_lines": []}
fatal: [192.168.10.202]: FAILED! => {"changed": true, "cmd": ["nft", "list", "ruleset", ">", "/etc/nftables.conf", "||", "true"], "delta": "0:00:00.006571", "end": "2026-02-26 20:13:47.432023", "msg": "non-zero return code", "rc": 1, "start": "2026-02-26 20:13:47.425452", "stderr": "Error: syntax error, unexpected >, expecting end of file or newline or semicolon\nlist ruleset > /etc/nftables.conf || true\n             ^", "stderr_lines": ["Error: syntax error, unexpected >, expecting end of file or newline or semicolon", "list ruleset > /etc/nftables.conf || true", "             ^"], "stdout": "", "stdout_lines": []}

PLAY RECAP *********************************************************************
192.168.10.201             : ok=6    changed=3    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   
192.168.10.202             : ok=6    changed=3    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   

