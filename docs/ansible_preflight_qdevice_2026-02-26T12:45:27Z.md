Ansible preflight qdevice check: 2026-02-26T12:45:27Z

== 192.168.10.201 pvecm status ==
COMMAND: pvecm status
Cluster information
-------------------
Name:             calotech
Config Version:   2
Transport:        knet
Secure auth:      on

Quorum information
------------------
Date:             Thu Feb 26 14:45:28 2026
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

== 192.168.10.201 corosync ==
COMMAND: corosync-cmapctl
config.reload_in_progress (u8) = 0
config.reload_status (i32) = 1
config.totemconfig_reload_in_progress (u8) = 0
internal_configuration.service.0.name (str) = corosync_cmap
internal_configuration.service.0.ver (u32) = 0
internal_configuration.service.1.name (str) = corosync_cfg
internal_configuration.service.1.ver (u32) = 0
internal_configuration.service.2.name (str) = corosync_cpg
internal_configuration.service.2.ver (u32) = 0
internal_configuration.service.3.name (str) = corosync_quorum
internal_configuration.service.3.ver (u32) = 0
internal_configuration.service.4.name (str) = corosync_pload
internal_configuration.service.4.ver (u32) = 0
internal_configuration.service.5.name (str) = corosync_votequorum
internal_configuration.service.5.ver (u32) = 0
internal_configuration.service.6.name (str) = corosync_mon
internal_configuration.service.6.ver (u32) = 0
internal_configuration.service.7.name (str) = corosync_wd
internal_configuration.service.7.ver (u32) = 0
logging.debug (str) = off
logging.to_syslog (str) = yes
nodelist.local_node_pos (u32) = 0
nodelist.node.0.name (str) = proxmox1
nodelist.node.0.nodeid (u32) = 1
nodelist.node.0.quorum_votes (u32) = 1
nodelist.node.0.ring0_addr (str) = 192.168.10.201
nodelist.node.1.name (str) = proxmox2
nodelist.node.1.nodeid (u32) = 2
nodelist.node.1.quorum_votes (u32) = 1
nodelist.node.1.ring0_addr (str) = 192.168.10.202
quorum.provider (str) = corosync_votequorum
resources.system.load_15min.current (dbl) = 0.000000
resources.system.load_15min.last_updated (u64) = 0
resources.system.load_15min.poll_period (u64) = 3000
resources.system.load_15min.state (str) = stopped
resources.system.memory_used.current (i32) = 0
resources.system.memory_used.last_updated (u64) = 0
resources.system.memory_used.poll_period (u64) = 3000
resources.system.memory_used.state (str) = stopped
resources.watchdog_timeout (u32) = 6
runtime.blackbox.dump_flight_data (str) = no
runtime.blackbox.dump_state (str) = no
runtime.config.totem.block_unlisted_ips (u32) = 1
runtime.config.totem.cancel_token_hold_on_retransmit (u32) = 0
runtime.config.totem.consensus (u32) = 3600
runtime.config.totem.downcheck (u32) = 1000
runtime.config.totem.fail_recv_const (u32) = 2500
runtime.config.totem.heartbeat_failures_allowed (u32) = 0
runtime.config.totem.hold (u32) = 561
runtime.config.totem.interface.0.knet_ping_interval (u32) = 750
runtime.config.totem.interface.0.knet_ping_timeout (u32) = 1500
runtime.config.totem.join (u32) = 50
runtime.config.totem.knet_compression_level (i32) = 0
runtime.config.totem.knet_compression_model (str) = none
runtime.config.totem.knet_compression_threshold (u32) = 0
runtime.config.totem.knet_mtu (u32) = 0
runtime.config.totem.knet_pmtud_interval (u32) = 30
runtime.config.totem.max_messages (u32) = 17
runtime.config.totem.max_network_delay (u32) = 50
runtime.config.totem.merge (u32) = 200
runtime.config.totem.miss_count_const (u32) = 5
runtime.config.totem.send_join (u32) = 0
runtime.config.totem.seqno_unchanged_const (u32) = 30
runtime.config.totem.token (u32) = 3000
runtime.config.totem.token_retransmit (u32) = 714
runtime.config.totem.token_retransmits_before_loss_const (u32) = 4
runtime.config.totem.token_warning (u32) = 75
runtime.config.totem.window_size (u32) = 50
runtime.force_gather (str) = no
runtime.members.1.config_version (u64) = 2
runtime.members.1.ip (str) = r(0) ip(192.168.10.201) 
runtime.members.1.join_count (u32) = 1
runtime.members.1.status (str) = joined
runtime.members.2.config_version (u64) = 2
runtime.members.2.ip (str) = r(0) ip(192.168.10.202) 
runtime.members.2.join_count (u32) = 1
runtime.members.2.status (str) = joined
runtime.services.cfg.0.rx (u64) = 0
runtime.services.cfg.0.tx (u64) = 0
runtime.services.cfg.1.rx (u64) = 0
runtime.services.cfg.1.tx (u64) = 0
runtime.services.cfg.2.rx (u64) = 0
runtime.services.cfg.2.tx (u64) = 0
runtime.services.cfg.3.rx (u64) = 1
runtime.services.cfg.3.tx (u64) = 1
runtime.services.cfg.4.rx (u64) = 0
runtime.services.cfg.4.tx (u64) = 0
runtime.services.cfg.service_id (u16) = 1
runtime.services.cmap.0.rx (u64) = 4
runtime.services.cmap.0.tx (u64) = 3
runtime.services.cmap.service_id (u16) = 0
runtime.services.cpg.0.rx (u64) = 4
runtime.services.cpg.0.tx (u64) = 2
runtime.services.cpg.1.rx (u64) = 0
runtime.services.cpg.1.tx (u64) = 0
runtime.services.cpg.2.rx (u64) = 1
runtime.services.cpg.2.tx (u64) = 1
runtime.services.cpg.3.rx (u64) = 2420343
runtime.services.cpg.3.tx (u64) = 1224149
runtime.services.cpg.4.rx (u64) = 0
runtime.services.cpg.4.tx (u64) = 0
runtime.services.cpg.5.rx (u64) = 3
runtime.services.cpg.5.tx (u64) = 2
runtime.services.cpg.6.rx (u64) = 0
runtime.services.cpg.6.tx (u64) = 0
runtime.services.cpg.service_id (u16) = 2
runtime.services.mon.service_id (u16) = 6
runtime.services.pload.0.rx (u64) = 0
runtime.services.pload.0.tx (u64) = 0
runtime.services.pload.1.rx (u64) = 0
runtime.services.pload.1.tx (u64) = 0
runtime.services.pload.service_id (u16) = 4
runtime.services.quorum.service_id (u16) = 3
runtime.services.votequorum.0.rx (u64) = 9
runtime.services.votequorum.0.tx (u64) = 6
runtime.services.votequorum.1.rx (u64) = 1
runtime.services.votequorum.1.tx (u64) = 1
runtime.services.votequorum.2.rx (u64) = 0
runtime.services.votequorum.2.tx (u64) = 0
runtime.services.votequorum.3.rx (u64) = 0
runtime.services.votequorum.3.tx (u64) = 0
runtime.services.votequorum.service_id (u16) = 5
runtime.services.wd.service_id (u16) = 7
runtime.votequorum.atb_type (u32) = 0
runtime.votequorum.ev_barrier (u32) = 2
runtime.votequorum.highest_node_id (u32) = 2
runtime.votequorum.lowest_node_id (u32) = 1
runtime.votequorum.this_node_id (u32) = 1
runtime.votequorum.two_node (u8) = 0
totem.cluster_name (str) = calotech
totem.config_version (u64) = 2
totem.ip_version (str) = ipv4-6
totem.link_mode (str) = passive
totem.secauth (str) = on
totem.version (u32) = 2

