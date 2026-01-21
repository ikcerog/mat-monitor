# RSS Monitor Pipeline - Streamlined

## Current Flow (Simplified)

```
RSS Feeds (20 sources)
    ↓
rss-collector.js → summary_cache.txt
    ↓
analyze_summaries.py
    ├─ ongoing_summary_cache_enhanced.txt (detailed compiled view)
    ├─ stories_export.json (granular LLM-ready data)
    ├─ macro_trends.json (strategic synthesis)
    ├─ analysis_scaffold.json (hierarchical framework)
    └─ trend_data.json (historical tracking)
```

## Output Files

### Core Outputs (JSON for LLM)
- **macro_trends.json** - Strategic synthesis with narrative threads, thematic clusters, momentum analysis
- **stories_export.json** - Granular story data in tabular format
- **analysis_scaffold.json** - Hierarchical trend framework

### Supporting Files
- **summary_cache.txt** - Raw RSS feed data
- **ongoing_summary_cache_enhanced.txt** - Human-readable detailed view with signal clustering
- **trend_data.json** - Historical trend tracking (internal use)

## Removed Files (Obsolete)
- ~~linkedin_*.txt~~ (6 files) - Removed, not needed
- ~~summary_popular.txt~~ - Removed
- ~~summary_obscure.txt~~ - Removed
- ~~ongoing_summary_cache.txt~~ - Removed (replaced by enhanced version)

## About the Old Content Issue

### Problem
You're seeing 2023-2024 news stories in your Power Automate output.

### Root Cause
The RSS feeds in the repository contain **stale data from before the housing/mortgage refocus**.

### Why This Happened
1. The RSS config was updated on Jan 21 to new housing-focused feeds
2. The GitHub Actions workflow runs on schedule (daily at 7:50 AM UTC)
3. The workflow hasn't run successfully since the config update
4. Your Power Automate is reading cached files that still have old marketing/adtech content

### Solution
Wait for the next GitHub Actions workflow run. When it succeeds, you'll see:
- Fresh 2026 content from HousingWire, National Mortgage News, etc.
- Housing/mortgage/culture topics instead of marketing/adtech
- Current dates in all outputs

### How to Verify Fresh Data
Check the first line of `summary_cache.txt`:
```
Last updated: [date/time]
```

Check the feed sources:
```
FEED: HousingWire
FEED: National Mortgage News
FEED: Inman
```

If you see "Marketing Dive" or "Adweek", it's still using old data.

### Manual Trigger
You can manually trigger the workflow from GitHub Actions:
1. Go to Actions tab
2. Select "RSS Feed Collector"
3. Click "Run workflow"

## GitHub Actions Schedule
- Runs daily at 7:50 AM UTC
- Collects from 20 RSS sources
- Commits updated files automatically
- Workflow file: `.github/workflows/rss-collector.yml`

## RSS Sources (20 feeds)
Focus areas:
- **Mortgage Industry**: HousingWire, National Mortgage News, Mortgage Professional America, Rocket Companies
- **Real Estate**: Inman, The Real Deal, Forbes Real Estate
- **Consumer Housing**: Curbed, Apartment Therapy, Good Housekeeping, LendingTree
- **Enterprise Culture**: Fast Company, Harvard Business Review
- **Finance**: Banking Dive
- **Community**: Reddit (Real Estate, First Time Home Buyer, Mortgages, Work, Fintech)
