import re
from typing import Dict, Any, List, Optional

class ToneAnalyzer:
    # Tone categories with associated keywords
    TONE_KEYWORDS = {
        "Informative": [
            "learn", "discover", "understand", "explain", "guide", 
            "tutorial", "how to", "tips", "facts", "knowledge",
            "comprehensive", "detailed", "instruction"
        ],
        "Entertaining": [
            "fun", "laugh", "crazy", "hilarious", "entertainment",
            "amusing", "comedy", "funny", "humor", "prank", "joke",
            "parody", "satire", "entertainment"
        ],
        "Inspirational": [
            "motivate", "inspire", "dream", "achieve", "success",
            "journey", "overcome", "story", "inspiration", "transformation",
            "personal development", "growth", "empower"
        ],
        "Educational": [
            "study", "education", "school", "college", "university",
            "lecture", "academic", "research", "science", "mathematics",
            "history", "analysis", "experiment", "theory"
        ],
        "Persuasive": [
            "convince", "review", "recommend", "best", "worst",
            "should", "opinion", "versus", "vs", "compare", "comparison",
            "debate", "argument", "perspective"
        ],
        "Professional": [
            "business", "industry", "professional", "corporate", "career",
            "job", "interview", "workplace", "strategy", "management",
            "leadership", "entrepreneur", "startup", "innovation"
        ],
        "Casual": [
            "chat", "hangout", "vlog", "day in the life", "chill",
            "relaxed", "informal", "personal", "lifestyle", "everyday",
            "routine", "casual", "laid-back", "conversational" 
        ],
        "Dramatic": [
            "shocking", "dramatic", "unbelievable", "never", "ever",
            "incredible", "amazing", "mind-blowing", "intense", "emotional",
            "revelation", "unexpected", "surprise", "suspense"
        ],
        "Thoughtful": [
            "reflection", "perspective", "thoughts", "opinion", "contemplation",
            "philosophy", "meaning", "purpose", "life", "existential",
            "deep", "thoughtful", "insightful", "wisdom"
        ]
    }
    
    def analyze_channel_tone(self, channel_data: Dict[str, Any]) -> str:
        """
        Analyze channel content to determine predominant tone.
        Returns the tone name as a string.
        """
        if not channel_data:
            return "Informative"  # Default fallback
            
        # Collect text from various sources to analyze
        text_sources = [
            channel_data.get('title', ''),
            channel_data.get('description', ''),
            channel_data.get('keywords', '')
        ]
        
        # Add video titles and descriptions
        for video in channel_data.get('videos', []):
            text_sources.append(video.get('title', ''))
            text_sources.append(video.get('description', ''))
            
        combined_text = ' '.join(text_sources).lower()
        
        # Count occurrences of tone keywords
        tone_scores = {}
        for tone, keywords in self.TONE_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                # Count occurrences of each keyword
                score += len(re.findall(rf'\b{re.escape(keyword)}\b', combined_text))
            tone_scores[tone] = score
        
        # Determine predominant tone based on keyword frequency
        if not tone_scores or max(tone_scores.values(), default=0) == 0:
            return "Informative"  # Default if no matches
            
        # Get tone with highest score
        predominant_tone = max(tone_scores.items(), key=lambda x: x[1])[0]
        return predominant_tone
    
    def get_secondary_tones(self, channel_data: Dict[str, Any], count: int = 2) -> List[str]:
        """
        Get secondary tones that complement the primary tone.
        Returns a list of tone names.
        """
        if not channel_data:
            return ["Conversational"]  # Default fallback
        
        # Collect text from various sources to analyze
        text_sources = [
            channel_data.get('title', ''),
            channel_data.get('description', ''),
            channel_data.get('keywords', '')
        ]
        
        # Add video titles and descriptions
        for video in channel_data.get('videos', []):
            text_sources.append(video.get('title', ''))
            text_sources.append(video.get('description', ''))
            
        combined_text = ' '.join(text_sources).lower()
        
        # Count occurrences of tone keywords
        tone_scores = {}
        for tone, keywords in self.TONE_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                # Count occurrences of each keyword
                score += len(re.findall(rf'\b{re.escape(keyword)}\b', combined_text))
            tone_scores[tone] = score
        
        # Sort tones by score in descending order
        sorted_tones = sorted(tone_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get top N tones excluding the main one
        return [tone for tone, _ in sorted_tones[1:count+1]]