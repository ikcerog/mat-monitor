#!/usr/bin/env python3
"""
RSS Summary Analyzer - Enhanced Edition with Advanced NLP
Analyzes summary_cache.txt to generate:
- summary_obscure.txt: Obscure/opportunity stories with buzzwords
- summary_popular.txt: Popular topics with buzzwords
- ongoing_summary_cache.txt: Multi-week compilation with enhanced entity tracking
- analysis_scaffold.json: Hierarchical JSON analysis framework
- linkedin_*.txt: 6 LinkedIn-ready content chunks for Power Automate
- Google Trends integration for housing/mortgage topics
"""

import re
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Import enhancement modules
from entity_extractor import EntityExtractor
from content_summarizer import ContentSummarizer
from json_story_exporter import export_stories_json

try:
    from signal_clustering import SignalClusterer
    CLUSTERING_AVAILABLE = True
except ImportError:
    CLUSTERING_AVAILABLE = False
    print("⚠️  scikit-learn not installed. Signal clustering disabled. Run: pip3 install scikit-learn numpy")

try:
    from scaffold_generator import ScaffoldGenerator
    SCAFFOLD_AVAILABLE = True
except ImportError:
    SCAFFOLD_AVAILABLE = False

try:
    from pytrends.request import TrendReq
    TRENDS_AVAILABLE = True
except ImportError:
    TRENDS_AVAILABLE = False
    print("⚠️  pytrends not installed. Google Trends features disabled. Run: pip3 install pytrends")

# Keywords that indicate popular/trending topics
POPULAR_INDICATORS = [
    'ai', 'artificial intelligence', 'generative ai', 'chatgpt', 'openai',
    'streaming', 'ctv', 'netflix', 'tiktok', 'meta', 'google', 'microsoft',
    'amazon', 'apple', 'meta', 'facebook', 'instagram', 'youtube',
    'merger', 'acquisition', 'm&a', 'deal', 'billion',
    'marketing', 'advertising', 'campaign', 'brand'
]

# Housing/Mortgage-specific keywords
HOUSING_KEYWORDS = [
    'housing', 'home', 'homebuyer', 'homeowner', 'real estate', 'property',
    'mortgage', 'loan', 'refinance', 'interest rate', 'rates', 'fed',
    'housing market', 'home price', 'home sale', 'listing', 'inventory',
    'affordability', 'first-time buyer', 'millennials', 'gen z',
    'down payment', 'credit', 'lending', 'fintech',
    'zillow', 'redfin', 'realtor', 'mls', 'appraisal',
    'home equity', 'heloc', 'refi', 'closing', 'escrow',
    'rental', 'rent', 'apartment', 'multifamily', 'housing shortage',
    'new construction', 'builder', 'suburban', 'urban', 'migration',
    'remote work', 'work from home', 'relocation', 'moving'
]

# Buzzword patterns to extract
BUZZWORD_PATTERNS = [
    r'\b(?:AI|ML|LLM|GenAI|ChatGPT|OpenAI)\b',
    r'\b(?:streaming|CTV|OTT|AVOD|SVOD)\b',
    r'\b(?:personalization|targeting|measurement|attribution)\b',
    r'\b(?:programmatic|automation|optimization)\b',
    r'\b(?:merger|acquisition|M&A|deal|partnership)\b',
    r'\b(?:data|analytics|insights|intelligence)\b',
    r'\b(?:ROI|KPI|performance|engagement|conversion)\b',
    r'\b(?:blockchain|crypto|metaverse|VR|AR)\b',
    r'\b(?:sustainability|ESG|climate|green)\b',
    r'\b(?:privacy|GDPR|compliance|security)\b',
    r'\b(?:housing|mortgage|homebuyer|real estate|refinance)\b',
    r'\b(?:interest rate|Fed|lending|fintech|affordability)\b',
]

ONGOING_CACHE_FILE = 'ongoing_summary_cache.txt'
TREND_DATA_FILE = 'trend_data.json'
MAX_WEEKS_TO_KEEP = 4  # Keep 4 weeks of history

