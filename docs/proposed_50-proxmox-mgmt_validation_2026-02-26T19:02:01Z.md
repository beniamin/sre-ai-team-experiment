/tmp/50-proxmox-mgmt.nft:7:1-2: Error: Could not process rule: Operation not permitted
table inet proxmox_mgmt {
^^
/tmp/50-proxmox-mgmt.nft:8:9-13: Error: Could not process rule: Operation not permitted
  chain input {
        ^^^^^
/tmp/50-proxmox-mgmt.nft:12:5-17: Error: Could not process rule: Operation not permitted
    iif lo accept
    ^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:13:5-39: Error: Could not process rule: Operation not permitted
    ct state established,related accept
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:17:5-49: Error: Could not process rule: Operation not permitted
    ip saddr 192.168.10.201 udp dport 5404 accept
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:18:5-49: Error: Could not process rule: Operation not permitted
    ip saddr 192.168.10.201 udp dport 5405 accept
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:20:5-49: Error: Could not process rule: Operation not permitted
    ip saddr 192.168.10.202 udp dport 5404 accept
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:21:5-49: Error: Could not process rule: Operation not permitted
    ip saddr 192.168.10.202 udp dport 5405 accept
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:25:5-47: Error: Could not process rule: Operation not permitted
    ip saddr 192.168.10.211 tcp dport 22 accept
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:26:5-49: Error: Could not process rule: Operation not permitted
    ip saddr 192.168.10.211 tcp dport 8006 accept
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:28:5-49: Error: Could not process rule: Operation not permitted
    ip saddr 192.168.10.211 tcp dport 2049 accept
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:29:5-49: Error: Could not process rule: Operation not permitted
    ip saddr 192.168.10.211 tcp dport 3260 accept
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:31:5-46: Error: Could not process rule: Operation not permitted
    ip saddr 192.168.10.10 tcp dport 22 accept
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:32:5-48: Error: Could not process rule: Operation not permitted
    ip saddr 192.168.10.10 tcp dport 8006 accept
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:34:5-48: Error: Could not process rule: Operation not permitted
    ip saddr 192.168.10.10 tcp dport 2049 accept
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:35:5-48: Error: Could not process rule: Operation not permitted
    ip saddr 192.168.10.10 tcp dport 3260 accept
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:38:5-29: Error: Could not process rule: Operation not permitted
    tcp dport 22 counter drop
    ^^^^^^^^^^^^^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:39:5-31: Error: Could not process rule: Operation not permitted
    tcp dport 8006 counter drop
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:40:5-31: Error: Could not process rule: Operation not permitted
    udp dport 5404 counter drop
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
/tmp/50-proxmox-mgmt.nft:41:5-31: Error: Could not process rule: Operation not permitted
    udp dport 5405 counter drop
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