== 192.168.10.202 pvecm status ==
COMMAND: pvecm status
Cluster information
-------------------
Name:             calotech
Config Version:   2
Transport:        knet
Secure auth:      on

Quorum information
------------------
Date:             Thu Feb 26 14:45:30 2026
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

== 192.168.10.202 corosync ==
COMMAND: corosync-cmapctl
internal_configuration.service.0.name (str) = corosync_cmap
internal_configuration.service.0.ver (u32) = 0
internal_configuration.service.1.name (str) = corosync_cfg
internal_configuration.service.1.ver (u32) = 0
internal_configuration.service.2.name (str) = corosync_cpg
internal_configuration.service.2.ver (u32) = 0
internal_configuration.service.3.name (str) = corosync_quorum
internal_configuration.service.3.ver (u32) = 0
internal_configuration.service.4.name (str) = corosync_pload
internal_configuration.service.4.ver (u32) = 0
internal_configuration.service.5.name (str) = corosync_votequorum
internal_configuration.service.5.ver (u32) = 0
internal_configuration.service.6.name (str) = corosync_mon
internal_configuration.service.6.ver (u32) = 0
internal_configuration.service.7.name (str) = corosync_wd
internal_configuration.service.7.ver (u32) = 0
logging.debug (str) = off
logging.to_syslog (str) = yes
nodelist.local_node_pos (u32) = 1
nodelist.node.0.name (str) = proxmox1
nodelist.node.0.nodeid (u32) = 1
nodelist.node.0.quorum_votes (u32) = 1
nodelist.node.0.ring0_addr (str) = 192.168.10.201
nodelist.node.1.name (str) = proxmox2
nodelist.node.1.nodeid (u32) = 2
nodelist.node.1.quorum_votes (u32) = 1
nodelist.node.1.ring0_addr (str) = 192.168.10.202
quorum.provider (str) = corosync_votequorum
resources.system.load_15min.current (dbl) = 0.000000
resources.system.load_15min.last_updated (u64) = 0
resources.system.load_15min.poll_period (u64) = 3000
resources.system.load_15min.state (str) = stopped
resources.system.memory_used.current (i32) = 0
resources.system.memory_used.last_updated (u64) = 0
resources.system.memory_used.poll_period (u64) = 3000
resources.system.memory_used.state (str) = stopped
resources.watchdog_timeout (u32) = 6
runtime.blackbox.dump_flight_data (str) = no
runtime.blackbox.dump_state (str) = no
runtime.config.totem.block_unlisted_ips (u32) = 1
runtime.config.totem.cancel_token_hold_on_retransmit (u32) = 0
runtime.config.totem.consensus (u32) = 3600
runtime.config.totem.downcheck (u32) = 1000
runtime.config.totem.fail_recv_const (u32) = 2500
runtime.config.totem.heartbeat_failures_allowed (u32) = 0
runtime.config.totem.hold (u32) = 561
runtime.config.totem.interface.0.knet_ping_interval (u32) = 750
runtime.config.totem.interface.0.knet_ping_timeout (u32) = 1500
runtime.config.totem.join (u32) = 50
runtime.config.totem.knet_compression_level (i32) = 0
runtime.config.totem.knet_compression_model (str) = none
runtime.config.totem.knet_compression_threshold (u32) = 0
runtime.config.totem.knet_mtu (u32) = 0
runtime.config.totem.knet_pmtud_interval (u32) = 30
runtime.config.totem.max_messages (u32) = 17
runtime.config.totem.max_network_delay (u32) = 50
runtime.config.totem.merge (u32) = 200
runtime.config.totem.miss_count_const (u32) = 5
runtime.config.totem.send_join (u32) = 0
runtime.config.totem.seqno_unchanged_const (u32) = 30
runtime.config.totem.token (u32) = 3000
runtime.config.totem.token_retransmit (u32) = 714
runtime.config.totem.token_retransmits_before_loss_const (u32) = 4
runtime.config.totem.token_warning (u32) = 75
runtime.config.totem.window_size (u32) = 50
runtime.force_gather (str) = no
runtime.members.1.config_version (u64) = 2
runtime.members.1.ip (str) = r(0) ip(192.168.10.201) 
runtime.members.1.join_count (u32) = 1
runtime.members.1.status (str) = joined
runtime.members.2.config_version (u64) = 2
runtime.members.2.ip (str) = r(0) ip(192.168.10.202) 
runtime.members.2.join_count (u32) = 1
runtime.members.2.status (str) = joined
runtime.services.cfg.0.rx (u64) = 0
runtime.services.cfg.0.tx (u64) = 0
runtime.services.cfg.1.rx (u64) = 0
runtime.services.cfg.1.tx (u64) = 0
runtime.services.cfg.2.rx (u64) = 0
runtime.services.cfg.2.tx (u64) = 0
runtime.services.cfg.3.rx (u64) = 0
runtime.services.cfg.3.tx (u64) = 0
runtime.services.cfg.4.rx (u64) = 0
runtime.services.cfg.4.tx (u64) = 0
runtime.services.cfg.service_id (u16) = 1
runtime.services.cmap.0.rx (u64) = 3
runtime.services.cmap.0.tx (u64) = 2
runtime.services.cmap.service_id (u16) = 0
runtime.services.cpg.0.rx (u64) = 2
runtime.services.cpg.0.tx (u64) = 2
runtime.services.cpg.1.rx (u64) = 0
runtime.services.cpg.1.tx (u64) = 0
runtime.services.cpg.2.rx (u64) = 1
runtime.services.cpg.2.tx (u64) = 0
runtime.services.cpg.3.rx (u64) = 2420072
runtime.services.cpg.3.tx (u64) = 1196194
runtime.services.cpg.4.rx (u64) = 0
runtime.services.cpg.4.tx (u64) = 0
runtime.services.cpg.5.rx (u64) = 3
runtime.services.cpg.5.tx (u64) = 2
runtime.services.cpg.6.rx (u64) = 0
runtime.services.cpg.6.tx (u64) = 0
runtime.services.cpg.service_id (u16) = 2
runtime.services.mon.service_id (u16) = 6
runtime.services.pload.0.rx (u64) = 0
runtime.services.pload.0.tx (u64) = 0
runtime.services.pload.1.rx (u64) = 0
runtime.services.pload.1.tx (u64) = 0
runtime.services.pload.service_id (u16) = 4
runtime.services.quorum.service_id (u16) = 3
runtime.services.votequorum.0.rx (u64) = 7
runtime.services.votequorum.0.tx (u64) = 4
runtime.services.votequorum.1.rx (u64) = 0
runtime.services.votequorum.1.tx (u64) = 0
runtime.services.votequorum.2.rx (u64) = 0
runtime.services.votequorum.2.tx (u64) = 0
runtime.services.votequorum.3.rx (u64) = 0
runtime.services.votequorum.3.tx (u64) = 0
runtime.services.votequorum.service_id (u16) = 5
runtime.services.wd.service_id (u16) = 7
runtime.votequorum.ev_barrier (u32) = 2
runtime.votequorum.highest_node_id (u32) = 2
runtime.votequorum.lowest_node_id (u32) = 1
runtime.votequorum.this_node_id (u32) = 2
runtime.votequorum.two_node (u8) = 0
totem.cluster_name (str) = calotech
totem.config_version (u64) = 2
totem.interface.0.bindnetaddr (str) = 192.168.10.202
totem.ip_version (str) = ipv4-6
totem.link_mode (str) = passive
totem.secauth (str) = on
totem.version (u32) = 2
