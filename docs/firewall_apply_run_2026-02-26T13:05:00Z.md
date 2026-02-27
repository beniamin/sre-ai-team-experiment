[ERROR]: YAML parsing failed: While scanning for the next token found character that cannot start any token.
Origin: /app/config/ansible_proxmox_hardening/play_host_firewall_compensations.yml:35:2

33               # allow established
34               ct state established,related accept;
35 {% for ip in admin_allowed_ips %}
    ^ column 2

