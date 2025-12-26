#!/usr/bin/env python3
"""
RSS Summary Analyzer
Analyzes summary_cache.txt to generate:
- summary_obscure.txt: Obscure/opportunity stories with buzzwords
- summary_popular.txt: Popular topics with buzzwords
"""

import re
from collections import Counter
from datetime import datetime
import sys

# Keywords that indicate popular/trending topics
POPULAR_INDICATORS = [
    'ai', 'artificial intelligence', 'generative ai', 'chatgpt', 'openai',
    'streaming', 'ctv', 'netflix', 'tiktok', 'meta', 'google', 'microsoft',
    'amazon', 'apple', 'meta', 'facebook', 'instagram', 'youtube',
    'merger', 'acquisition', 'm&a', 'deal', 'billion',
    'marketing', 'advertising', 'campaign', 'brand'
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
]

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
    # Popular: top 30% by score or score > 3
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

def main():
    print("━" * 80)
    print("RSS Summary Analyzer")
    print("━" * 80)
    print()

    # Read summary cache
    print("📖 Reading summary_cache.txt...")
    content = read_summary_cache()

    # Extract stories
    print("🔍 Extracting stories...")
    stories = extract_stories(content)
    print(f"   Found {len(stories)} stories")

    # Analyze stories
    print("📊 Analyzing stories...")
    popular_stories, obscure_stories = analyze_stories(stories)
    print(f"   Popular stories: {len(popular_stories)}")
    print(f"   Obscure stories: {len(obscure_stories)}")
    print()

    # Generate output files
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
    print("━" * 80)
    print("✓ Analysis Complete!")
    print("━" * 80)

if __name__ == '__main__':
    main()
