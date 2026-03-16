#!/usr/bin/env python3
"""
Pricing Intelligence Blog — Post Publisher
==========================================
Drop a JSON file in /posts and run this script to:
  1. Register it in posts/index.json
  2. Commit & push to GitHub

Usage:
  python publish.py posts/2026-03-20-my-new-post.json
  python publish.py --all   (re-sync all posts in /posts folder)
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

POSTS_DIR = Path(__file__).parent / "posts"
INDEX_FILE = POSTS_DIR / "index.json"


def load_index():
    if INDEX_FILE.exists():
        with open(INDEX_FILE) as f:
            return json.load(f)
    return []


def save_index(index):
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)
    print(f"✓ Updated posts/index.json ({len(index)} posts)")


def validate_post(path: Path):
    """Basic validation of post JSON structure."""
    required = ["id", "title", "date", "content", "excerpt"]
    with open(path) as f:
        post = json.load(f)
    missing = [k for k in required if k not in post]
    if missing:
        print(f"✗ Missing required fields: {missing}")
        return False
    print(f"✓ Post valid: '{post['title']}'")
    return True


def add_post(filename: str, index: list) -> list:
    if filename not in index:
        index.insert(0, filename)  # newest first
        print(f"✓ Added: {filename}")
    else:
        print(f"→ Already in index: {filename}")
    return index


def sync_all(index: list) -> list:
    """Rebuild index from all JSON files in /posts (except index.json)."""
    files = sorted(
        [f.name for f in POSTS_DIR.glob("*.json") if f.name != "index.json"],
        reverse=True  # newest first (relies on date-prefixed filenames)
    )
    print(f"→ Found {len(files)} post files")
    return files


def git_push(message: str):
    """Stage, commit, and push."""
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✓ Pushed to GitHub")
    except subprocess.CalledProcessError as e:
        print(f"✗ Git error: {e}")
        sys.exit(1)


def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(0)

    index = load_index()

    if args[0] == "--all":
        index = sync_all(index)
        save_index(index)
        git_push(f"sync: rebuild index with {len(index)} posts")

    else:
        post_path = Path(args[0])
        if not post_path.exists():
            print(f"✗ File not found: {post_path}")
            sys.exit(1)

        if not validate_post(post_path):
            sys.exit(1)

        filename = post_path.name
        index = add_post(filename, index)
        save_index(index)

        # Read title for commit message
        with open(post_path) as f:
            post = json.load(f)

        git_push(f"post: {post['title']}")

    print("\n✅ Done! Blog updated at your GitHub Pages URL.")


if __name__ == "__main__":
    main()
