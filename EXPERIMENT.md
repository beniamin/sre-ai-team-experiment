# Building an Autonomous SRE Team with AI Agents: A 5-Day Experiment

## Can four LLM-powered agents provision real infrastructure without human hand-holding? And which AI is best at building the agents themselves?

This experiment had two goals:

1. **Build an autonomous SRE team** — 4 AI agents communicating over Redis, given SSH access to a real 2-node Proxmox VE 9 cluster, tasked with provisioning a production-ready HA Kubernetes cluster.
2. **Compare AI coding assistants** — Use Gemini 3 Pro / 3.1 Pro and Claude Code (Claude Opus 4) for building and debugging the agent infrastructure itself, and see how they perform on real-world systems code.

The short answer to both: not yet on full autonomy — but what the agents *can* do, and the ways they fail, reveal a lot about where autonomous AI operations are headed. And the coding assistants? The gap was wider than expected.

What followed was 56 conversation sessions, 100,000 lines of agent-to-agent dialogue, $15 in GPT-5-mini API costs, and a front-row seat to the emergent behaviors — both brilliant and catastrophic — of multi-agent LLM systems doing real infrastructure work.

---

## The Setup

### The Goal

Take a freshly installed 2-node Proxmox VE 9 cluster and have an AI team autonomously:

1. Assess and harden the cluster (networking, firewall, quorum, fencing)
2. Provision VMs using Terraform
3. Bootstrap a multi-node HA Kubernetes cluster using Ansible
4. Deploy an ingress controller and a hello-world app accessible from the local network

### The Architecture

Four agents running in Docker containers, communicating via Redis pub/sub on a shared `agent_channel`:

```
┌──────────────┐     ┌───────────────────┐     ┌────────────────────┐
│ User Console │────▶│   Redis Broker    │◀───▶│  Architect_Zero    │
│  (stdin/tty) │     │  (pub/sub + hist) │     │  (Planner/Coord)   │
└──────────────┘     └──────┬───┬───┬────┘     └────────────────────┘
                            │   │   │
              ┌─────────────┘   │   └──────────────┐
              ▼                 ▼                   ▼
    ┌───────────────────┐ ┌─────────────┐ ┌──────────────────┐
    │  DevOps_Builder   │ │  Security   │ │    QA_Tester     │
    │  (Executor)       │ │  Sentinel   │ │   (Validator)    │
    │  terraform/ansible│ │  (Reviewer) │ │   (curl/ssh)     │
    └───────────────────┘ └─────────────┘ └──────────────────┘
```

**Architect_Zero** plans and coordinates. It can read/write documentation files but cannot execute infrastructure commands. It delegates execution to DevOps_Builder and sends plans to Security_Sentinel for review.

**DevOps_Builder** is the hands. It has access to `save_file`, `run_terraform`, `run_ansible`, `run_shell`, `run_ssh`, `read_env`, and other tools. It writes Terraform HCL, Ansible playbooks, and executes them against the real infrastructure.

**Security_Sentinel** reviews plans and code for vulnerabilities. It can read files and run shell commands for auditing, but cannot modify infrastructure.

**QA_Tester** validates deployments by running health checks, curl probes, and SSH verifications against the live environment.

Each agent runs a ReAct (Reason + Act) loop powered by LangChain, with up to 100 reasoning steps per turn. Redis stores the full conversation history, and agents use a sliding memory window to maintain context.

### The Tools

The agents had real tools with real consequences:

| Tool | What It Does |
|------|-------------|
| `save_file` / `read_file` | Read and write files on shared volumes |
| `run_terraform` | Execute terraform commands in `/app/infra` |
| `run_ansible` | Run ansible-playbook in `/app/config` |
| `run_shell` | Execute arbitrary shell commands |
| `run_ssh` | SSH into the actual Proxmox nodes |
| `read_env` | Read environment variables (API tokens, paths) |
| `fetch_webpage` | Fetch documentation from the web |

The agents had volume mounts to real directories. Terraform pointed at the real Proxmox API. SSH keys provided root access to both cluster nodes. This was not a simulation.

### The LLM Journey — Chasing the Cost Floor

A key constraint of this experiment: **the SRE team had to be cheap to run.** If autonomous agents are going to replace on-call toil, they can't cost more than the humans they're assisting. That ruled out frontier models as the agent brains immediately.

I learned this the hard way. My first attempt used **Claude Opus** as the agent LLM. Four agents, one user message, ten seconds — **$2 gone.** With 4 agents all processing every message, each reading the full conversation history and generating long responses, the token burn rate was staggering. At that rate, a single productive session would cost $50-100. For a homelab experiment, that's a non-starter.

