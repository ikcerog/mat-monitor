#!/usr/bin/env python3
"""
RSS Summary Analyzer - Enhanced Edition
Analyzes summary_cache.txt to generate:
- summary_obscure.txt: Obscure/opportunity stories with buzzwords
- summary_popular.txt: Popular topics with buzzwords
- ongoing_summary_cache.txt: Multi-week compilation with trend tracking
- linkedin_*.txt: 5 LinkedIn-ready content chunks for Power Automate
"""

import re
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Keywords that indicate popular/trending topics
POPULAR_INDICATORS = [
    'ai', 'artificial intelligence', 'generative ai', 'chatgpt', 'openai',
    'streaming', 'ctv', 'netflix', 'tiktok', 'meta', 'google', 'microsoft',
    'amazon', 'apple', 'meta', 'facebook', 'instagram', 'youtube',
    'merger', 'acquisition', 'm&a', 'deal', 'billion',
    'marketing', 'advertising', 'campaign', 'brand'
]

# Housing/Mortgage-specific keywords for Rocket relevance
HOUSING_KEYWORDS = [
    'housing', 'home', 'homebuyer', 'homeowner', 'real estate', 'property',
    'mortgage', 'loan', 'refinance', 'interest rate', 'rates', 'fed',
    'housing market', 'home price', 'home sale', 'listing', 'inventory',
    'affordability', 'first-time buyer', 'millennials', 'gen z',
    'down payment', 'credit', 'lending', 'fintech', 'rocket',
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
    """Extract individual stories from the content"""
    stories = []
    current_feed = None

    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Check for feed header
        if line.startswith('FEED:'):
            current_feed = line.replace('FEED:', '').strip()
            i += 1
            continue

        # Check for story title (non-empty, not SOURCE, not URL)
        if line and not line.startswith('SOURCE:') and not line.startswith('http') and current_feed:
            title = line
            url = ''
            description = ''

            # Next line might be URL
            if i + 1 < len(lines) and lines[i + 1].strip().startswith('http'):
                url = lines[i + 1].strip()
                i += 1

            # Next line(s) might be description
            if i + 1 < len(lines):
                i += 1
                desc_lines = []
                while i < len(lines) and lines[i].strip() and not lines[i].startswith('FEED:') and not lines[i].startswith('http'):
                    desc_lines.append(lines[i].strip())
                    i += 1
                description = ' '.join(desc_lines)

            if title:
                stories.append({
                    'feed': current_feed,
                    'title': title,
                    'url': url,
                    'description': description,
                    'text': f"{title} {description}".lower()
                })

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
            return data
    return {
        'buzzword_history': defaultdict(list),  # {buzzword: [(date, count), ...]}
        'topic_history': defaultdict(list),     # {topic: [(date, count), ...]}
        'last_updated': None
    }

def save_trend_data(data):
    """Save trend data"""
    with open(TREND_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def update_ongoing_cache(stories, date_str):
    """Update ongoing_summary_cache.txt with new stories"""
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

    # Prepare new entry
    new_entry = [
        '',
        f'=== DATE: {date_str} ===',
        f'Stories added: {len(stories)}',
        ''
    ]

    # Add stories
    for story in stories[:30]:  # Limit to 30 stories per day
        new_entry.append(f"• {story['title']}")
        if story['buzzwords']:
            new_entry.append(f"  [{', '.join(sorted(set(story['buzzwords']))[:5])}]")
        new_entry.append('')

    # Combine
    output = '\n'.join(filtered_content).strip() + '\n' + '\n'.join(new_entry)

    # Write file
    with open(ONGOING_CACHE_FILE, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"✓ Updated {ONGOING_CACHE_FILE} (keeping {MAX_WEEKS_TO_KEEP} weeks of history)")

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

def generate_linkedin_chunks(stories, trends, popular_stories, obscure_stories):
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

    # Chunk 6: Housing & Mortgage Trends (Rocket-relevant)
    chunk6 = [
        "# LinkedIn Post: Housing & Homebuyer Trends",
        f"Generated: {datetime.now().strftime('%m/%d/%Y')}\n",
        "## 🏠 HOUSING & HOMEBUYER TRENDS\n",
        "Real estate insights relevant for mortgage companies like Rocket\n"
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
                if any(kw in story['text'] for kw in ['rocket', 'mortgage', 'loan']):
                    chunk6.append("  💡 Direct Rocket mention/relevance")

        if buyer_stories:
            chunk6.append("\n### What Homebuyers Are Talking About:")
            for story in buyer_stories[:3]:
                chunk6.append(f"• {story['title']}")
                # Identify conversation hooks for Rocket
                hooks = []
                if 'affordability' in story['text']:
                    hooks.append("Affordability angle")
                if any(kw in story['text'] for kw in ['millennials', 'gen z']):
                    hooks.append("Gen focus")
                if 'first' in story['text'] or 'down payment' in story['text']:
                    hooks.append("First-time buyer")
                if hooks:
                    chunk6.append(f"  🎯 Rocket angles: {', '.join(hooks)}")

        if finance_stories:
            chunk6.append("\n### Mortgage & Fintech:")
            for story in finance_stories[:3]:
                chunk6.append(f"• {story['title']}")
                if 'rocket' in story['text'].lower():
                    chunk6.append("  ⭐ ROCKET MENTIONED")

        # Add conversation starters
        chunk6.append("\n### Conversation Starters for Rocket:")
        chunk6.append("• Use market dynamics to discuss how Rocket helps navigate challenges")
        chunk6.append("• Address buyer concerns with Rocket's tech-first approach")
        chunk6.append("• Position Rocket as innovator in fintech lending space")

    else:
        chunk6.append("\n• No housing-specific stories this period")
        chunk6.append("\n### General Talking Points:")
        chunk6.append("• Digital transformation in mortgage lending")
        chunk6.append("• Tech-enabled homebuying experience")
        chunk6.append("• Rocket's innovation in fintech space")

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

    # Save trend data
    save_trend_data(trend_data)

    # Update ongoing cache
    date_str = datetime.now().strftime('%m/%d/%Y')
    print("📝 Updating ongoing cache...")
    update_ongoing_cache(stories, date_str)
    print()

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

    # Generate LinkedIn chunks
    print("📱 Generating LinkedIn content chunks...")
    generate_linkedin_chunks(stories, trends, popular_stories, obscure_stories)
    print()

    print("━" * 80)
    print("✓ Analysis Complete!")
    print("━" * 80)

if __name__ == '__main__':
    main()
