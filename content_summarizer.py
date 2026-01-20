#!/usr/bin/env python3
"""
Content Summarization Module
Uses extractive summarization to create brief summaries (2-3 sentences)
"""

import re
import math
from collections import Counter
from typing import List, Dict, Tuple


class ContentSummarizer:
    """Extractive text summarization using sentence scoring"""

    def __init__(self, max_sentences: int = 3):
        """
        Args:
            max_sentences: Maximum number of sentences in summary
        """
        self.max_sentences = max_sentences
        self.stopwords = self._load_stopwords()

    def _load_stopwords(self) -> set:
        """Common English stopwords"""
        return {
            'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
            'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below',
            'between', 'both', 'but', 'by', 'can', 'cannot', 'could', 'did', 'do', 'does',
            'doing', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had',
            'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him',
            'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself',
            'just', 'me', 'might', 'more', 'most', 'must', 'my', 'myself', 'no', 'nor',
            'not', 'now', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours',
            'ourselves', 'out', 'over', 'own', 'same', 'she', 'should', 'so', 'some',
            'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then',
            'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under',
            'until', 'up', 'very', 'was', 'we', 'were', 'what', 'when', 'where', 'which',
            'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'you', 'your', 'yours',
            'yourself', 'yourselves'
        }

    def summarize(self, text: str, title: str = "", entities: Dict = None) -> str:
        """
        Create extractive summary from text

        Args:
            text: Full article text
            title: Article title (for context)
            entities: Optional extracted entities to boost scoring

        Returns:
            Summary string (2-3 sentences)
        """
        if not text or len(text.strip()) < 50:
            return text.strip()

        # Split into sentences
        sentences = self._split_sentences(text)

        if len(sentences) <= self.max_sentences:
            return ' '.join(sentences)

        # Score sentences
        sentence_scores = self._score_sentences(sentences, title, entities)

        # Select top sentences while maintaining order
        top_sentences = self._select_top_sentences(sentences, sentence_scores, self.max_sentences)

        return ' '.join(top_sentences)

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Basic sentence splitting on . ! ?
        # Avoid splitting on common abbreviations
        text = re.sub(r'\bMr\.', 'Mr', text)
        text = re.sub(r'\bMrs\.', 'Mrs', text)
        text = re.sub(r'\bDr\.', 'Dr', text)
        text = re.sub(r'\bInc\.', 'Inc', text)
        text = re.sub(r'\bLtd\.', 'Ltd', text)
        text = re.sub(r'\bCo\.', 'Co', text)

        # Split on sentence boundaries
        sentences = re.split(r'[.!?]+\s+', text)

        # Clean and filter
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

        return sentences

    def _score_sentences(self, sentences: List[str], title: str = "", entities: Dict = None) -> Dict[int, float]:
        """
        Score sentences based on multiple factors:
        1. TF-IDF word importance
        2. Position (first/last sentences often important)
        3. Entity density
        4. Title overlap
        5. Length (prefer medium-length sentences)
        """
        scores = {}

        # Calculate word frequencies (TF)
        word_freq = self._calculate_word_frequencies(sentences)

        # Get title words for overlap scoring
        title_words = set(self._tokenize(title.lower())) if title else set()

        # Flatten entities for density scoring
        entity_words = set()
        if entities:
            for entity_list in entities.values():
                for entity in entity_list:
                    entity_words.update(self._tokenize(entity.lower()))

        for idx, sentence in enumerate(sentences):
            score = 0.0
            words = self._tokenize(sentence.lower())

            # 1. TF-IDF score (word importance)
            tf_idf_score = sum(word_freq.get(word, 0) for word in words) / max(len(words), 1)
            score += tf_idf_score * 3.0

            # 2. Position score (first and last sentences often important)
            if idx == 0:
                score += 2.0  # First sentence bonus
            elif idx == len(sentences) - 1:
                score += 1.0  # Last sentence bonus
            elif idx == 1:
                score += 1.5  # Second sentence bonus

            # 3. Entity density score
            if entity_words:
                entity_count = sum(1 for word in words if word in entity_words)
                entity_density = entity_count / max(len(words), 1)
                score += entity_density * 4.0

            # 4. Title overlap score
            if title_words:
                overlap = len(set(words) & title_words)
                score += overlap * 2.0

            # 5. Length score (prefer medium-length sentences: 10-30 words)
            word_count = len(words)
            if 10 <= word_count <= 30:
                score += 1.0
            elif word_count < 5:
                score -= 1.0  # Penalize very short sentences
            elif word_count > 50:
                score -= 0.5  # Penalize very long sentences

            # 6. Numeric data bonus (statistics, metrics often important)
            if re.search(r'\d+', sentence):
                score += 0.5

            scores[idx] = score

        return scores

    def _calculate_word_frequencies(self, sentences: List[str]) -> Dict[str, float]:
        """Calculate TF-IDF-like word frequencies"""
        # Count word occurrences across all sentences
        word_counts = Counter()
        doc_count = {}  # How many sentences contain each word

        for sentence in sentences:
            words = self._tokenize(sentence.lower())
            word_counts.update(words)

            # Track document frequency
            unique_words = set(words)
            for word in unique_words:
                doc_count[word] = doc_count.get(word, 0) + 1

        # Calculate TF-IDF-like scores
        total_sentences = len(sentences)
        word_freq = {}

        for word, count in word_counts.items():
            if word not in self.stopwords and len(word) > 2:
                # TF: term frequency
                tf = count

                # IDF: inverse document frequency
                idf = math.log(total_sentences / (doc_count[word] + 1))

                word_freq[word] = tf * idf

        # Normalize
        max_freq = max(word_freq.values()) if word_freq else 1
        word_freq = {word: freq / max_freq for word, freq in word_freq.items()}

        return word_freq

    def _tokenize(self, text: str) -> List[str]:
        """Simple word tokenization"""
        # Remove punctuation and split
        text = re.sub(r'[^\w\s-]', ' ', text)
        words = text.split()
        return [w for w in words if len(w) > 1]

    def _select_top_sentences(self, sentences: List[str], scores: Dict[int, float],
                             max_sentences: int) -> List[str]:
        """
        Select top N sentences while maintaining original order

        Args:
            sentences: List of all sentences
            scores: Dictionary mapping sentence index to score
            max_sentences: Number of sentences to select

        Returns:
            List of top sentences in original order
        """
        # Sort by score (descending)
        sorted_indices = sorted(scores.keys(), key=lambda i: scores[i], reverse=True)

        # Take top N
        top_indices = sorted_indices[:max_sentences]

        # Sort by original position to maintain flow
        top_indices.sort()

        # Return sentences in original order
        return [sentences[i] for i in top_indices]


