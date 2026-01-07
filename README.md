# RSS Feed Collector

Automated RSS feed collector with AI-powered trend analysis that compiles feeds into multiple formats optimized for AI consumption and social media content generation.

## Features

- **Automatic daily collection** via GitHub Actions at 7:50 AM UTC
- **Manual trigger option** from GitHub Actions tab
- **Clean text conversion** - RSS feeds to markup-free text
- **Trend analysis** - Tracks emerging, building, and lasting trends over time
- **Multi-week compilation** - Maintains 4-week rolling history
- **LinkedIn-ready content** - Generates 5 post-ready content chunks
- **Configurable feed sources** and settings
- **Automatic commits** to repository

## Files

### Core Scripts
- `rss-collector.js` - Main RSS feed collector
- `analyze_summaries.py` - Enhanced analyzer with trend tracking
- `rss-config.json` - RSS feeds and settings configuration
- `.github/workflows/rss-collector.yml` - GitHub Actions workflow

### Daily Summary Files
- `summary_cache.txt` - Complete daily feed compilation (all stories)
- `summary_popular.txt` - Top 20 popular/trending stories with buzzwords
- `summary_obscure.txt` - Top 20 niche/opportunity stories with buzzwords

### Multi-Week Tracking
- `ongoing_summary_cache.txt` - 4-week rolling compilation with date markers
- `trend_data.json` - Historical buzzword and topic frequency data

### LinkedIn Content Chunks (Power Automate Ready)
- `linkedin_01_emerging.txt` - New emerging trends
- `linkedin_02_building.txt` - Trends gaining momentum
- `linkedin_03_lasting.txt` - Consistent long-term trends
- `linkedin_04_deals.txt` - Major deals and announcements
- `linkedin_05_niche.txt` - Niche opportunities and innovations
- `linkedin_06_housing.txt` - Housing/mortgage trends (industry-specific)

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

### ongoing_summary_cache.txt

Multi-week compilation that maintains a rolling 4-week history:

```
=== DATE: MM/DD/YYYY ===
Stories added: N

• Story Title
  [BUZZWORD1, BUZZWORD2]

• Next Story...
  [BUZZWORDS]
```

**Purpose:**
- Tracks stories over time to identify trend patterns
- Automatically removes entries older than 4 weeks
- Enables long-term trend analysis (emerging → building → lasting)

### linkedin_*.txt Files

Six LinkedIn-ready content chunks optimized for Power Automate/Copilot:

1. **linkedin_01_emerging.txt** - 🚀 New emerging trends (first seen in last 3 days)
2. **linkedin_02_building.txt** - 📈 Trends gaining momentum (50%+ growth)
3. **linkedin_03_lasting.txt** - 🎯 Consistent long-term trends (8+ weeks tracked)
4. **linkedin_04_deals.txt** - 💼 Major deals, M&A, partnerships
5. **linkedin_05_niche.txt** - 💡 Under-the-radar opportunities
6. **linkedin_06_housing.txt** - 🏠 Housing/homebuyer trends for mortgage industry

**Format:**
```
# LinkedIn Post: [Title]
Generated: MM/DD/YYYY

## [Section Title]

• Trend/Story
  Tags: [BUZZWORDS]

• Next item...
```

**Use Case:** Feed these files into Power Automate with Office Copilot to:
- Generate polished LinkedIn posts automatically
- Maintain consistent social media presence
- Create content from fresh industry insights
- Customize tone and style via GPT prompts

#### linkedin_06_housing.txt - Special Focus

This chunk is specifically designed for **mortgage companies and real estate professionals** and includes:

**Three Strategic Categories:**
1. **Market Dynamics** - Housing market trends, pricing, inventory
   - Flags direct industry mentions
   - Market challenges and opportunities

2. **What Homebuyers Are Talking About** - Consumer insights
   - Affordability concerns
   - Generational focus (Millennials, Gen Z)
   - First-time buyer challenges
   - **Conversation hooks** automatically identified

3. **Mortgage & Fintech** - Industry developments
   - Interest rate discussions
   - Fintech innovations
   - Lending technology trends

**Conversation Starters** - Pre-written angles for content creation:
- Market challenges → Solutions and approaches
- Buyer concerns → Technology-enabled strategies
- Industry trends → Innovation positioning

**Example output:**
```
### What Homebuyers Are Talking About:
• Millennials struggle with affordability in 2026 housing market
  🎯 Content angles: Affordability angle, Gen focus, First-time buyer

### Mortgage & Fintech:
• Tech-enabled mortgage platforms reshape homebuying experience
  💡 Direct industry mention/relevance
```

### trend_data.json

Historical tracking data (8 weeks):
- Buzzword frequency over time
- Topic appearance patterns
- Used to calculate emerging/building/lasting trends
- Automatically maintained by analyzer

## Trend Analysis Explained

The analyzer tracks three types of trends:

1. **Emerging Trends** - Topics/buzzwords that appeared for the first time in the last 3 days
   - Identifies brand new industry conversations
   - Great for being first to comment on new developments

2. **Building Trends** - Topics showing 50%+ growth compared to earlier periods
   - Spots topics gaining traction
   - Ideal for jumping on momentum before peak popularity

3. **Lasting Trends** - Topics appearing consistently over 8+ weeks
   - Identifies evergreen industry themes
   - Perfect for thought leadership and positioning

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
