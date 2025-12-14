"""
AI-Powered YouTube Content Categorization System
Analyzes video titles and descriptions to determine if content is distracting for students
Uses multiple analysis techniques without external APIs for maximum accuracy
"""

import re
import string
from collections import Counter
from typing import Dict, List, Tuple, Optional
import math

class YouTubeContentAnalyzer:
    """
    Advanced AI system for categorizing YouTube content as educational or distracting
    Uses multiple analysis techniques including keyword analysis, sentiment detection,
    pattern recognition, and content scoring for maximum accuracy.
    """
    
    def __init__(self):
        # Educational keywords with weights (higher = more educational)
        self.educational_keywords = {
            # Academic subjects
            'tutorial': 0.9, 'lesson': 0.9, 'course': 0.9, 'lecture': 0.9,
            'learn': 0.8, 'study': 0.8, 'education': 0.9, 'academic': 0.9,
            'school': 0.7, 'university': 0.8, 'college': 0.8, 'student': 0.7,
            'teacher': 0.8, 'professor': 0.8, 'instructor': 0.8,
            
            # Programming & Technology
            'programming': 0.9, 'coding': 0.9, 'python': 0.8, 'javascript': 0.8,
            'java': 0.8, 'c++': 0.8, 'html': 0.7, 'css': 0.7, 'react': 0.7,
            'algorithm': 0.9, 'data structure': 0.9, 'software': 0.7,
            'development': 0.8, 'programming tutorial': 0.9, 'code': 0.8,
            
            # Science & Math
            'science': 0.8, 'physics': 0.8, 'chemistry': 0.8, 'biology': 0.8,
            'mathematics': 0.9, 'math': 0.8, 'calculus': 0.9, 'algebra': 0.8,
            'statistics': 0.8, 'research': 0.8, 'experiment': 0.7,
            'theory': 0.8, 'formula': 0.8, 'equation': 0.8,
            
            # Language & Literature
            'language': 0.7, 'grammar': 0.8, 'vocabulary': 0.7, 'writing': 0.7,
            'literature': 0.8, 'poetry': 0.7, 'essay': 0.8, 'reading': 0.7,
            'english': 0.7, 'spanish': 0.7, 'french': 0.7, 'german': 0.7,
            
            # History & Social Sciences
            'history': 0.8, 'historical': 0.8, 'documentary': 0.7,
            'politics': 0.7, 'economics': 0.8, 'philosophy': 0.8,
            'psychology': 0.8, 'sociology': 0.8, 'geography': 0.7,
            
            # Skills & Professional Development
            'skill': 0.7, 'training': 0.8, 'workshop': 0.8, 'seminar': 0.8,
            'certification': 0.8, 'career': 0.7, 'job': 0.6, 'interview': 0.7,
            'resume': 0.7, 'portfolio': 0.7, 'professional': 0.7,
            
            # Creative but Educational
            'art tutorial': 0.7, 'drawing': 0.6, 'painting': 0.6, 'design': 0.7,
            'music theory': 0.8, 'composition': 0.7, 'photography': 0.6,
            
            # How-to and DIY (educational context)
            'how to': 0.6, 'diy': 0.6, 'guide': 0.7, 'tips': 0.6,
            'tricks': 0.5, 'hack': 0.5, 'method': 0.7, 'technique': 0.7,
            
            # Academic Content Indicators
            'explanation': 0.8, 'analysis': 0.8, 'review': 0.6, 'summary': 0.7,
            'overview': 0.7, 'introduction': 0.7, 'basics': 0.7, 'fundamentals': 0.8,
            'advanced': 0.8, 'beginner': 0.7, 'intermediate': 0.7,
        }
        
        # Distracting keywords with weights (higher = more distracting)
        self.distracting_keywords = {
            # Entertainment & Gaming
            'game': 0.8, 'gaming': 0.9, 'play': 0.7, 'fun': 0.6, 'funny': 0.7,
            'comedy': 0.8, 'joke': 0.7, 'meme': 0.8, 'viral': 0.7,
            'entertainment': 0.8, 'funny moments': 0.9, 'fails': 0.8,
            'prank': 0.8, 'challenge': 0.7, 'reaction': 0.7,
            
            # Social Media & Lifestyle
            'vlog': 0.7, 'lifestyle': 0.6, 'daily': 0.6, 'routine': 0.5,
            'morning': 0.5, 'night': 0.5, 'day in my life': 0.7,
            'haul': 0.6, 'unboxing': 0.6, 'review': 0.5, 'try on': 0.6,
            
            # Music & Dance
            'music': 0.6, 'song': 0.6, 'dance': 0.7, 'dancing': 0.7,
            'cover': 0.6, 'remix': 0.6, 'mashup': 0.6, 'beat': 0.6,
            'lyrics': 0.5, 'music video': 0.7, 'concert': 0.6,
            
            # Sports & Fitness (can be distracting)
            'sports': 0.6, 'football': 0.6, 'basketball': 0.6, 'soccer': 0.6,
            'workout': 0.5, 'fitness': 0.5, 'gym': 0.5, 'exercise': 0.5,
            'highlight': 0.7, 'match': 0.6, 'game': 0.6,
            
            # Movies & TV
            'movie': 0.7, 'film': 0.7, 'trailer': 0.7, 'cinema': 0.7,
            'tv show': 0.7, 'series': 0.7, 'episode': 0.7, 'season': 0.7,
            'netflix': 0.7, 'disney': 0.6, 'marvel': 0.6, 'dc': 0.6,
            
            # Drama & Controversy
            'drama': 0.8, 'scandal': 0.9, 'controversy': 0.9, 'fight': 0.8,
            'argument': 0.8, 'beef': 0.8, 'exposed': 0.8, 'truth': 0.6,
            'revealed': 0.7, 'shocking': 0.8, 'crazy': 0.7,
            
            # Clickbait & Sensational
            'clickbait': 0.9, 'you won\'t believe': 0.9, 'shocking': 0.8,
            'amazing': 0.6, 'incredible': 0.6, 'unbelievable': 0.7,
            'mind blown': 0.8, 'this will change': 0.7, 'secret': 0.7,
            
            # Social Media Drama
            'tiktok': 0.7, 'instagram': 0.6, 'twitter': 0.6, 'facebook': 0.6,
            'youtube drama': 0.9, 'influencer': 0.7, 'celebrity': 0.7,
            
            # Time-wasting Content
            'satisfying': 0.6, 'oddly satisfying': 0.7, 'asmr': 0.6,
            'relaxing': 0.5, 'calming': 0.5, 'sleep': 0.5, 'meditation': 0.4,
            'background': 0.5, 'ambient': 0.5,
            
            # Food & Cooking (can be distracting)
            'cooking': 0.5, 'recipe': 0.5, 'food': 0.5, 'eating': 0.6,
            'mukbang': 0.7, 'taste test': 0.6, 'food review': 0.6,
            
            # Travel & Adventure
            'travel': 0.5, 'vacation': 0.6, 'trip': 0.5, 'adventure': 0.6,
            'explore': 0.5, 'journey': 0.5, 'destination': 0.5,
        }
        
        # Neutral keywords (don't strongly indicate either category)
        self.neutral_keywords = {
            'video': 0.0, 'channel': 0.0, 'subscribe': 0.0, 'like': 0.0,
            'comment': 0.0, 'share': 0.0, 'new': 0.0, 'latest': 0.0,
            'update': 0.0, 'news': 0.0, 'information': 0.0, 'content': 0.0,
        }
        
        # Patterns that indicate educational content
        self.educational_patterns = [
            r'\b(how to|tutorial|guide|lesson|course|learn|study)\b',
            r'\b(programming|coding|algorithm|data structure)\b',
            r'\b(math|mathematics|calculus|algebra|geometry)\b',
            r'\b(science|physics|chemistry|biology|research)\b',
            r'\b(education|academic|school|university|college)\b',
            r'\b(explanation|analysis|theory|formula|equation)\b',
            r'\b(beginner|intermediate|advanced|fundamentals)\b',
            r'\b(step by step|detailed|comprehensive)\b',
        ]
        
        # Patterns that indicate distracting content
        self.distracting_patterns = [
            r'\b(funny|comedy|joke|meme|viral)\b',
            r'\b(gaming|gameplay|play|fun)\b',
            r'\b(drama|scandal|controversy|fight)\b',
            r'\b(prank|challenge|reaction|fails)\b',
            r'\b(music video|song|dance|cover)\b',
            r'\b(movie|film|trailer|cinema)\b',
            r'\b(vlog|lifestyle|daily routine)\b',
            r'\b(clickbait|shocking|amazing|unbelievable)\b',
            r'\b(you won\'t believe|this will change|mind blown)\b',
        ]
        
        # Sentiment indicators
        self.positive_sentiment_words = [
            'amazing', 'awesome', 'incredible', 'fantastic', 'wonderful',
            'brilliant', 'excellent', 'perfect', 'great', 'good', 'best',
            'love', 'enjoy', 'fun', 'exciting', 'thrilling', 'amazing'
        ]
        
        self.negative_sentiment_words = [
            'terrible', 'awful', 'horrible', 'bad', 'worst', 'hate',
            'disgusting', 'stupid', 'dumb', 'boring', 'annoying',
            'frustrating', 'disappointing', 'sad', 'angry'
        ]
        
        # Content length thresholds
        self.min_description_length = 50
        self.max_title_length = 100
        
    def preprocess_text(self, text: str) -> str:
        """Clean and normalize text for analysis"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\-\.\,\!\?]', '', text)
        
        return text.strip()
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        text = self.preprocess_text(text)
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
            'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
        }
        
        words = text.split()
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords
    
    def calculate_keyword_score(self, text: str) -> Tuple[float, float]:
        """Calculate educational and distracting scores based on keywords"""
        keywords = self.extract_keywords(text)
        
        educational_score = 0.0
        distracting_score = 0.0
        
        for keyword in keywords:
            # Check educational keywords
            for edu_keyword, weight in self.educational_keywords.items():
                if keyword in edu_keyword or edu_keyword in keyword:
                    educational_score += weight
                    break
            
            # Check distracting keywords
            for dist_keyword, weight in self.distracting_keywords.items():
                if keyword in dist_keyword or dist_keyword in keyword:
                    distracting_score += weight
                    break
        
        # Normalize scores by number of keywords
        if keywords:
            educational_score /= len(keywords)
            distracting_score /= len(keywords)
        
        return educational_score, distracting_score
    
    def analyze_patterns(self, text: str) -> Tuple[float, float]:
        """Analyze text for educational and distracting patterns"""
        text = self.preprocess_text(text)
        
        educational_matches = 0
        distracting_matches = 0
        
        for pattern in self.educational_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                educational_matches += 1
        
        for pattern in self.distracting_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                distracting_matches += 1
        
        # Normalize by total possible patterns
        edu_pattern_score = educational_matches / len(self.educational_patterns)
        dist_pattern_score = distracting_matches / len(self.distracting_patterns)
        
        return edu_pattern_score, dist_pattern_score
    
    def analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment of the text"""
        text = self.preprocess_text(text)
        words = text.split()
        
        positive_count = sum(1 for word in words if word in self.positive_sentiment_words)
        negative_count = sum(1 for word in words if word in self.negative_sentiment_words)
        
        if not words:
            return 0.0
        
        # Calculate sentiment score (-1 to 1)
        sentiment_score = (positive_count - negative_count) / len(words)
        return sentiment_score
    
    def analyze_content_structure(self, title: str, description: str) -> Dict[str, float]:
        """Analyze content structure for educational indicators"""
        scores = {
            'has_description': 1.0 if description and len(description) > self.min_description_length else 0.0,
            'title_length_appropriate': 1.0 if len(title) <= self.max_title_length else 0.5,
            'description_length': min(len(description) / 200, 1.0) if description else 0.0,
            'has_educational_structure': 0.0,
        }
        
        # Check for educational content structure
        if description:
            desc_lower = description.lower()
            structure_indicators = [
                'introduction', 'overview', 'summary', 'conclusion',
                'chapter', 'section', 'part', 'step', 'method',
                'objective', 'goal', 'purpose', 'learning'
            ]
            
            structure_count = sum(1 for indicator in structure_indicators if indicator in desc_lower)
            scores['has_educational_structure'] = min(structure_count / 3, 1.0)
        
        return scores
    
    def calculate_final_score(self, title: str, description: str = "") -> Dict[str, float]:
        """Calculate final distraction score for the content"""
        # Combine title and description for analysis
        full_text = f"{title} {description}" if description else title
        
        # Get keyword scores
        edu_keyword_score, dist_keyword_score = self.calculate_keyword_score(full_text)
        
        # Get pattern scores
        edu_pattern_score, dist_pattern_score = self.analyze_patterns(full_text)
        
        # Get sentiment score
        sentiment_score = self.analyze_sentiment(full_text)
        
        # Get content structure scores
        structure_scores = self.analyze_content_structure(title, description)
        
        # Calculate weighted final scores
        educational_score = (
            edu_keyword_score * 0.4 +
            edu_pattern_score * 0.3 +
            structure_scores['has_educational_structure'] * 0.2 +
            structure_scores['has_description'] * 0.1
        )
        
        distracting_score = (
            dist_keyword_score * 0.4 +
            dist_pattern_score * 0.3 +
            abs(sentiment_score) * 0.2 +  # High sentiment (positive or negative) can be distracting
            (1 - structure_scores['title_length_appropriate']) * 0.1
        )
        
        # Calculate final distraction probability
        distraction_probability = distracting_score / (educational_score + distracting_score + 0.1)
        
        return {
            'educational_score': educational_score,
            'distracting_score': distracting_score,
            'distraction_probability': distraction_probability,
            'is_distracting': distraction_probability > 0.5,
            'confidence': abs(educational_score - distracting_score),
            'sentiment_score': sentiment_score,
            'structure_scores': structure_scores
        }
    
    def categorize_content(self, title: str, description: str = "") -> Dict[str, any]:
        """
        Main function to categorize YouTube content as distracting or educational
        
        Args:
            title (str): YouTube video title
            description (str): YouTube video description (optional)
            
        Returns:
            Dict containing categorization results and detailed analysis
        """
        if not title:
            return {
                'is_distracting': True,
                'confidence': 0.0,
                'reason': 'No title provided',
                'scores': {}
            }
        
        # Calculate scores
        scores = self.calculate_final_score(title, description)
        
        # Determine category
        is_distracting = scores['is_distracting']
        confidence = scores['confidence']
        
        # Generate reasoning
        reasoning = []
        if scores['educational_score'] > scores['distracting_score']:
            reasoning.append("Content appears educational based on keywords and patterns")
        else:
            reasoning.append("Content appears distracting based on keywords and patterns")
        
        if scores['sentiment_score'] > 0.3:
            reasoning.append("High positive sentiment may indicate entertainment content")
        elif scores['sentiment_score'] < -0.3:
            reasoning.append("Negative sentiment may indicate controversial content")
        
        if scores['structure_scores']['has_description']:
            reasoning.append("Detailed description suggests educational intent")
        else:
            reasoning.append("Lack of description may indicate entertainment content")
        
        return {
            'is_distracting': is_distracting,
            'confidence': confidence,
            'reasoning': reasoning,
            'scores': scores,
            'recommendation': 'BLOCK' if is_distracting else 'ALLOW',
            'educational_score': scores['educational_score'],
            'distracting_score': scores['distracting_score']
        }


