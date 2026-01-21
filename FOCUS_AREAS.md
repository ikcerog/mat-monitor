# Focus Areas: US Housing, Mortgage, Storytelling & Culture

## Overview

This RSS monitoring system is specifically focused on:

1. **US Housing Market** (with some Canada overlap)
2. **Mortgage Industry & Technology**
3. **Consumer Housing & Lifestyle**
4. **Enterprise Culture & Workplace**
5. **Storytelling & Brand Narratives**

**NOT focused on**:
- Physical technology/cloud platforms (unless directly related to mortgage/housing)
- General advertising/marketing
- Non-US markets (except Canada where relevant)

---

## 📰 **RSS Sources (20 feeds)**

### Mortgage Industry (4 feeds)
- **HousingWire** - Leading mortgage industry news
- **National Mortgage News** - Lending & mortgage trends
- **Mortgage Professional America** - Professional insights
- **Rocket Companies News** - Major lender updates

### Real Estate (3 feeds)
- **Inman** - Real estate news & technology
- **The Real Deal** - Real estate business & markets
- **Forbes Real Estate** - Market analysis & trends

### Consumer Housing & Lifestyle (3 feeds)
- **Good Housekeeping** - Consumer baseline
- **Apartment Therapy** - Home design & living
- **Curbed** - Housing, architecture & design

### Enterprise Culture & Workplace (3 feeds)
- **Fast Company - Work Life** - Workplace culture
- **Fast Company - Innovation** - Best work stories
- **Harvard Business Review** - Leadership & culture

### Financial Services (2 feeds)
- **Banking Dive** - Banking & fintech
- **LendingTree Blog** - Consumer finance

### Community (5 feeds - Reddit)
- **r/RealEstate** - Market discussions
- **r/FirstTimeHomeBuyer** - Consumer insights
- **r/Mortgages** - Lending conversations
- **r/Work** - Workplace culture
- **r/Fintech** - Technology trends

---

## 🎯 **Entity Extraction Focus**

### Brands We Track
**Mortgage Lenders:**
- Rocket Mortgage, Better.com, loanDepot, UWM, Guaranteed Rate
- Wells Fargo, Chase, Bank of America (mortgage divisions)

**Real Estate Platforms:**
- Zillow, Redfin, Realtor.com, Compass, Opendoor

**Consumer Housing:**
- IKEA, Wayfair, Home Depot, Lowe's

**Mortgage Technology:**
- Blend, ICE Mortgage Technology, Black Knight, DocuSign, Snapdocs

### Technologies We Track
**Mortgage-Specific:**
- LOS (loan origination system), POS, digital mortgage, eClosing, automated underwriting

**Customer Experience:**
- CRM, customer experience, personalization, journey mapping

**AI & Storytelling:**
- AI for customer engagement, chatbots, NLP, sentiment analysis

**Design & UX:**
- User experience, mobile apps, design thinking, accessibility

### Themes We Track
**Cultural Themes:**
- Company culture, employee experience, remote/hybrid work
- Work-life balance, mental health, DEI
- Innovation culture, best place to work

**Storytelling Themes:**
- Brand narrative, content marketing, thought leadership
- Customer stories, authenticity, emotional connection
- Brand voice, messaging

**Housing Market Terms:**
- Home prices, inventory, bidding wars, appraisal
- Down payment, closing costs, contingency

### Products We Track
**Mortgage Products:**
- 30-year fixed, 15-year fixed, ARM, FHA/VA/USDA loans
- HELOC, refinance, jumbo loans

**Digital Tools:**
- Mortgage calculators, pre-approval tools, mobile apps

### Metrics We Track
**Mortgage Metrics:**
- Interest rates, APR, LTV, DTI, credit scores
- Median home price, housing inventory, days on market

**Business Metrics:**
- Customer satisfaction, NPS, conversion rates
- Loan volume, origination volume

---

## 📊 **Output Files**

