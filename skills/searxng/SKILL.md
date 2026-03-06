# SearXNG Search

Search the web using your local SearXNG instance - a privacy-respecting metasearch engine.

## Commands

### Web Search
```bash
python3 /home/admin/.openclaw/workspace/skills/searxng/scripts/searxng.py search "query"              # Top 10 results
python3 /home/admin/.openclaw/workspace/skills/searxng/scripts/searxng.py search "query" -n 20        # Top 20 results
python3 /home/admin/.openclaw/workspace/skills/searxng/scripts/searxng.py search "query" --format json # JSON output
```

### Category Search
```bash
python3 /home/admin/.openclaw/workspace/skills/searxng/scripts/searxng.py search "query" --category images
python3 /home/admin/.openclaw/workspace/skills/searxng/scripts/searxng.py search "query" --category videos
```

### Advanced Options
```bash
python3 /home/admin/.openclaw/workspace/skills/searxng/scripts/searxng.py search "query" --language en
python3 /home/admin/.openclaw/workspace/skills/searxng/scripts/searxng.py search "query" --time-range day
```

## Configuration

**Required:** Set the `SEARXNG_URL` environment variable to your SearXNG instance:

```bash
export SEARXNG_URL=http://localhost:8080
```

Default (if not set): `http://localhost:8080`

## Features

- 🔒 Privacy-focused (uses your local instance)
- 🌐 Multi-engine aggregation
- 📰 Multiple search categories
- 🎨 Rich formatted output
- 🚀 Fast JSON mode for programmatic use

## API

Uses your local SearXNG JSON API endpoint (no authentication required by default).