def analyze_youtube_content(title: str, description: str = "") -> Dict[str, any]:
    """
    Convenience function to analyze YouTube content
    
    Args:
        title (str): YouTube video title
        description (str): YouTube video description (optional)
        
    Returns:
        Dict containing analysis results
    """
    analyzer = YouTubeContentAnalyzer()
    return analyzer.categorize_content(title, description)


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    test_cases = [
        {
            "title": "Python Programming Tutorial for Beginners",
            "description": "Learn Python programming from scratch with this comprehensive tutorial. We'll cover variables, loops, functions, and more."
        },
        {
            "title": "Funny Cat Videos Compilation 2024",
            "description": "The funniest cat videos that will make you laugh out loud! Watch these adorable cats doing silly things."
        },
        {
            "title": "Calculus 1: Introduction to Derivatives",
            "description": "In this educational video, we introduce the concept of derivatives in calculus. Perfect for students studying mathematics."
        },
        {
            "title": "EPIC Gaming Fails That Will Shock You",
            "description": "You won't believe these crazy gaming moments! Watch as players make hilarious mistakes in their favorite games."
        },
        {
            "title": "Machine Learning Algorithms Explained",
            "description": "A detailed explanation of various machine learning algorithms including linear regression, decision trees, and neural networks."
        }
    ]
    
    analyzer = YouTubeContentAnalyzer()
    
    print("YouTube Content Analysis Results:")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        result = analyzer.categorize_content(test_case["title"], test_case["description"])
        
        print(f"\nTest Case {i}:")
        print(f"Title: {test_case['title']}")
        print(f"Description: {test_case['description'][:100]}...")
        print(f"Result: {'DISTRACTING' if result['is_distracting'] else 'EDUCATIONAL'}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Educational Score: {result['educational_score']:.2f}")
        print(f"Distracting Score: {result['distracting_score']:.2f}")
        print(f"Reasoning: {'; '.join(result['reasoning'])}")
        print("-" * 30)
