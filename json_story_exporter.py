#!/usr/bin/env python3
"""
JSON Story Exporter
Exports stories and signals in granular JSON format for LLM consumption
"""

import json
from datetime import datetime
from typing import List, Dict


def export_stories_json(stories: List[Dict], signals: List[Dict] = None,
                       output_file: str = 'stories_export.json') -> None:
    """
    Export stories in granular JSON format optimized for LLM consumption

    Args:
        stories: List of story dictionaries
        signals: Optional list of signal clusters
        output_file: Output filename
    """

    # Build tabular structure
    export_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_stories": len(stories),
            "total_signals": len(signals) if signals else 0,
            "date_range": _calculate_date_range(stories),
            "format_version": "1.0"
        },

        "stories": _format_stories_for_export(stories),

        "signals": _format_signals_for_export(signals, stories) if signals else [],

        "summary_statistics": _calculate_statistics(stories, signals)
    }

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(f"✓ Exported {len(stories)} stories to {output_file}")


def _format_stories_for_export(stories: List[Dict]) -> List[Dict]:
    """Format individual stories for tabular export"""
    formatted_stories = []

    for idx, story in enumerate(stories, 1):
        entities = story.get('entities', {})

        formatted_story = {
            "id": idx,
            "title": story.get('title', ''),
            "url": story.get('url', ''),
            "source": {
                "outlet": story.get('outlet', 'Unknown'),
                "category": story.get('feed_category', ''),
                "source_url": story.get('source_url', '')
            },
            "publication": {
                "date": story.get('date', ''),
                "author": story.get('author', '')
            },
            "content": {
                "description": story.get('description', ''),
                "summary": story.get('summary', ''),
                "full_content_available": bool(story.get('full_content'))
            },
            "entities": {
                "brands": entities.get('brands', []),
                "technologies": entities.get('technologies', []),
                "products": entities.get('products', []),
                "people": entities.get('people', []),
                "metrics": entities.get('metrics', []),
                "cultural_themes": entities.get('cultural_themes', []),
                "storytelling_themes": entities.get('storytelling_themes', []),
                "housing_terms": entities.get('housing_terms', [])
            },
            "analysis": {
                "entity_count": sum(len(v) for v in entities.values() if isinstance(v, list)),
                "has_mortgage_focus": _has_mortgage_focus(story),
                "has_housing_focus": _has_housing_focus(story),
                "has_culture_focus": _has_culture_focus(story),
                "has_storytelling_focus": _has_storytelling_focus(story)
            }
        }

        formatted_stories.append(formatted_story)

    return formatted_stories


def _format_signals_for_export(signals: List[Dict], stories: List[Dict]) -> List[Dict]:
    """Format signal clusters for tabular export"""
    if not signals:
        return []

    formatted_signals = []

    for signal in signals:
        entities = signal.get('entities', {})

        formatted_signal = {
            "signal_id": signal.get('cluster_id', ''),
            "name": signal.get('cluster_name', ''),
            "description": signal.get('description', ''),
            "metrics": {
                "story_count": signal.get('story_count', 0),
                "momentum": signal.get('momentum', 'stable'),
                "confidence": signal.get('confidence', 'low')
            },
            "timeline": {
                "first_seen": signal.get('first_seen', ''),
                "peak_date": signal.get('peak_date', '')
            },
            "sources": {
                "outlets": signal.get('outlets', []),
                "outlet_count": len(signal.get('outlets', []))
            },
            "entities": {
                "brands": entities.get('brands', [])[:5],
                "technologies": entities.get('technologies', [])[:5],
                "cultural_themes": entities.get('cultural_themes', [])[:5],
                "storytelling_themes": entities.get('storytelling_themes', [])[:5],
                "housing_terms": entities.get('housing_terms', [])[:5]
            },
            "related_buzzwords": signal.get('related_buzzwords', [])[:10],
            "story_ids": [stories.index(s) + 1 for s in signal.get('stories', [])[:20]],
            "analysis": {
                "is_mortgage_focused": _signal_has_mortgage_focus(signal),
                "is_housing_focused": _signal_has_housing_focus(signal),
                "is_culture_focused": _signal_has_culture_focus(signal),
                "is_storytelling_focused": _signal_has_storytelling_focus(signal)
            }
        }

        formatted_signals.append(formatted_signal)

    return formatted_signals