def read_summary_cache(filepath='summary_cache.txt'):
    """Read and parse the summary_cache.txt file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"Error: {filepath} not found")
        sys.exit(1)

def extract_stories(content):
    """Extract individual stories from the enhanced content format"""
    stories = []
    current_feed = None
    current_source = None
    current_category = None

    # Initialize extractors
    entity_extractor = EntityExtractor()
    summarizer = ContentSummarizer(max_sentences=3)

    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Check for feed header
        if line.startswith('FEED:'):
            current_feed = line.replace('FEED:', '').strip()
            i += 1
            continue

        # Check for source URL
        if line.startswith('SOURCE:'):
            current_source = line.replace('SOURCE:', '').strip()
            i += 1
            continue

        # Check for category
        if line.startswith('CATEGORY:'):
            current_category = line.replace('CATEGORY:', '').strip()
            i += 1
            continue

        # Check for story title (new format: TITLE: ...)
        if line.startswith('TITLE:'):
            title = line.replace('TITLE:', '').strip()
            url = ''
            description = ''
            full_content = ''
            date = ''
            author = ''

            # Parse all story fields
            i += 1
            while i < len(lines):
                line = lines[i].strip()

                if line.startswith('URL:'):
                    url = line.replace('URL:', '').strip()
                elif line.startswith('DATE:'):
                    date = line.replace('DATE:', '').strip()
                elif line.startswith('AUTHOR:'):
                    author = line.replace('AUTHOR:', '').strip()
                elif line.startswith('DESCRIPTION:'):
                    description = line.replace('DESCRIPTION:', '').strip()
                elif line.startswith('CONTENT:'):
                    full_content = line.replace('CONTENT:', '').strip()
                elif line.startswith('---') or line.startswith('TITLE:') or line.startswith('FEED:'):
                    # End of this story
                    break

                i += 1

            if title:
                # Extract entities
                text_for_extraction = f"{description} {full_content}" if full_content else description
                entities = entity_extractor.extract_entities(text_for_extraction, title)

                # Generate summary
                summary = ''
                if full_content and len(full_content) > len(description) + 100:
                    summary = summarizer.summarize(full_content, title, entities)
                elif description:
                    summary = description[:200]  # Use description as fallback

                stories.append({
                    'feed': current_feed or 'Unknown',
                    'outlet': current_feed or 'Unknown',
                    'feed_category': current_category,
                    'source_url': current_source,
                    'title': title,
                    'url': url,
                    'date': date,
                    'author': author,
                    'description': description,
                    'full_content': full_content,
                    'summary': summary,
                    'entities': entities,
                    'text': f"{title} {description} {full_content}".lower()
                })

            continue

        i += 1

    return stories

def extract_buzzwords(text):
    """Extract buzzwords from text"""
    buzzwords = set()
    for pattern in BUZZWORD_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        buzzwords.update([m.upper() for m in matches])
    return list(buzzwords)

def calculate_popularity_score(story):
    """Calculate how 'popular' a story is based on keywords"""
    text = story['text']
    score = 0

    # Check for popular indicators
    for indicator in POPULAR_INDICATORS:
        if indicator in text:
            score += text.count(indicator)

    # Bonus for company names that appear frequently
    major_companies = ['google', 'microsoft', 'amazon', 'meta', 'apple', 'netflix', 'disney', 'tiktok']
    for company in major_companies:
        if company in text:
            score += 2

    return score

def analyze_stories(stories):
    """Analyze stories to categorize as obscure or popular"""
    # Calculate popularity scores
    for story in stories:
        story['popularity_score'] = calculate_popularity_score(story)
        story['buzzwords'] = extract_buzzwords(story['text'])

    # Sort by popularity
    stories_sorted = sorted(stories, key=lambda x: x['popularity_score'], reverse=True)

    # Split into popular and obscure
    threshold_index = max(len(stories) // 3, 10)  # At least top 10
    popular_stories = [s for s in stories_sorted[:threshold_index] if s['popularity_score'] > 0]

    # Obscure: stories with low popularity score but still interesting (has buzzwords or unique topics)
    obscure_stories = [s for s in stories if s['popularity_score'] <= 2 and len(s['buzzwords']) > 0]

    # If we don't have enough obscure stories, take some from the bottom
    if len(obscure_stories) < 10:
        remaining = [s for s in stories_sorted if s not in popular_stories]
        obscure_stories = remaining[-15:]

    return popular_stories[:20], obscure_stories[:20]  # Limit to 20 each

def generate_summary_file(stories, filepath, title):
    """Generate a concise summary file"""
    output = []
    output.append(f"# {title}")
    output.append(f"Generated: {datetime.now().strftime('%m/%d/%Y at %I:%M:%S %p')}")
    output.append(f"Stories: {len(stories)}\n")

    # Collect all buzzwords
    all_buzzwords = []
    for story in stories:
        all_buzzwords.extend(story['buzzwords'])

    # Count and sort buzzwords
    buzzword_counts = Counter(all_buzzwords)
    top_buzzwords = [word for word, count in buzzword_counts.most_common(15)]

    if top_buzzwords:
        output.append(f"KEY BUZZWORDS: {', '.join(top_buzzwords)}\n")

    output.append("---\n")

    # Add stories in compact format
    for i, story in enumerate(stories, 1):
        # Title
        output.append(f"{i}. {story['title']}")

        # Compact description (first 150 chars)
        if story['description']:
            desc = story['description'][:150]
            if len(story['description']) > 150:
                desc += '...'
            output.append(f"   {desc}")

        # Buzzwords for this story
        if story['buzzwords']:
            output.append(f"   [{', '.join(sorted(set(story['buzzwords'])))}]")

        output.append("")  # Blank line between stories

    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))

    print(f"✓ Generated {filepath} ({len(stories)} stories, {len(output)} lines)")

def load_trend_data():
    """Load historical trend data"""
    if Path(TREND_DATA_FILE).exists():
        with open(TREND_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Convert regular dicts back to defaultdicts
            data['buzzword_history'] = defaultdict(list, data.get('buzzword_history', {}))
            data['topic_history'] = defaultdict(list, data.get('topic_history', {}))
            # Add seen_stories set for deduplication
            data['seen_stories'] = set(data.get('seen_stories', []))
            return data
    return {
        'buzzword_history': defaultdict(list),  # {buzzword: [(date, count), ...]}
        'topic_history': defaultdict(list),     # {topic: [(date, count), ...]}
        'seen_stories': set(),  # Set of story titles we've seen before
        'last_updated': None
    }

def save_trend_data(data):
    """Save trend data"""
    # Convert set to list for JSON serialization
    data_to_save = data.copy()
    if 'seen_stories' in data_to_save:
        data_to_save['seen_stories'] = list(data_to_save['seen_stories'])
    with open(TREND_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, indent=2)

def update_ongoing_cache(stories, date_str, trend_data):
    """Update ongoing_summary_cache.txt with new stories only (de-duplicated)"""
    # Read existing ongoing cache
    existing_content = []
    if Path(ONGOING_CACHE_FILE).exists():
        with open(ONGOING_CACHE_FILE, 'r', encoding='utf-8') as f:
            existing_content = f.read().split('\n')

    # Remove entries older than MAX_WEEKS_TO_KEEP
    cutoff_date = datetime.now() - timedelta(weeks=MAX_WEEKS_TO_KEEP)
    filtered_content = []
    current_date = None
    skip_section = False

    for line in existing_content:
        if line.startswith('=== DATE:'):
            # Extract date from marker
            date_match = re.search(r'(\d{2}/\d{2}/\d{4})', line)
            if date_match:
                entry_date = datetime.strptime(date_match.group(1), '%m/%d/%Y')
                if entry_date >= cutoff_date:
                    skip_section = False
                    filtered_content.append(line)
                else:
                    skip_section = True
            else:
                filtered_content.append(line)
        elif not skip_section:
            filtered_content.append(line)

    # Get set of previously seen stories
    seen_stories = trend_data.get('seen_stories', set())

    # Filter stories: only new ones, exclude Reddit unless trending
    new_stories = []
    for story in stories:
        # Skip if we've seen this story before
        if story['title'] in seen_stories:
            continue

        # Skip Reddit stories unless they have buzzwords (indicating trending)
        if 'Reddit' in story.get('feed', '') and len(story.get('buzzwords', [])) == 0:
            continue

        # This is a new story, add it
        new_stories.append(story)
        seen_stories.add(story['title'])

    # Update trend_data with new seen stories
    trend_data['seen_stories'] = seen_stories

    # Clean up old stories from seen_stories set (keep last 8 weeks worth)
    cutoff_8weeks = datetime.now() - timedelta(weeks=8)
    # We can't easily date the titles, so we'll just limit the size
    if len(seen_stories) > 5000:  # Keep max 5000 titles
        # Keep only the most recent 3000
        trend_data['seen_stories'] = set(list(seen_stories)[-3000:])

    if not new_stories:
        print(f"✓ No new stories to add to {ONGOING_CACHE_FILE}")
        return

    # Prepare new entry
    new_entry = [
        '',
        f'=== DATE: {date_str} ===',
        f'New stories: {len(new_stories)}',
        ''
    ]

    # Add stories with descriptions
    for story in new_stories[:30]:  # Limit to 30 stories per day
        new_entry.append(f"• {story['title']}")

        # Add description if available (truncate to 200 chars)
        if story.get('description'):
            desc = story['description'][:200]
            if len(story['description']) > 200:
                desc += '...'
            new_entry.append(f"  {desc}")

        # Add buzzwords
        if story['buzzwords']:
            new_entry.append(f"  [{', '.join(sorted(set(story['buzzwords']))[:5])}]")
        new_entry.append('')

    # Combine
    output = '\n'.join(filtered_content).strip() + '\n' + '\n'.join(new_entry)

    # Write file
    with open(ONGOING_CACHE_FILE, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"✓ Updated {ONGOING_CACHE_FILE} ({len(new_stories)} new stories, keeping {MAX_WEEKS_TO_KEEP} weeks)")

def analyze_trends(stories, trend_data):
    """Analyze trends: emerging, building, lasting"""
    today = datetime.now().strftime('%Y-%m-%d')

    # Count buzzwords and topics today
    buzzword_counts = Counter()
    topic_counts = Counter()

    for story in stories:
        for buzzword in story['buzzwords']:
            buzzword_counts[buzzword] += 1

        # Extract key topics (first few words of title)
        words = story['title'].lower().split()[:3]
        topic = ' '.join(words)
        topic_counts[topic] += 1

    # Update history
    for buzzword, count in buzzword_counts.items():
        trend_data['buzzword_history'][buzzword].append({'date': today, 'count': count})

    for topic, count in topic_counts.items():
        trend_data['topic_history'][topic].append({'date': today, 'count': count})

    # Clean old entries (keep last 8 weeks)
    cutoff = (datetime.now() - timedelta(weeks=8)).strftime('%Y-%m-%d')

    for buzzword in list(trend_data['buzzword_history'].keys()):
        trend_data['buzzword_history'][buzzword] = [
            entry for entry in trend_data['buzzword_history'][buzzword]
            if entry['date'] >= cutoff
        ]
        if not trend_data['buzzword_history'][buzzword]:
            del trend_data['buzzword_history'][buzzword]

    for topic in list(trend_data['topic_history'].keys()):
        trend_data['topic_history'][topic] = [
            entry for entry in trend_data['topic_history'][topic]
            if entry['date'] >= cutoff
        ]
        if not trend_data['topic_history'][topic]:
            del trend_data['topic_history'][topic]

    trend_data['last_updated'] = today

    # Categorize trends
    emerging_trends = []  # New in last 3 days
    building_trends = []  # Growing over last 2 weeks
    lasting_trends = []   # Consistent over 4+ weeks

    recent_cutoff = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')

    for buzzword, history in trend_data['buzzword_history'].items():
        if not history:
            continue

        # Check if emerging (first appeared in last 3 days)
        first_appearance = min(entry['date'] for entry in history)
        if first_appearance >= recent_cutoff:
            emerging_trends.append({
                'term': buzzword,
                'count': sum(e['count'] for e in history),
                'first_seen': first_appearance
            })

        # Check if building (increasing over time)
        if len(history) >= 3:
            recent = sum(e['count'] for e in history[-3:])
            older = sum(e['count'] for e in history[:-3]) if len(history) > 3 else 0
            if recent > older * 1.5:  # 50% growth
                building_trends.append({
                    'term': buzzword,
                    'recent_count': recent,
                    'growth': f"{((recent - older) / max(older, 1)) * 100:.0f}%"
                })

        # Check if lasting (appears consistently)
        if len(history) >= 8:  # At least 8 data points
            lasting_trends.append({
                'term': buzzword,
                'appearances': len(history),
                'total_count': sum(e['count'] for e in history)
            })

    return {
        'emerging': sorted(emerging_trends, key=lambda x: x['count'], reverse=True)[:10],
        'building': sorted(building_trends, key=lambda x: x['recent_count'], reverse=True)[:10],
        'lasting': sorted(lasting_trends, key=lambda x: x['total_count'], reverse=True)[:10]
    }

def fetch_google_trends(keywords, timeframe='today 3-m', geo='US'):
    """Fetch Google Trends data for specified housing/mortgage keywords"""
    if not TRENDS_AVAILABLE:
        return None

    try:
        # Initialize pytrends
        pytrends = TrendReq(hl='en-US', tz=360)

        trends_data = {
            'trending_searches': [],
            'rising_queries': {},
            'interest_over_time': {},
            'related_topics': {}
        }

        # Batch keywords (Google Trends API limits to 5 keywords per request)
        keyword_batches = [keywords[i:i+5] for i in range(0, len(keywords), 5)]

        for batch in keyword_batches:
            try:
                # Build payload
                pytrends.build_payload(batch, cat=0, timeframe=timeframe, geo=geo)

                # Get interest over time
                interest_df = pytrends.interest_over_time()
                if not interest_df.empty:
                    for keyword in batch:
                        if keyword in interest_df.columns:
                            avg_interest = interest_df[keyword].mean()
                            recent_interest = interest_df[keyword].tail(4).mean()  # Last 4 weeks
                            trends_data['interest_over_time'][keyword] = {
                                'average': round(avg_interest, 1),
                                'recent': round(recent_interest, 1),
                                'trend': 'rising' if recent_interest > avg_interest * 1.2 else 'stable'
                            }

                # Get related queries (rising)
                try:
                    related_queries = pytrends.related_queries()
                    for keyword in batch:
                        if keyword in related_queries and related_queries[keyword]['rising'] is not None:
                            rising = related_queries[keyword]['rising']
                            if not rising.empty:
                                trends_data['rising_queries'][keyword] = rising.head(5)['query'].tolist()
                except Exception as e:
                    print(f"  Note: Could not fetch related queries - {str(e)[:50]}")

            except Exception as e:
                print(f"  Warning: Error fetching trends for batch: {str(e)[:80]}")
                continue

        return trends_data

    except Exception as e:
        print(f"⚠️  Google Trends error: {str(e)[:100]}")
        return None

def analyze_google_trends_for_housing():
    """Analyze Google Trends for housing/mortgage insights"""
    if not TRENDS_AVAILABLE:
        return {
            'available': False,
            'message': 'Google Trends data unavailable. Install pytrends: pip3 install pytrends'
        }

    print("🔍 Fetching Google Trends data for housing/mortgage topics...")

    # Key search terms for mortgage companies
    primary_keywords = [
        'mortgage rates',
        'home buying',
        'refinance mortgage',
        'first time home buyer',
        'housing market'
    ]

    secondary_keywords = [
        'mortgage calculator',
        'home loan',
        'fha loan',
        'va loan',
        'down payment assistance'
    ]

    # Fetch trends for primary keywords
    primary_trends = fetch_google_trends(primary_keywords)

    # Fetch trends for secondary keywords
    secondary_trends = fetch_google_trends(secondary_keywords)

    if not primary_trends and not secondary_trends:
        return {
            'available': False,
            'message': 'Could not fetch Google Trends data. API may be temporarily unavailable.'
        }

    # Combine and analyze
    insights = {
        'available': True,
        'hot_topics': [],
        'rising_searches': [],
        'storytelling_angles': [],
        'content_opportunities': []
    }

    # Identify hot topics (high recent interest)
    all_trends = {}
    if primary_trends and 'interest_over_time' in primary_trends:
        all_trends.update(primary_trends['interest_over_time'])
    if secondary_trends and 'interest_over_time' in secondary_trends:
        all_trends.update(secondary_trends['interest_over_time'])

    if all_trends:
        # Sort by recent interest
        sorted_trends = sorted(all_trends.items(), key=lambda x: x[1]['recent'], reverse=True)
        for keyword, data in sorted_trends[:5]:
            insights['hot_topics'].append({
                'keyword': keyword,
                'interest': data['recent'],
                'trend': data['trend']
            })

    # Collect rising queries
    all_rising = {}
    if primary_trends and 'rising_queries' in primary_trends:
        all_rising.update(primary_trends['rising_queries'])
    if secondary_trends and 'rising_queries' in secondary_trends:
        all_rising.update(secondary_trends['rising_queries'])

    if all_rising:
        for keyword, queries in all_rising.items():
            if queries:
                insights['rising_searches'].extend([
                    {'query': q, 'related_to': keyword} for q in queries[:3]
                ])

    # Generate storytelling angles based on trends
    if insights['hot_topics']:
        for topic in insights['hot_topics'][:3]:
            if 'rates' in topic['keyword']:
                insights['storytelling_angles'].append(
                    f"Rate shopping trends: Address concerns about {topic['keyword']}"
                )
            elif 'first time' in topic['keyword']:
                insights['storytelling_angles'].append(
                    f"First-time buyer focus: Educational content for new homebuyers"
                )
            elif 'refinance' in topic['keyword']:
                insights['storytelling_angles'].append(
                    f"Refi opportunity: Market conditions driving {topic['keyword']} searches"
                )
            elif 'buying' in topic['keyword'] or 'market' in topic['keyword']:
                insights['storytelling_angles'].append(
                    f"Market insights: Buyers researching {topic['keyword']}"
                )

    # Identify content opportunities (gaps between what's trending and what you're covering)
    if insights['rising_searches']:
        insights['content_opportunities'].append(
            "Create content addressing top rising queries (FAQs, guides, calculators)"
        )

    if any('calculator' in t['keyword'] for t in insights['hot_topics']):
        insights['content_opportunities'].append(
            "High interest in calculators - opportunity for interactive tools"
        )

    if any('fha' in t['keyword'] or 'va' in t['keyword'] for t in insights['hot_topics']):
        insights['content_opportunities'].append(
            "Government-backed loan programs seeing high search volume"
        )

    print(f"  ✓ Found {len(insights['hot_topics'])} hot topics")
    print(f"  ✓ Identified {len(insights['rising_searches'])} rising queries")
    print(f"  ✓ Generated {len(insights['storytelling_angles'])} storytelling angles")

    return insights

def generate_linkedin_chunks(stories, trends, popular_stories, obscure_stories, google_trends=None):
    """Generate 6 LinkedIn-ready content chunks"""

    # Chunk 1: Emerging Trends
    chunk1 = [
        "# LinkedIn Post: Emerging Trends",
        f"Generated: {datetime.now().strftime('%m/%d/%Y')}\n",
        "## 🚀 EMERGING TRENDS (New This Week)\n"
    ]

    if trends['emerging']:
        for trend in trends['emerging'][:5]:
            chunk1.append(f"• {trend['term']} - {trend['count']} mentions (first seen: {trend['first_seen']})")
    else:
        chunk1.append("• No new emerging trends identified this week")

    chunk1.append("\n## Story Highlights:")
    for story in popular_stories[:3]:
        chunk1.append(f"\n• {story['title']}")
        if story['buzzwords']:
            chunk1.append(f"  Tags: {', '.join(sorted(set(story['buzzwords']))[:4])}")

    # Chunk 2: Building Momentum
    chunk2 = [
        "# LinkedIn Post: Building Momentum",
        f"Generated: {datetime.now().strftime('%m/%d/%Y')}\n",
        "## 📈 BUILDING MOMENTUM (Gaining Traction)\n"
    ]

    if trends['building']:
        for trend in trends['building'][:5]:
            chunk2.append(f"• {trend['term']} - {trend['recent_count']} recent mentions (↑{trend['growth']})")
    else:
        chunk2.append("• No significant momentum shifts detected")

    chunk2.append("\n## Stories Driving Growth:")
    for story in popular_stories[3:6] if len(popular_stories) > 3 else popular_stories[:3]:
        chunk2.append(f"\n• {story['title']}")

    # Chunk 3: Lasting Trends
    chunk3 = [
        "# LinkedIn Post: Lasting Trends",
        f"Generated: {datetime.now().strftime('%m/%d/%Y')}\n",
        "## 🎯 LASTING TRENDS (Consistent Focus Areas)\n"
    ]

    if trends['lasting']:
        for trend in trends['lasting'][:5]:
            chunk3.append(f"• {trend['term']} - {trend['appearances']} weeks tracked, {trend['total_count']} total mentions")
    else:
        chunk3.append("• Not enough historical data for lasting trend analysis")

    chunk3.append("\n## Industry Staples:")
    for story in popular_stories[6:9] if len(popular_stories) > 6 else popular_stories[:3]:
        chunk3.append(f"\n• {story['title']}")

    # Chunk 4: Major Deals & Announcements
    chunk4 = [
        "# LinkedIn Post: Major Deals & Announcements",
        f"Generated: {datetime.now().strftime('%m/%d/%Y')}\n",
        "## 💼 MAJOR DEALS & ANNOUNCEMENTS\n"
    ]

    deal_stories = [s for s in stories if any(kw in s['text'] for kw in ['deal', 'acquisition', 'm&a', 'merger', 'partnership', 'billion'])]
    for story in deal_stories[:5]:
        chunk4.append(f"\n• {story['title']}")
        if story['buzzwords']:
            chunk4.append(f"  {', '.join([b for b in sorted(set(story['buzzwords'])) if b in ['DEAL', 'ACQUISITION', 'M&A', 'PARTNERSHIP']])}")

    if not deal_stories:
        chunk4.append("• No major deals announced this week")

    # Chunk 5: Niche Opportunities
    chunk5 = [
        "# LinkedIn Post: Niche Opportunities",
        f"Generated: {datetime.now().strftime('%m/%d/%Y')}\n",
        "## 💡 NICHE OPPORTUNITIES (Under-the-Radar Innovations)\n"
    ]

    for story in obscure_stories[:5]:
        chunk5.append(f"\n• {story['title']}")
        if story['buzzwords']:
            chunk5.append(f"  Key areas: {', '.join(sorted(set(story['buzzwords']))[:4])}")

    # Chunk 6: Housing & Mortgage Trends
    chunk6 = [
        "# LinkedIn Post: Housing & Homebuyer Trends",
        f"Generated: {datetime.now().strftime('%m/%d/%Y')}\n",
        "## 🏠 HOUSING & HOMEBUYER TRENDS\n",
        "Real estate insights relevant for mortgage companies\n"
    ]

    # Filter housing-related stories
    housing_stories = [s for s in stories if any(kw in s['text'] for kw in HOUSING_KEYWORDS)]

    if housing_stories:
        # Group by category
        market_stories = [s for s in housing_stories if any(kw in s['text'] for kw in ['market', 'price', 'inventory', 'sale', 'listing'])]
        buyer_stories = [s for s in housing_stories if any(kw in s['text'] for kw in ['buyer', 'millennials', 'gen z', 'first-time', 'affordability'])]
        finance_stories = [s for s in housing_stories if any(kw in s['text'] for kw in ['mortgage', 'rate', 'fed', 'loan', 'fintech', 'lending'])]

        if market_stories:
            chunk6.append("\n### Market Dynamics:")
            for story in market_stories[:3]:
                chunk6.append(f"• {story['title']}")
                if any(kw in story['text'] for kw in ['mortgage', 'loan', 'lending']):
                    chunk6.append("  💡 Direct industry mention/relevance")

        if buyer_stories:
            chunk6.append("\n### What Homebuyers Are Talking About:")
            for story in buyer_stories[:3]:
                chunk6.append(f"• {story['title']}")
                # Identify conversation hooks
                hooks = []
                if 'affordability' in story['text']:
                    hooks.append("Affordability angle")
                if any(kw in story['text'] for kw in ['millennials', 'gen z']):
                    hooks.append("Gen focus")
                if 'first' in story['text'] or 'down payment' in story['text']:
                    hooks.append("First-time buyer")
                if hooks:
                    chunk6.append(f"  🎯 Content angles: {', '.join(hooks)}")

        if finance_stories:
            chunk6.append("\n### Mortgage & Fintech:")
            for story in finance_stories[:3]:
                chunk6.append(f"• {story['title']}")

        # Add Google Trends insights if available
        if google_trends and google_trends.get('available'):
            chunk6.append("\n### 🔥 GOOGLE TRENDS INSIGHTS (What People Are Searching)")
            chunk6.append("Real-time search data - your storytelling opportunities:\n")

            # Hot topics
            if google_trends.get('hot_topics'):
                chunk6.append("**Top Search Topics:**")
                for topic in google_trends['hot_topics'][:5]:
                    trend_emoji = "📈" if topic['trend'] == 'rising' else "➡️"
                    chunk6.append(f"• {trend_emoji} {topic['keyword']} (interest level: {topic['interest']})")

            # Rising searches
            if google_trends.get('rising_searches'):
                chunk6.append("\n**Rising Queries (What's Gaining Momentum):**")
                for item in google_trends['rising_searches'][:6]:
                    chunk6.append(f"• \"{item['query']}\" (related to: {item['related_to']})")

            # Storytelling angles
            if google_trends.get('storytelling_angles'):
                chunk6.append("\n**💡 Storytelling Angles:**")
                for angle in google_trends['storytelling_angles'][:4]:
                    chunk6.append(f"• {angle}")

            # Content opportunities
            if google_trends.get('content_opportunities'):
                chunk6.append("\n**📝 Content Opportunities:**")
                for opp in google_trends['content_opportunities']:
                    chunk6.append(f"• {opp}")

        elif google_trends and not google_trends.get('available'):
            chunk6.append("\n### Google Trends Insights")
            chunk6.append(f"• {google_trends.get('message', 'Google Trends data unavailable')}")

        # Add conversation starters
        chunk6.append("\n### Conversation Starters:")
        chunk6.append("• Use market dynamics to discuss solutions for navigating challenges")
        chunk6.append("• Address buyer concerns with technology-enabled approaches")
        chunk6.append("• Position as innovator in fintech lending space")

    else:
        chunk6.append("\n• No housing-specific stories this period")
        chunk6.append("\n### General Talking Points:")
        chunk6.append("• Digital transformation in mortgage lending")
        chunk6.append("• Tech-enabled homebuying experience")
        chunk6.append("• Innovation in fintech lending space")

    # Write all chunks
    chunks = [
        ('linkedin_01_emerging.txt', chunk1),
        ('linkedin_02_building.txt', chunk2),
        ('linkedin_03_lasting.txt', chunk3),
        ('linkedin_04_deals.txt', chunk4),
        ('linkedin_05_niche.txt', chunk5),
        ('linkedin_06_housing.txt', chunk6)
    ]

    for filename, content in chunks:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        print(f"✓ Generated {filename}")

def generate_enhanced_ongoing_cache(signals, stories, date_str):
    """Generate enhanced ongoing cache with signal clustering and entity tracking"""

    output = []

    # Header with statistics
    output.append("=" * 80)
    output.append(f"ENHANCED ANALYSIS: {date_str}")
    output.append("=" * 80)

    total_stories = sum(signal['story_count'] for signal in signals)
    outlets = set(story['outlet'] for story in stories)

    output.append(f"Total Stories: {len(stories)} | Clustered: {total_stories} | Unique Outlets: {len(outlets)} | Signals: {len(signals)}")

    # Top trends
    top_trends = []
    for signal in signals[:5]:
        momentum_symbol = {"rising": "↑", "stable": "→", "declining": "↓"}.get(signal['momentum'], "→")
        top_trends.append(f"{signal['cluster_name']} ({momentum_symbol}{signal['story_count']})")

    if top_trends:
        output.append(f"Top Signals: {' | '.join(top_trends)}")

    output.append("")

    # Generate signal-based sections
    for signal in signals:
        output.append("=" * 80)
        output.append(f"SIGNAL: {signal['cluster_name']} [{signal['story_count']} stories, {signal['momentum'].title()}]")
        output.append("=" * 80)
        output.append(signal['description'])

        # Key players
        entities = signal.get('entities', {})
        brands = entities.get('brands', [])[:5]
        technologies = entities.get('technologies', [])[:5]

        entity_parts = []
        if brands:
            entity_parts.append(f"Brands[{', '.join(brands)}]")
        if technologies:
            entity_parts.append(f"Tech[{', '.join(technologies)}]")

        if entity_parts:
            output.append(f"Key Players: {' | '.join(entity_parts)}")

        output.append("")

        # Stories within this signal
        for story in signal.get('stories', [])[:15]:  # Limit to 15 stories per signal
            # Title
            output.append(f"• {story.get('title', 'Untitled')}")

            # Metadata line
            meta_parts = []
            outlet = story.get('outlet', 'Unknown')
            date = story.get('date', '')
            if date:
                try:
                    # Format date nicely
                    dt = datetime.fromisoformat(date.replace('Z', '+00:00'))
                    date_formatted = dt.strftime('%b %d, %Y')
                    meta_parts.append(f"SOURCE: {outlet} | DATE: {date_formatted}")
                except:
                    meta_parts.append(f"SOURCE: {outlet}")
            else:
                meta_parts.append(f"SOURCE: {outlet}")

            if meta_parts:
                output.append(f"  {meta_parts[0]}")

            # Summary
            summary = story.get('summary', story.get('description', ''))
            if summary:
                # Wrap summary to ~80 chars per line
                summary_lines = [summary[i:i+76] for i in range(0, len(summary), 76)]
                for line in summary_lines[:3]:  # Max 3 lines
                    output.append(f"  {line}")

            # Entities
            story_entities = story.get('entities', {})
            entity_tags = []

            for category in ['brands', 'technologies', 'companies']:
                items = story_entities.get(category, [])
                if items:
                    label = {'brands': 'Brands', 'technologies': 'Tech', 'companies': 'Companies'}[category]
                    entity_tags.append(f"{label}[{', '.join(items[:3])}]")

            if entity_tags:
                output.append(f"  ENTITIES: {' | '.join(entity_tags)}")

            # URL
            url = story.get('url', '')
            if url:
                output.append(f"  URL: {url}")

            output.append("")

        output.append("")

    # Write to file (append to existing if within timeframe)
    # For now, we'll create a new enhanced file
    with open('ongoing_summary_cache_enhanced.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))

    print(f"   ✓ Generated ongoing_summary_cache_enhanced.txt ({len(output)} lines)")

def main():
    print("━" * 80)
    print("RSS Summary Analyzer - Enhanced Edition")
    print("━" * 80)
    print()

    # Read summary cache
    print("📖 Reading summary_cache.txt...")
    content = read_summary_cache()

    # Extract stories
    print("🔍 Extracting stories...")
    stories = extract_stories(content)
    print(f"   Found {len(stories)} stories")

    if len(stories) == 0:
        print("⚠️  No stories found - skipping analysis")
        return

    # Analyze stories
    print("📊 Analyzing stories...")
    popular_stories, obscure_stories = analyze_stories(stories)
    print(f"   Popular stories: {len(popular_stories)}")
    print(f"   Obscure stories: {len(obscure_stories)}")
    print()

    # Load trend data
    print("📈 Loading trend data...")
    trend_data = load_trend_data()

    # Analyze trends
    print("🔍 Analyzing trends...")
    trends = analyze_trends(stories, trend_data)
    print(f"   Emerging trends: {len(trends['emerging'])}")
    print(f"   Building trends: {len(trends['building'])}")
    print(f"   Lasting trends: {len(trends['lasting'])}")
    print()

    # Update ongoing cache (this modifies trend_data with seen_stories)
    date_str = datetime.now().strftime('%m/%d/%Y')
    print("📝 Updating ongoing cache...")
    update_ongoing_cache(stories, date_str, trend_data)
    print()

    # Save trend data (must come AFTER update_ongoing_cache to include seen_stories)
    save_trend_data(trend_data)

    # Generate summary files
    print("📝 Generating summary files...")
    generate_summary_file(
        popular_stories,
        'summary_popular.txt',
        'POPULAR TOPICS & TRENDS'
    )
    generate_summary_file(
        obscure_stories,
        'summary_obscure.txt',
        'OBSCURE OPPORTUNITIES & EMERGING STORIES'
    )
    print()

    # Fetch Google Trends data for housing
    print("🌐 Analyzing Google Trends for housing/mortgage...")
    google_trends = analyze_google_trends_for_housing()
    print()

    # Generate LinkedIn chunks
    print("📱 Generating LinkedIn content chunks...")
    generate_linkedin_chunks(stories, trends, popular_stories, obscure_stories, google_trends)
    print()

    # Generate signal clusters (if available)
    signals = []
    if CLUSTERING_AVAILABLE:
        print("🔍 Clustering stories into signals...")
        try:
            clusterer = SignalClusterer(min_cluster_size=3)
            signals = clusterer.cluster_stories(stories, trend_data)
            print(f"   Identified {len(signals)} signals")
            print()
        except Exception as e:
            print(f"   ⚠️  Clustering failed: {e}")
            print()

    # Generate JSON scaffold (if available)
    if SCAFFOLD_AVAILABLE and signals:
        print("📊 Generating analysis scaffold JSON...")
        try:
            generator = ScaffoldGenerator()
            scaffold = generator.generate_scaffold(signals, stories, trend_data)

            # Write scaffold to JSON file
            with open('analysis_scaffold.json', 'w', encoding='utf-8') as f:
                json.dump(scaffold, f, indent=2, ensure_ascii=False)

            print(f"   ✓ Generated analysis_scaffold.json")
            print(f"   • {len(signals)} signals identified")
            print(f"   • {scaffold['meta']['timeframe']['total_stories']} total stories")
            print(f"   • {scaffold['meta']['timeframe']['unique_outlets']} unique outlets")
            print(f"   • {len(scaffold['trends']['emerging'])} emerging trends")
            print(f"   • {len(scaffold['trends']['building'])} building trends")
            print(f"   • {len(scaffold['trends']['lasting'])} lasting trends")
            print(f"   • {len(scaffold['north_star_questions'])} strategic questions")
            print()
        except Exception as e:
            print(f"   ⚠️  Scaffold generation failed: {e}")
            print()

    # Generate enhanced ongoing cache (if we have signals)
    if signals:
        print("📝 Generating enhanced ongoing cache with signals...")
        try:
            generate_enhanced_ongoing_cache(signals, stories, date_str)
        except Exception as e:
            print(f"   ⚠️  Enhanced cache generation failed: {e}")
            print()

    # Generate JSON export for LLM consumption
    print("📊 Generating JSON story export for LLM consumption...")
    try:
        export_stories_json(stories, signals, output_file='stories_export.json')
        print(f"   ✓ Generated stories_export.json")
        print(f"   • {len(stories)} stories exported")
        print(f"   • Tabular format optimized for LLM analysis")
        print()
    except Exception as e:
        print(f"   ⚠️  JSON export failed: {e}")
        print()

    print("━" * 80)
    print("✓ Analysis Complete!")
    print("━" * 80)

if __name__ == '__main__':
    main()
