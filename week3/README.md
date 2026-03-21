# Week 3: TMDB MCP Server

This project implements a local MCP server that wraps the TMDB API and connects to Claude Desktop over STDIO.

We built three tools on top of TMDB:

- `search_media`: search movies or TV shows by keyword
- `get_recommendations`: get similar titles from a TMDB id
- `trending_media`: get trending movies or TV shows

## Setup

This project uses the existing course Python environment and project dependencies managed in `pyproject.toml`.

Install dependencies from the repository root:

```bash
poetry lock
poetry install
```

Create a local environment file at `week3/.env`:

```env
TMDB_API_KEY=your_tmdb_api_key_here
```

## Run Locally

The MCP server entrypoint is:

```bash
python -m week3.server.main
```

In practice, Claude Desktop launches this process for us.

## Claude Desktop Configuration

Add the following to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "globalShortcut": "",
  "preferences": {
    "menuBarEnabled": false,
    "quickEntryShortcut": "off",
    "coworkScheduledTasksEnabled": true,
    "ccdScheduledTasksEnabled": true,
    "sidebarMode": "chat",
    "bypassPermissionsModeEnabled": true,
    "coworkWebSearchEnabled": true
  },
  "mcpServers": {
    "tmdb-discovery": {
      "command": "/opt/anaconda3/envs/cs146s/bin/python",
      "args": ["-m", "week3.server.main"],
      "cwd": "****YOUR_PATH_HERE******/modern-software-dev-assignments",
      "env": {
        "PYTHONPATH": "****YOUR_PATH_HERE******/modern-software-dev-assignments"
      }
    }
  }
}
```

After saving the config, fully quit and reopen Claude Desktop.
