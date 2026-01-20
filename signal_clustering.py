#!/usr/bin/env python3
"""
Signal Clustering Module
Clusters stories into recurring signals using TF-IDF + K-means
"""

import re
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
from datetime import datetime, timedelta

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    print("⚠️  scikit-learn not installed. Signal clustering disabled. Run: pip3 install scikit-learn numpy")
    SKLEARN_AVAILABLE = False


class SignalClusterer:
    """Cluster stories into thematic signals"""

    def __init__(self, min_cluster_size: int = 3, max_cluster_size: int = 50):
        """
        Args:
            min_cluster_size: Minimum stories per cluster
            max_cluster_size: Maximum stories per cluster
        """
        self.min_cluster_size = min_cluster_size
        self.max_cluster_size = max_cluster_size

    def cluster_stories(self, stories: List[Dict], trend_history: Dict = None) -> List[Dict]:
        """
        Cluster stories into thematic signals

        Args:
            stories: List of story dictionaries with title, description, entities, etc.
            trend_history: Optional historical trend data for momentum calculation

        Returns:
            List of cluster/signal dictionaries
        """
        if not SKLEARN_AVAILABLE:
            print("⚠️  Clustering requires scikit-learn. Returning unclustered stories.")
            return self._create_single_cluster(stories)

        if len(stories) < self.min_cluster_size:
            return self._create_single_cluster(stories)

        # 1. Prepare text for vectorization
        story_texts, entity_texts = self._prepare_texts(stories)

        # 2. Vectorize with TF-IDF
        try:
            # Combine story text with entities (entities weighted 2x)
            combined_texts = [f"{text} {entities} {entities}" for text, entities in zip(story_texts, entity_texts)]

            vectorizer = TfidfVectorizer(
                max_features=500,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.8
            )
            tfidf_matrix = vectorizer.fit_transform(combined_texts)

        except Exception as e:
            print(f"⚠️  TF-IDF vectorization failed: {e}")
            return self._create_single_cluster(stories)

        # 3. Determine optimal number of clusters
        n_clusters = self._determine_optimal_clusters(tfidf_matrix, len(stories))

        if n_clusters < 2:
            return self._create_single_cluster(stories)

        # 4. Perform K-means clustering
        try:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(tfidf_matrix)

        except Exception as e:
            print(f"⚠️  K-means clustering failed: {e}")
            return self._create_single_cluster(stories)

        # 5. Group stories by cluster
        clusters = defaultdict(list)
        for idx, label in enumerate(cluster_labels):
            clusters[label].append(stories[idx])

        # 6. Create signal objects
        signals = []
        feature_names = vectorizer.get_feature_names_out()

        for cluster_id, cluster_stories in clusters.items():
            # Skip clusters that are too small
            if len(cluster_stories) < self.min_cluster_size:
                continue

            # Get top terms for this cluster
            cluster_indices = [i for i, label in enumerate(cluster_labels) if label == cluster_id]
            cluster_center = kmeans.cluster_centers_[cluster_id]
            top_term_indices = cluster_center.argsort()[-10:][::-1]
            top_terms = [feature_names[i] for i in top_term_indices]

            # Create signal
            signal = self._create_signal(
                cluster_id=cluster_id,
                stories=cluster_stories,
                top_terms=top_terms,
                trend_history=trend_history
            )
            signals.append(signal)

        # Sort by story count (descending)
        signals.sort(key=lambda s: s['story_count'], reverse=True)

        return signals

    def _prepare_texts(self, stories: List[Dict]) -> Tuple[List[str], List[str]]:
        """Prepare story texts and entity texts for vectorization"""
        story_texts = []
        entity_texts = []

        for story in stories:
            # Combine title (weighted), description, and summary
            title = story.get('title', '')
            description = story.get('description', '')
            summary = story.get('summary', '')

            # Title appears 2x for emphasis
            text = f"{title} {title} {description} {summary}"
            story_texts.append(text)

            # Flatten entities into text
            entities = story.get('entities', {})
            entity_list = []
            for category, items in entities.items():
                entity_list.extend(items)
            entity_texts.append(' '.join(entity_list))

        return story_texts, entity_texts

    def _determine_optimal_clusters(self, tfidf_matrix, n_stories: int) -> int:
        """Determine optimal number of clusters based on story count"""
        # Dynamic K based on story volume
        # Rules:
        # - 10-20 stories: 2-3 clusters
        # - 21-50 stories: 3-5 clusters
        # - 51-100 stories: 5-8 clusters
        # - 101-200 stories: 8-12 clusters
        # - 201+ stories: 12-20 clusters

        if n_stories < 10:
            return 1
        elif n_stories <= 20:
            return min(3, n_stories // 7)
        elif n_stories <= 50:
            return min(5, n_stories // 10)
        elif n_stories <= 100:
            return min(8, n_stories // 12)
        elif n_stories <= 200:
            return min(12, n_stories // 16)
        else:
            return min(20, n_stories // 20)

    def _create_signal(self, cluster_id: int, stories: List[Dict],
                      top_terms: List[str], trend_history: Dict = None) -> Dict:
        """Create a signal object from a cluster"""

        # Generate cluster name from top terms and entities
        cluster_name = self._generate_cluster_name(stories, top_terms)

        # Extract all entities from cluster stories
        all_entities = self._aggregate_entities(stories)

        # Get unique outlets
        outlets = list(set(story.get('outlet', 'Unknown') for story in stories))

        # Calculate date range
        dates = []
        for story in stories:
            date_str = story.get('date', '')
            if date_str:
                try:
                    dates.append(datetime.fromisoformat(date_str.replace('Z', '+00:00')))
                except:
                    pass

        first_seen = min(dates).isoformat() if dates else None
        peak_date = max(dates).isoformat() if dates else None

        # Calculate momentum
        momentum = self._calculate_momentum(cluster_name, stories, trend_history)

        # Sort stories by relevance (those with more matching top terms)
        sorted_stories = self._sort_stories_by_relevance(stories, top_terms)

        # Create signal object
        signal = {
            'cluster_id': f"signal_{cluster_id:03d}",
            'cluster_name': cluster_name,
            'description': self._generate_description(cluster_name, all_entities),
            'frequency': len(stories),
            'story_count': len(stories),
            'momentum': momentum,
            'confidence': self._calculate_confidence(len(stories)),
            'first_seen': first_seen,
            'peak_date': peak_date,
            'outlets': outlets,
            'stories': sorted_stories[:self.max_cluster_size],  # Limit stories per cluster
            'entities': all_entities,
            'related_buzzwords': top_terms[:5],
            'top_terms': top_terms
        }

        return signal

    def _generate_cluster_name(self, stories: List[Dict], top_terms: List[str]) -> str:
        """Generate human-readable cluster name"""

        # Get most common entities
        entity_counter = Counter()
        for story in stories:
            entities = story.get('entities', {})
            for category in ['brands', 'technologies', 'agencies']:
                entity_counter.update(entities.get(category, []))

        # Combine top entities and terms
        top_entities = [e for e, _ in entity_counter.most_common(3)]

        # Create name from entities and terms
        if top_entities:
            primary = top_entities[0]
            if len(top_entities) > 1:
                name = f"{primary} & {top_entities[1]}"
            else:
                name = primary

            # Add context from top terms
            relevant_terms = [t for t in top_terms[:3] if t.lower() not in primary.lower()]
            if relevant_terms:
                context = relevant_terms[0].replace('_', ' ').title()
                name = f"{name} - {context}"
        else:
            # Fallback: use top terms
            name = ' '.join(top_terms[:3]).replace('_', ' ').title()

        # Clean and truncate
        name = name.strip()
        if len(name) > 60:
            name = name[:57] + "..."

        return name

    def _generate_description(self, cluster_name: str, entities: Dict) -> str:
        """Generate cluster description"""

        # Get top technologies and brands
        brands = entities.get('brands', [])[:3]
        technologies = entities.get('technologies', [])[:3]

        desc_parts = []

        if brands:
            desc_parts.append(f"Stories featuring {', '.join(brands)}")

        if technologies:
            tech_str = ', '.join(technologies)
            if desc_parts:
                desc_parts.append(f"focusing on {tech_str}")
            else:
                desc_parts.append(f"Coverage of {tech_str}")

        if not desc_parts:
            desc_parts.append(f"Cluster of related stories")

        return ' '.join(desc_parts) + '.'

    def _aggregate_entities(self, stories: List[Dict]) -> Dict[str, List[str]]:
        """Aggregate entities from multiple stories"""
        aggregated = defaultdict(Counter)

        for story in stories:
            entities = story.get('entities', {})
            for category, items in entities.items():
                aggregated[category].update(items)

        # Convert to sorted lists (top 10 per category)
        result = {}
        for category, counter in aggregated.items():
            result[category] = [item for item, _ in counter.most_common(10)]

        return result

    def _calculate_momentum(self, cluster_name: str, stories: List[Dict],
                           trend_history: Dict = None) -> str:
        """Calculate momentum: rising, stable, declining"""

        if not trend_history or 'buzzword_history' not in trend_history:
            return "stable"

        # Count stories in last 7 days vs previous 7 days
        now = datetime.now()
        recent_cutoff = now - timedelta(days=7)
        older_cutoff = now - timedelta(days=14)

        recent_count = 0
        older_count = 0

        for story in stories:
            date_str = story.get('date', '')
            if date_str:
                try:
                    story_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    if story_date >= recent_cutoff:
                        recent_count += 1
                    elif story_date >= older_cutoff:
                        older_count += 1
                except:
                    pass

        # Calculate momentum
        if older_count == 0:
            return "rising" if recent_count >= 3 else "stable"

        growth_rate = (recent_count - older_count) / older_count

        if growth_rate > 0.5:
            return "rising"
        elif growth_rate < -0.3:
            return "declining"
        else:
            return "stable"

    def _calculate_confidence(self, story_count: int) -> str:
        """Calculate confidence level based on story count"""
        if story_count >= 10:
            return "high"
        elif story_count >= 5:
            return "medium"
        else:
            return "low"

    def _sort_stories_by_relevance(self, stories: List[Dict], top_terms: List[str]) -> List[Dict]:
        """Sort stories by relevance to cluster (term overlap)"""
        scored_stories = []

        for story in stories:
            title = story.get('title', '').lower()
            description = story.get('description', '').lower()
            text = f"{title} {description}"

            # Count how many top terms appear in this story
            term_count = sum(1 for term in top_terms if term.lower() in text)

            scored_stories.append((term_count, story))

        # Sort by term count (descending), then preserve original order
        scored_stories.sort(key=lambda x: x[0], reverse=True)

        return [story for _, story in scored_stories]

    def _create_single_cluster(self, stories: List[Dict]) -> List[Dict]:
        """Create a single catch-all cluster when clustering fails"""
        return [{
            'cluster_id': 'signal_001',
            'cluster_name': 'Mixed Stories',
            'description': 'Various industry stories and updates',
            'frequency': len(stories),
            'story_count': len(stories),
            'momentum': 'stable',
            'confidence': 'low',
            'first_seen': None,
            'peak_date': None,
            'outlets': list(set(s.get('outlet', 'Unknown') for s in stories)),
            'stories': stories[:self.max_cluster_size],
            'entities': self._aggregate_entities(stories),
            'related_buzzwords': [],
            'top_terms': []
        }]


# Convenience function
def cluster_stories_into_signals(stories: List[Dict], trend_history: Dict = None,
                                 min_cluster_size: int = 3) -> List[Dict]:
    """
    Quick story clustering

    Args:
        stories: List of story dictionaries
        trend_history: Optional historical trend data
        min_cluster_size: Minimum stories per cluster

    Returns:
        List of signal dictionaries
    """
    clusterer = SignalClusterer(min_cluster_size=min_cluster_size)
    return clusterer.cluster_stories(stories, trend_history)


# Example usage
if __name__ == "__main__":
    # Test clustering
    sample_stories = [
        {
            'title': 'Nielsen, Roku deepen data-sharing pact',
            'description': 'Enhanced streaming measurement partnership',
            'outlet': 'Marketing Dive',
            'date': '2026-01-08',
            'entities': {
                'brands': ['Nielsen', 'Roku'],
                'technologies': ['CTV', 'streaming']
            }
        },
        {
            'title': 'Lexus takes generative AI for a spin',
            'description': 'AI-powered marketing content',
            'outlet': 'Adweek',
            'date': '2026-01-08',
            'entities': {
                'brands': ['Lexus', 'AKQA'],
                'technologies': ['GenAI', 'AI']
            }
        },
        {
            'title': 'Rocket embraces AI in NFL campaign',
            'description': 'Fintech brand uses AI for creative',
            'outlet': 'Marketing Dive',
            'date': '2026-01-08',
            'entities': {
                'brands': ['Rocket'],
                'technologies': ['AI']
            }
        }
    ]

    clusterer = SignalClusterer()
    signals = clusterer.cluster_stories(sample_stories)

    print("\n=== Signal Clustering Test ===")
    for signal in signals:
        print(f"\n{signal['cluster_name']} ({signal['story_count']} stories)")
        print(f"  Momentum: {signal['momentum']}")
        print(f"  Top terms: {', '.join(signal['top_terms'][:5])}")
