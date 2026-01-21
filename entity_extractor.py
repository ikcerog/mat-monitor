#!/usr/bin/env python3
"""
Advanced Entity Extraction Module
Uses custom regex patterns for industry-specific entity extraction
"""

import re
from collections import defaultdict
from typing import Dict, List, Set


# Industry-specific entity patterns (using non-capturing groups to avoid tuple returns)
BRAND_PATTERNS = [
    # Major tech platforms
    r'\b(?:Google|Meta|Facebook|Instagram|WhatsApp|Microsoft|Apple|Amazon|Netflix|Disney|TikTok|YouTube|LinkedIn)\b',
    # Ad tech & martech
    r'\b(?:The Trade Desk|Roku|Nielsen|Comscore|Oracle|Salesforce|Adobe|HubSpot|Mailchimp)\b',
    # Brands & retailers
    r'\b(?:Nike|Adidas|Coca-Cola|Pepsi|McDonald\'s|Starbucks|Walmart|Target)\b',
    # Automotive
    r'\b(?:Tesla|Ford|GM|Toyota|Honda|BMW|Mercedes|Audi|Lexus|Porsche)\b',
    # Fast food & CPG
    r'\b(?:Mondelēz|Oreo|Chips Ahoy|Campbell\'s|Heineken|Tiffany|Listerine|Cava|Heinz)\b',
    # Financial services
    r'\b(?:Rocket|Rocket Mortgage|Zillow|Redfin|Realtor\.com|Quicken Loans|Chase|Wells Fargo|Bank of America)\b',
    # Media & entertainment
    r'\b(?:Warner Bros|Universal|Paramount|HBO|Hulu|Peacock|ESPN|CNN|CNBC|NBC|ABC|CBS|Fox)\b',
    # Airlines & travel
    r'\b(?:United|Delta|American Airlines|Southwest|Jet2|Airbnb|Booking\.com|Expedia)\b',
    # Telecom
    r'\b(?:T-Mobile|Verizon|AT&T|Sprint|Comcast|Spectrum)\b',
    # Retail & ecommerce
    r'\b(?:eBay|Etsy|Shopify|Wayfair|Chewy|Instacart|DoorDash|Uber Eats)\b',
    # Insurance
    r'\b(?:Allstate|State Farm|Geico|Progressive|Aviva)\b',
]

AGENCY_PATTERNS = [
    r'\b(?:Ogilvy|BBDO|DDB|Publicis|WPP|Omnicom|IPG|Dentsu|Havas|Saatchi & Saatchi|Wieden\+Kennedy|AKQA|R/GA|Droga5|72andSunny|Mother|VCCP|Adam & Eve/DDB|Anomaly|Rapp|Who Wot Why)\b',
]

TECHNOLOGY_PATTERNS = [
    # AI & ML
    r'\b(?:ChatGPT|GPT-4|GPT-3|Claude|Gemini|DALL-E|Midjourney|Stable Diffusion|LLM|GenAI|Generative AI|Machine Learning|Deep Learning|Neural Network)\b',
    # Ad tech
    r'\b(?:CTV|OTT|AVOD|SVOD|FAST|programmatic|DSP|SSP|DMP|CDP|header bidding|prebid)\b',
    # Marketing tech
    r'\b(?:attribution|measurement|personalization|optimization|A/B testing|multivariate testing|journey orchestration)\b',
    # Emerging tech
    r'\b(?:blockchain|Web3|metaverse|VR|AR|XR|NFT|cryptocurrency|Bitcoin|Ethereum)\b',
    # Platforms & tools
    r'\b(?:Google Analytics|Google Ads|Facebook Ads|Instagram Ads|TikTok Ads|Snapchat Ads|Pinterest Ads)\b',
]

PEOPLE_PATTERNS = [
    # Common exec titles that might be missed (capturing group for the name)
    r'\b([A-Z][a-z]+ [A-Z][a-z]+)(?:\s+(?:CEO|CMO|CTO|CFO|COO|VP|SVP|EVP|President|Director|Manager))\b',
]

PRODUCT_PATTERNS = [
    # Tech products
    r'\b(?:iPhone|iPad|Mac|MacBook|AirPods|Apple Watch|Vision Pro|Surface|Xbox|PlayStation|Quest|Oculus)\b',
    # Platforms
    r'\b(?:AWS|Azure|Google Cloud|GCP|Salesforce Platform|Adobe Experience Cloud)\b',
    # Software
    r'\b(?:Photoshop|Illustrator|Premiere|After Effects|Figma|Canva|Slack|Teams|Zoom)\b',
]

# Metrics & KPIs
METRICS_PATTERNS = [
    r'\b(?:ROI|ROAS|CTR|CPC|CPM|CPA|CPI|CPL|LTV|CAC|conversion rate|engagement rate|bounce rate|impressions|reach|frequency)\b',
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
            'metrics': set()
        }

        # Combine title and text (title gets processed separately for emphasis)
        full_text = f"{title} {title} {text}"  # Title appears twice for weight

        # Pattern-based extraction
        entities['brands'].update(self._extract_pattern(self.brand_regex, full_text))
        entities['agencies'].update(self._extract_pattern(self.agency_regex, full_text))
        entities['technologies'].update(self._extract_pattern(self.tech_regex, full_text))
        entities['products'].update(self._extract_pattern(self.product_regex, full_text))
        entities['metrics'].update(self._extract_pattern(self.metrics_regex, full_text))

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
