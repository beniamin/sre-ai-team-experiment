=== NODE: 192.168.10.201 ===

=== pvecm status ===
Cluster information
-------------------
Name:             calotech
Config Version:   2
Transport:        knet
Secure auth:      on

Quorum information
------------------
Date:             Thu Feb 26 15:22:49 2026
Quorum provider:  corosync_votequorum
Nodes:            2
Node ID:          0x00000001
Ring ID:          1.13
Quorate:          Yes

Votequorum information
----------------------
Expected votes:   2
Highest expected: 2
Total votes:      2
Quorum:           2  
Flags:            Quorate 

Membership information
----------------------
    Nodeid      Votes Name
0x00000001          1 192.168.10.201 (local)
0x00000002          1 192.168.10.202

=== corosync-cmapctl / corosync-cfgtool ===
config.reload_in_progress (u8) = 0
config.reload_status (i32) = 1
... (truncated) ...

=== systemctl status pve-cluster corosync ===
● pve-cluster.service - The Proxmox VE cluster filesystem
     Loaded: loaded (/usr/lib/systemd/system/pve-cluster.service; enabled; preset: enabled)
     Active: active (running) since Tue 2026-02-17 14:38:04 EET; 1 week 2 days ago

● corosync.service - Corosync Cluster Engine
     Loaded: loaded (/usr/lib/systemd/system/corosync.service; enabled; preset: enabled)
     Active: active (running) since Tue 2026-02-17 14:38:05 EET; 1 week 2 days ago

STDERR:
Warning: Permanently added '192.168.10.201' (ECDSA) to the list of known hosts.

=== NODE: 192.168.10.202 ===

=== pvecm status ===
Cluster information
-------------------
Name:             calotech
Config Version:   2
Transport:        knet
Secure auth:      on

Quorum information
------------------
Date:             Thu Feb 26 15:22:49 2026
Quorum provider:  corosync_votequorum
Nodes:            2
Node ID:          0x00000002
Ring ID:          1.13
Quorate:          Yes

Votequorum information
----------------------
Expected votes:   2
Highest expected: 2
Total votes:      2
Quorum:           2  
Flags:            Quorate 

Membership information
----------------------
    Nodeid      Votes Name
0x00000001          1 192.168.10.201
0x00000002          1 192.168.10.202 (local)

=== corosync-cmapctl / corosync-cfgtool ===
config.reload_in_progress (u8) = 0
config.reload_status (i32) = 1
... (truncated) ...

=== systemctl status pve-cluster corosync ===
● pve-cluster.service - The Proxmox VE cluster filesystem
     Loaded: loaded (/usr/lib/systemd/system/pve-cluster.service; enabled; preset: enabled)
     Active: active (running) since Tue 2026-02-17 14:38:04 EET; 1 week 2 days ago

● corosync.service - Corosync Cluster Engine
     Loaded: loaded (/usr/lib/systemd/system/corosync.service; enabled; preset: enabled)
     Active: active (running) since Tue 2026-02-17 14:38:05 EET; 1 week 2 days ago

STDERR:
Warning: Permanently added '192.168.10.202' (ECDSA) to the list of known hosts.