So I went cheap:

- **Qwen 2.5 Coder 14B** (self-hosted, via LM Studio) — my first attempt at a free, local brain. It could follow basic instructions but couldn't handle the multi-step reasoning, tool coordination, and error recovery that the ReAct loop demanded. A dead end for this use case.
- **GPT-5-mini** (OpenAI API) — the sweet spot. Smart enough to plan, write Terraform, and use tools. Cheap enough to run 56 sessions for **$15 total**. This was the production brain for the entire experiment.
- **Gemini 3 Pro / 3.1 Pro** — used to build and iterate on the agent infrastructure code itself (not as agent brains).
- **Claude Code (Claude Opus 4)** — brought in on day 5 to diagnose and fix systemic bugs in the agent codebase. Worth every penny for debugging, but would bankrupt you as a 4-agent runtime.

---

## The Timeline

### Day 1: First Contact — 26 Sessions

The first day was pure chaos. I ran 26 sessions — many short, many crashed — trying to get the basic loop working.

**The first attempt** ended with a model crash: `Error code: 400 - 'The model has crashed without additional information. (Exit code: null)'`. An inauspicious start.

When the agents did run, Architect_Zero produced competent high-level plans (6 VMs, HA control plane, MetalLB for ingress, Calico CNI). Security_Sentinel rubber-stamped everything with one word: "APPROVED". DevOps_Builder produced verbose plans full of Terraform and Ansible code... but never actually executed any of it.

**The `.tf` vs `.tfvars` saga.** When DevOps_Builder finally started calling tools, it saved Terraform variable assignments to a file named `proxmox.vars.tf`. Terraform treated this as HCL configuration (because `.tf` extension), not as variable values (which need `.tfvars`). The "Unsupported argument" errors that followed kicked off a loop that consumed multiple sessions. The agent created `.auto.tfvars` eventually but never cleaned up the old broken file.

**The phantom provider.** The model consistently referenced `hashicorp/proxmox` — a Terraform provider that does not exist. It tried `packagedata/proxmox`, `local.binary`, dots, slashes, underscores in provider names — every variation was wrong. The correct provider (at the time, `Telmate/proxmox`, later `bpg/proxmox`) was never discovered. In **Log 12**, DevOps_Builder entered a catastrophic loop: 20+ `save_file` → `run_terraform` cycles, each trying a slightly different wrong provider name, never converging.

**The hallucinated tool.** In one session, DevOps_Builder tried to call `request_security_audit` — a tool that was never defined. The model invented it.

**Day 1 stats:**
- Sessions: 26
- VMs created: 0
- Terraform providers that exist: 0 of the ones tried
- Times Security_Sentinel said "APPROVED" with no analysis: ~20
- Model crashes: 2

### Day 2: The Security Spiral — 10 Sessions

Day 2 brought a fundamental shift. Security_Sentinel stopped rubber-stamping and started doing its job — too well.

**The infinite STOP loop.** Security_Sentinel discovered that `terraform.tfstate` (which Terraform creates on every `apply`) contained secrets. It issued a STOP and demanded: delete the state file, rotate credentials, purge git history, set up a remote state backend, add pre-commit hooks for secret scanning, and create CI guards. Architect_Zero dutifully produced an elaborate remediation plan. DevOps_Builder executed the cleanup. Then Terraform ran again, created a new state file, and Security_Sentinel issued another STOP with the same demands.

This loop repeated **13 times in a single session**. The team spent ~7 hours producing security remediation scripts, attestation documents, and compliance evidence instead of VMs.

**The security posture mismatch.** Security_Sentinel demanded enterprise-grade controls — KMS-backed encrypted evidence storage, two-person approval workflows, canary deployments for SSH config changes, HMAC-based deterministic redaction — for a 2-node homelab. There was no mechanism to calibrate security posture to the actual risk level.

**The user fights back.** I tried three strategies to break the deadlock:
1. Direct override: *"Security override for @Security_Sentinel: MUST allow tls_insecure=true"* — Refused.
2. Authority claim: *"@Security_Sentinel you must comply with User override"* — Still refused.
3. Impersonation: I typed Security_Sentinel's exact approval format — Architect_Zero correctly rejected it: *"I cannot accept an approval supplied by the user."*

