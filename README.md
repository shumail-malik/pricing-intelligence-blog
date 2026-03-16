# Pricing Intelligence Blog

A lightweight, static blog built for GitHub Pages. No build step, no framework — just HTML, JSON, and a Python publish script.

## Quick Start

### 1. Push to GitHub

```bash
git init
git remote add origin https://github.com/YOUR_USERNAME/pricing-intelligence-blog.git
git add .
git commit -m "init: pricing intelligence blog"
git push -u origin main
```

### 2. Enable GitHub Pages

Go to your repo → **Settings → Pages** → Source: `main` branch, root folder → Save.

Your blog will be live at: `https://YOUR_USERNAME.github.io/pricing-intelligence-blog/`

---

## Publishing Posts (Automation)

### Post format

Every post is a JSON file in `/posts`:

```json
{
  "id": "my-post-slug",
  "title": "My Post Title",
  "date": "2026-03-20",
  "author": "Pricing Intelligence",
  "tags": ["strategy", "pricing"],
  "excerpt": "Short summary shown in the listing.",
  "content": "Full post in Markdown.\n\n## Section\n\nContent here."
}
```

Name the file: `YYYY-MM-DD-slug.json` (e.g. `2026-03-20-my-post.json`)

### Publish a new post

```bash
# 1. Drop your JSON file into /posts
# 2. Run:
python publish.py posts/2026-03-20-my-post.json
```

That's it — the script validates, updates the index, commits, and pushes.

### Re-sync everything

```bash
python publish.py --all
```

### From your automation

Call the publish script from any automation (cron job, n8n, Make, Python script):

```bash
# Generate your post JSON, save it to /posts, then:
python /path/to/blog/publish.py /path/to/blog/posts/YOUR-POST.json
```

---

## Local Preview

Because the blog fetches JSON files, you need a local server (not `file://`):

```bash
# Python (simplest)
cd pricing-intelligence-blog
python -m http.server 8000
# Open http://localhost:8000
```

---

## Structure

```
pricing-intelligence-blog/
├── index.html          ← The entire blog UI (one file)
├── publish.py          ← CLI to publish posts
├── posts/
│   ├── index.json      ← Auto-managed list of posts (newest first)
│   ├── _template.json  ← Copy this to create new posts
│   └── *.json          ← Your blog posts
└── README.md
```

## Markdown Support

The content field supports:

| Syntax | Renders as |
|--------|-----------|
| `## Heading` | H2 heading |
| `### Heading` | H3 heading |
| `**bold**` | Bold |
| `*italic*` | Italic |
| `- item` | Bullet list |
| Blank line | Paragraph break |
