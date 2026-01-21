# Summary Cache Enhancement System

## Overview

This enhancement transforms the RSS summary cache from a simple text-based list into a rich, hierarchical analytical framework that enables macro-level trend analysis, entity tracking, and signal clustering.

## What's New

### 1. **Enhanced Data Capture**
- **Full article content** extraction (when available from RSS feeds)
- **Rich metadata**: publication dates, authors, source outlets
- **Structured format**: All data clearly labeled and parseable

### 2. **Advanced Entity Extraction**
Automatically identifies and categorizes:
- **Brands**: Nike, Lexus, Campbell's, etc.
- **Technologies**: AI, GenAI, CTV, OTT, streaming, etc.
- **Companies**: Agencies, platforms, publishers
- **People**: Executives, marketers, influencers
- **Products**: Specific products and platforms
- **Metrics**: ROI, ROAS, CTR, conversion rates

### 3. **Content Summarization**
- Extracts 2-3 sentence summaries from full article content
- Uses intelligent sentence scoring (TF-IDF + entity density + position)
- Preserves key facts and insights

### 4. **Signal Clustering**
- Groups related stories into thematic "signals"
- Uses TF-IDF vectorization + K-means clustering
- Identifies:
  - **Emerging signals**: New topics appearing (3-10 stories)
  - **Building signals**: Growing momentum (10+ stories, rising)
  - **Lasting signals**: Sustained topics (15+ stories, stable)
- Calculates momentum: Rising ↑ / Stable → / Declining ↓

### 5. **Hierarchical JSON Analysis**
Creates `analysis_scaffold.json` with structure:
```
Timeframe → Environment → Signals → Trends → Implications → Risks → Questions
```

**Sections:**
- **Meta**: Coverage statistics, time period, outlet breakdown
- **Environment**: Macro context, market dynamics, regulatory climate
- **Signals**: Clustered stories with entities and momentum
- **Trends**: Emerging, building, and lasting trends
- **Implications**: Opportunities, threats, strategic shifts
- **Risks**: Technological, regulatory, competitive, market
- **North Star Questions**: Strategic questions for leadership

### 6. **Enhanced Text Output**
`ongoing_summary_cache_enhanced.txt` includes:
- **Source attribution**: Every story shows outlet name
- **Entity highlights**: Brands, technologies, companies called out
- **Signal clustering**: Stories grouped by theme
- **Content summaries**: Brief summaries instead of just descriptions
- **Metadata**: Dates, authors, URLs clearly visible

## File Structure

```
mat-monitor/
├── entity_extractor.py          # NLP-based entity extraction
├── content_summarizer.py        # Extractive text summarization
├── signal_clustering.py         # Story clustering logic
├── scaffold_generator.py        # JSON hierarchy builder
├── analyze_summaries.py         # Enhanced main analyzer
├── rss-collector.js             # Enhanced RSS collector
├── requirements.txt             # Python dependencies
├── analysis_scaffold.json       # NEW: Hierarchical analysis
├── ongoing_summary_cache_enhanced.txt  # NEW: Enhanced cache
└── [existing files...]
```

## New Dependencies

### Python (install with `pip3 install -r requirements.txt`)
- `scikit-learn>=1.3.0` - Clustering and vectorization
- `numpy>=1.24.0` - Numerical operations
- `pytrends>=4.9.0` - Google Trends (already installed)

**Note**: Signal clustering requires scikit-learn and numpy. If not available, the system will still work without clustering.

## How It Works

### Data Flow

```
RSS Feeds (19 sources)
    ↓
rss-collector.js (enhanced)
    ↓
summary_cache.txt (structured format with TITLE/URL/DATE/AUTHOR/DESCRIPTION/CONTENT)
    ↓
analyze_summaries.py (enhanced)
    ├─→ Entity Extraction (brands, tech, companies, people)
    ├─→ Content Summarization (2-3 sentences)
    ├─→ Signal Clustering (TF-IDF + K-means)
    └─→ Outputs:
        ├─ analysis_scaffold.json (hierarchical analysis)
        ├─ ongoing_summary_cache_enhanced.txt (rich text format)
        ├─ summary_popular.txt (top stories)
        ├─ summary_obscure.txt (niche opportunities)
        └─ linkedin_*.txt (6 content chunks)
```

### Entity Extraction

**Pattern-based** regex extraction:
- 100+ known brands (Google, Meta, Nike, Lexus, etc.)
- Technology terms (AI, GenAI, CTV, programmatic, etc.)
- Agencies (AKQA, Ogilvy, Publicis, etc.)
- Products (iPhone, AWS, Salesforce, etc.)
- Metrics (ROI, ROAS, CTR, etc.)
- Industry-specific terminology

### Signal Clustering

**Algorithm**:
1. Vectorize stories using TF-IDF (titles + descriptions + entities)
2. Determine optimal cluster count (dynamic based on story volume)
3. Run K-means clustering
4. Generate cluster names from top terms + entities
5. Calculate momentum (comparing last 7 days vs previous 7)

**Example Signal**:
```
SIGNAL: Lexus & AKQA - Generative [15 stories, Rising]
Brands using AI for marketing content creation.
Key Players: Brands[Lexus, AKQA, Campbell's] | Tech[GenAI, AI, ChatGPT]
```

## Output Examples