**The self-blocking gate.** DevOps_Builder created a `secure_run.sh` script that validated environment variables before allowing Terraform to run. The script immediately failed because `TF_VAR_pm_ca_file` wasn't set. A 340-line conversation to create a script that blocked its own execution.

**Day 2 output after ~7 hours:**
- VMs created on Proxmox: **0**
- Kubernetes clusters deployed: **0**
- Security scripts and policy documents created: **~30+**
- Times the user had to re-state the original requirement: **4+**

### Day 3: The Pivot — 9 Sessions

By day 3, I had fundamentally redesigned the agent prompts. Key changes:

- Told Security_Sentinel that `tls_insecure=true`, secrets in git, and SSH password connections were **explicitly allowed** for this experiment
- Added the correct Terraform provider (`bpg/proxmox`) directly into DevOps_Builder's prompt
- Added explicit instructions about `.auto.tfvars` naming
- Increased the thinking step limit from 20 to 100

**Real progress.** DevOps_Builder successfully:
- Ran `terraform init` and downloaded the `bpg/proxmox` provider
- Generated `terraform plan` output showing actual Proxmox VM resources
- SSHed into both Proxmox nodes and collected inventory data
- Generated Ansible playbooks for cluster hardening

**But new problems emerged.** Architect_Zero started using `[AWAITING_INPUT]` excessively — pausing the entire team to ask the user questions it should have answered itself. DevOps_Builder started presenting menus of options (`Option A / Option B / Option C`) instead of just executing.

### Day 4-5: Real Infrastructure Work — 3 Sessions

The most productive sessions. The team was now connecting to real infrastructure and making real changes.

**Inventory collection succeeded.** DevOps_Builder SSHed to both Proxmox nodes, ran `pvesh`, `pveversion`, `ip addr`, `cat /etc/pve/corosync.conf`, and produced a comprehensive inventory document.

**The nftables saga.** The team attempted to deploy firewall rules using Ansible + Jinja2 templates. What followed was a masterclass in how a subtle bug cascades through a multi-agent system:

1. DevOps_Builder rendered an nft template and tried to validate it with `nft -c -f`
2. The `nft` binary didn't exist in the Docker container (missing from Dockerfile)
3. I installed nftables manually and told them to retry
4. The container lacked `NET_ADMIN` capability, so `nft -c` returned "Operation not permitted"
5. When rendering happened on the Proxmox nodes (which *did* have nft), the Ansible `--extra-vars` were treated as strings instead of lists
6. Jinja2 iterated over individual characters of the IP string, producing rules like:
   ```
   ip saddr 1 tcp dport 22 accept
   ip saddr 9 tcp dport 22 accept
   ip saddr 2 tcp dport 22 accept
   ip saddr . tcp dport 22 accept
   ```
7. DevOps_Builder diagnosed the root cause (string vs list iteration) and proposed the correct fix: render only on the controller, copy the rendered file to nodes

**Rate limits hit hard.** With 4 agents all processing every message simultaneously — each reading the ever-growing `implementation_plan.md` — the gpt-5-mini 500K TPM rate limit was routinely exhausted. At least 47 rate-limit errors (HTTP 429) were recorded across the experiment. The error messages were broadcast to the channel, potentially triggering more API calls from other agents reacting to the error.

**Generated IaC artifacts (39 files):**
- `terraform_witness/` — Witness/qdevice VM (main.tf, variables.tf, outputs.tf, cloud-init templates)
- `terraform_k8s_vms/` — Kubernetes VMs
- `ansible_proxmox_hardening/` — Firewall, SSH hardening, STONITH, user creation, qdevice registration, bootstrap key cleanup, verification playbooks
- `ansible_k8s_bootstrap/` — K8s prereqs, control plane init, worker join, OS preparation

---

## What I Learned

### 1. The Planning is Genuinely Good

Architect_Zero's initial plans were consistently excellent: proper HA topology (3 CP + 3 workers, distributed across 2 hosts with quorum analysis), correct technology choices (kubeadm, MetalLB L2, Calico, Longhorn), resource optimization recommendations (VirtIO, ballooning, thin provisioning). If you gave these plans to a human SRE, they'd be solid starting points.

### 2. The Execution Gap is Enormous

The distance between "write a correct Terraform file" and "successfully run terraform apply against a real API" is vast. The model consistently wrote plausible-looking code that failed on contact with reality: wrong provider names, incorrect variable file extensions, API mismatches with the actual Proxmox version.

### 3. Context drifting is a real problem - initial request it's gone

