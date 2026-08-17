# Installation

Install these before starting the curriculum. All sessions assume the tools below are on your `$PATH` and authenticated.

---

## 1. Operating System

| OS | Supported? | Notes |
|----|-----------|-------|
| macOS | Yes | Works as-is. Homebrew recommended. |
| Linux | Yes | Works as-is. Install dependencies via your package manager. |
| Windows | Via WSL only | Install [WSL](https://learn.microsoft.com/en-us/windows/wsl/install), then run every command from inside the WSL shell. Native Windows PowerShell is not supported. |

---

## 2. Gas City

Gas City is the orchestration framework this workshop is built on. It manages agents, packs, rigs, and beads. Please follow the steps below to install Gas City, and refer to the [Gas City documentation](https://github.com/gastownhall/gascity/blob/main/docs/getting-started/installation.md) for additional details.

```bash
# macOS / WSL / Linux (with Homebrew)
brew install gastownhall/gascity/gascity

# Verify (must report >= 1.0.0)
gc version
```

If you already have an older version of Gas City installed, you may need to uninstall it and install the latest version:
```bash
brew uninstall gascity
brew install gastownhall/gascity/gascity

# or
brew link --overwrite gascity
```

Gas City brings in the core tool dependencies it needs: `tmux`, `jq`, `git`, `dolt`. On macOS they are installed as Homebrew dependencies. On Linux, install any missing ones via your package manager.

Confirm everything is wired up:

```bash
gc doctor
```

All `check-core-tools` lines should show `✓`. Two deprecation warnings are **expected** for the factory's intentional v1-shape workarounds (documented in `my-factory/README.md`):

- `v2-default-rig-import-format` — tracked at [workshop:#781](https://github.com/gastownhall/gascity/issues/781)
- `v2-workspace-name` — tracked at [comment on #600](https://github.com/gastownhall/gascity/issues/600)

Warnings for optional integrations (Jira, Linear, Sentry, etc.) are also expected at this point — you'll enable those later.

---

## 3. CLI Coding Agents

You need **at least one** CLI coding agent. Multiple agents give broader capabilities and redundancy — different models have different strengths.

### Recommended

- **[OpenCode](https://github.com/anomalyco/opencode)** (`curl -fsSL https://opencode.ai/install | bash` or `brew install anomalyco/tap/opencode`) — `provider = "opencode"`. **This is the shipped default** in `my-factory/city.toml.template`. No paid subscription required — runs on pay-as-you-go API credits (Anthropic, OpenRouter) or provider-native auth.
- **Claude Code** (`brew install anthropic/tap/claude`) — subscribe to Claude Max 20×
- **Codex CLI** — subscribe to Codex Pro 20× or similar

### Minimum

OpenCode with API credits, or one of Claude Code / Codex CLI at a paid tier, sufficient for sustained multi-agent runs.

### Also fully supported

- [Gemini CLI](https://github.com/google-gemini/gemini-cli) — `provider = "gemini"`

### Others (compatibility not guaranteed)

- [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli)
- [Cursor](https://www.cursor.com/) (agents mode)

For the authoritative list of providers Gas City natively supports — along with the `provider = "..."` value to put in `city.toml` — see [`internal/config/provider.go#L203-L209`](https://github.com/gastownhall/gascity/blob/73f09ddd78fed9b90e0589b324255c36d030eb46/internal/config/provider.go#L203-L209) in the Gas City source.

### Telling your factory which agent to use

Whichever agent you pick, name it once in your city configuration. **The shipped
default is OpenCode**, so if you are using a different agent you must change this.
After you copy the templates (see the Quickstart in [`README.md`](README.md)), edit
`my-factory/city.toml`:

```toml
[workspace]
name = "my-factory"
provider = "opencode"        # or "claude", "codex", "gemini", ...

[providers.opencode]         # must name the same provider as above
base = "builtin:opencode"
```

Every agent in the factory inherits `provider`, so changing it switches the whole
pipeline. Gas City also needs the matching `[providers.<name>]` catalog entry —
`gc doctor --fix` adds it for you, and the template ships it so the config validates
before you run doctor. Change both together.

You can override the provider for a single agent by setting `provider` in that
agent's `agent.toml`, which is how you would run, say, the reviewer on a different
model than the builder.

Note that `[session] provider` is a different setting — it selects where sessions
run (`tmux`, `k8s`), not which agent CLI to use. Check what actually resolved with:

```bash
gc config explain --agent <agent-name>
```

---

## 4. Authenticate

Each agent provider has its own auth flow. After installing:

```bash
# Claude Code
claude login

# Codex
codex login

# (repeat per provider)
```

Then confirm Gas City can see the authenticated CLI:

```bash
gc doctor
```

---

## 5. Python installation

[Python 3.8+](https://www.python.org/downloads/) is required to run the factory-activity-agent script, which makes the curriculum setup and teardown much easier. You can check your Python version with `python3 --version`.

---

## 6. Clone This Repo

```bash
git clone https://github.com/actual-software/software-factory-intensive.git
cd software-factory-intensive
```

Your Gas City factory lives at `my-factory/` — you'll copy the committed templates and register it in L1 (or see [`my-factory/README.md`](my-factory/README.md) for the step-by-step). Your per-session deliverables land under `activities/`. See `reference-project/fired-up-pizza/` for a completed example.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `gc: command not found` | Homebrew didn't link the binary. Run `brew link gascity` or ensure `$(brew --prefix)/bin` is on `$PATH`. |
| `gc doctor` fails `check-core-tools` | Install the missing tool via `brew install <tool>` (macOS) or your package manager (Linux). |
| Windows `gc` runs but hangs | You're likely running from PowerShell. Switch to the WSL shell. |
| Provider not recognized | Check your `provider = "..."` value matches one in the [Gas City provider registry](https://github.com/gastownhall/gascity/blob/73f09ddd78fed9b90e0589b324255c36d030eb46/internal/config/provider.go#L203-L209). |
