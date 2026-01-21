#!/usr/bin/env python3
"""
Advanced Entity Extraction Module
Uses custom regex patterns for industry-specific entity extraction
"""

import re
from collections import defaultdict
from typing import Dict, List, Set


# Industry-specific entity patterns (using non-capturing groups to avoid tuple returns)
# Focus: US Housing, Mortgage, Consumer Lifestyle, Enterprise Culture, Storytelling

BRAND_PATTERNS = [
    # Mortgage lenders & servicers
    r'\b(?:Rocket Mortgage|Rocket Companies|Quicken Loans|Better\.com|loanDepot|United Wholesale Mortgage|UWM|Guaranteed Rate|Caliber Home Loans|HomePoint Financial|PennyMac|Mr\. Cooper|CrossCountry Mortgage|Movement Mortgage|New American Funding)\b',
    # Banks with mortgage divisions
    r'\b(?:Wells Fargo|Chase|JPMorgan Chase|Bank of America|U\.S\. Bank|PNC Bank|Truist|Citizens Bank|TD Bank|HSBC|Citibank)\b',
    # Real estate platforms
    r'\b(?:Zillow|Redfin|Realtor\.com|Compass|Opendoor|Offerpad|RedfinNow|Zillow Offers|iBuyer|Knock)\b',
    # Consumer housing & lifestyle brands
    r'\b(?:IKEA|Wayfair|Home Depot|Lowe\'s|West Elm|Pottery Barn|Crate & Barrel|Williams Sonoma|CB2|Article)\b',
    # Insurance & title companies
    r'\b(?:First American|Fidelity National|Old Republic|Stewart Title|CoreLogic|Allstate|State Farm|Liberty Mutual)\b',
    # Fintech & mortgage tech
    r'\b(?:Blend|Ellie Mae|ICE Mortgage Technology|Black Knight|Roostify|SimpleNexus|DocuSign|Snapdocs|Stavvy|Notarize)\b',
    # Credit & verification
    r'\b(?:Equifax|Experian|TransUnion|FICO|VantageScore|Fannie Mae|Freddie Mac|FHA|VA|USDA)\b',
    # Real estate franchises
    r'\b(?:Keller Williams|RE/MAX|Coldwell Banker|Century 21|Berkshire Hathaway HomeServices|Sotheby\'s International Realty|eXp Realty)\b',
]

AGENCY_PATTERNS = [
    # Creative agencies (for storytelling/brand work)
    r'\b(?:Wieden\+Kennedy|Ogilvy|AKQA|R/GA|Droga5|72andSunny|Mother|VCCP|Anomaly|Huge|Work & Co|Collins|Pentagram|Wolff Olins)\b',
]

TECHNOLOGY_PATTERNS = [
    # Mortgage & lending tech
    r'\b(?:LOS|loan origination system|POS|point of sale|digital mortgage|eClosing|eNote|MISMO|automated underwriting|AUS|DU|Desktop Underwriter|LP|Loan Prospector|URLA|1003)\b',
    # CRM & customer experience
    r'\b(?:Salesforce|HubSpot|customer experience|CX|personalization|journey mapping|omnichannel|engagement platform)\b',
    # AI & automation (storytelling/customer-focused)
    r'\b(?:AI|artificial intelligence|machine learning|chatbot|virtual assistant|predictive analytics|NLP|natural language processing|sentiment analysis)\b',
    # Data & analytics
    r'\b(?:data analytics|business intelligence|BI|visualization|dashboard|reporting|insights|predictive modeling)\b',
    # Digital experience
    r'\b(?:UX|user experience|UI|design thinking|mobile app|web app|responsive design|accessibility)\b',
    # Cloud & infrastructure (minimal - only if essential to story)
    r'\b(?:cloud platform|SaaS|API integration|microservices)\b',
]