### 1. **stories_export.json** - NEW! Primary LLM-Ready Format
```json
{
  "metadata": {
    "generated_at": "2026-01-20T...",
    "total_stories": 150,
    "total_signals": 8,
    "date_range": {...}
  },
  "stories": [
    {
      "id": 1,
      "title": "...",
      "url": "...",
      "source": {
        "outlet": "HousingWire",
        "category": "Mortgage Industry"
      },
      "publication": {
        "date": "...",
        "author": "..."
      },
      "content": {
        "description": "...",
        "summary": "...",
        "full_content_available": true
      },
      "entities": {
        "brands": ["Rocket Mortgage", "..."],
        "technologies": ["digital mortgage", "..."],
        "cultural_themes": ["employee experience"],
        "storytelling_themes": ["brand narrative"],
        "housing_terms": ["home prices", "..."]
      },
      "analysis": {
        "has_mortgage_focus": true,
        "has_housing_focus": true,
        "has_culture_focus": false,
        "has_storytelling_focus": true
      }
    }
  ],
  "signals": [
    {
      "signal_id": "signal_001",
      "name": "Digital Mortgage Innovation",
      "metrics": {
        "story_count": 15,
        "momentum": "rising"
      },
      "entities": {...},
      "analysis": {
        "is_mortgage_focused": true,
        "is_storytelling_focused": true
      }
    }
  ],
  "summary_statistics": {
    "by_category": {...},
    "by_focus_area": {
      "mortgage": 45,
      "housing": 38,
      "culture": 22,
      "storytelling": 15
    }
  }
}
```

**Perfect for:**
- Feeding to LLMs for analysis
- Tabular data processing
- Trend identification
- Focus area filtering

### 2. **ongoing_summary_cache_enhanced.txt** - Human-Readable
Organized by signals with:
- Source attribution (outlet name, date)
- Entity highlights (brands, technologies, themes)
- Content summaries
- Clear formatting

### 3. **analysis_scaffold.json** - Strategic Analysis
Hierarchical structure:
- Timeframe → Environment → Signals → Trends → Implications → Risks → Questions

### 4. **Traditional Outputs** (Still Generated)
- `summary_popular.txt` - Top trending stories
- `summary_obscure.txt` - Niche opportunities
- `linkedin_*.txt` - 6 content chunks for social media
- `trend_data.json` - Historical tracking

---

## 🔍 **Use Cases**

### For LLM Analysis
**Use `stories_export.json`:**
```
"Show me all stories focused on mortgage technology from this week"
→ Filter: analysis.has_mortgage_focus = true AND entities.technologies

"What cultural themes are appearing in enterprise stories?"
→ Group by: entities.cultural_themes where source.category = "Enterprise Culture"

"Which brands are getting the most storytelling coverage?"
→ Count: entities.brands where analysis.has_storytelling_focus = true
```

### For Market Research
**Use `analysis_scaffold.json`:**
- Identify emerging mortgage trends
- Track competitor activity
- Monitor regulatory changes
- Spot market opportunities

### For Content Creation
**Use `ongoing_summary_cache_enhanced.txt`:**
- Find story inspiration
- Track industry narratives
- Identify customer pain points
- Discover storytelling angles

### For Social Media
**Use `linkedin_*.txt`:**
- Ready-made content chunks
- Trend-based narratives
- Niche insights
- Industry commentary

---

## 📈 **Typical Story Distribution**

Based on focus areas:

```
Mortgage Industry:     30-40% of stories
Real Estate:           20-25%
Consumer Housing:      15-20%
Enterprise Culture:    10-15%
Financial Services:    10-15%
Community:            5-10%
```

Focus distribution:
```
Mortgage Focus:        35-45% of stories
Housing Focus:         30-40%
Culture Focus:         15-25%
Storytelling Focus:    10-20%
```

---

## 🎯 **Key Story Indicators**

**High-Value Mortgage Stories:**
- New lending products or technologies
- Rate changes and market shifts
- Regulatory changes (CFPB, GSEs)
- Major lender announcements
- Industry M&A activity

**High-Value Housing Stories:**
- Market trend shifts (inventory, prices)
- First-time homebuyer insights
- Affordability challenges/solutions
- Design and lifestyle trends
- Regional market analysis

