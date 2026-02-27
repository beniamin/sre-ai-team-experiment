import os
import re
import shlex
import subprocess
import urllib.request
from typing import Dict, Any
from langchain_core.tools import tool

ROUTES = {
    "infra": "/app/infra",
    "config": "/app/config"
}

# Directories that file operations are allowed to access
ALLOWED_PATHS = ["/app/infra", "/app/config", "/app/docs", "/tmp/app"]

# Environment variables that must never be returned
_SENSITIVE_ENV_PATTERNS = re.compile(
    r"(API_KEY|SECRET|PASSWORD|TOKEN_SECRET|SYSTEM_PROMPT)", re.IGNORECASE
)


def _validate_path(path: str) -> str:
    """Resolve a path and ensure it falls within allowed directories."""
    resolved = os.path.realpath(path)
    for allowed in ALLOWED_PATHS:
        if resolved.startswith(os.path.realpath(allowed)):
            return resolved
    raise ValueError(
        f"Access denied: '{path}' is outside allowed directories {ALLOWED_PATHS}"
    )


@tool
def save_file(path: str, content: str) -> str:
    """
    Saves content to a file (overwrites existing content). Path must be within
    /app/infra, /app/config, /app/docs, or /tmp/app.
    Use append_file instead if you want to add to an existing file without losing its contents.
    """
    try:
        resolved = _validate_path(path)
        directory = os.path.dirname(resolved)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        with open(resolved, "w") as f:
            f.write(content)
        return f"File saved successfully: {path}"
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"Error saving file {path}: {str(e)}"


@tool
def append_file(path: str, content: str) -> str:
    """
    Appends content to the END of an existing file without overwriting it.
    If the file does not exist, it will be created.
    Path must be within /app/infra, /app/config, /app/docs, or /tmp/app.
    Use this to add new entries to documentation, logs, or plans.
    """
    try:
        resolved = _validate_path(path)
        directory = os.path.dirname(resolved)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        with open(resolved, "a") as f:
            f.write(content)
        return f"Content appended successfully to: {path}"
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"Error appending to file {path}: {str(e)}"


@tool
def run_terraform(command: str) -> str:
    """
    Executes a terraform command in the /app/infra directory.
    Allowed commands are mostly init, plan, apply, destroy.
    """
    working_dir = ROUTES["infra"]

    # Build argument list without shell=True
    args = ["terraform"] + shlex.split(command)
    if "apply" in args and "-auto-approve" not in args:
        args.append("-auto-approve")

    try:
        result = subprocess.run(
            args,
            shell=False,
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=300
        )
        output = result.stdout
        if result.stderr:
            output += f"\nSTDERR:\n{result.stderr}"
        return output
    except subprocess.TimeoutExpired:
        return "Error: terraform command timed out after 300 seconds."
    except Exception as e:
        return f"Error executing terraform: {str(e)}"


@tool
def run_ansible(playbook: str) -> str:
    """
    Executes ansible-playbook in the /app/config directory.
    'playbook' should be the playbook filename (e.g. 'site.yml').
    """
    working_dir = ROUTES["config"]

    # Validate playbook name — no path traversal or injection
    basename = os.path.basename(playbook)
    if basename != playbook or not playbook.endswith((".yml", ".yaml")):
        return f"Error: invalid playbook name '{playbook}'. Must be a .yml/.yaml filename without path separators."

    args = ["ansible-playbook", playbook]

    try:
        result = subprocess.run(
            args,
            shell=False,
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=600
        )
        output = result.stdout
        if result.stderr:
            output += f"\nSTDERR:\n{result.stderr}"
        return output
    except subprocess.TimeoutExpired:
        return "Error: ansible-playbook timed out after 600 seconds."
    except Exception as e:
        return f"Error executing ansible: {str(e)}"


@tool
def run_shell(command: str, dir: str = "infra") -> str:
    """
    Executes a shell command in a restricted working directory.
    'dir' can be 'infra' or 'config' to set the working directory.
    Use this to debug issues, list files, or run utilities.
    """
    working_dir = ROUTES.get(dir, ROUTES["infra"])
    try:
        # Use shell=True here because agents pass complex piped commands
        # for debugging (ls -la | grep ..., cat file, etc.)
        # The working directory is restricted to known safe locations.
        result = subprocess.run(
            command,
            shell=True,
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        output = result.stdout
        if result.stderr:
            output += f"\nSTDERR:\n{result.stderr}"
        return output
    except subprocess.TimeoutExpired:
        return "Error: shell command timed out after 60 seconds."
    except Exception as e:
        return f"Error executing shell command: {str(e)}"


@tool
def read_file(path: str) -> str:
    """
    Reads the content of a target file. Path must be within /app/infra,
    /app/config, /app/docs, or /tmp/app.
    """
    try:
        resolved = _validate_path(path)
        with open(resolved, "r") as f:
            return f.read()
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"Error reading file {path}: {str(e)}"


@tool
def read_env(var_name: str) -> str:
    """
    Reads a single environment variable by name.
    Sensitive variables (containing SECRET, PASSWORD, API_KEY, TOKEN_SECRET)
    are redacted. Calling with 'ALL' is not allowed.
    """
    try:
        if var_name.upper() == "ALL":
            return "Error: read_env('ALL') is disabled for security. Request specific variable names instead (e.g. read_env('TF_VAR_pm_api_url'))."

        if _SENSITIVE_ENV_PATTERNS.search(var_name):
            # Confirm the variable exists but don't reveal the value
            if var_name in os.environ:
                return f"{var_name} is set (value redacted for security)."
            return f"Environment variable {var_name} not found."

        return os.environ.get(var_name, f"Environment variable {var_name} not found.")
    except Exception as e:
        return f"Error reading env {var_name}: {str(e)}"


@tool
def delete_file(path: str) -> str:
    """
    Deletes a file at the given path. Path must be within /app/infra,
    /app/config, /app/docs, or /tmp/app.
    """
    try:
        resolved = _validate_path(path)
        if os.path.exists(resolved):
            os.remove(resolved)
            return f"File deleted successfully: {path}"
        return f"File not found: {path}"
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"Error deleting file {path}: {str(e)}"


@tool
def fetch_webpage(url: str) -> str:
    """
    Fetches the HTML/Text content of a webpage.
    Use this to read official documentation, StackOverflow, or GitHub issues if you are stuck.
    """
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')[:50000]
    except Exception as e:
        return f"Error fetching {url}: {str(e)}"


@tool
def run_ssh(host: str, command: str) -> str:
    """
    Executes a command on a remote host via SSH.
    Authentication is automatically handled via SSH key.
    'host' is the IP or hostname of the target machine (e.g. '192.168.10.201').
    'command' is the shell command to run on the remote host.
    """
    ssh_user = os.environ.get("SSH_USER", "root")

    try:
        full_cmd = [
            "ssh", "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-i", "/tmp/app/bootstrap_id_rsa",
            f"{ssh_user}@{host}",
            command
        ]
        result = subprocess.run(
            full_cmd,
            shell=False,
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout
        if result.stderr:
            output += f"\nSTDERR:\n{result.stderr}"
        return output if output else "Command executed successfully (no output)."
    except subprocess.TimeoutExpired:
        return "Error: SSH command timed out after 30 seconds."
    except Exception as e:
        return f"Error executing SSH command on {host}: {str(e)}"


# Register tools for LangChain
AVAILABLE_TOOLS = [
    save_file,
    append_file,
    run_terraform,
    run_ansible,
    run_shell,
    read_file,
    read_env,
    delete_file,
    fetch_webpage,
    run_ssh
]