PEOPLE_PATTERNS = [
    # Common exec titles (capturing group for the name)
    r'\b([A-Z][a-z]+ [A-Z][a-z]+)(?:\s+(?:CEO|CMO|CTO|CFO|COO|VP|SVP|EVP|President|Director|Chief|Head of|Managing Director))\b',
]

PRODUCT_PATTERNS = [
    # Mortgage products
    r'\b(?:30-year fixed|15-year fixed|adjustable-rate mortgage|ARM|FHA loan|VA loan|USDA loan|jumbo loan|conventional loan|conforming loan|non-conforming|HELOC|home equity line|refinance|cash-out refi|rate-and-term refi)\b',
    # Digital tools
    r'\b(?:mobile app|mortgage calculator|rate comparison tool|pre-approval|digital application|eSign|digital closing)\b',
    # Consumer products (home-related)
    r'\b(?:smart home|home security|Ring|Nest|Ecobee|SimpliSafe)\b',
]

# Metrics & KPIs
METRICS_PATTERNS = [
    # Mortgage & housing metrics
    r'\b(?:interest rate|mortgage rate|APR|basis points|bps|loan-to-value|LTV|debt-to-income|DTI|credit score|FICO score|median home price|housing inventory|days on market|DOM|absorption rate)\b',
    # Business metrics
    r'\b(?:ROI|return on investment|customer satisfaction|CSAT|NPS|Net Promoter Score|conversion rate|retention rate|churn rate|loan volume|origination volume|pull-through rate)\b',
    # Consumer metrics
    r'\b(?:affordability|home affordability index|first-time homebuyer|buyer demand|seller market|buyer market)\b',
]

# Cultural & workplace terms
CULTURAL_PATTERNS = [
    r'\b(?:company culture|workplace culture|employee experience|remote work|hybrid work|work-life balance|mental health|wellbeing|diversity|equity|inclusion|DEI|belonging|psychological safety|team building|collaboration|innovation culture|best place to work|employer brand|talent acquisition|retention|employee engagement|purpose-driven|mission-driven|values-driven)\b',
]

# Storytelling & content terms
STORYTELLING_PATTERNS = [
    r'\b(?:brand story|brand narrative|storytelling|content marketing|thought leadership|customer story|case study|testimonial|user-generated content|UGC|authentic|authenticity|human-centered|empathy|emotional connection|brand voice|brand positioning|messaging|narrative arc|compelling story)\b',
]

# Housing market terms
HOUSING_PATTERNS = [
    r'\b(?:housing market|real estate market|home prices|home values|appreciation|depreciation|housing shortage|inventory shortage|supply and demand|seller\'s market|buyer\'s market|bidding war|multiple offers|contingency|appraisal|inspection|closing costs|down payment|earnest money|escrow|title insurance)\b',
]


