# AI MiniLab — Autonomous SRE Team Experiment

An experiment in building a team of 4 LLM-powered AI agents that communicate over Redis pub/sub to autonomously provision and harden real infrastructure on a 2-node Proxmox VE 9 cluster.

Read the full experiment write-up in [ARTICLE.md](ARTICLE.md).

---

## Scope

This project explores two questions:

1. **Can a team of cheap LLM agents autonomously manage real infrastructure?**
   Four agents — a planner, an executor, a security reviewer, and a validator — coordinate via Redis to assess a Proxmox cluster, write Terraform and Ansible code, and deploy workloads. The constraint: the team must run on budget LLMs (GPT-5-mini at ~$0.27/session).

2. **How do AI coding assistants compare on real systems code?**
   Gemini 3 Pro / 3.1 Pro was used to build the agent framework. Claude Code (Opus 4) was used for debugging. Gemini produced a working skeleton but could not diagnose structural bugs even when shown symptoms. Claude identified 13 bugs on the first prompt with full causal chain analysis.

---

## Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌────────────────────┐
│ User Console │────>│   Redis Broker    │<--->│  Architect_Zero    │
│  (stdin/tty) │     │  (pub/sub + hist) │     │  (Planner/Coord)   │
└──────────────┘     └──────┬───┬───┬────┘     └────────────────────┘
                            │   │   │
              ┌─────────────┘   │   └──────────────┐
              v                 v                   v
    ┌──────────────────┐ ┌─────────────┐ ┌──────────────────┐
    │  DevOps_Builder   │ │  Security   │ │    QA_Tester     │
    │  (Executor)       │ │  Sentinel   │ │   (Validator)    │
    │  terraform/ansible│ │  (Reviewer) │ │   (curl/ssh)     │
    └──────────────────┘ └─────────────┘ └──────────────────┘