### analysis_scaffold.json
```json
{
  "meta": {
    "timeframe": {
      "period": "Week of January 13-20, 2026",
      "total_stories": 850,
      "unique_outlets": 19
    }
  },
  "signals": [
    {
      "cluster_name": "AI-Driven Content Creation Surge",
      "momentum": "rising",
      "story_count": 45,
      "entities": {
        "brands": ["Lexus", "Campbell's", "Rocket"],
        "technologies": ["GenAI", "ChatGPT", "AI"]
      }
    }
  ],
  "trends": {
    "emerging": [...],
    "building": [...],
    "lasting": [...]
  },
  "implications": {
    "opportunities": [...],
    "threats": [...]
  },
  "north_star_questions": [
    {
      "question": "Will AI democratize creativity or concentrate it among platform owners?",
      "category": "Industry Structure",
      "urgency": "high"
    }
  ]
}
```

### ongoing_summary_cache_enhanced.txt
```
================================================================================
ENHANCED ANALYSIS: 01/20/2026
================================================================================
Total Stories: 850 | Clustered: 823 | Unique Outlets: 19 | Signals: 23
Top Signals: AI Content Creation (↑45) | CTV Measurement (↑32) | Privacy Tech (→28)

================================================================================
SIGNAL: AI-Driven Content Creation [45 stories, Rising]
================================================================================
Brands increasingly using generative AI for marketing content creation.
Key Players: Brands[Lexus, AKQA, Campbell's] | Tech[GenAI, ChatGPT]

• Lexus takes generative AI for a spin in new holiday marketing content
  SOURCE: Marketing Dive | DATE: Jan 08, 2026
  Lexus partnered with AKQA to create "Built for Every Kind of Wonder"
  featuring surreal AI-generated scenes like floating ski slopes, testing the
  creative limits of generative AI in automotive marketing.
  ENTITIES: Brands[Lexus, AKQA] | Tech[GenAI, AI]
  URL: https://...

[... more stories ...]
```

## Usage

### Run Enhanced Analysis
```bash
# 1. Collect RSS feeds (enhanced with full content)
npm run collect

# 2. Run enhanced analyzer
python3 analyze_summaries.py
```

### Outputs Generated
- `analysis_scaffold.json` - Machine-readable hierarchical analysis
- `ongoing_summary_cache_enhanced.txt` - Human-readable enhanced cache
- `summary_popular.txt` - Top trending stories
- `summary_obscure.txt` - Niche opportunities
- `linkedin_*.txt` - 6 content chunks for social media
- `trend_data.json` - Historical trend tracking

## Configuration

No configuration changes required! The system is backward-compatible and will:
- Work without spaCy (using pattern-based extraction)
- Work without clustering (falls back to single cluster)
- Work without full content (uses descriptions)

## Key Features for Analysis

### 1. **Source Visibility**
Every story now shows:
- Outlet name (e.g., "Marketing Dive", "Adweek")
- Publication date
- Author (when available)

### 2. **Entity Tracking**
See exactly which:
- Brands are mentioned most
- Technologies are trending
- Companies are making moves
- People are being quoted

### 3. **Content Depth**
- Full article summaries (not just headlines)
- Key facts preserved
- Context maintained

### 4. **Trend Analysis**
- Momentum indicators (rising/stable/declining)
- Historical comparison (week over week)
- Emerging patterns detected early

### 5. **Strategic Insights**
- Opportunities identified automatically
- Risks flagged by category
- Strategic questions for leadership
- Market dynamics tracked

## Best Practices

### For Macro-Level Analysis
1. Start with `analysis_scaffold.json` for the big picture
2. Review the "Signals" section for clustered themes
3. Check "Trends" → "Emerging" for early signals
4. Read "North Star Questions" for strategic thinking

### For Content Research
1. Use `ongoing_summary_cache_enhanced.txt` for readable format
2. Search for specific brands/technologies
3. Filter by outlet or date
4. Follow URL links for full articles

### For Social Media
1. Use `linkedin_*.txt` files for ready-made content
2. Chunk 1-3: Trend-based narratives
3. Chunk 4-5: Deals and niche opportunities
4. Chunk 6: Housing/mortgage focus with Google Trends

## Troubleshooting

### "Clustering not available"
- scikit-learn missing → Run: `pip3 install scikit-learn numpy`
- System will group all stories into one cluster (degraded but functional)
- JSON scaffold generation will still work

### "No full content captured"
- Some RSS feeds don't provide full content
- System will use descriptions instead
- Summaries may be shorter but still useful

## Methodology

**The methodology synthesizes source material by:**
1. **Clustering stories** into recurring signals using TF-IDF + K-means
2. **Inferring dynamics** from entity patterns and momentum trends
3. **Abstracting insights** into hierarchical, machine-readable JSON scaffold
4. **Organizing by**: Timeframe → Environment → Trends → Implications → Risks → Questions
5. **Designed for**: Macro-context grounding rather than narrative summary

This approach enables:
- Pattern recognition across hundreds of stories
- Trend emergence detection
- Strategic foresight
- Data-driven decision support

## Future Enhancements

Potential additions:
- Sentiment analysis per signal
- Competitive intelligence tracking
- Custom entity dictionaries
- Multi-week trend visualization
- API endpoint for programmatic access
- Real-time alerting for emerging signals

## License & Credits

Enhanced by Claude (Anthropic) on 2026-01-20

Original system: mat-monitor RSS aggregator