# Convenience function
def summarize_text(text: str, title: str = "", entities: Dict = None, max_sentences: int = 3) -> str:
    """
    Quick text summarization

    Args:
        text: Full article text
        title: Article title (optional)
        entities: Extracted entities (optional)
        max_sentences: Maximum sentences in summary

    Returns:
        Summary string
    """
    summarizer = ContentSummarizer(max_sentences=max_sentences)
    return summarizer.summarize(text, title, entities)


# Example usage
if __name__ == "__main__":
    # Test summarization
    sample_title = "Nielsen, Roku deepen data-sharing pact to enhance streaming measurement"
    sample_text = """
    Nielsen and Roku announced today an expanded partnership to enhance streaming TV measurement.
    As part of the agreement, Nielsen will continue to receive support for offerings like Big Data + Panel
    while Roku gains access to streaming TV ratings. The partnership is designed to provide more accurate
    measurement of streaming viewership across platforms. Industry experts say this deal could reshape
    how advertisers measure CTV performance. Both companies have been investing heavily in measurement
    technology. The announcement comes as the streaming wars intensify. Traditional TV measurement has
    been criticized for not capturing streaming viewership accurately. This partnership aims to solve
    that problem by combining Nielsen's measurement expertise with Roku's platform data. The deal
    strengthens both companies' positions in the growing CTV advertising market which is expected to
    reach $30 billion by 2025. Other measurement companies are watching closely to see if similar
    partnerships emerge. The streaming measurement landscape has become increasingly competitive.
    """

    sample_entities = {
        'brands': ['Nielsen', 'Roku'],
        'technologies': ['CTV', 'streaming', 'Big Data']
    }

    summarizer = ContentSummarizer(max_sentences=3)
    summary = summarizer.summarize(sample_text, sample_title, sample_entities)

    print("\n=== Content Summarization Test ===")
    print(f"\nOriginal length: {len(sample_text)} characters")
    print(f"Summary length: {len(summary)} characters")
    print(f"\nSummary:\n{summary}")