def _calculate_statistics(stories: List[Dict], signals: List[Dict]) -> Dict:
    """Calculate summary statistics"""

    # Count stories by category
    category_counts = {}
    for story in stories:
        category = story.get('feed_category', 'Unknown')
        category_counts[category] = category_counts.get(category, 0) + 1

    # Count stories by focus area
    focus_counts = {
        'mortgage': sum(1 for s in stories if _has_mortgage_focus(s)),
        'housing': sum(1 for s in stories if _has_housing_focus(s)),
        'culture': sum(1 for s in stories if _has_culture_focus(s)),
        'storytelling': sum(1 for s in stories if _has_storytelling_focus(s))
    }

    # Count entities
    entity_counts = {
        'brands': set(),
        'technologies': set(),
        'people': set()
    }

    for story in stories:
        entities = story.get('entities', {})
        entity_counts['brands'].update(entities.get('brands', []))
        entity_counts['technologies'].update(entities.get('technologies', []))
        entity_counts['people'].update(entities.get('people', []))

    return {
        "by_category": category_counts,
        "by_focus_area": focus_counts,
        "unique_entities": {
            "brands": len(entity_counts['brands']),
            "technologies": len(entity_counts['technologies']),
            "people": len(entity_counts['people'])
        },
        "signals_summary": {
            "total": len(signals) if signals else 0,
            "rising": len([s for s in (signals or []) if s.get('momentum') == 'rising']),
            "stable": len([s for s in (signals or []) if s.get('momentum') == 'stable']),
            "declining": len([s for s in (signals or []) if s.get('momentum') == 'declining'])
        }
    }


def _calculate_date_range(stories: List[Dict]) -> Dict:
    """Calculate date range from stories"""
    dates = []
    for story in stories:
        date_str = story.get('date', '')
        if date_str:
            try:
                date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                dates.append(date)
            except:
                pass

    if dates:
        return {
            "earliest": min(dates).isoformat(),
            "latest": max(dates).isoformat(),
            "span_days": (max(dates) - min(dates)).days
        }

    return {}


def _has_mortgage_focus(story: Dict) -> bool:
    """Check if story has mortgage focus"""
    entities = story.get('entities', {})
    text = story.get('text', '').lower()

    mortgage_brands = ['rocket mortgage', 'better.com', 'loandepot', 'uwm', 'guaranteed rate']
    mortgage_terms = ['mortgage', 'loan', 'lending', 'refinance', 'apr', 'interest rate']

    has_brand = any(brand.lower() in entities.get('brands', []) for brand in mortgage_brands)
    has_term = any(term in text for term in mortgage_terms)
    has_product = any('loan' in p.lower() for p in entities.get('products', []))

    return has_brand or has_term or has_product


def _has_housing_focus(story: Dict) -> bool:
    """Check if story has housing focus"""
    entities = story.get('entities', {})

    return len(entities.get('housing_terms', [])) > 0 or \
           any(b.lower() in ['zillow', 'redfin', 'realtor.com'] for b in entities.get('brands', []))


def _has_culture_focus(story: Dict) -> bool:
    """Check if story has culture/workplace focus"""
    entities = story.get('entities', {})
    return len(entities.get('cultural_themes', [])) > 0


def _has_storytelling_focus(story: Dict) -> bool:
    """Check if story has storytelling focus"""
    entities = story.get('entities', {})
    return len(entities.get('storytelling_themes', [])) > 0


def _signal_has_mortgage_focus(signal: Dict) -> bool:
    """Check if signal has mortgage focus"""
    entities = signal.get('entities', {})
    brands = [b.lower() for b in entities.get('brands', [])]

    mortgage_brands = ['rocket', 'better.com', 'loandepot', 'uwm', 'wells fargo', 'chase']
    return any(mb in ' '.join(brands) for mb in mortgage_brands)


def _signal_has_housing_focus(signal: Dict) -> bool:
    """Check if signal has housing focus"""
    entities = signal.get('entities', {})
    return len(entities.get('housing_terms', [])) > 0


def _signal_has_culture_focus(signal: Dict) -> bool:
    """Check if signal has culture focus"""
    entities = signal.get('entities', {})
    return len(entities.get('cultural_themes', [])) > 0


def _signal_has_storytelling_focus(signal: Dict) -> bool:
    """Check if signal has storytelling focus"""
    entities = signal.get('entities', {})
    return len(entities.get('storytelling_themes', [])) > 0


# Example usage
if __name__ == "__main__":
    # Test with sample data
    sample_stories = [
        {
            'title': 'Rocket Mortgage launches new AI-powered platform',
            'url': 'https://example.com/1',
            'outlet': 'HousingWire',
            'feed_category': 'Mortgage Industry',
            'date': '2026-01-20',
            'description': 'New platform aims to streamline homebuying',
            'summary': 'Rocket Mortgage introduces AI technology...',
            'entities': {
                'brands': ['Rocket Mortgage'],
                'technologies': ['AI', 'machine learning'],
                'cultural_themes': ['innovation culture']
            },
            'text': 'rocket mortgage ai platform homebuying'
        }
    ]

    export_stories_json(sample_stories, output_file='test_export.json')
    print("\n✓ Test export completed")
