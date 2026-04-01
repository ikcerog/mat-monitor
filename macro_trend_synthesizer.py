#!/usr/bin/env python3
"""
Macro Trend Synthesizer
Analyzes the ongoing summary cache and generates a processed, macro-level JSON
that synthesizes trends, themes, and narratives for LLM consumption
"""

import json
from datetime import datetime, timedelta, timezone
from collections import Counter, defaultdict
from typing import List, Dict, Set


class MacroTrendSynthesizer:
    """Synthesize macro-level trends from signals and stories"""

    def __init__(self):
        pass

    def synthesize(self, signals: List[Dict], stories: List[Dict],
                   trend_data: Dict = None) -> Dict:
        """
        Generate macro-level trend synthesis

        Args:
            signals: Clustered signals from signal_clustering
            stories: All stories from current period
            trend_data: Historical trend data

        Returns:
            Synthesized macro trend dictionary
        """

        synthesis = {
            "meta": {
                "generated_at": datetime.now().isoformat(),
                "synthesis_period": self._get_synthesis_period(stories),
                "data_points": {
                    "total_stories": len(stories),
                    "total_signals": len(signals),
                    "time_span_days": self._calculate_time_span(stories)
                }
            },

            "narrative_threads": self._identify_narrative_threads(signals, stories),

            "thematic_clusters": self._build_thematic_clusters(signals, stories),

            "momentum_analysis": self._analyze_momentum(signals),

            "entity_landscape": self._map_entity_landscape(stories),

            "focus_area_insights": self._analyze_focus_areas(signals, stories),

            "emerging_patterns": self._detect_emerging_patterns(signals, trend_data),

            "strategic_narrative": self._generate_strategic_narrative(signals, stories),

            "macro_observations": self._generate_macro_observations(signals, stories)
        }

        return synthesis

    def _get_synthesis_period(self, stories: List[Dict]) -> str:
        """Determine the time period covered"""
        dates = self._extract_dates(stories)
        if dates:
            start = min(dates)
            end = max(dates)
            days = (end - start).days

            if days <= 7:
                return f"Week of {start.strftime('%B %d')} - {end.strftime('%d, %Y')}"
            elif days <= 30:
                return f"Month of {end.strftime('%B %Y')}"
            else:
                return f"{start.strftime('%B %d')} - {end.strftime('%B %d, %Y')}"
        return "Recent period"

    def _identify_narrative_threads(self, signals: List[Dict], stories: List[Dict]) -> List[Dict]:
        """
        Identify overarching narrative threads across signals
        These are the "big stories" emerging
        """
        threads = []

        # Group signals by thematic similarity
        theme_groups = self._group_signals_by_theme(signals)

        for theme, related_signals in theme_groups.items():
            if len(related_signals) < 2:
                continue

            total_stories = sum(s['story_count'] for s in related_signals)

            # Extract key entities across this theme
            all_entities = self._aggregate_entities_from_signals(related_signals)

            thread = {
                "thread_id": f"thread_{len(threads) + 1:02d}",
                "narrative": self._craft_narrative(theme, related_signals),
                "theme": theme,
                "supporting_signals": [s['cluster_id'] for s in related_signals],
                "story_count": total_stories,
                "momentum": self._aggregate_momentum(related_signals),
                "key_players": {
                    "brands": all_entities['brands'][:5],
                    "technologies": all_entities['technologies'][:5],
                    "themes": all_entities.get('cultural_themes', [])[:3]
                },
                "time_depth": self._calculate_thread_depth(related_signals),
                "outlook": self._assess_thread_outlook(related_signals)
            }

            threads.append(thread)

        # Sort by story count (most significant first)
        threads.sort(key=lambda x: x['story_count'], reverse=True)

        return threads[:10]  # Top 10 threads

    def _build_thematic_clusters(self, signals: List[Dict], stories: List[Dict]) -> Dict:
        """
        Build thematic view organized by focus areas
        """
        clusters = {
            "mortgage_innovation": {
                "description": "Technology and innovation in mortgage lending",
                "signals": [],
                "story_count": 0,
                "key_themes": set()
            },
            "housing_market_dynamics": {
                "description": "Consumer housing market trends and shifts",
                "signals": [],
                "story_count": 0,
                "key_themes": set()
            },
            "customer_experience": {
                "description": "Consumer-facing improvements and storytelling",
                "signals": [],
                "story_count": 0,
                "key_themes": set()
            },
            "workplace_culture": {
                "description": "Enterprise culture and employee experience",
                "signals": [],
                "story_count": 0,
                "key_themes": set()
            },
            "industry_transformation": {
                "description": "Broader industry changes and disruption",
                "signals": [],
                "story_count": 0,
                "key_themes": set()
            }
        }

        # Categorize each signal
        for signal in signals:
            categories = self._categorize_signal(signal)

            for category in categories:
                if category in clusters:
                    clusters[category]["signals"].append({
                        "id": signal['cluster_id'],
                        "name": signal['cluster_name'],
                        "story_count": signal['story_count'],
                        "momentum": signal['momentum']
                    })
                    clusters[category]["story_count"] += signal['story_count']

                    # Extract themes
                    entities = signal.get('entities', {})
                    clusters[category]["key_themes"].update(entities.get('cultural_themes', []))
                    clusters[category]["key_themes"].update(entities.get('storytelling_themes', []))

        # Convert sets to lists and clean up
        for cluster in clusters.values():
            cluster["key_themes"] = sorted(list(cluster["key_themes"]))[:5]
            cluster["signals"].sort(key=lambda x: x['story_count'], reverse=True)

        return clusters

    def _analyze_momentum(self, signals: List[Dict]) -> Dict:
        """Analyze overall momentum patterns"""

        momentum_counts = Counter(s['momentum'] for s in signals)

        rising_signals = [s for s in signals if s['momentum'] == 'rising']
        declining_signals = [s for s in signals if s['momentum'] == 'declining']

        return {
            "overall_sentiment": self._determine_overall_sentiment(momentum_counts),
            "distribution": {
                "rising": momentum_counts.get('rising', 0),
                "stable": momentum_counts.get('stable', 0),
                "declining": momentum_counts.get('declining', 0)
            },
            "hot_topics": [
                {
                    "name": s['cluster_name'],
                    "story_count": s['story_count'],
                    "velocity": "high" if s['story_count'] >= 15 else "medium"
                }
                for s in sorted(rising_signals, key=lambda x: x['story_count'], reverse=True)[:5]
            ],
            "cooling_topics": [
                {
                    "name": s['cluster_name'],
                    "story_count": s['story_count']
                }
                for s in declining_signals[:3]
            ]
        }

    def _map_entity_landscape(self, stories: List[Dict]) -> Dict:
        """Map the landscape of key entities"""

        brand_mentions = Counter()
        tech_mentions = Counter()
        people_mentions = Counter()
        cultural_themes = Counter()
        storytelling_themes = Counter()

        for story in stories:
            entities = story.get('entities', {})
            brand_mentions.update(entities.get('brands', []))
            tech_mentions.update(entities.get('technologies', []))
            people_mentions.update(entities.get('people', []))
            cultural_themes.update(entities.get('cultural_themes', []))
            storytelling_themes.update(entities.get('storytelling_themes', []))

        return {
            "dominant_brands": [
                {"name": name, "mentions": count}
                for name, count in brand_mentions.most_common(10)
            ],
            "key_technologies": [
                {"name": name, "mentions": count}
                for name, count in tech_mentions.most_common(10)
            ],
            "influential_voices": [
                {"name": name, "mentions": count}
                for name, count in people_mentions.most_common(5)
            ],
            "cultural_movements": [
                {"theme": name, "frequency": count}
                for name, count in cultural_themes.most_common(5)
            ],
            "storytelling_approaches": [
                {"approach": name, "frequency": count}
                for name, count in storytelling_themes.most_common(5)
            ]
        }

    def _analyze_focus_areas(self, signals: List[Dict], stories: List[Dict]) -> Dict:
        """Analyze coverage across focus areas"""

        mortgage_signals = [s for s in signals if self._is_mortgage_focused_signal(s)]
        housing_signals = [s for s in signals if self._is_housing_focused_signal(s)]
        culture_signals = [s for s in signals if self._is_culture_focused_signal(s)]
        storytelling_signals = [s for s in signals if self._is_storytelling_focused_signal(s)]

        return {
            "mortgage_lending": {
                "signal_count": len(mortgage_signals),
                "story_count": sum(s['story_count'] for s in mortgage_signals),
                "top_signals": [s['cluster_name'] for s in mortgage_signals[:3]],
                "momentum": self._aggregate_momentum(mortgage_signals),
                "key_insight": self._extract_key_insight(mortgage_signals, "mortgage")
            },
            "housing_market": {
                "signal_count": len(housing_signals),
                "story_count": sum(s['story_count'] for s in housing_signals),
                "top_signals": [s['cluster_name'] for s in housing_signals[:3]],
                "momentum": self._aggregate_momentum(housing_signals),
                "key_insight": self._extract_key_insight(housing_signals, "housing")
            },
            "enterprise_culture": {
                "signal_count": len(culture_signals),
                "story_count": sum(s['story_count'] for s in culture_signals),
                "top_signals": [s['cluster_name'] for s in culture_signals[:3]],
                "momentum": self._aggregate_momentum(culture_signals),
                "key_insight": self._extract_key_insight(culture_signals, "culture")
            },
            "brand_storytelling": {
                "signal_count": len(storytelling_signals),
                "story_count": sum(s['story_count'] for s in storytelling_signals),
                "top_signals": [s['cluster_name'] for s in storytelling_signals[:3]],
                "momentum": self._aggregate_momentum(storytelling_signals),
                "key_insight": self._extract_key_insight(storytelling_signals, "storytelling")
            }
        }

    def _detect_emerging_patterns(self, signals: List[Dict], trend_data: Dict) -> List[Dict]:
        """Detect emerging patterns that deserve attention"""

        patterns = []

        # New signals (first appearance)
        new_signals = [s for s in signals if s.get('first_seen') and self._is_recent(s['first_seen'])]

        if new_signals:
            patterns.append({
                "pattern_type": "new_emergence",
                "description": f"{len(new_signals)} new topic(s) appearing",
                "examples": [s['cluster_name'] for s in new_signals[:3]],
                "significance": "high" if len(new_signals) >= 3 else "medium"
            })

        # Rising momentum across multiple signals
        rising_count = len([s for s in signals if s['momentum'] == 'rising'])
        if rising_count >= len(signals) * 0.4:  # 40%+ rising
            patterns.append({
                "pattern_type": "momentum_surge",
                "description": f"Broad momentum surge across {rising_count} signals",
                "significance": "high",
                "implication": "Industry-wide shift or major event driving coverage"
            })

        # Technology adoption patterns
        tech_signals = self._find_technology_focused_signals(signals)
        if len(tech_signals) >= 3:
            tech_entities = self._aggregate_entities_from_signals(tech_signals)
            patterns.append({
                "pattern_type": "technology_wave",
                "description": "Technology adoption theme across multiple signals",
                "technologies": tech_entities['technologies'][:5],
                "signal_count": len(tech_signals),
                "significance": "high"
            })

        # Cultural shift patterns
        culture_entities = Counter()
        for signal in signals:
            culture_entities.update(signal.get('entities', {}).get('cultural_themes', []))

        if culture_entities:
            top_culture = culture_entities.most_common(1)[0]
            if top_culture[1] >= 3:  # Appears in 3+ signals
                patterns.append({
                    "pattern_type": "cultural_movement",
                    "description": f"'{top_culture[0]}' emerging as key cultural theme",
                    "frequency": top_culture[1],
                    "significance": "medium"
                })

        return patterns

    def _generate_strategic_narrative(self, signals: List[Dict], stories: List[Dict]) -> Dict:
        """Generate the overarching strategic narrative"""

        # Identify the "main story"
        top_signal = max(signals, key=lambda s: s['story_count']) if signals else None

        # Identify key shifts
        shifts = []
        rising_signals = [s for s in signals if s['momentum'] == 'rising']
        if rising_signals:
            top_rising = max(rising_signals, key=lambda s: s['story_count'])
            shifts.append(f"Growing focus on {top_rising['cluster_name'].lower()}")

        # Identify dominant themes
        all_entities = self._aggregate_entities_from_signals(signals)
        top_themes = all_entities.get('cultural_themes', [])[:2]

        return {
            "headline": self._craft_headline(top_signal, rising_signals),
            "executive_summary": self._craft_executive_summary(signals, stories),
            "key_shifts": shifts[:3],
            "dominant_themes": top_themes,
            "attention_areas": [
                s['cluster_name'] for s in sorted(signals, key=lambda x: x['story_count'], reverse=True)[:3]
            ],
            "strategic_questions": self._generate_strategic_questions(signals)
        }

    def _generate_macro_observations(self, signals: List[Dict], stories: List[Dict]) -> List[str]:
        """Generate high-level macro observations"""

        observations = []

        # Coverage intensity
        total_stories = sum(s['story_count'] for s in signals)
        if total_stories >= 100:
            observations.append(f"High coverage intensity with {total_stories} stories across {len(signals)} themes")

        # Momentum assessment
        rising_pct = len([s for s in signals if s['momentum'] == 'rising']) / len(signals) if signals else 0
        if rising_pct >= 0.5:
            observations.append("Predominantly rising momentum suggests active market dynamics")
        elif rising_pct <= 0.2:
            observations.append("Limited momentum suggests consolidation or quieter period")

        # Entity diversity
        all_entities = self._aggregate_entities_from_signals(signals)
        brand_count = len(all_entities.get('brands', []))
        if brand_count >= 20:
            observations.append(f"Broad ecosystem participation ({brand_count} brands mentioned)")
        elif brand_count <= 5:
            observations.append("Coverage concentrated among few key players")

        # Technology focus
        tech_count = len(all_entities.get('technologies', []))
        if tech_count >= 10:
            observations.append(f"Technology-heavy coverage ({tech_count} technologies tracked)")

        # Cultural emphasis
        cultural_signals = [s for s in signals if len(s.get('entities', {}).get('cultural_themes', [])) > 0]
        if len(cultural_signals) >= len(signals) * 0.3:
            observations.append("Strong cultural/workplace narrative emerging")

        return observations[:5]

    # Helper methods

    def _group_signals_by_theme(self, signals: List[Dict]) -> Dict[str, List[Dict]]:
        """Group signals by broader themes"""
        theme_groups = defaultdict(list)

        for signal in signals:
            # Determine theme based on entities and name
            theme = self._determine_theme(signal)
            theme_groups[theme].append(signal)

        return dict(theme_groups)

    def _determine_theme(self, signal: Dict) -> str:
        """Determine broader theme for a signal"""
        name = signal['cluster_name'].lower()
        entities = signal.get('entities', {})

        # Check for mortgage/lending theme
        if any(term in name for term in ['mortgage', 'lending', 'loan', 'rate']):
            return "Mortgage & Lending"

        # Check for housing market theme
        if any(term in name for term in ['housing', 'home', 'real estate', 'market']):
            return "Housing Market"

        # Check for technology theme
        if entities.get('technologies') and len(entities['technologies']) >= 2:
            return "Technology & Innovation"

        # Check for culture theme
        if entities.get('cultural_themes'):
            return "Workplace & Culture"

        # Check for storytelling theme
        if entities.get('storytelling_themes'):
            return "Brand & Storytelling"

        return "Industry Dynamics"

    def _craft_narrative(self, theme: str, signals: List[Dict]) -> str:
        """Craft narrative description for a thread"""
        top_signal = max(signals, key=lambda s: s['story_count'])

        if theme == "Mortgage & Lending":
            return f"Mortgage lending evolution centered on {top_signal['cluster_name'].lower()}"
        elif theme == "Housing Market":
            return f"Housing market dynamics showing {top_signal['cluster_name'].lower()}"
        elif theme == "Technology & Innovation":
            return f"Technology adoption wave: {top_signal['cluster_name'].lower()}"
        elif theme == "Workplace & Culture":
            return f"Cultural shift toward {top_signal['cluster_name'].lower()}"
        elif theme == "Brand & Storytelling":
            return f"Storytelling focus on {top_signal['cluster_name'].lower()}"
        else:
            return f"Industry movement: {top_signal['cluster_name'].lower()}"

    def _aggregate_entities_from_signals(self, signals: List[Dict]) -> Dict:
        """Aggregate entities from multiple signals"""
        aggregated = defaultdict(Counter)

        for signal in signals:
            entities = signal.get('entities', {})
            for category, items in entities.items():
                if isinstance(items, list):
                    aggregated[category].update(items)

        # Convert to sorted lists
        result = {}
        for category, counter in aggregated.items():
            result[category] = [item for item, _ in counter.most_common(20)]

        return result

    def _aggregate_momentum(self, signals: List[Dict]) -> str:
        """Aggregate momentum across signals"""
        if not signals:
            return "stable"

        rising = sum(1 for s in signals if s['momentum'] == 'rising')
        declining = sum(1 for s in signals if s['momentum'] == 'declining')

        if rising > len(signals) * 0.6:
            return "rising"
        elif declining > len(signals) * 0.4:
            return "declining"
        else:
            return "mixed"

    def _calculate_thread_depth(self, signals: List[Dict]) -> str:
        """Calculate how long a thread has been developing"""
        # Simplified - would analyze first_seen dates
        avg_stories = sum(s['story_count'] for s in signals) / len(signals) if signals else 0

        if avg_stories >= 15:
            return "sustained"
        elif avg_stories >= 7:
            return "developing"
        else:
            return "emerging"

    def _assess_thread_outlook(self, signals: List[Dict]) -> str:
        """Assess outlook for thread"""
        momentum = self._aggregate_momentum(signals)

        if momentum == "rising":
            return "expanding"
        elif momentum == "declining":
            return "contracting"
        else:
            return "evolving"

    def _categorize_signal(self, signal: Dict) -> List[str]:
        """Categorize a signal into focus areas"""
        categories = []

        entities = signal.get('entities', {})
        name = signal['cluster_name'].lower()

        # Check mortgage
        mortgage_brands = ['rocket', 'better.com', 'loandepot', 'uwm', 'wells fargo', 'chase']
        if any(b in ' '.join(entities.get('brands', [])).lower() for b in mortgage_brands):
            categories.append('mortgage_innovation')

        # Check housing
        if entities.get('housing_terms') or any(term in name for term in ['housing', 'home', 'market']):
            categories.append('housing_market_dynamics')

        # Check customer experience
        if entities.get('storytelling_themes') or 'customer' in name or 'experience' in name:
            categories.append('customer_experience')

        # Check culture
        if entities.get('cultural_themes'):
            categories.append('workplace_culture')

        # Check transformation
        if entities.get('technologies') and len(entities['technologies']) >= 2:
            categories.append('industry_transformation')

        return categories if categories else ['industry_transformation']

    def _determine_overall_sentiment(self, momentum_counts: Counter) -> str:
        """Determine overall sentiment from momentum distribution"""
        total = sum(momentum_counts.values())
        if not total:
            return "neutral"

        rising_pct = momentum_counts.get('rising', 0) / total

        if rising_pct >= 0.5:
            return "optimistic"
        elif rising_pct <= 0.2:
            return "cautious"
        else:
            return "balanced"

    def _is_mortgage_focused_signal(self, signal: Dict) -> bool:
        """Check if signal is mortgage-focused"""
        entities = signal.get('entities', {})
        brands = [b.lower() for b in entities.get('brands', [])]
        mortgage_brands = ['rocket', 'better.com', 'loandepot', 'uwm', 'wells fargo', 'chase']
        return any(mb in ' '.join(brands) for mb in mortgage_brands)

    def _is_housing_focused_signal(self, signal: Dict) -> bool:
        """Check if signal is housing-focused"""
        return len(signal.get('entities', {}).get('housing_terms', [])) > 0

    def _is_culture_focused_signal(self, signal: Dict) -> bool:
        """Check if signal is culture-focused"""
        return len(signal.get('entities', {}).get('cultural_themes', [])) > 0

    def _is_storytelling_focused_signal(self, signal: Dict) -> bool:
        """Check if signal is storytelling-focused"""
        return len(signal.get('entities', {}).get('storytelling_themes', [])) > 0

    def _extract_key_insight(self, signals: List[Dict], focus: str) -> str:
        """Extract key insight for a focus area"""
        if not signals:
            return "Limited coverage in this period"

        top_signal = max(signals, key=lambda s: s['story_count'])
        momentum = self._aggregate_momentum(signals)

        insights = {
            "mortgage": f"Primary focus on {top_signal['cluster_name'].lower()} with {momentum} momentum",
            "housing": f"Market narrative centered on {top_signal['cluster_name'].lower()}",
            "culture": f"Cultural emphasis on {top_signal['cluster_name'].lower()}",
            "storytelling": f"Storytelling direction: {top_signal['cluster_name'].lower()}"
        }

        return insights.get(focus, f"Key theme: {top_signal['cluster_name']}")

    def _find_technology_focused_signals(self, signals: List[Dict]) -> List[Dict]:
        """Find signals with strong technology focus"""
        return [s for s in signals if len(s.get('entities', {}).get('technologies', [])) >= 2]

    def _is_recent(self, date_str: str, days: int = 14) -> bool:
        """Check if date is recent"""
        try:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return (datetime.now(timezone.utc) - date).days <= days
        except:
            return False

    def _craft_headline(self, top_signal: Dict, rising_signals: List[Dict]) -> str:
        """Craft headline for the period"""
        if not top_signal:
            return "Industry monitoring update"

        if len(rising_signals) >= 3:
            return f"Rising activity across {len(rising_signals)} themes, led by {top_signal['cluster_name']}"
        else:
            return f"Focus on {top_signal['cluster_name']}"

    def _craft_executive_summary(self, signals: List[Dict], stories: List[Dict]) -> str:
        """Craft 2-3 sentence executive summary"""
        total_stories = sum(s['story_count'] for s in signals)
        rising_count = len([s for s in signals if s['momentum'] == 'rising'])

        summary_parts = []

        # Coverage intensity
        summary_parts.append(f"Analysis of {total_stories} stories across {len(signals)} thematic areas")

        # Momentum
        if rising_count >= len(signals) * 0.5:
            summary_parts.append(f"strong momentum with {rising_count} rising themes")
        else:
            summary_parts.append(f"mixed momentum across the landscape")

        # Top focus
        if signals:
            top_signal = max(signals, key=lambda s: s['story_count'])
            summary_parts.append(f"Primary attention on {top_signal['cluster_name'].lower()}")

        return ". ".join(summary_parts) + "."

    def _generate_strategic_questions(self, signals: List[Dict]) -> List[str]:
        """Generate strategic questions based on signals"""
        questions = []

        # Rising signals generate questions
        rising_signals = sorted([s for s in signals if s['momentum'] == 'rising'],
                              key=lambda x: x['story_count'], reverse=True)

        if rising_signals:
            top_rising = rising_signals[0]
            questions.append(f"How will {top_rising['cluster_name'].lower()} reshape competitive dynamics?")

        # Technology signals
        tech_signals = self._find_technology_focused_signals(signals)
        if tech_signals:
            questions.append("What's driving technology adoption patterns?")

        # Cultural signals
        culture_signals = [s for s in signals if self._is_culture_focused_signal(s)]
        if culture_signals:
            questions.append("How are cultural shifts influencing industry direction?")

        return questions[:3]

    def _extract_dates(self, stories: List[Dict]) -> List[datetime]:
        """Extract dates from stories"""
        dates = []
        for story in stories:
            date_str = story.get('date', '')
            if date_str:
                try:
                    dates.append(datetime.fromisoformat(date_str.replace('Z', '+00:00')))
                except:
                    pass
        return dates

    def _calculate_time_span(self, stories: List[Dict]) -> int:
        """Calculate time span in days"""
        dates = self._extract_dates(stories)
        if dates:
            return (max(dates) - min(dates)).days + 1
        return 0


