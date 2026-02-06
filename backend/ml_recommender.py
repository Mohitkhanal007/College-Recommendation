"""
Enhanced Machine Learning Recommendation Module
Uses content-based filtering with weighted features and confidence scoring
"""

import json
import math
from typing import List, Dict, Tuple

class CollegeRecommender:
    def __init__(self, colleges_file: str):
        """
        Initialize the recommender with college data
        """
        with open(colleges_file, 'r', encoding='utf-8') as f:
            self.colleges = json.load(f)
        
        # Build feature vocabulary from all colleges
        self._build_vocabulary()
        
        # Feature weights - higher weight means more important
        # These weights help prioritize certain features in recommendations
        self.feature_weights = {
            'program': 6.0,      # CRITICAL - program match (increased further)
            'stream': 3.0,       # Very important - stream requirement
            'location': 4.0,     # INCREASED - Location is now a strong factor
            'budget': 0.8,       # Less important - budget
            'gpa': 0.5           # Less weight (already filtered)
        }
    
    def _build_vocabulary(self):
        """
        Build vocabulary of all possible features from colleges
        This helps us create consistent feature vectors
        """
        self.all_programs = set()
        self.all_streams = set()
        self.all_locations = set()
        self.all_budget_ranges = set()
        self.all_career_focus = set()
        self.all_interests = set()
        
        for college in self.colleges:
            self.all_programs.update(college['programs'])
            self.all_streams.update(college['streams'])
            self.all_locations.add(college['location'])
            self.all_budget_ranges.add(college['budget_range'])
            self.all_career_focus.update(college['career_focus'])
            self.all_interests.update(college['interests'])
        
        # Convert to sorted lists for consistent indexing
        self.all_programs = sorted(list(self.all_programs))
        self.all_streams = sorted(list(self.all_streams))
        self.all_locations = sorted(list(self.all_locations))
        self.all_budget_ranges = sorted(list(self.all_budget_ranges))
    
    def _college_to_vector(self, college: Dict) -> List[float]:
        """
        Convert a college into a weighted feature vector
        Each dimension represents a feature with appropriate weight
        """
        vector = []
        weights = []
        
        # Program features (weighted)
        for program in self.all_programs:
            val = 1.0 if program in college['programs'] else 0.0
            vector.append(val)
            weights.append(self.feature_weights['program'])
        
        # Stream features (weighted)
        for stream in self.all_streams:
            val = 1.0 if stream in college['streams'] else 0.0
            vector.append(val)
            weights.append(self.feature_weights['stream'])
        
        # Location feature (weighted)
        for location in self.all_locations:
            val = 1.0 if location == college['location'] else 0.0
            vector.append(val)
            weights.append(self.feature_weights['location'])
        
        # Budget range (weighted)
        for budget in self.all_budget_ranges:
            val = 1.0 if budget == college['budget_range'] else 0.0
            vector.append(val)
            weights.append(self.feature_weights['budget'])
        
        # GPA requirement (normalized and weighted)
        gpa_score = college['min_gpa'] / 4.0
        vector.append(gpa_score)
        weights.append(self.feature_weights['gpa'])
        
        return vector, weights
    
    def _user_to_vector(self, user_profile: Dict) -> List[float]:
        """
        Convert user profile into a feature vector
        Same structure as college vector for comparison
        """
        vector = []
        
        # Program features - user's preferred program gets weight 1.0
        preferred_program = user_profile.get('preferred_program', '')
        for program in self.all_programs:
            if preferred_program.lower() in program.lower() or program.lower() in preferred_program.lower():
                vector.append(1.0)
            else:
                vector.append(0.0)
        
        # Stream features
        user_stream = user_profile.get('stream', '')
        for stream in self.all_streams:
            vector.append(1.0 if stream.lower() == user_stream.lower() else 0.0)
        
        # Location feature
        user_location = user_profile.get('location', '')
        for location in self.all_locations:
            if user_location.lower() == 'any' or user_location.lower() in location.lower() or location.lower() in user_location.lower():
                vector.append(1.0)
            else:
                vector.append(0.0)
        
        # Budget range
        user_budget = user_profile.get('budget_range', '')
        for budget in self.all_budget_ranges:
            vector.append(1.0 if budget.lower() == user_budget.lower() else 0.0)
        
        # GPA (normalized)
        user_gpa = float(user_profile.get('gpa', 0))
        gpa_score = user_gpa / 4.0
        vector.append(gpa_score)
        
        return vector
    
    def _weighted_cosine_similarity(self, vec1: List[float], vec2: List[float], weights: List[float]) -> float:
        """
        Calculate weighted cosine similarity between two vectors
        Features with higher weights contribute more to similarity
        """
        # Apply weights to both vectors
        weighted_vec1 = [v * w for v, w in zip(vec1, weights)]
        weighted_vec2 = [v * w for v, w in zip(vec2, weights)]
        
        dot_product = sum(a * b for a, b in zip(weighted_vec1, weighted_vec2))
        magnitude1 = math.sqrt(sum(a * a for a in weighted_vec1))
        magnitude2 = math.sqrt(sum(a * a for a in weighted_vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def _calculate_confidence(self, similarity: float, matched_features: Dict) -> float:
        """
        Calculate confidence score based on similarity and feature matches
        Higher confidence means more reliable recommendation
        """
        base_confidence = similarity
        
        # Boost confidence for critical matches
        if matched_features.get('program', False):
            base_confidence += 0.1
        if matched_features.get('stream', False):
            base_confidence += 0.08
        if matched_features.get('location', False):
            base_confidence += 0.15 # Increased confidence for location
        
        # Cap at 1.0
        return min(1.0, base_confidence)
    
    def _analyze_feature_matches(self, college: Dict, user_profile: Dict) -> Dict:
        """
        Analyze which features match between college and user profile
        Returns dictionary of matched features
        """
        matches = {
            'program': False,
            'stream': False,
            'location': False,
            'budget': False,
            'gpa_eligible': False
        }
        
        # Program match
        preferred_program = user_profile.get('preferred_program', '').lower()
        college_programs = [p.lower() for p in college['programs']]
        matches['program'] = any(preferred_program in p or p in preferred_program for p in college_programs)
        
        # Stream match
        user_stream = user_profile.get('stream', '').lower()
        matches['stream'] = user_stream in [s.lower() for s in college['streams']]
        
        # Location match
        user_location = user_profile.get('location', '').lower()
        if user_location == 'any' or user_location in college['location'].lower():
            matches['location'] = True
        
        # Budget match
        user_budget = user_profile.get('budget_range', '').lower()
        matches['budget'] = user_budget == college['budget_range'].lower()
        
        # GPA eligibility
        user_gpa = float(user_profile.get('gpa', 0))
        matches['gpa_eligible'] = user_gpa >= college['min_gpa']
        
        return matches
    
    def _filter_by_gpa(self, colleges: List[Dict], user_gpa: float) -> List[Dict]:
        """
        Filter out colleges where user's GPA is below minimum requirement
        """
        filtered = []
        for college in colleges:
            if user_gpa >= college['min_gpa']:
                filtered.append(college)
        return filtered
    
    def _generate_explanation(self, college: Dict, user_profile: Dict, similarity: float, matches: Dict) -> str:
        """
        Generate detailed human-readable explanation for why a college was recommended
        """
        reasons = []
        
        if matches['program']:
            reasons.append(f"offers your preferred program")
        
        if matches['stream']:
            reasons.append(f"accepts students from {user_profile.get('stream')} stream")
        
        if matches['location']:
            reasons.append(f"located in {college['location']}")
        
        if matches['budget']:
            reasons.append(f"fits your {college['budget_range']} budget range")
        
        if matches['gpa_eligible']:
            user_gpa = float(user_profile.get('gpa', 0))
            reasons.append(f"your GPA ({user_gpa}) meets requirement ({college['min_gpa']})")
        
        if not reasons:
            reasons.append("has some similarity with your profile")
        
        explanation = f"This college was recommended because it {reasons[0]}"
        if len(reasons) > 1:
            explanation += f", and it also {', '.join(reasons[1:])}"
        
        return explanation
    
    def recommend(self, user_profile: Dict, top_n: int = 5) -> List[Dict]:
        """
        Main recommendation function with enhanced scoring
        Returns top N colleges matching user profile with detailed analysis
        """
        # Filter by GPA first
        user_gpa = float(user_profile.get('gpa', 0))
        eligible_colleges = self._filter_by_gpa(self.colleges, user_gpa)
        
        if not eligible_colleges:
            return []
        
        # STRICT FILTER: Only include colleges that offer the preferred program
        preferred_program = user_profile.get('preferred_program', '').lower().strip()
        if preferred_program:
            program_filtered = []
            for college in eligible_colleges:
                college_programs = [p.lower() for p in college['programs']]
                # Check if preferred program matches any college program
                # FIX: Removed 'cp in preferred_program' to prevent "BBS" matching "MBBS"
                program_match = any(
                    preferred_program == cp or  # Exact match
                    f" {preferred_program} " in f" {cp} " or # Word match
                    (len(preferred_program) > 3 and preferred_program in cp) # Substring match only for longer queries
                    for cp in college_programs
                )
                if program_match:
                    program_filtered.append(college)
            
            # If we requested a specific program, ONLY show colleges with that program
            # Do NOT fall back to generic suggestions if specific intent is clear
            eligible_colleges = program_filtered
        
        # Convert user profile to vector
        user_vector = self._user_to_vector(user_profile)
        
        # Calculate similarity for each college
        college_scores = []
        for college in eligible_colleges:
            college_vector, weights = self._college_to_vector(college)
            similarity = self._weighted_cosine_similarity(user_vector, college_vector, weights)
            
            # Analyze feature matches
            matches = self._analyze_feature_matches(college, user_profile)
            
            # Calculate confidence
            confidence = self._calculate_confidence(similarity, matches)
            
            # Calculate match percentage for each feature category
            feature_scores = {
                'program_match': 1.0 if matches['program'] else 0.0,
                'stream_match': 1.0 if matches['stream'] else 0.0,
                'location_match': 1.0 if matches['location'] else 0.0,
                'budget_match': 1.0 if matches['budget'] else 0.0,
            }
            
            # Boost score for critical matches
            score_multiplier = 1.0
            if matches['program']:
                score_multiplier *= 2.0  # Double the score if program matches
            
            if matches['location']:
                score_multiplier *= 2.0  # Double the score if location matches (STRONG BOOST)
            
            college_scores.append({
                'college': college,
                'similarity': similarity,
                'confidence': confidence,
                'matches': matches,
                'feature_scores': feature_scores,
                'score': similarity * confidence * score_multiplier  # Combined score with multipliers
            })
        
        # Sort by combined score (descending)
        college_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Get top N and add detailed information
        recommendations = []
        for item in college_scores[:top_n]:
            college = item['college'].copy()
            college['similarity_score'] = round(item['similarity'], 3)
            college['confidence_score'] = round(item['confidence'], 3)
            college['combined_score'] = round(item['score'], 3)
            college['feature_matches'] = item['matches']
            college['feature_scores'] = item['feature_scores']
            college['explanation'] = self._generate_explanation(
                college, user_profile, item['similarity'], item['matches']
            )
            recommendations.append(college)
        
        return recommendations
    
    def compare_colleges(self, college_ids: List[int]) -> Dict:
        """
        Compare multiple colleges side by side
        Returns comparison data
        """
        selected_colleges = [c for c in self.colleges if c['id'] in college_ids]
        
        if not selected_colleges:
            return {'error': 'No colleges found'}
        
        comparison = {
            'colleges': selected_colleges,
            'common_features': {},
            'differences': {}
        }
        
        # Find common programs
        if len(selected_colleges) > 0:
            common_programs = set(selected_colleges[0]['programs'])
            for college in selected_colleges[1:]:
                common_programs &= set(college['programs'])
            comparison['common_features']['programs'] = list(common_programs)
        
        return comparison
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the college dataset
        """
        stats = {
            'total_colleges': len(self.colleges),
            'by_location': {},
            'by_budget': {},
            'by_stream': {},
            'programs_count': len(self.all_programs),
            'average_min_gpa': 0.0
        }
        
        total_gpa = 0
        for college in self.colleges:
            # Location stats
            loc = college['location']
            stats['by_location'][loc] = stats['by_location'].get(loc, 0) + 1
            
            # Budget stats
            budget = college['budget_range']
            stats['by_budget'][budget] = stats['by_budget'].get(budget, 0) + 1
            
            # Stream stats
            for stream in college['streams']:
                stats['by_stream'][stream] = stats['by_stream'].get(stream, 0) + 1
            
            total_gpa += college['min_gpa']
        
        stats['average_min_gpa'] = round(total_gpa / len(self.colleges), 2)
        
        return stats
