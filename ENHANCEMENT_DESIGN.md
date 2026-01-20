# Summary Cache Enhancement Design

## Overview
Transform the summary cache from a simple text-based list into a rich, hierarchical analytical framework that enables macro-level trend analysis, entity tracking, and signal clustering.

## Current Limitations
1. **No source attribution** - Feed names not visible in ongoing_summary_cache.txt
2. **Limited content** - Only 200-char descriptions, no full article content
3. **Basic entity extraction** - Only regex-based buzzword matching
4. **Flat structure** - No hierarchical organization or clustering
5. **No analytical framework** - Missing implications, risks, strategic questions

## Enhancement Strategy

### 1. Enhanced Data Capture

#### RSS Collector Improvements
- **Full content extraction**: Fetch complete article text when available
- **Richer metadata**:
  - Publication date
  - Author information
  - Source outlet name (prominently displayed)
  - Article category/tags
- **Better HTML cleaning**: Preserve paragraph structure while removing ads/scripts

#### New Data Schema
```javascript
{
  title: string,
  url: string,
  outlet: string,              // NEW: Source name
  outlet_url: string,           // NEW: Feed URL
  published_date: datetime,     // NEW
  author: string,               // NEW
  description: string,          // 300 chars
  full_content: string,         // NEW: Full article text
  summary: string,              // NEW: AI-generated summary (2-3 sentences)
  feed_category: string         // e.g., "Advertising", "AdTech"
}
```

### 2. Advanced Entity Extraction

#### Technology Stack
- **spaCy** for NLP (en_core_web_sm model)
- **Custom patterns** for industry-specific terms

#### Entity Categories
1. **Organizations** (ORG)
   - Brands: Nike, Coca-Cola, Netflix
   - Companies: Google, Meta, Microsoft
   - Agencies: AKQA, Ogilvy, Wieden+Kennedy

2. **Technologies** (PRODUCT/TECH)
   - AI models: ChatGPT, Claude, GPT-4
   - Platforms: TikTok, Instagram, YouTube
   - Tech terms: GenAI, CTV, OTT, AVOD, programmatic

3. **People** (PERSON)
   - Executives, marketers, influencers

4. **Locations** (GPE)
   - Markets, regions, countries

5. **Custom Industry Terms**
   - Marketing buzzwords: personalization, attribution, retargeting
   - Finance terms: mortgage, refinance, APR, interest rate
   - Metrics: ROI, KPI, ROAS, CTR

#### Entity Storage Format
```json
{
  "entities": {
    "brands": ["Nike", "Adidas"],
    "technologies": ["GenAI", "ChatGPT", "CTV"],
    "companies": ["Google", "Meta"],
    "people": ["Tim Cook"],
    "locations": ["US", "Europe"],
    "products": ["iPhone 15", "Vision Pro"]
  }
}
```

### 3. Content Summarization

#### Approach
- **Extractive summarization** using sentence scoring:
  - TF-IDF for keyword importance
  - Position-based scoring (first/last paragraphs)
  - Entity density scoring
  - Maximum 2-3 sentences per article

#### Example
**Original** (800 words): "Nielsen and Roku announced today an expanded partnership..."

**Summary**: "Nielsen and Roku expanded their data-sharing partnership to enhance streaming TV measurement. Nielsen will receive Big Data + Panel support while Roku gains access to streaming ratings. The deal strengthens both companies' positions in the growing CTV advertising market."

### 4. Hierarchical JSON Scaffold

#### Structure: Timeframe → Environment → Signals → Trends → Implications → Risks → Questions