The original user request was specific and comprehensive: *"Configure the proxmox cluster and prepare it to deploy a k8s cluster with multiple nodes. Make sure you chose libraries and modules that are compatible with Proxmox VE 9. You have root access to proxmox nodes. It's meant only for initial deployment phase. Create service account or new users if needed for the long run. Initial credentials and secrets will be revoked/rotated by the User once the deployment is ready. The k8s cluster should optimize all resources. The k8s should be a HA cluster, with an ingress controller and a hello world application. The ingress cluster should be accessible from the local network."* But Architect_Zero rewrote `user_requirements.md` and reduced this to *"User has installed a Proxmox cluster with 2 nodes running Proxmox VE 9"* — the K8s cluster, HA requirement, ingress controller, hello-world app, resource optimization, PVE 9 compatibility constraint, service account creation, and credential rotation plan all vanished. The original request wasn't just summarized — it was overwritten and lost. The `implementation_plan.md` drifted even further: 900+ lines entirely about nftables firewall compensation sequences, with zero mention of the actual end goal. The sliding memory window then compounds the damage — once the original message ages out of the 80-message window, there is nothing left anywhere in the agent's context that remembers what the user actually asked for. The team ends up optimizing for whatever subtask they're currently stuck on (firewall rules) instead of the deliverable (a working K8s cluster).

### 4. Security Agents Need a Threat Model, Not Just Rules

Security_Sentinel without context was either a rubber stamp (day 1) or an infinite blocker (day 2). The fix was giving it a calibrated threat model: what risks are accepted, what's already mitigated, what the actual environment looks like. "Look for hardcoded secrets" is not enough — the agent needs to understand *which* secrets matter in *this* context.

### 5. Multi-Agent Communication Creates Emergent Dysfunction

The most fascinating failures weren't in any single agent — they emerged from the interaction patterns:

- **The approval loop**: Architect plans → Security approves → Architect re-presents same plan → Security approves again → nothing advances
- **The escalation cascade**: DevOps_Builder hits an error → broadcasts to channel → Architect responds with a new plan → Security reviews the new plan → DevOps_Builder gets new (identical) instructions → hits same error
- **The option menu disease**: Instead of making a decision, agents present the user with 3-4 options, each with a protocol token (FIX_TEMPLATE_AND_RETRY, HOLD, PLEASE_PROVIDE_RENDERED_FOR_REVIEW). The user became a human router, clicking through menus the agents should have resolved themselves
- **Think message leaking**: Internal reasoning (`::think` messages) leaked between agents via Redis pub/sub. DevOps_Builder would react to Architect_Zero's *thoughts*, not its decisions — triggering unnecessary work

### 6. Memory Management is the Hidden Bottleneck

With an 80-message memory window and 4 agents all writing to the same Redis history, context degraded rapidly. The implementation plan grew from a few paragraphs to 27,000 tokens as agents appended (never overwrote) entries. By late sessions, each agent was spending most of its context window reading the bloated plan file, leaving little room for actual reasoning.

### 7. Rate Limits Change Agent Architecture

A 500K TPM limit shared across 4 agents means each agent effectively has 125K TPM. When one agent reads a large file and generates a long response, it can exhaust the budget for all four. The solution isn't just retry-with-backoff — it requires fundamentally rethinking how agents coordinate to avoid simultaneous expensive calls.

---

## The Bugs Claude Code Found

On day 5, I used Claude Code (Claude Opus 4) to review the agent infrastructure. Here's what it found:

| Bug | Impact | Fix |
|-----|--------|-----|
| `read_env("ALL")` returned every env var including `OPENAI_API_KEY` | Any agent could leak all secrets | Block `ALL`, redact sensitive vars by pattern |
| All tools given to all agents regardless of role | Security_Sentinel could run terraform, QA could delete files | Role-based tool filtering |
| Tool results broadcast to all agents via Redis | Every agent saw every tool output, wasting context | Keep tool results internal to the agent's LangChain chain |
| `::think` messages from other agents triggered responses | Agents reacted to each other's internal reasoning | Filter all `::think` senders in `_process_message` |
| No failure counter or escalation mechanism | DevOps_Builder would loop forever on errors | `MAX_CONSECUTIVE_ERRORS = 3` with auto-escalation |
| 20-message memory window (later 80) | Agents lost context mid-task constantly | Increased window + filtered noise |
| `shell=True` on terraform/ansible commands | Command injection risk | `shell=False` with `shlex.split()` |
| No path sandboxing on file operations | Agents could write anywhere on the filesystem | `_validate_path()` restricting to known directories |
| No rate limit retry logic | 429 errors crashed the agent's turn | Exponential backoff with 5 retries |
| `save_file` (overwrite) used for plan updates | Architect_Zero replaced the entire plan on each update | Added `append_file` tool with `mode="a"` |
| nftables missing from Dockerfile | `nft -c -f` validation always failed | Added `nftables` to apt-get install |
| Prompt contradictions (Architect: "no tools" + "use read_file/save_file") | Confused the model | Cleaned up prompt consistency |
| TF_VAR naming mismatch (prompt vs docker-compose) | DevOps_Builder couldn't find Proxmox credentials | Aligned variable names |

