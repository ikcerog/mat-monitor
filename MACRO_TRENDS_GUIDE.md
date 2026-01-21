# Macro Trends JSON Guide

## Overview

**`macro_trends.json`** is the **processed, synthesized view** of ongoing trends and narratives emerging from your RSS monitoring. This is the file you want to feed to LLMs for strategic analysis.

### What Makes It Different?

| File | Purpose | When to Use |
|------|---------|-------------|
| `stories_export.json` | Raw tabular data of individual stories | When you need granular story details |
| `analysis_scaffold.json` | Hierarchical framework (timeframe → trends → implications → risks) | When you need structured analysis components |
| **`macro_trends.json`** | **Synthesized narrative threads and strategic insights** | **When you need the "big picture" story** |

---

## Structure

```json
{
  "meta": {
    "generated_at": "2026-01-20T...",
    "synthesis_period": "Week of January 13 - 20, 2026",
    "data_points": {
      "total_stories": 150,
      "total_signals": 8,
      "time_span_days": 7
    }
  },

  "narrative_threads": [
    {
      "thread_id": "thread_01",
      "narrative": "Mortgage lending evolution centered on digital mortgage adoption",
      "theme": "Mortgage & Lending",
      "story_count": 45,
      "momentum": "rising",
      "key_players": {
        "brands": ["Rocket Mortgage", "Better.com", "..."],
        "technologies": ["digital mortgage", "AI", "..."],
        "themes": ["innovation culture"]
      },
      "outlook": "expanding"
    }
  ],

  "thematic_clusters": {
    "mortgage_innovation": {
      "description": "Technology and innovation in mortgage lending",
      "signals": [...],
      "story_count": 52,
      "key_themes": ["digital transformation", "customer experience"]
    },
    "housing_market_dynamics": {...},
    "customer_experience": {...},
    "workplace_culture": {...},
    "industry_transformation": {...}
  },

  "momentum_analysis": {
    "overall_sentiment": "optimistic",
    "distribution": {
      "rising": 5,
      "stable": 2,
      "declining": 1
    },
    "hot_topics": [
      {
        "name": "Digital Mortgage Innovation",
        "story_count": 45,
        "velocity": "high"
      }
    ]
  },

  "entity_landscape": {
    "dominant_brands": [
      {"name": "Rocket Mortgage", "mentions": 23},
      {"name": "Zillow", "mentions": 18}
    ],
    "key_technologies": [
      {"name": "digital mortgage", "mentions": 34},
      {"name": "AI", "mentions": 28}
    ],
    "cultural_movements": [
      {"theme": "innovation culture", "frequency": 12}
    ]
  },

  "focus_area_insights": {
    "mortgage_lending": {
      "signal_count": 3,
      "story_count": 52,
      "top_signals": ["Digital Mortgage Adoption", "..."],
      "momentum": "rising",
      "key_insight": "Primary focus on digital transformation with rising momentum"
    },
    "housing_market": {...},
    "enterprise_culture": {...},
    "brand_storytelling": {...}
  },

  "emerging_patterns": [
    {
      "pattern_type": "technology_wave",
      "description": "Technology adoption theme across multiple signals",
      "technologies": ["digital mortgage", "AI", "automation"],
      "signal_count": 4,
      "significance": "high"
    }
  ],

  "strategic_narrative": {
    "headline": "Rising activity across 5 themes, led by Digital Mortgage Innovation",
    "executive_summary": "Analysis of 150 stories across 8 thematic areas. Strong momentum with 5 rising themes. Primary attention on digital mortgage adoption.",
    "key_shifts": [
      "Growing focus on digital mortgage innovation"
    ],
    "dominant_themes": ["innovation culture", "customer experience"],
    "strategic_questions": [
      "How will digital mortgage adoption reshape competitive dynamics?",
      "What's driving technology adoption patterns?"
    ]
  },

  "macro_observations": [
    "High coverage intensity with 150 stories across 8 themes",
    "Predominantly rising momentum suggests active market dynamics",
    "Broad ecosystem participation (25 brands mentioned)",
    "Technology-heavy coverage (15 technologies tracked)"
  ]
}
```

---

## Key Sections Explained

### 1. **Narrative Threads**
**What it is:** The "big stories" emerging across multiple signals
**Use for:** Understanding overarching narratives

Example:
```json
{
  "narrative": "Mortgage lending evolution centered on digital mortgage adoption",
  "story_count": 45,
  "momentum": "rising",
  "outlook": "expanding"
}
```

**LLM Prompt:**
```
"Based on the narrative threads, what are the top 3 stories I should be paying attention to?"
```

---

### 2. **Thematic Clusters**
**What it is:** Stories organized by focus area (mortgage, housing, culture, etc.)
**Use for:** Drilling into specific areas of interest