```

### Agents

| Agent | Role | Tools |
|-------|------|-------|
| **Architect_Zero** | Plans infrastructure topology, coordinates the team, manages documentation. Cannot execute commands — delegates to others. | `save_file`, `append_file`, `read_file` |
| **DevOps_Builder** | Writes and executes Terraform, Ansible, and shell commands against real infrastructure. | All tools: `save_file`, `run_terraform`, `run_ansible`, `run_shell`, `run_ssh`, `read_file`, `read_env`, `delete_file`, `fetch_webpage` |
| **Security_Sentinel** | Reviews plans and generated IaC for vulnerabilities. Must approve before execution proceeds. | `read_file`, `read_env`, `run_shell` (audit only) |
| **QA_Tester** | Validates deployed services via health checks, connectivity tests, and SSH probes. | `run_shell`, `read_file`, `run_ssh`, `fetch_webpage` |

### Communication

- All agents share a single Redis pub/sub channel (`agent_channel`)
- Agents address each other with `@AgentName` tags in messages
- Only `Architect_Zero` responds to `User` messages; others respond only when tagged
- `::think` messages are internal reasoning (logged but filtered from agent memory)
- Chat history is stored in a Redis list with an 80-message sliding window

### Key Mechanisms

- **ReAct Loop**: Each agent runs a LangChain ReAct loop (up to 100 steps per request) — the LLM reasons, calls tools, observes results, and repeats
- **Tool Error Escalation**: After X consecutive tool failures, the agent auto-escalates to Architect_Zero with execution context
- **Execution Logging**: Every tool call is logged to `/app/docs/execution_log_{role}.md` for cross-agent debugging
- **Path Sandboxing**: File operations are restricted to `/app/infra`, `/app/config`, `/app/docs`, `/tmp/app`
- **Secret Redaction**: `read_env` redacts variables matching `API_KEY`, `SECRET`, `PASSWORD`, `TOKEN_SECRET`

---

## Deployment

### Prerequisites

- Docker and Docker Compose
- An OpenAI-compatible API key (OpenAI, or a local LLM server like LM Studio)
- (Optional) SSH access to target Proxmox nodes with a bootstrap key

### 1. Clone the repository

```bash
git clone https://github.com/your-org/ai-minilab.git
cd ai-minilab
```

### 2. Configure environment variables

Copy the template and fill in your values:

```bash
cp .env.template .env
```

Edit `.env` with your OpenAI API key (or self-hosted LLM endpoint), Proxmox API token, and SSH user. The template includes comments explaining each variable.

### 3. Set up SSH access (optional)

If you want the agents to manage real infrastructure, place a bootstrap SSH private key at `tmp/bootstrap_id_rsa`:

```bash
mkdir -p tmp
cp /path/to/your/key tmp/bootstrap_id_rsa
chmod 600 tmp/bootstrap_id_rsa
```

### 4. Start the team

```bash
docker-compose up --build
```

This starts 6 containers:
- `redis-broker` — Message broker
- `agent-architect` — Architect_Zero (planner)
- `agent-devops` — DevOps_Builder (executor)
- `agent-security` — Security_Sentinel (reviewer)
- `agent-qa` — QA_Tester (validator)
- `user-console` — Interactive console

### 5. Interact with the team

Attach to the user console:

```bash
docker attach user-console
```

Type your instructions. Only `Architect_Zero` listens to user messages — it then coordinates the rest of the team.

**Console commands:**

| Command | Effect |
|---------|--------|
| `STOP` | Halts all agents (they stop processing) |
| `CLEAR` | Aborts all activity and wipes Redis chat history |
| `exit` / `quit` | Exits the console |

**Example session:**

```
[User]: Assess the current state of my 2-node Proxmox cluster at 192.168.10.201 and 192.168.10.202
[Architect_Zero]: I'll coordinate an inventory collection...
[Architect_Zero]: @DevOps_Builder SSH into both nodes and collect...
[DevOps_Builder]: Running inventory commands...
```

### 6. View agent output

All execution artifacts are saved to the `docs/` directory:

```bash
ls docs/
# execution_log_Architect_Zero.md
# execution_log_DevOps_Builder.md
# execution_log_Security_Sentinel.md
# user_requirements.md
# implementation_plan.md
# ...
```

Generated Terraform and Ansible code lives in `generated_iac/`.

---
## Project Structure

```
ai-minilab/
├── agents/                     # Agent runtime code
│   ├── Dockerfile              # Python 3.11 + Terraform + Ansible + kubectl
│   ├── core.py                 # DistributedAgent class (ReAct loop, Redis, LLM)
│   ├── main.py                 # Entry point — loads prompts, wires tools per role
│   ├── tools.py                # Tool definitions with path sandboxing
│   ├── requirements.txt        # redis, langchain-openai, pydantic
│   └── prompts/                # System prompts (one .md file per agent role)
│       ├── Architect_Zero.md
│       ├── DevOps_Builder.md
│       ├── Security_Sentinel.md
│       └── QA_Tester.md
├── client/                     # User console
│   ├── console.py              # Interactive Redis CLI (stdin/tty)
│   └── logs/                   # Conversation logs (auto-generated)
├── generated_iac/              # Agent-generated Infrastructure as Code
│   ├── infra/                  # Terraform modules (Proxmox VMs, witness)
│   └── config/                 # Ansible playbooks (hardening, K8s bootstrap)
├── docs/                       # Execution artifacts and documentation
│   ├── user_requirements.md    # Operator decisions and constraints
│   ├── implementation_plan.md  # Living plan maintained by Architect_Zero
│   └── execution_log_*.md      # Per-agent tool call logs
├── tmp/                        # Bootstrap SSH key, CA certs
├── docker-compose.yml          # 6 services: Redis + 4 agents + user console
├── .env.template               # Environment variable template (copy to .env)
├── .env                        # Your local config (not committed, in .gitignore)
├── ARTICLE.md                  # Full experiment write-up
└── README.md                   # This file
```

---

## Customization

### Changing the LLM

Edit `.env` to point to any OpenAI-compatible API:

```env
# GPT-5-mini (tested, ~$0.27/session)
LLM_MODEL=gpt-5-mini

# Local Qwen via LM Studio (tested, quality limitations)
OPENAI_API_BASE=http://host.docker.internal:1234/v1
LLM_MODEL=qwen/qwen2.5-coder-14b
```

### Modifying agent behavior

Agent system prompts live in `agents/prompts/`. Edit the `.md` files to change how each agent reasons, what rules it follows, and how it coordinates with the team.

### Adding tools

Define new tools in `agents/tools.py` using the `@tool` decorator, then add them to the `ROLE_TOOLS` mapping in `agents/main.py`.

---

## License

This project is an experiment. Use at your own risk. The agents have SSH access to real infrastructure and will execute commands if configured to do so.