```json
{
  "meta": {
    "generated_at": "2026-01-20T14:30:00Z",
    "timeframe": {
      "period": "Week of January 13-20, 2026",
      "coverage_days": 7,
      "date_range": ["2026-01-13", "2026-01-20"],
      "total_stories": 850,
      "unique_outlets": 19,
      "outlets_breakdown": {
        "Advertising": 12,
        "AdTech": 4,
        "Finance": 2,
        "Community": 5
      }
    }
  },

  "environment": {
    "macro_context": {
      "economic_indicators": [
        "Interest rates trending down",
        "Consumer spending stable"
      ],
      "industry_landscape": [
        "CTV advertising growth accelerating",
        "AI adoption in marketing accelerating"
      ],
      "regulatory_climate": [
        "Privacy regulations tightening globally",
        "TikTok US operations uncertainty"
      ]
    },
    "market_dynamics": {
      "growth_areas": ["Streaming advertising", "AI-powered personalization"],
      "declining_areas": ["Linear TV spend", "Cookie-based targeting"],
      "consolidation_activity": ["M&A deals at record pace"]
    }
  },

  "signals": [
    {
      "cluster_id": "signal_001",
      "cluster_name": "AI-Driven Content Creation Surge",
      "description": "Brands increasingly using generative AI for marketing content, from video to copy",
      "frequency": 45,
      "momentum": "rising",
      "confidence": "high",
      "story_count": 45,
      "first_seen": "2025-12-15",
      "peak_date": "2026-01-18",
      "outlets": ["Adweek", "Marketing Dive", "Campaign Live"],
      "stories": [
        {
          "title": "Lexus takes generative AI for a spin...",
          "outlet": "Marketing Dive",
          "date": "2026-01-08",
          "url": "https://...",
          "summary": "Lexus partnered with AKQA...",
          "relevance_score": 0.95
        }
      ],
      "entities": {
        "brands": ["Lexus", "Campbell's", "Rocket"],
        "technologies": ["GenAI", "ChatGPT", "DALL-E"],
        "companies": ["AKQA", "OpenAI"],
        "people": []
      },
      "related_buzzwords": ["AI", "GENERATIVE AI", "AUTOMATION", "CREATIVITY"]
    }
  ],

  "trends": {
    "emerging": [
      {
        "name": "AI Video Generation",
        "first_appearance": "2026-01-15",
        "growth_rate": 250,
        "mention_count": 12,
        "key_players": ["OpenAI", "Runway", "Pika"]
      }
    ],
    "building": [
      {
        "name": "CTV Measurement Standardization",
        "duration_weeks": 8,
        "growth_rate": 65,
        "mention_count": 87,
        "key_players": ["Nielsen", "Roku", "Comscore"]
      }
    ],
    "lasting": [
      {
        "name": "Privacy-First Advertising",
        "duration_weeks": 52,
        "stability_score": 0.85,
        "mention_count": 450,
        "key_players": ["Google", "Apple", "Meta"]
      }
    ]
  },

  "implications": {
    "opportunities": [
      {
        "category": "Technology Adoption",
        "insight": "Agencies embracing AI early are winning pitches",
        "evidence": ["AKQA-Lexus partnership", "Saatchi AI initiatives"],
        "actionability": "high",
        "affected_sectors": ["Creative Agencies", "Brand Marketing"]
      }
    ],
    "threats": [
      {
        "category": "Market Disruption",
        "insight": "Traditional creative roles being automated",
        "evidence": ["AI-generated campaigns increasing", "Copywriter layoffs"],
        "urgency": "medium",
        "affected_sectors": ["Creative Services", "Production"]
      }
    ],
    "strategic_shifts": [
      {
        "shift": "From campaign creation to AI orchestration",
        "drivers": ["Cost efficiency", "Speed to market", "Personalization scale"],
        "timeline": "12-18 months",
        "adoption_stage": "early majority"
      }
    ]
  },

  "risks": {
    "technological": [
      {
        "risk": "AI hallucinations in customer-facing content",
        "probability": "medium",
        "impact": "high",
        "mitigation": "Human review workflows"
      }
    ],
    "regulatory": [
      {
        "risk": "FTC crackdown on AI-generated endorsements",
        "probability": "high",
        "impact": "medium",
        "affected_sectors": ["Influencer Marketing", "Social Commerce"]
      }
    ],
    "competitive": [
      {
        "risk": "Platform consolidation reducing choice",
        "probability": "medium",
        "impact": "high",
        "evidence": ["Omnicom-IPG merger", "Publicis acquisitions"]
      }
    ],
    "market": [
      {
        "risk": "Economic downturn reducing ad spend",
        "probability": "low",
        "impact": "high",
        "indicators": ["Consumer confidence", "CMO budgets"]
      }
    ]
  },

  "north_star_questions": [
    {
      "question": "Will AI democratize creativity or concentrate it among platform owners?",
      "category": "Industry Structure",
      "signals": ["signal_001", "signal_005"],
      "urgency": "high"
    },
    {
      "question": "How will CTV measurement standardization affect publisher bargaining power?",
      "category": "Market Dynamics",
      "signals": ["signal_002"],
      "urgency": "medium"
    },
    {
      "question": "What happens to brand authenticity in an AI-generated content world?",
      "category": "Cultural Impact",
      "signals": ["signal_001", "signal_003"],
      "urgency": "medium"
    }
  ],

  "raw_data_summary": {
    "total_articles": 850,
    "articles_with_full_content": 623,
    "unique_entities_extracted": 1247,
    "clusters_identified": 23,
    "outliers": 47
  }
}
```

### 5. Signal Clustering Algorithm

#### Approach: TF-IDF + K-Means + Entity Overlap

1. **Story Vectorization**
   - TF-IDF on titles + summaries + entities
   - Weight entities higher (2x multiplier)
   - Normalize vectors

2. **Clustering**
   - K-means with dynamic K (based on story volume)
   - Minimum cluster size: 3 stories
   - Maximum cluster size: 50 stories

3. **Cluster Naming**
   - Extract top TF-IDF terms
   - Combine with most frequent entities
   - Generate human-readable label

4. **Momentum Calculation**
   ```python
   momentum = (recent_7_days - previous_7_days) / previous_7_days

   if momentum > 0.5: "rising"
   elif momentum < -0.3: "declining"
   else: "stable"
   ```

### 6. Enhanced Output Formats

#### A. JSON Analysis File (`analysis_scaffold.json`)
- Full hierarchical structure as defined above
- Machine-readable for downstream tools
- Updated daily

