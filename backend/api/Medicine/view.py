# api/Medicine/views.py
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from difflib import SequenceMatcher
import re

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from api.Medicine.model import Medicine
from .serializer import MedicineSerializer, MedicineSuggestionSerializer

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['dose']
    search_fields = ['medicine_name', 'full_description']
    

    # Medical synonyms and related terms
    MEDICAL_SYNONYMS = {
        'heart': ['cardiac', 'cardio', 'myocardium', 'palpitation', 'pulse', 'heartbeat', 'tachycardia', 'bradycardia'],
        'stomach': ['gastric', 'abdominal', 'belly', 'epigastric', 'digestive', 'pet', 'abdomen'],
        'pain': ['ache', 'discomfort', 'soreness', 'dard', 'painful'],
        'appetite': ['hunger', 'craving', 'food'],
        'eating': ['food', 'meal', 'diet'],
        'fever': ['pyrexia', 'temperature', 'bukhar', 'hot'],
        'weakness': ['fatigue', 'tired', 'exhaustion', 'debility', 'kamzori', 'weak'],
        'breathing': ['respiration', 'dyspnea', 'breathless', 'sob', 'dyspnoea'],
        'urine': ['urinary', 'urination', 'bladder', 'incontinence'],
        'liver': ['hepatic', 'hepato'],
        'sleep': ['insomnia', 'sleepless', 'wakeful', 'restless'],
        'nausea': ['vomiting', 'sick', 'queasy', 'eructations'],
        'sexual': ['impotency', 'libido', 'erectile', 'prostatic'],
        'cough': ['expectoration', 'sputum'],
        'chest': ['thoracic', 'lungs', 'respiratory'],
        'jaundice': ['yellow', 'icterus'],
        'breath': ['breathing', 'offensive'],
    }

    def _expand_with_synonyms(self, text):
        """Expand text with medical synonyms"""
        text_lower = text.lower()
        expanded = [text_lower]
        
        for key, synonyms in self.MEDICAL_SYNONYMS.items():
            if key in text_lower:
                expanded.extend(synonyms)
            for syn in synonyms:
                if syn in text_lower:
                    expanded.append(key)
                    expanded.extend(synonyms)
        
        return ' '.join(set(expanded))

    def _normalize_text(self, text):
        """Normalize text"""
        text = text.lower().strip()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    def _calculate_advanced_score(self, symptoms, description):
        """Advanced scoring with medical domain knowledge"""
        # Normalize
        symptom_text = self._normalize_text(' '.join(symptoms))
        desc_text = self._normalize_text(description)
        
        # Split into sections
        desc_first_sentence = desc_text.split('.')[0] if '.' in desc_text else desc_text[:150]
        desc_primary = desc_text[:250]
        
        symptom_words = set(symptom_text.split())
        desc_words = set(desc_text.split())
        desc_primary_words = set(desc_primary.split())
        desc_first_words = set(desc_first_sentence.split())
        
        # Stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'not', 'no', 'all'}
        symptom_words = symptom_words - stop_words
        desc_words = desc_words - stop_words
        desc_primary_words = desc_primary_words - stop_words
        desc_first_words = desc_first_words - stop_words
        
        if not symptom_words:
            return 0
        
        # Expand with synonyms for matching
        expanded_symptom_words = set()
        for word in symptom_words:
            expanded_symptom_words.add(word)
            for key, synonyms in self.MEDICAL_SYNONYMS.items():
                if word == key or word in synonyms:
                    expanded_symptom_words.add(key)
                    expanded_symptom_words.update(synonyms)
        
        # Score components
        score = 0
        
        # 1. First sentence match (HIGHEST PRIORITY) - 40 points
        first_sentence_matches = expanded_symptom_words & desc_first_words
        if first_sentence_matches:
            score += 40 * (len(first_sentence_matches) / len(symptom_words))
        
        # 2. Primary section match (first 250 chars) - 30 points
        primary_matches = expanded_symptom_words & desc_primary_words
        if primary_matches:
            score += 30 * (len(primary_matches) / len(symptom_words))
        
        # 3. Exact keyword matches in full description - 20 points
        exact_matches = symptom_words & desc_words
        if exact_matches:
            score += 20 * (len(exact_matches) / len(symptom_words))
        
        # 4. Synonym matches in full description - 15 points
        synonym_matches = expanded_symptom_words & desc_words
        if synonym_matches:
            score += 15 * (len(synonym_matches) / len(symptom_words))
        
        # 5. Partial word matching - 10 points
        partial_count = 0
        for s_word in symptom_words:
            if len(s_word) < 4:
                continue
            for d_word in desc_words:
                if len(d_word) < 4:
                    continue
                if s_word in d_word or d_word in s_word:
                    partial_count += 1
                    break
        if partial_count > 0:
            score += 10 * (partial_count / len(symptom_words))
        
        # 6. Fuzzy matching for typos - 5 points
        fuzzy_count = 0
        for s_word in symptom_words:
            if len(s_word) < 4:
                continue
            for d_word in desc_words:
                if len(d_word) < 4:
                    continue
                ratio = SequenceMatcher(None, s_word, d_word).ratio()
                if ratio > 0.85:
                    fuzzy_count += 1
                    break
        if fuzzy_count > 0:
            score += 5 * (fuzzy_count / len(symptom_words))
        
        return min(score, 100)

    @action(detail=False, methods=["post"], url_path="suggest")
    def suggest_medicine(self, request):
        serializer = MedicineSuggestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        symptoms = serializer.validated_data["symptoms"]
        all_medicines = Medicine.objects.all()
        
        if not all_medicines.exists():
            return Response({"message": "No medicines available in database"})
        
        # Calculate scores
        medicine_scores = []
        for med in all_medicines:
            score = self._calculate_advanced_score(symptoms, med.full_description)
            
            if score > 10:  # Threshold for relevance
                medicine_scores.append({
                    "medicine_id": str(med.id),
                    "medicine_name": med.medicine_name,
                    "confidence": min(int(score), 100),
                    "description_preview": med.full_description[:150] + "..."
                })
        
        # Sort by confidence
        medicine_scores.sort(key=lambda x: x["confidence"], reverse=True)
        
        return Response({
            "input_symptoms": symptoms,
            "results": medicine_scores[:5],
            "total_found": len(medicine_scores)
        })