Example:
```json
{
  "mortgage_innovation": {
    "story_count": 52,
    "signals": ["Digital Mortgage Adoption", "Rate Comparison Tools"],
    "key_themes": ["digital transformation", "customer experience"]
  }
}
```

**LLM Prompt:**
```
"Analyze the mortgage_innovation cluster and tell me what technologies are being adopted most"
```

---

### 3. **Momentum Analysis**
**What it is:** Overall sentiment and velocity of topics
**Use for:** Understanding market energy and direction

Example:
```json
{
  "overall_sentiment": "optimistic",
  "hot_topics": [
    {"name": "Digital Mortgage Innovation", "velocity": "high"}
  ]
}
```

**LLM Prompt:**
```
"Is the industry showing optimistic or cautious sentiment? What's driving it?"
```

---

### 4. **Entity Landscape**
**What it is:** Map of key brands, technologies, people, and themes
**Use for:** Competitive intelligence and market mapping

Example:
```json
{
  "dominant_brands": [
    {"name": "Rocket Mortgage", "mentions": 23}
  ],
  "key_technologies": [
    {"name": "digital mortgage", "mentions": 34}
  ]
}
```

**LLM Prompt:**
```
"Who are the dominant players in this period? What technologies are they focusing on?"
```

---

### 5. **Focus Area Insights**
**What it is:** Breakdown by your core focus areas
**Use for:** Targeted analysis of mortgage/housing/culture/storytelling

Example:
```json
{
  "mortgage_lending": {
    "momentum": "rising",
    "key_insight": "Primary focus on digital transformation"
  }
}
```

**LLM Prompt:**
```
"Compare the momentum across all focus areas. Which area has the most activity?"
```

---

### 6. **Emerging Patterns**
**What it is:** New patterns detected (technology waves, cultural movements, etc.)
**Use for:** Early signal detection

Example:
```json
{
  "pattern_type": "technology_wave",
  "description": "Technology adoption theme across multiple signals",
  "significance": "high"
}
```

**LLM Prompt:**
```
"What emerging patterns should I be aware of? Which ones are most significant?"
```

---

### 7. **Strategic Narrative**
**What it is:** The executive summary and strategic questions
**Use for:** C-level briefings and strategic planning

Example:
```json
{
  "headline": "Rising activity across 5 themes, led by Digital Mortgage Innovation",
  "executive_summary": "Analysis of 150 stories across 8 thematic areas...",
  "strategic_questions": [
    "How will digital mortgage adoption reshape competitive dynamics?"
  ]
}
```

**LLM Prompt:**
```
"Give me a 1-minute executive brief based on the strategic narrative"
```

---

### 8. **Macro Observations**
**What it is:** High-level observations about the overall landscape
**Use for:** Context setting and framing

Example:
```json
[
  "High coverage intensity with 150 stories across 8 themes",
  "Predominantly rising momentum suggests active market dynamics"
]
```

---

## Usage Examples

### Example 1: Weekly Executive Brief

**Prompt to LLM:**
```
Using macro_trends.json, create a 3-paragraph executive brief covering:
1. What happened this week (use strategic_narrative.executive_summary)
2. Key themes and momentum (use thematic_clusters and momentum_analysis)
3. Strategic questions to consider (use strategic_narrative.strategic_questions)
```

---

### Example 2: Competitive Intelligence

**Prompt to LLM:**
```
From macro_trends.json, analyze:
1. Which brands are dominating coverage? (entity_landscape.dominant_brands)
2. What technologies are they investing in? (entity_landscape.key_technologies)
3. Are they gaining or losing momentum? (check if brands appear in hot_topics)
```

---

### Example 3: Content Strategy

**Prompt to LLM:**
```
Based on narrative_threads and emerging_patterns:
1. What are the 3 biggest stories I could write about?
2. What angles are NOT being covered (gaps in coverage)?
3. What storytelling approaches are trending? (entity_landscape.storytelling_approaches)
```

---

### Example 4: Trend Forecasting

**Prompt to LLM:**
```
Looking at emerging_patterns and momentum_analysis:
1. What patterns have "high" significance?
2. Which topics are showing "high" velocity?
3. What should we expect to see more of in the next 2 weeks?
```

---

### Example 5: Focus Area Deep Dive

**Prompt to LLM:**
```
Analyze the mortgage_lending section in focus_area_insights:
1. What's the key insight?
2. What are the top signals?
3. How does this compare to other focus areas?
4. What should our mortgage team be paying attention to?
```

---

## Comparison: When to Use Each File