#### B. Enhanced Text Cache (`ongoing_summary_cache.txt`)
- **Header section** with weekly statistics
- **Source attribution** for every story
- **Entity highlights** for each story
- **Cluster organization** (stories grouped by signal)

Example format:
```
================================================================================
WEEKLY ANALYSIS: January 13-20, 2026
================================================================================
Total Stories: 850 | Unique Outlets: 19 | Clusters Identified: 23
Top Trends: AI Content Creation (↑45), CTV Measurement (↑87), Privacy Tech (→450)

================================================================================
SIGNAL: AI-Driven Content Creation Surge [45 stories, Rising]
================================================================================
Brands increasingly using generative AI for marketing content creation.
Key Players: OpenAI, AKQA, Lexus, Campbell's
Technologies: GenAI, ChatGPT, DALL-E

• Lexus takes generative AI for a spin in new holiday marketing content
  SOURCE: Marketing Dive | DATE: Jan 8, 2026
  SUMMARY: Lexus partnered with AKQA to create "Built for Every Kind of Wonder"
  featuring surreal AI-generated scenes like floating ski slopes, testing the
  creative limits of generative AI technology in automotive marketing.
  ENTITIES: Brands[Lexus, AKQA] | Tech[GenAI, AI]
  URL: https://...

• Inside Rocket's new NFL campaign as in-house creative team embraces AI
  SOURCE: Adweek | DATE: Jan 8, 2026
  SUMMARY: Fintech brand Rocket continues "Room to Dream" platform with AI-
  powered creative production, focusing on homeownership as the American dream
  theme that debuted during Super Bowl.
  ENTITIES: Brands[Rocket] | Tech[AI] | Sectors[Fintech]
  URL: https://...

[...43 more stories...]

================================================================================
SIGNAL: CTV Measurement Standardization [32 stories, Building]
================================================================================
...
```

#### C. Executive Summary (`executive_summary.txt`)
- 1-page overview
- Top 5 signals
- Key implications
- Critical questions

### 7. Implementation Plan

#### Phase 1: Enhanced Data Capture
- ✅ Update RSS collector to fetch full content
- ✅ Add metadata extraction (date, author, outlet)
- ✅ Improve HTML cleaning

#### Phase 2: Entity Extraction
- ✅ Install spaCy with en_core_web_sm model
- ✅ Create entity extraction module
- ✅ Build custom pattern matchers for industry terms
- ✅ Test on sample articles

#### Phase 3: Content Summarization
- ✅ Implement extractive summarization
- ✅ Sentence scoring algorithm
- ✅ Test quality of summaries

#### Phase 4: Signal Clustering
- ✅ TF-IDF vectorization
- ✅ K-means clustering
- ✅ Cluster naming logic
- ✅ Momentum calculation

#### Phase 5: JSON Scaffold Generation
- ✅ Build hierarchical structure
- ✅ Populate all sections (environment, trends, implications, risks, questions)
- ✅ Generate analysis_scaffold.json

#### Phase 6: Enhanced Output Generation
- ✅ Update ongoing_summary_cache.txt format
- ✅ Create executive_summary.txt
- ✅ Update existing outputs (popular, obscure, LinkedIn chunks)

#### Phase 7: Testing & Refinement
- ✅ End-to-end testing
- ✅ Validate entity extraction accuracy
- ✅ Review cluster quality
- ✅ Ensure backward compatibility

## Dependencies

### Python Packages (requirements.txt)
```
pytrends>=4.9.0
spacy>=3.7.0
scikit-learn>=1.3.0
numpy>=1.24.0
```

### spaCy Model
```bash
python3 -m spacy download en_core_web_sm
```

### Node.js Packages (package.json)
No new dependencies required (existing html-to-text and rss-parser sufficient)

## File Structure

```
mat-monitor/
├── rss-collector.js           # Enhanced with full content extraction
├── analyze_summaries.py       # Enhanced with NLP and clustering
├── entity_extractor.py        # NEW: Advanced entity extraction module
├── content_summarizer.py      # NEW: Extractive summarization
├── signal_clustering.py       # NEW: Story clustering logic
├── scaffold_generator.py      # NEW: JSON hierarchy builder
├── requirements.txt           # NEW: Python dependencies
├── summary_cache.txt          # Existing
├── ongoing_summary_cache.txt  # Enhanced format
├── analysis_scaffold.json     # NEW: Machine-readable analysis
├── executive_summary.txt      # NEW: 1-page overview
├── trend_data.json            # Enhanced with entity tracking
└── [existing files...]
```

## Success Metrics

1. **Entity Extraction Accuracy**: >85% precision on manual review
2. **Cluster Coherence**: >0.7 silhouette score
3. **Summary Quality**: Captures key facts in <3 sentences
4. **Source Attribution**: 100% of stories show outlet clearly
5. **JSON Validity**: Passes schema validation
6. **Backward Compatibility**: Existing workflows unaffected

## Timeline

- Design: Complete ✓
- Implementation: 4-6 hours
- Testing: 1-2 hours
- Documentation: 1 hour
- **Total**: 1 business day

---

**Next Steps**: Proceed with implementation in phases, starting with enhanced data capture.
