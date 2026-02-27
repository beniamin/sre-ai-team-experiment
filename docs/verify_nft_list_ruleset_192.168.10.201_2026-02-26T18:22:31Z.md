table inet filter {
	chain input {
		type filter hook input priority filter; policy accept;
	}

	chain forward {
		type filter hook forward priority filter; policy accept;
	}

	chain output {
		type filter hook output priority filter; policy accept;
	}
}
table inet proxmox_mgmt {
	chain input {
		type filter hook input priority filter; policy accept;
		iif "lo" accept
		ct state established,related accept
		ip saddr 192.168.10.201 udp dport 5404 accept
		ip saddr 192.168.10.201 udp dport 5405 accept
		ip saddr 192.168.10.202 udp dport 5404 accept
		ip saddr 192.168.10.202 udp dport 5405 accept
		ip saddr 192.168.10.211 tcp dport 22 accept
		ip saddr 192.168.10.211 tcp dport 8006 accept
		ip saddr 192.168.10.211 tcp dport 2049 accept
		ip saddr 192.168.10.211 tcp dport 3260 accept
		ip saddr 192.168.10.10 tcp dport 22 accept
		ip saddr 192.168.10.10 tcp dport 8006 accept
		ip saddr 192.168.10.10 tcp dport 2049 accept
		ip saddr 192.168.10.10 tcp dport 3260 accept
		tcp dport 22 counter packets 0 bytes 0 drop
		tcp dport 8006 counter packets 0 bytes 0 drop
		udp dport 5404 counter packets 0 bytes 0 drop
		udp dport 5405 counter packets 0 bytes 0 drop
		... (truncated duplicate entries)
	}
}
exit:0

STDERR:
Warning: Permanently added '192.168.10.201' (ECDSA) to the list of known hosts.
