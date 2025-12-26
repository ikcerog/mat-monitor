# RSS Feed Collector

Automated RSS feed collector that compiles feeds into a clean text file optimized for AI model consumption.

## Features

- Automatic daily collection via GitHub Actions at 7:50 AM
- Manual trigger option from GitHub Actions tab
- Converts RSS feeds to clean, markup-free text
- Configurable feed sources and settings
- Automatic commits to repository

## Files

- `rss-collector.js` - Main collector script
- `analyze_summaries.py` - Python script that analyzes RSS summaries
- `rss-config.json` - RSS feeds and settings configuration
- `summary_cache.txt` - Output file with compiled feeds (all stories)
- `summary_popular.txt` - Curated popular topics and trends with buzzwords
- `summary_obscure.txt` - Curated obscure/opportunity stories with buzzwords
- `.github/workflows/rss-collector.yml` - GitHub Actions workflow

## Setup

### 1. Install Dependencies (for local testing)

```bash
npm install
```

**Note:** Python 3.x is also required for the summary analyzer.

### 2. Configure RSS Feeds

Edit `rss-config.json`:

```json
{
  "feeds": [
    {
      "name": "Your Feed Name",
      "url": "https://example.com/rss",
      "enabled": true
    }
  ],
  "settings": {
    "maxArticlesPerFeed": 10,
    "includeDescription": true,
    "includeContent": true,
    "separator": "\n---\n"
  }
}
```

**Adding/Removing Feeds:**
- Add new feed objects to the `feeds` array
- Set `enabled: false` to temporarily disable a feed
- Remove feed objects to permanently delete them

### 3. Adjust Collection Time

Edit `.github/workflows/rss-collector.yml`:

```yaml
schedule:
  - cron: '50 7 * * *'  # Change to your desired time (UTC)
```

**Time Format:** `'minute hour * * *'`

**Examples:**
- `'50 7 * * *'` = 7:50 AM UTC
- `'30 12 * * *'` = 12:30 PM UTC
- `'0 0 * * *'` = Midnight UTC

**Convert your timezone to UTC:** https://www.worldtimebuddy.com/

### 4. GitHub Actions Permissions

The workflow uses `GITHUB_TOKEN` which is automatically provided by GitHub Actions. No additional secrets needed!

The workflow has `permissions: contents: write` which allows it to commit the updated `summary_cache.txt` file.

## Usage

### Automatic Collection

The workflow runs automatically based on the schedule in `rss-collector.yml`.

### Manual Run

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **RSS Feed Collector** workflow
4. Click **Run workflow** button
5. Click **Run workflow** to confirm

### Local Testing

```bash
# Run just the RSS collector
npm run collect

# Run just the analyzer
npm run analyze

# Run both (collector + analyzer)
npm run collect:all
```

This will fetch feeds and update all summary files locally.

## Output Format

### summary_cache.txt

Contains all RSS feed stories with headlines and descriptions:

```
Last updated: MM/DD/YYYY at HH:MM:SS AM/PM
Total feeds: N

FEED: Feed Title
SOURCE: https://example.com/rss

Article Title
https://link-to-article
Brief description...

[... more articles ...]
```

### summary_popular.txt

Curated list of popular/trending stories optimized for AI prompts:

```
# POPULAR TOPICS & TRENDS
Generated: MM/DD/YYYY at HH:MM:SS AM/PM
Stories: 20

KEY BUZZWORDS: AI, DEAL, CTV, OPENAI, M&A, ...

---

1. Story Title
   Description excerpt...
   [AI, DEAL, OPENAI]

2. Next Story...
   ...
```

### summary_obscure.txt

Curated list of obscure/opportunity stories optimized for AI prompts:

```
# OBSCURE OPPORTUNITIES & EMERGING STORIES
Generated: MM/DD/YYYY at HH:MM:SS AM/PM
Stories: 20

KEY BUZZWORDS: PARTNERSHIP, PERSONALIZATION, VR, ...

---

1. Story Title
   Description excerpt...
   [PARTNERSHIP, AI]

2. Next Story...
   ...
```

**Why two separate files?**
- `summary_popular.txt` - Mainstream trends, major deals, big tech news
- `summary_obscure.txt` - Niche opportunities, emerging tech, specialized partnerships
- Both are concise (~80-85 lines) to minimize token usage as prompt attachments
- Buzzwords at the top provide quick context for AI models

## GitHub Policy Compliance

The workflow:
- Runs once daily (complies with reasonable usage)
- Can be manually triggered (for testing/debugging)
- Only commits when changes are detected
- Uses official GitHub Actions and standard tokens
- Follows GitHub Actions best practices

**Note:** GitHub Actions has a usage limit. The free tier includes:
- Public repos: Unlimited minutes
- Private repos: 2,000 minutes/month

This workflow typically uses ~1-2 minutes per run, so 30 days = ~30-60 minutes/month.

## Troubleshooting

### Workflow not running

1. Check that GitHub Actions is enabled for your repository
2. Verify the workflow file is in `.github/workflows/`
3. Check Actions tab for any errors

### Feeds not fetching

1. Verify RSS feed URLs are correct and accessible
2. Check Actions logs for specific error messages
3. Test locally with `npm run collect`

### Commits not appearing

1. Ensure `permissions: contents: write` is in the workflow
2. Check that `summary_cache.txt` actually changed
3. Review Actions logs for git errors

## Customization

### Change Output Filename

Edit `rss-collector.js`:

```javascript
const OUTPUT_FILE = path.join(__dirname, 'your-filename.txt');
```

And update the workflow to commit your new filename.

### Adjust Text Cleaning

Edit the `htmlToCleanText` function in `rss-collector.js` to modify how HTML is converted to text.

### Change Article Limit

Edit `rss-config.json`:

```json
"settings": {
  "maxArticlesPerFeed": 20  // Change this number
}
```

## License

MIT
