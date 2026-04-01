#!/usr/bin/env python3
"""
Scaffold Generator - Hierarchical JSON Analysis Framework
Creates: Timeframe → Environment → Signals → Trends → Implications → Risks → Questions
"""

import json
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import List, Dict


class ScaffoldGenerator:
    """Generate hierarchical JSON analysis scaffold"""

    def __init__(self):
        pass

    def generate_scaffold(self, signals: List[Dict], stories: List[Dict],
                         trend_data: Dict = None) -> Dict:
        """
        Generate complete hierarchical scaffold

        Args:
            signals: Clustered signals from signal_clustering
            stories: All stories
            trend_data: Historical trend data

        Returns:
            Complete scaffold dictionary
        """

        # Build scaffold structure
        scaffold = {
            'meta': self._generate_meta(stories),
            'environment': self._generate_environment(signals, stories, trend_data),
            'signals': self._format_signals(signals),
            'trends': self._generate_trends(signals, trend_data),
            'implications': self._generate_implications(signals, stories),
            'risks': self._generate_risks(signals, stories),
            'north_star_questions': self._generate_questions(signals, stories),
            'raw_data_summary': self._generate_raw_summary(signals, stories)
        }

        return scaffold

    def _generate_meta(self, stories: List[Dict]) -> Dict:
        """Generate metadata section"""

        # Calculate date range
        dates = []
        for story in stories:
            date_str = story.get('date', '')
            if date_str:
                try:
                    dates.append(datetime.fromisoformat(date_str.replace('Z', '+00:00')))
                except:
                    pass

        if dates:
            min_date = min(dates)
            max_date = max(dates)
            coverage_days = (max_date - min_date).days + 1
            date_range = [min_date.date().isoformat(), max_date.date().isoformat()]

            # Format period
            if coverage_days <= 1:
                period = f"Day of {max_date.strftime('%B %d, %Y')}"
            elif coverage_days <= 7:
                period = f"Week of {min_date.strftime('%B %d')}-{max_date.strftime('%d, %Y')}"
            else:
                period = f"{min_date.strftime('%B %d')} - {max_date.strftime('%B %d, %Y')}"
        else:
            coverage_days = 7
            date_range = []
            period = "Recent period"

        # Count outlets by category
        outlet_categories = Counter()
        outlets_set = set()
        for story in stories:
            outlet = story.get('outlet', 'Unknown')
            category = story.get('feed_category', 'Uncategorized')
            outlets_set.add(outlet)
            if category:
                outlet_categories[category] += 1

        return {
            'generated_at': datetime.now().isoformat(),
            'timeframe': {
                'period': period,
                'coverage_days': coverage_days,
                'date_range': date_range,
                'total_stories': len(stories),
                'unique_outlets': len(outlets_set),
                'outlets_breakdown': dict(outlet_categories)
            }
        }

    def _generate_environment(self, signals: List[Dict], stories: List[Dict],
                             trend_data: Dict = None) -> Dict:
        """Generate environment/context section"""

        # Extract macro trends from top signals
        macro_trends = []
        for signal in signals[:5]:  # Top 5 signals
            trend = f"{signal['cluster_name']} (↑{signal['story_count']} mentions)"
            macro_trends.append(trend)

        # Identify growth areas from rising signals
        growth_areas = []
        declining_areas = []
        for signal in signals:
            if signal['momentum'] == 'rising':
                growth_areas.append(signal['cluster_name'])
            elif signal['momentum'] == 'declining':
                declining_areas.append(signal['cluster_name'])

        # M&A activity
        ma_stories = [s for s in stories if any(
            kw in s.get('title', '').lower() + s.get('description', '').lower()
            for kw in ['merger', 'acquisition', 'm&a', 'acquire', 'deal', 'partnership']
        )]

        consolidation_activity = []
        if ma_stories:
            consolidation_activity.append(f"{len(ma_stories)} M&A/partnership announcements detected")

        return {
            'macro_context': {
                'industry_landscape': macro_trends[:3],
                'regulatory_climate': self._infer_regulatory_trends(stories)
            },
            'market_dynamics': {
                'growth_areas': growth_areas[:5],
                'declining_areas': declining_areas[:3],
                'consolidation_activity': consolidation_activity
            }
        }

    def _infer_regulatory_trends(self, stories: List[Dict]) -> List[str]:
        """Infer regulatory trends from story content"""
        regulatory_keywords = {
            'privacy': ['privacy', 'gdpr', 'ccpa', 'data protection'],
            'ai_regulation': ['ai regulation', 'ai act', 'ai governance'],
            'antitrust': ['antitrust', 'monopoly', 'ftc', 'department of justice'],
            'content_moderation': ['content moderation', 'misinformation', 'section 230']
        }

        trends = []
        for category, keywords in regulatory_keywords.items():
            matching = [s for s in stories if any(
                kw in s.get('title', '').lower() + s.get('description', '').lower()
                for kw in keywords
            )]
            if len(matching) >= 3:
                trends.append(f"{category.replace('_', ' ').title()}: {len(matching)} stories")

        return trends[:3]

    def _format_signals(self, signals: List[Dict]) -> List[Dict]:
        """Format signals for scaffold output"""
        formatted = []

        for signal in signals:
            # Format stories within signal
            formatted_stories = []
            for story in signal.get('stories', [])[:10]:  # Limit to 10 per signal
                formatted_stories.append({
                    'title': story.get('title', ''),
                    'outlet': story.get('outlet', 'Unknown'),
                    'date': story.get('date', ''),
                    'url': story.get('url', ''),
                    'summary': story.get('summary', story.get('description', ''))[:200],
                    'relevance_score': 0.85  # Placeholder - could calculate based on cluster distance
                })

            formatted.append({
                'cluster_id': signal['cluster_id'],
                'cluster_name': signal['cluster_name'],
                'description': signal['description'],
                'frequency': signal['frequency'],
                'momentum': signal['momentum'],
                'confidence': signal['confidence'],
                'story_count': signal['story_count'],
                'first_seen': signal['first_seen'],
                'peak_date': signal['peak_date'],
                'outlets': signal['outlets'],
                'stories': formatted_stories,
                'entities': signal['entities'],
                'related_buzzwords': signal['related_buzzwords']
            })

        return formatted

    def _generate_trends(self, signals: List[Dict], trend_data: Dict = None) -> Dict:
        """Generate trends section"""

        # Categorize signals by momentum and duration
        emerging = []  # Rising signals, recent appearance
        building = []  # Rising signals, sustained growth
        lasting = []   # Stable signals, long duration

        for signal in signals:
            if signal['momentum'] == 'rising':
                if signal['story_count'] < 10:
                    emerging.append({
                        'name': signal['cluster_name'],
                        'first_appearance': signal['first_seen'],
                        'growth_rate': 100,  # Placeholder
                        'mention_count': signal['story_count'],
                        'key_players': signal['entities'].get('brands', [])[:3]
                    })
                else:
                    building.append({
                        'name': signal['cluster_name'],
                        'duration_weeks': 4,  # Placeholder
                        'growth_rate': 65,
                        'mention_count': signal['story_count'],
                        'key_players': signal['entities'].get('brands', [])[:3]
                    })
            elif signal['story_count'] >= 15:
                lasting.append({
                    'name': signal['cluster_name'],
                    'duration_weeks': 12,  # Placeholder
                    'stability_score': 0.85,
                    'mention_count': signal['story_count'],
                    'key_players': signal['entities'].get('brands', [])[:3]
                })

        return {
            'emerging': sorted(emerging, key=lambda x: x['mention_count'], reverse=True)[:5],
            'building': sorted(building, key=lambda x: x['mention_count'], reverse=True)[:5],
            'lasting': sorted(lasting, key=lambda x: x['mention_count'], reverse=True)[:5]
        }

    def _generate_implications(self, signals: List[Dict], stories: List[Dict]) -> Dict:
        """Generate implications section"""

        opportunities = []
        threats = []
        strategic_shifts = []

        # Analyze top signals for implications
        for signal in signals[:10]:
            entities = signal.get('entities', {})
            technologies = entities.get('technologies', [])
            momentum = signal.get('momentum', 'stable')

            # Opportunities: Rising trends with clear technology adoption
            if momentum == 'rising' and technologies:
                opportunities.append({
                    'category': 'Technology Adoption',
                    'insight': f"{signal['cluster_name']} adoption accelerating",
                    'evidence': [f"{signal['story_count']} stories in recent period"],
                    'actionability': 'high' if signal['story_count'] >= 10 else 'medium',
                    'affected_sectors': self._identify_sectors(signal)
                })

            # Threats: Declining trends or disruptive technologies
            if momentum == 'declining':
                threats.append({
                    'category': 'Market Disruption',
                    'insight': f"{signal['cluster_name']} showing decline",
                    'evidence': [f"Momentum: {momentum}"],
                    'urgency': 'medium',
                    'affected_sectors': self._identify_sectors(signal)
                })

            # Strategic shifts: Major technology/platform changes
            if any(tech in ' '.join(technologies).lower() for tech in ['ai', 'ctv', 'streaming', 'web3']):
                strategic_shifts.append({
                    'shift': signal['cluster_name'],
                    'drivers': technologies[:3],
                    'timeline': '12-18 months',
                    'adoption_stage': 'early majority' if signal['story_count'] >= 20 else 'early adopters'
                })

        return {
            'opportunities': opportunities[:5],
            'threats': threats[:3],
            'strategic_shifts': strategic_shifts[:5]
        }

    def _generate_risks(self, signals: List[Dict], stories: List[Dict]) -> Dict:
        """Generate risks section"""

        risks = {
            'technological': [],
            'regulatory': [],
            'competitive': [],
            'market': []
        }

        # Scan for risk-related stories
        for signal in signals:
            name = signal['cluster_name'].lower()
            entities = signal.get('entities', {})

            # Technological risks
            if any(term in name for term in ['ai', 'automation', 'algorithm']):
                risks['technological'].append({
                    'risk': f"AI implementation challenges in {signal['cluster_name']}",
                    'probability': 'medium',
                    'impact': 'high',
                    'mitigation': 'Human oversight and quality control processes'
                })

            # Regulatory risks
            if any(term in name for term in ['privacy', 'data', 'compliance']):
                risks['regulatory'].append({
                    'risk': f"Regulatory scrutiny of {signal['cluster_name']}",
                    'probability': 'high',
                    'impact': 'medium',
                    'affected_sectors': self._identify_sectors(signal)
                })

            # Competitive risks
            if any(term in name for term in ['merger', 'acquisition', 'consolidation']):
                risks['competitive'].append({
                    'risk': 'Market consolidation reducing competition',
                    'probability': 'medium',
                    'impact': 'high',
                    'evidence': [f"{signal['story_count']} M&A stories"]
                })

        # Limit each category
        for category in risks:
            risks[category] = risks[category][:3]

        return risks

    def _generate_questions(self, signals: List[Dict], stories: List[Dict]) -> List[Dict]:
        """Generate north-star strategic questions"""

        questions = []
        categories_used = set()

        for signal in signals[:15]:
            name = signal['cluster_name']
            entities = signal.get('entities', {})
            technologies = entities.get('technologies', [])

            # AI/Automation questions
            if 'ai' in ' '.join(technologies).lower() and 'Industry Structure' not in categories_used:
                questions.append({
                    'question': f"How will {name} reshape competitive dynamics in the industry?",
                    'category': 'Industry Structure',
                    'signals': [signal['cluster_id']],
                    'urgency': 'high' if signal['momentum'] == 'rising' else 'medium'
                })
                categories_used.add('Industry Structure')

            # Platform/Market questions
            if signal['story_count'] >= 15 and 'Market Dynamics' not in categories_used:
                questions.append({
                    'question': f"What are the long-term implications of {name} for market structure?",
                    'category': 'Market Dynamics',
                    'signals': [signal['cluster_id']],
                    'urgency': 'medium'
                })
                categories_used.add('Market Dynamics')

            # Cultural/Brand questions
            if any(entities.get(cat) for cat in ['brands', 'companies']) and 'Cultural Impact' not in categories_used:
                top_brands = entities.get('brands', [])[:2]
                if top_brands:
                    questions.append({
                        'question': f"How do consumers perceive brand authenticity when {name.lower()}?",
                        'category': 'Cultural Impact',
                        'signals': [signal['cluster_id']],
                        'urgency': 'medium'
                    })
                    categories_used.add('Cultural Impact')

        return questions[:5]

    def _identify_sectors(self, signal: Dict) -> List[str]:
        """Identify affected industry sectors from signal"""
        sectors = set()

        entities = signal.get('entities', {})
        name = signal['cluster_name'].lower()

        # Technology sectors
        if any(tech in name for tech in ['ai', 'ml', 'automation', 'platform']):
            sectors.add('Technology')

        # Advertising/Marketing
        if any(term in name for term in ['advertising', 'marketing', 'campaign', 'brand']):
            sectors.add('Advertising & Marketing')

        # Media/Entertainment
        if any(term in name for term in ['streaming', 'ctv', 'media', 'content']):
            sectors.add('Media & Entertainment')

        # Finance
        if any(term in name for term in ['fintech', 'mortgage', 'banking', 'finance']):
            sectors.add('Financial Services')

        return list(sectors)[:3]

    def _generate_raw_summary(self, signals: List[Dict], stories: List[Dict]) -> Dict:
        """Generate raw data summary"""

        # Count stories with full content
        with_content = sum(1 for s in stories if s.get('full_content'))

        # Count unique entities
        all_entities = set()
        for signal in signals:
            entities = signal.get('entities', {})
            for category, items in entities.items():
                all_entities.update(items)

        # Count outliers (stories not in any major cluster)
        clustered_count = sum(signal['story_count'] for signal in signals)
        outliers = len(stories) - clustered_count

        return {
            'total_articles': len(stories),
            'articles_with_full_content': with_content,
            'unique_entities_extracted': len(all_entities),
            'clusters_identified': len(signals),
            'outliers': max(0, outliers)
        }


