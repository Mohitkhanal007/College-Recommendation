# College Recommendation Module

import json
import math
from typing import List, Dict, Tuple

class CollegeRecommender:
    def __init__(self, colleges_file: str):
        # Initialize the recommender with college data
        with open(colleges_file, 'r', encoding='utf-8') as f:
            self.colleges = json.load(f)
        
        self._build_vocabulary()
        
        # Feature weights for matching
        self.feature_weights = {
            'program': 6.0,
            'stream': 3.0,
            'location': 4.0,
            'budget': 0.8,
            'gpa': 0.5
        }
    
    def _build_vocabulary(self):
        # Build vocabulary of features from colleges
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
    
    def _normalize_gpa(self, gpa: float) -> float:
        # Normalize GPA to 0-1 scale
        return min(max(gpa / 4.0, 0.0), 1.0)
    
    def _preprocess_user_input(self, user_profile: Dict) -> Dict:
        # Validate and standardize user inputs
        processed = user_profile.copy()
        
        # Normalize GPA
        if 'gpa' in processed:
            processed['gpa'] = float(processed['gpa'])
        
        # Standardize text fields
        for field in ['stream', 'preferred_program', 'location', 'budget_range']:
            if field in processed and processed[field]:
                processed[field] = str(processed[field]).strip()
        
        # Handle optional fields
        processed['interests'] = processed.get('interests', '').strip()
        processed['career_goals'] = processed.get('career_goals', '').strip()
        
        return processed
    
    def _handle_missing_data(self, user_profile: Dict) -> Dict:
        # Provide defaults for missing optional fields
        defaults = {
            'interests': '',
            'career_goals': '',
            'top_n': 5
        }
        
        for key, default_value in defaults.items():
            if key not in user_profile or not user_profile[key]:
                user_profile[key] = default_value
        
        return user_profile
    
    def _college_to_vector(self, college: Dict) -> List[float]:
        # Convert college to feature vector
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
        # Convert user profile to feature vector
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
        # Calculate similarity between two vectors
        weighted_vec1 = [v * w for v, w in zip(vec1, weights)]
        weighted_vec2 = [v * w for v, w in zip(vec2, weights)]
        
        dot_product = sum(a * b for a, b in zip(weighted_vec1, weighted_vec2))
        magnitude1 = math.sqrt(sum(a * a for a in weighted_vec1))
        magnitude2 = math.sqrt(sum(a * a for a in weighted_vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def _calculate_confidence(self, similarity: float, matched_features: Dict) -> float:
        # Calculate confidence score
        base_confidence = similarity
        
        if matched_features.get('program', False):
            base_confidence += 0.1
        if matched_features.get('stream', False):
            base_confidence += 0.08
        if matched_features.get('location', False):
            base_confidence += 0.15
        
        return min(1.0, base_confidence)
    
    def _analyze_feature_matches(self, college: Dict, user_profile: Dict) -> Dict:
        # Check which features match
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
        # Filter colleges by GPA requirement
        filtered = []
        for college in colleges:
            if user_gpa >= college['min_gpa']:
                filtered.append(college)
        return filtered
    
    def _generate_explanation(self, college: Dict, user_profile: Dict, similarity: float, matches: Dict) -> str:
        # Generate explanation for recommendation
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
        # Main recommendation function with preprocessing
        user_profile = self._preprocess_user_input(user_profile)
        user_profile = self._handle_missing_data(user_profile)
        
        user_gpa = float(user_profile.get('gpa', 0))
        eligible_colleges = self._filter_by_gpa(self.colleges, user_gpa)
        
        if not eligible_colleges:
            return []
        
        # Filter colleges by preferred program
        preferred_program = user_profile.get('preferred_program', '').lower().strip()
        if preferred_program:
            program_filtered = []
            for college in eligible_colleges:
                college_programs = [p.lower() for p in college['programs']]
                program_match = any(
                    preferred_program == cp or
                    f" {preferred_program} " in f" {cp} " or
                    (len(preferred_program) > 3 and preferred_program in cp)
                    for cp in college_programs
                )
                if program_match:
                    program_filtered.append(college)
            
            eligible_colleges = program_filtered
        
        user_vector = self._user_to_vector(user_profile)
        
        college_scores = []
        for college in eligible_colleges:
            college_vector, weights = self._college_to_vector(college)
            similarity = self._weighted_cosine_similarity(user_vector, college_vector, weights)
            
            matches = self._analyze_feature_matches(college, user_profile)
            
            confidence = self._calculate_confidence(similarity, matches)
            
            feature_scores = {
                'program_match': 1.0 if matches['program'] else 0.0,
                'stream_match': 1.0 if matches['stream'] else 0.0,
                'location_match': 1.0 if matches['location'] else 0.0,
                'budget_match': 1.0 if matches['budget'] else 0.0,
            }
            
            score_multiplier = 1.0
            if matches['program']:
                score_multiplier *= 2.0
            
            if matches['location']:
                score_multiplier *= 2.0
            
            college_scores.append({
                'college': college,
                'similarity': similarity,
                'confidence': confidence,
                'matches': matches,
                'feature_scores': feature_scores,
                'score': similarity * confidence * score_multiplier
            })
        
        college_scores.sort(key=lambda x: x['score'], reverse=True)
        
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
        # Compare multiple colleges
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
        # Get statistics about colleges
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