def generate_macro_synthesis(signals: List[Dict], stories: List[Dict],
                             trend_data: Dict = None,
                             output_file: str = 'macro_trends.json') -> None:
    """
    Generate macro trend synthesis JSON

    Args:
        signals: Clustered signals
        stories: All stories
        trend_data: Historical trend data
        output_file: Output filename
    """
    synthesizer = MacroTrendSynthesizer()
    synthesis = synthesizer.synthesize(signals, stories, trend_data)

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(synthesis, f, indent=2, ensure_ascii=False)

    print(f"✓ Generated {output_file}")
    print(f"   • {len(synthesis['narrative_threads'])} narrative threads")
    print(f"   • {len(synthesis['thematic_clusters'])} thematic clusters")
    print(f"   • {len(synthesis['emerging_patterns'])} emerging patterns")


# Example usage
if __name__ == "__main__":
    # Test with sample data
    sample_signals = [{
        'cluster_id': 'signal_001',
        'cluster_name': 'Digital Mortgage Adoption',
        'story_count': 15,
        'momentum': 'rising',
        'entities': {
            'brands': ['Rocket Mortgage', 'Better.com'],
            'technologies': ['digital mortgage', 'AI'],
            'cultural_themes': ['innovation culture']
        }
    }]

    sample_stories = [{
        'title': 'Test Story',
        'date': '2026-01-20',
        'entities': {
            'brands': ['Rocket Mortgage'],
            'technologies': ['AI']
        }
    }]

    generate_macro_synthesis(sample_signals, sample_stories)