### Use `macro_trends.json` when you want:
✅ The "story" of what's happening
✅ Strategic synthesis and executive summary
✅ Narrative threads and thematic patterns
✅ Macro observations and momentum analysis
✅ **Perfect for:** Leadership briefings, trend reports, strategic planning

### Use `stories_export.json` when you want:
✅ Individual story details
✅ Granular entity extraction
✅ Tabular data for filtering/sorting
✅ **Perfect for:** Research, data analysis, content mining

### Use `analysis_scaffold.json` when you want:
✅ Hierarchical structure (timeframe → trends → implications → risks)
✅ Component-based analysis
✅ Structured strategic questions
✅ **Perfect for:** Presentations, reports, decision frameworks

---

## Sample LLM Workflows

### Workflow 1: Daily Briefing
1. Load `macro_trends.json`
2. Ask LLM: "Summarize the strategic_narrative in 3 bullet points"
3. Ask LLM: "What are the hot_topics I should know about?"
4. Ask LLM: "Any emerging_patterns with high significance?"

### Workflow 2: Content Planning
1. Load `macro_trends.json`
2. Ask LLM: "What are the narrative_threads with 'expanding' outlook?"
3. Ask LLM: "For each thread, suggest 2 content angles"
4. Ask LLM: "Check entity_landscape.storytelling_approaches for trending formats"

### Workflow 3: Competitive Analysis
1. Load `macro_trends.json`
2. Ask LLM: "Compare dominant_brands by mention count"
3. Ask LLM: "What technologies are the top 3 brands focusing on?"
4. Ask LLM: "Are they in hot_topics or cooling_topics?"

### Workflow 4: Strategic Planning
1. Load `macro_trends.json`
2. Ask LLM: "Analyze thematic_clusters by story_count and momentum"
3. Ask LLM: "Which cluster represents the biggest opportunity?"
4. Ask LLM: "Review strategic_questions and prioritize top 3"

---

## Pro Tips

### 🎯 **Best Practices**

1. **Start with Strategic Narrative**
   The `strategic_narrative` section gives you the headline and executive summary - perfect for context setting.

2. **Use Thematic Clusters for Focus**
   Drill into specific `thematic_clusters` (mortgage, housing, culture, etc.) based on your area of interest.

3. **Check Momentum for Urgency**
   `hot_topics` with "high" velocity need immediate attention.

4. **Leverage Entity Landscape for Intelligence**
   Track `dominant_brands` and `key_technologies` over time to spot competitive shifts.

5. **Emerging Patterns = Early Signals**
   Patterns with "high" significance are worth investigating immediately.

### 🚨 **Watch Out For**

- **Low Story Counts:** Threads with <5 stories may be noise, not signal
- **"Declining" Momentum:** Topics in `cooling_topics` may still be important (check story_count)
- **Thematic Clusters:** Some signals can belong to multiple clusters - that's intentional

### 📊 **Tracking Over Time**

Compare `macro_trends.json` week-over-week:
- Are the same brands staying dominant?
- Are new technologies appearing in the landscape?
- Are narrative threads persisting or changing?
- Is overall sentiment shifting?

---

## Integration Points

### Feed to ChatGPT/Claude
```
I'm sharing our weekly macro trends analysis. Please review and provide:
1. Top 3 insights
2. Competitive threats or opportunities
3. Content ideas based on narrative threads

[Paste macro_trends.json]
```

### Build Dashboards
```javascript
// Extract key metrics for visualization
const data = JSON.parse(macro_trends);
const hotTopics = data.momentum_analysis.hot_topics;
const dominantBrands = data.entity_landscape.dominant_brands;
```

### Create Reports
```python
import json

with open('macro_trends.json') as f:
    trends = json.load(f)

print(f"## Executive Summary")
print(trends['strategic_narrative']['executive_summary'])
print(f"\n## Key Insights")
for thread in trends['narrative_threads'][:3]:
    print(f"- {thread['narrative']}")
```

---

## File Location

**Generated:** Daily at 7:50 AM UTC (GitHub Actions)
**Path:** `/home/user/mat-monitor/macro_trends.json`
**Tracked in Git:** Yes (auto-committed)

---

## Questions?

**Q: How often is this updated?**
A: Daily, whenever the RSS collector runs

**Q: What if there are no signals?**
A: File won't be generated (requires signal clustering to work)

**Q: Can I customize what goes into this?**
A: Yes! Edit `macro_trend_synthesizer.py` to adjust the synthesis logic

**Q: What's the difference between this and the enhanced .txt file?**
A: The .txt is human-readable and organized by signals. The JSON is machine-readable with synthesized strategic insights.

---

**Bottom Line:** `macro_trends.json` is your **processed, considered, macro-level view** of what's happening. Feed this to your LLM for strategic analysis, briefings, and trend identification. 🎯
