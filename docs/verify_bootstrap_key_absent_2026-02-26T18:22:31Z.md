Bootstrap key presence check

Command used: grep -F '<bootstrap-key>' /root/.ssh/authorized_keys || true

Results per node:

--- 192.168.10.201 ---
No match found (exit:1)

--- 192.168.10.202 ---
No match found (exit:1)

Interpretation: The bootstrap public key was not found in /root/.ssh/authorized_keys on either node. exit:1 indicates grep did not find the key, which is expected after bootstrap key cleanup.

exit:0