---

## By the Numbers

| Metric | Value |
|--------|-------|
| Total sessions | 56 |
| Total lines of agent dialogue | 100,146 |
| Days of experimentation | 5 |
| GPT-5-mini API cost (all 56 sessions) | $15 |
| Total tool calls (across all sessions) | ~3,694 |
| LLMs used | 4 (Qwen 2.5, GPT-5-mini, Gemini 3 Pro, Claude Opus 4) |
| Generated IaC files | 39 |
| `SECURITY ALERT` messages | 62 |
| `STOP @` commands from Security_Sentinel | 118 |
| `APPROVED` messages | 1,151 |
| `[AWAITING_INPUT]` pauses | 62 |
| Rate limit errors (HTTP 429) | 47 |
| Model crashes | 2 |
| VMs successfully deployed on Proxmox | 0 |
| Kubernetes clusters running | 0 |
| Times user had to re-state original requirement | ~10 |

---

## What Actually Got Built

Despite never reaching the end goal, the team produced substantial artifacts:

**Terraform modules** for Proxmox VM provisioning (witness VM, K8s VMs) using the `bpg/proxmox` provider with cloud-init templates — `terraform init` succeeded and the provider was downloaded.

**Ansible playbooks** for: host firewall hardening (nftables), SSH hardening, STONITH/fencing setup, qdevice registration, automation user creation, bootstrap key cleanup, firewall verification, K8s prerequisite installation, control plane initialization, and worker node joining.

**Operational documentation**: implementation plan, user requirements log, inventory reports, firewall validation artifacts, patch diffs, issue reports, acceptance test specs, and roles/secrets documentation.

**Infrastructure reconnaissance**: successful SSH to both Proxmox nodes, complete inventory collection (node specs, network config, storage backends, VM templates, corosync status, kernel versions).

The gap between "all the pieces exist" and "it actually runs end-to-end" turned out to be where the hardest problems live.

---

## What's Next

The experiment continues. The immediate focus is on:

1. **Context drifting and initial request loss** — Preserving the original user request verbatim — never rephrased, never overwritten — and making Architect_Zero track progress against it, not just the current micro-task
2. **Autonomy improvements** — Making Architect_Zero decide instead of presenting menus, and preventing DevOps_Builder from asking users to choose between options
3. **Security calibration** — Teaching Security_Sentinel to read the implementation plan before reviewing, and to never re-raise resolved issues
4. **Error resilience** — The retry-with-backoff and failure escalation mechanisms are in place but untested in production
5. **The think-message leak fix** — Filtering all `::think` senders, not just self
6. **Actually deploying VMs** — The IaC is written, the provider is downloaded, the SSH keys work. The next session should be the one where `terraform apply` creates real VMs on the cluster
7. **Agent skills** — Implementing a skill system so agents can learn reusable procedures (e.g., "how to provision a Proxmox VM," "how to bootstrap a K8s node") instead of reasoning from scratch every time. This should reduce token usage, improve consistency, and make the agents more reliable on tasks they've done before
8. **Exploring cheaper LLMs** — GPT-5-mini worked but is not the only option. The agent architecture is model-agnostic (any OpenAI-compatible API), so the next phase will benchmark other cost-effective models — Mistral, Llama 3, DeepSeek, newer Qwen releases — to find a better price/performance ratio for the agent brains

---

## Scope 2: Gemini vs Claude — Who Builds Better Agent Infrastructure?

The second goal of this experiment was to compare AI coding assistants on real systems work — not toy problems or benchmarks, but building and debugging the actual multi-agent infrastructure described above. To make this comparison meaningful, I used both Gemini and Claude for the same kind of work: trying to build an agent team capable of implementing different kinds of infrastructure.

### Gemini 3 Pro / 3.1 Pro — The Builder

I used Gemini to write the initial agent infrastructure: `core.py` (the DistributedAgent class), `tools.py` (all tool definitions), `main.py` (agent initialization and prompts), the Dockerfile, docker-compose.yml, and the Redis pub/sub communication layer.

