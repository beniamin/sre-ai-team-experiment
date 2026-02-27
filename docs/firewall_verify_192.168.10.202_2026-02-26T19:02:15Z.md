=== nft rules ===
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
		iif "lo" accept
		ct state established,related accept
		tcp dport 22 counter packets 0 bytes 0 drop
		tcp dport 8006 counter packets 0 bytes 0 drop
		udp dport 5404 counter packets 0 bytes 0 drop
		udp dport 5405 counter packets 0 bytes 0 drop
		iif "lo" accept
		ct state established,related accept
		tcp dport 22 counter packets 0 bytes 0 drop
		tcp dport 8006 counter packets 0 bytes 0 drop
		udp dport 5404 counter packets 0 bytes 0 drop
		udp dport 5405 counter packets 0 bytes 0 drop
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
		iif "lo" accept
		ct state established,related accept
		tcp dport 22 counter packets 0 bytes 0 drop
		tcp dport 8006 counter packets 0 bytes 0 drop
		udp dport 5404 counter packets 0 bytes 0 drop
		udp dport 5405 counter packets 0 bytes 0 drop
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
	}
}

=== pvecm status ===
Cluster information
-------------------
Name:             calotech
Config Version:   2
Transport:        knet
Secure auth:      on

Quorum information
------------------
Date:             Thu Feb 26 21:02:17 2026
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

=== corosync ===
Local node ID 2, transport knet
nodeid: 1 reachable
   LINK: 0 udp (192.168.10.202->192.168.10.201) enabled connected mtu: 1397

=== local curl ===
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>proxmox2 - Proxmox Virtual Environment</title>
    <link rel="icon" sizes="128x128" href="/pve2/images/logo-128.png" />
    <link rel="apple-touch-icon" sizes="128x128" href="/pve2/images/logo-128.png" />
    <link rel="stylesheet" type="text/css" href="/pve2/ext6/theme-crisp/resources/theme-crisp-all.css?ver=7.0.0" />
    <link rel="stylesheet" type="text/css" href="/pve2/ext6/crisp/resources/charts-all.css?ver=7.0.0" />
    <link rel="stylesheet" type="text/css" href="/pve2/fa/css/font-awesome.css" />
    <link rel="stylesheet" type="text/css" href="/pve2/font-logos/css/font-logos.css" />
    <link rel="stylesheet" type="text/css" href="/pve2/css/ext6-pve.css?ver=9.1.1" />
    <link rel="stylesheet" type="text/css" href="/pwt/css/ext6-pmx.css?ver=v5.1.2-t1763394412" />
    <link rel="stylesheet" type="text/css" media="(prefers-color-scheme: dark)" href="/pwt/themes/theme-proxmox-dark.css?ver=v5.1.2-t1763394412" />
    
    <script type='text/javascript'>
        function gettext(message) { return message; }
        function ngettext(singular, plural, count) { return count === 1 ? singular : plural; }
    </script>
    
    <script type="text/javascript" src="/pve2/ext6/ext-all.js?ver=7.0.0"></script>
    <script type="text/javascript" src="/pve2/ext6/charts.js?ver=7.0.0"></script>
    
    <script type="text/javascript" src="/pve2/js/u2f-api.js"></script>
    <script type="text/javascript" src="/qrcode.min.js"></script>
    <script type="text/javascript">
    Proxmox = {
        Setup: { auth_cookie_name: 'PVEAuthCookie' },
        defaultLang: 'en',
        NodeName: 'proxmox2',
        UserName: '',
        CSRFPreventionToken: 'null',
        ConsentText: ''
    };
    </script>
    <script type="text/javascript" src="/proxmoxlib.js?ver=v5.1.2-t1763394412"></script>
    <script type="text/javascript" src="/pve2/js/pvemanagerlib.js?ver=9.1.1"></script>
    <script type="text/javascript" src="/pve2/ext6/locale/locale-en.js?ver=7.0.0"></script>

    <script type="text/javascript">
    if (typeof(PVE) === 'undefined') PVE = {};
    Ext.History.fieldid = 'x-history-field';
    Ext.onReady(function() { Ext.create('PVE.StdWorkspace');});
    </script>

  </head>
  <body>
    <!-- Fields required for history management -->
    <form id="history-form" class="x-hidden">
    <input type="hidden" id="x-history-field"/>
    </form>
  </body>
</html>
