Second attempt to apply firewall template produced an nft load error due to malformed rendered file. Collected output saved from Ansible run at 2026-02-26T13:24:30Z.

See /app/config/ansible_proxmox_hardening/templates/50-proxmox-mgmt.nft.j2 for the template used. The template rendering produced invalid nft syntax because admin_allowed_ips list items weren't quoted and the join formatting placed brackets incorrectly.

Ansible output excerpt:

/etc/nftables.d/50-proxmox-mgmt.nft:9:14-14: Error: syntax error, unexpected '['
    ip saddr [ tcp dport { 22, 8006 } accept;
             ^
... (truncated)

Next step: adjust template to render valid nftables syntax by producing per-ip rules rather than inline list constructs.
