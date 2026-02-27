
PLAY [Apply host-level firewall compensations on Proxmox nodes] ****************

TASK [Ensure nftables present] *************************************************
[ERROR]: Task failed: Failed to connect to the host via ssh: Host key verification failed.
Origin: /app/config/ansible_proxmox_hardening/play_host_firewall_compensations.yml:11:7

 9     proxmox_node_ips: []
10   tasks:
11     - name: Ensure nftables present
         ^ column 7

fatal: [192.168.10.201]: UNREACHABLE! => {"changed": false, "msg": "Task failed: Failed to connect to the host via ssh: Host key verification failed.", "unreachable": true}
fatal: [192.168.10.202]: UNREACHABLE! => {"changed": false, "msg": "Task failed: Failed to connect to the host via ssh: Host key verification failed.", "unreachable": true}

PLAY RECAP *********************************************************************
192.168.10.201             : ok=0    changed=0    unreachable=1    failed=0    skipped=0    rescued=0    ignored=0   
192.168.10.202             : ok=0    changed=0    unreachable=1    failed=0    skipped=0    rescued=0    ignored=0   