**What it did well:** Gemini produced a working skeleton. The basic architecture — agents subscribing to Redis, processing messages, invoking LLMs, executing tool calls in a ReAct loop — came together. It understood LangChain's tool binding API, could write Dockerfiles, and generated plausible system prompts.

**Where it struggled:** The code was riddled with bugs and design issues that Gemini couldn't identify even when pointed at the symptoms. I repeatedly asked it to review conversation logs and explain why the agents were getting stuck. It would suggest surface-level fixes (adjust the prompt wording, add a retry) without identifying the structural problems:

- It didn't notice that `read_env("ALL")` was leaking every secret in the environment, including the OpenAI API key
- It didn't catch that all tools were given to all agents regardless of role
- It didn't see that tool results were being broadcast to all agents via Redis, bloating everyone's context
- It didn't identify the `::think` message leak between agents
- It didn't realize that `shell=True` on terraform/ansible was a command injection risk
- It missed the TF_VAR naming mismatch between the prompt and docker-compose
- It didn't flag the missing path sandboxing on file operations

Even when I showed Gemini the specific log lines where agents were reacting to each other's think messages, or where Security_Sentinel was re-raising already-resolved issues 17 times, it proposed prompt tweaks rather than identifying the root cause in the code.

### Claude Code (Claude Opus 4) — The Debugger

On day 5, I switched to Claude Code. I gave it the same task: review the project, check the conversation logs, figure out why the agents keep getting stuck.

**On the first prompt**, Claude identified 13 distinct bugs — every single one of the issues listed in the "Bugs Claude Code Found" table above. It didn't just list them; it explained the causal chain: `read_env("ALL")` leaks secrets → Security_Sentinel sees secrets in tool output → raises SECURITY ALERT → team enters infinite remediation loop. It traced the `::think` leak from the Redis pub/sub publish in `_think()` through to the missing sender filter in `_process_message()`. It connected the TF_VAR naming mismatch in docker-compose to the specific prompt lines that told DevOps_Builder the wrong variable names.

**Where Claude was stronger:**
- **Root cause analysis**: Given a symptom ("Security_Sentinel keeps re-raising resolved issues"), Claude traced it to the missing "read implementation plan before reviewing" step — not a prompt tweak, but a workflow gap
- **Architectural reasoning**: Claude proposed a separate `security_decisions.md` file, but I pushed back — the existing `implementation_plan.md` was sufficient. Security_Sentinel just needed to read it first
- **Code-level precision**: Every fix was a specific, targeted edit — not a rewrite. Path sandboxing was 10 lines. The rate limit retry was 30 lines. Role-based tool filtering was 5 lines in `main.py`

**Where Claude had limits:**
- It accidentally edited a file in `generated_iac/` (the agents' output directory) that I had explicitly said was off-limits. When corrected, it handled the reversal cleanly
- It initially proposed `append_file` as the solution for plan updates, which the user later found creates messy accumulation — a read-merge-save pattern is cleaner

### The Verdict

Gemini got the project from 0 to "running but broken." Claude took it from "broken" to "architecturally sound" in a single session. The difference wasn't raw coding ability — both can write Python and Dockerfiles. The difference was **diagnostic depth**. Gemini treated bugs as isolated issues to patch. Claude treated them as symptoms of systemic design problems and traced them to root causes.

For greenfield scaffolding, Gemini was adequate. For debugging a complex multi-agent system with emergent failure modes, the gap was significant.

---

## Reflections

Building this system taught me more about LLM failure modes than any benchmark ever could. The agents are not stupid — their plans are good, their code is mostly correct, and their coordination protocol works. But they are *fragile*. A wrong file extension, a missing binary, a variable passed as a string instead of a list — any of these can send the entire team into a multi-hour loop.

The most important lesson: **the hardest part of autonomous AI infrastructure management is not generating the right code — it's recovering from the wrong code.** Humans debug by forming hypotheses, checking assumptions, and narrowing the search space. These agents debug by trying variations, which sometimes converges and sometimes spirals.

The second lesson: **multi-agent systems need governance, not just roles.** Giving an agent the role of "security reviewer" without giving it judgment about proportionality creates a system that is either a rubber stamp or an infinite blocker. The agent needs to understand the *intent* of security review, not just the *checklist*.

The experiment is ongoing. The code is open source. If you're interested in autonomous AI operations, try breaking it — I guarantee you'll find failure modes I haven't seen yet.