**High-Value Culture Stories:**
- "Best places to work" features
- Innovation culture case studies
- Employee experience initiatives
- Remote/hybrid work trends
- DEI programs and impact

**High-Value Storytelling:**
- Brand narrative transformations
- Customer success stories
- Thought leadership pieces
- Authentic brand voice examples
- Emotional connection strategies

---

## 💡 **Analysis Tips**

### Finding Mortgage Technology Stories
```python
# From stories_export.json
mortgage_tech = [
    story for story in data['stories']
    if story['analysis']['has_mortgage_focus']
    and len(story['entities']['technologies']) > 0
]
```

### Tracking Cultural Themes
```python
# Count cultural theme frequency
from collections import Counter

cultural_themes = Counter()
for story in data['stories']:
    if story['analysis']['has_culture_focus']:
        cultural_themes.update(story['entities']['cultural_themes'])

print(cultural_themes.most_common(10))
```

### Identifying Storytelling Excellence
```python
# Find stories with strong storytelling signals
storytelling_stories = [
    story for story in data['stories']
    if story['analysis']['has_storytelling_focus']
    and len(story['entities']['storytelling_themes']) >= 2
]
```

---

## 🔄 **Daily Workflow**

1. **Automated Collection** (7:50 AM UTC daily)
   - Fetch 20 RSS feeds
   - Extract full content + metadata
   - Capture dates, authors, outlets

2. **Entity Extraction**
   - Identify brands, technologies, themes
   - Tag focus areas (mortgage, housing, culture, storytelling)
   - Extract people, products, metrics

3. **Content Summarization**
   - Generate 2-3 sentence summaries
   - Preserve key facts and insights
   - Maintain storytelling elements

4. **Signal Clustering** (if scikit-learn available)
   - Group related stories
   - Calculate momentum (rising/stable/declining)
   - Identify emerging patterns

5. **Generate Outputs**
   - `stories_export.json` - LLM-ready tabular format
   - `ongoing_summary_cache_enhanced.txt` - Human-readable
   - `analysis_scaffold.json` - Strategic analysis
   - LinkedIn chunks, popular/obscure summaries

6. **Commit & Push**
   - Auto-commit all outputs to git
   - Track changes over time

---

## 🚀 **Getting Started**

### Run Manually
```bash
npm run collect              # Collect RSS feeds
python3 analyze_summaries.py # Analyze & generate outputs
```

### Use JSON Export
```python
import json

# Load the export
with open('stories_export.json', 'r') as f:
    data = json.load(f)

# Get all mortgage stories
mortgage_stories = [
    s for s in data['stories']
    if s['analysis']['has_mortgage_focus']
]

# Print summary
for story in mortgage_stories[:5]:
    print(f"{story['title']}")
    print(f"  Source: {story['source']['outlet']}")
    print(f"  Brands: {', '.join(story['entities']['brands'])}")
    print()
```

### Feed to LLM
```
Prompt: "Analyze these mortgage industry stories and identify the top 3
emerging trends. Focus on technology adoption and customer experience."

[Paste contents of stories_export.json where has_mortgage_focus: true]
```

---

## 📝 **Customization**

### Add New RSS Sources
Edit `rss-config.json`:
```json
{
  "name": "New Source",
  "url": "https://example.com/feed/",
  "category": "Mortgage Industry",
  "enabled": true
}
```

### Add New Entity Patterns
Edit `entity_extractor.py`:
```python
BRAND_PATTERNS = [
    r'\b(?:NewBrand|AnotherBrand)\b',
    # ... existing patterns
]
```

### Adjust Focus Detection
Edit `json_story_exporter.py`:
```python
def _has_mortgage_focus(story: Dict) -> bool:
    # Customize detection logic
    pass
```

---

**System Optimized For:** US Housing Market | Mortgage Industry | Consumer Storytelling | Enterprise Culture

**Best For:** Market research | Content inspiration | Trend tracking | Competitive intelligence | Brand storytelling