# Convenience function
def generate_analysis_scaffold(signals: List[Dict], stories: List[Dict],
                               trend_data: Dict = None) -> Dict:
    """
    Quick scaffold generation

    Args:
        signals: Clustered signals
        stories: All stories
        trend_data: Historical trend data

    Returns:
        Complete scaffold dictionary
    """
    generator = ScaffoldGenerator()
    return generator.generate_scaffold(signals, stories, trend_data)


# Example usage
if __name__ == "__main__":
    # Test scaffold generation
    sample_signals = [{
        'cluster_id': 'signal_001',
        'cluster_name': 'AI-Driven Content Creation',
        'description': 'Brands using AI for marketing',
        'frequency': 15,
        'story_count': 15,
        'momentum': 'rising',
        'confidence': 'high',
        'first_seen': '2026-01-01',
        'peak_date': '2026-01-15',
        'outlets': ['Adweek', 'Marketing Dive'],
        'stories': [],
        'entities': {
            'brands': ['Lexus', 'AKQA'],
            'technologies': ['GenAI', 'AI']
        },
        'related_buzzwords': ['AI', 'GENERATIVE']
    }]

    sample_stories = [
        {
            'title': 'Test Story',
            'outlet': 'Test Outlet',
            'date': '2026-01-15',
            'description': 'Test description'
        }
    ]

    generator = ScaffoldGenerator()
    scaffold = generator.generate_scaffold(sample_signals, sample_stories)

    print("\n=== Scaffold Generation Test ===")
    print(json.dumps(scaffold['meta'], indent=2))