class EntityExtractor:
    """Advanced entity extraction using custom regex patterns"""

    def __init__(self):
        self.brand_regex = re.compile('|'.join(BRAND_PATTERNS), re.IGNORECASE)
        self.agency_regex = re.compile('|'.join(AGENCY_PATTERNS), re.IGNORECASE)
        self.tech_regex = re.compile('|'.join(TECHNOLOGY_PATTERNS), re.IGNORECASE)
        self.people_regex = re.compile('|'.join(PEOPLE_PATTERNS))
        self.product_regex = re.compile('|'.join(PRODUCT_PATTERNS), re.IGNORECASE)
        self.metrics_regex = re.compile('|'.join(METRICS_PATTERNS), re.IGNORECASE)
        self.cultural_regex = re.compile('|'.join(CULTURAL_PATTERNS), re.IGNORECASE)
        self.storytelling_regex = re.compile('|'.join(STORYTELLING_PATTERNS), re.IGNORECASE)
        self.housing_regex = re.compile('|'.join(HOUSING_PATTERNS), re.IGNORECASE)

    def extract_entities(self, text: str, title: str = "") -> Dict[str, List[str]]:
        """
        Extract entities from text using custom regex patterns

        Args:
            text: Article content
            title: Article title (given higher weight)

        Returns:
            Dictionary with entity categories and lists of unique entities
        """
        entities = {
            'brands': set(),
            'agencies': set(),
            'technologies': set(),
            'companies': set(),
            'people': set(),
            'locations': set(),
            'products': set(),
            'metrics': set(),
            'cultural_themes': set(),
            'storytelling_themes': set(),
            'housing_terms': set()
        }

        # Combine title and text (title gets processed separately for emphasis)
        full_text = f"{title} {title} {text}"  # Title appears twice for weight

        # Pattern-based extraction
        entities['brands'].update(self._extract_pattern(self.brand_regex, full_text))
        entities['agencies'].update(self._extract_pattern(self.agency_regex, full_text))
        entities['technologies'].update(self._extract_pattern(self.tech_regex, full_text))
        entities['products'].update(self._extract_pattern(self.product_regex, full_text))
        entities['metrics'].update(self._extract_pattern(self.metrics_regex, full_text))
        entities['cultural_themes'].update(self._extract_pattern(self.cultural_regex, full_text))
        entities['storytelling_themes'].update(self._extract_pattern(self.storytelling_regex, full_text))
        entities['housing_terms'].update(self._extract_pattern(self.housing_regex, full_text))

        # Extract people names (from PEOPLE_PATTERNS)
        people_matches = self.people_regex.findall(full_text)
        if people_matches:
            # people_matches will be a list of captured names
            entities['people'].update(people_matches)

        # 3. Clean and deduplicate
        cleaned_entities = {}
        for category, entity_set in entities.items():
            # Remove empty strings, single characters, and common false positives
            cleaned = set()
            for e in entity_set:
                # Handle both strings and potential tuples/lists
                if isinstance(e, (tuple, list)):
                    # If it's a tuple/list, join non-empty elements
                    e = ' '.join(str(x) for x in e if x)
                elif not isinstance(e, str):
                    e = str(e)

                e = e.strip()
                if len(e) > 1 and e.lower() not in ['new', 'more', 'get', 'see', 'the', 'and']:
                    cleaned.add(e)

            # Convert to sorted list
            cleaned_entities[category] = sorted(list(cleaned))

        return cleaned_entities

    def _extract_pattern(self, regex, text: str) -> Set[str]:
        """Extract entities using regex pattern"""
        matches = regex.findall(text)
        return set(matches) if matches else set()

    def extract_from_story(self, story: Dict) -> Dict[str, List[str]]:
        """
        Extract entities from a story object

        Args:
            story: Dictionary with 'title', 'description', and optionally 'full_content'

        Returns:
            Dictionary of categorized entities
        """
        title = story.get('title', '')
        description = story.get('description', '')
        full_content = story.get('full_content', '')

        # Combine available text
        text = f"{description} {full_content}"

        return self.extract_entities(text, title)


# Convenience function for quick extraction
def extract_entities_from_text(text: str, title: str = "") -> Dict[str, List[str]]:
    """
    Quick entity extraction from text

    Args:
        text: Article content
        title: Article title (optional)

    Returns:
        Dictionary of categorized entities
    """
    extractor = EntityExtractor()
    return extractor.extract_entities(text, title)


# Example usage
if __name__ == "__main__":
    # Test with sample article
    sample_title = "Nielsen, Roku deepen data-sharing pact to enhance streaming measurement"
    sample_text = """
    As part of the agreement, Nielsen will continue to receive support for offerings
    like Big Data + Panel while Roku gains access to streaming TV ratings. The partnership
    strengthens both companies' positions in the growing CTV advertising market.
    """

    extractor = EntityExtractor()
    entities = extractor.extract_entities(sample_text, sample_title)

    print("\n=== Entity Extraction Test ===")
    for category, items in entities.items():
        if items:
            print(f"\n{category.upper()}:")
            for item in items:
                print(f"  - {item}")
