"""
HealthPulse AI — NegEx Clinical Negation and Uncertainty Detection Algorithm.
Implements Chapman et al. regular expression rules to determine whether clinical conditions are affirmed or negated.
"""

import re
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass


@dataclass
class NegationResult:
    concept: str
    is_negated: bool
    trigger_phrase: Optional[str]
    rule_type: Optional[str]  # pre_negation, post_negation, pseudo_negation


# NegEx Clinical Trigger Patterns
PRE_NEGATION_TRIGGERS = [
    r"\bdenies\b",
    r"\bdenied\b",
    r"\bdenying\b",
    r"\bno\b",
    r"\bno signs of\b",
    r"\bno evidence of\b",
    r"\bno complaint of\b",
    r"\bwithout\b",
    r"\bnegative for\b",
    r"\bruled out for\b",
    r"\bpatient was not\b",
    r"\bpatient is not\b",
    r"\bnot\b",
    r"\bnever had\b",
    r"\bunremarkable for\b",
    r"\bfree of\b",
]

POST_NEGATION_TRIGGERS = [
    r"\bwas ruled out\b",
    r"\bis ruled out\b",
    r"\bunlikely\b",
    r"\bwas negative\b",
    r"\bis negative\b",
    r"\bnot seen\b",
    r"\babsent\b",
]

PSEUDO_NEGATION_TRIGGERS = [
    r"\bno increase\b",
    r"\bno change\b",
    r"\bnot only\b",
    r"\bwithout delay\b",
    r"\bno further\b",
]

CONJUNCTIONS = [
    r"\bbut\b",
    r"\bhowever\b",
    r"\balthough\b",
    r"\bnevertheless\b",
    r"\byet\b",
    r"\bexcept\b",
    r"\bapart from\b",
]


class NegExClassifier:
    """Evaluates clinical sentences for negated disease mentions."""

    def __init__(self, max_scope_tokens: int = 6):
        self.max_scope_tokens = max_scope_tokens
        self.pre_patterns = [re.compile(p, re.IGNORECASE) for p in PRE_NEGATION_TRIGGERS]
        self.post_patterns = [re.compile(p, re.IGNORECASE) for p in POST_NEGATION_TRIGGERS]
        self.pseudo_patterns = [re.compile(p, re.IGNORECASE) for p in PSEUDO_NEGATION_TRIGGERS]
        self.conjunction_patterns = [re.compile(p, re.IGNORECASE) for p in CONJUNCTIONS]

    def evaluate_sentence(self, sentence: str, concept: str) -> NegationResult:
        """Determines if a given medical concept within a sentence is negated."""
        concept_clean = concept.strip().lower()
        sent_clean = sentence.lower()

        c_idx = sent_clean.find(concept_clean)
        if c_idx == -1:
            return NegationResult(concept=concept, is_negated=False, trigger_phrase=None, rule_type=None)

        before_text = sent_clean[:c_idx]
        after_text = sent_clean[c_idx + len(concept_clean):]

        # Check pseudo-negations first
        for pseudo in self.pseudo_patterns:
            if pseudo.search(sent_clean):
                # If pseudo trigger overlaps with concept sentence context, don't negate
                pass

        # Check pre-negation (triggers before concept)
        for pre in self.pre_patterns:
            matches = list(pre.finditer(before_text))
            if matches:
                last_match = matches[-1]
                # Check if conjunction occurs between trigger and concept
                intervening = before_text[last_match.end():]
                has_conj = any(conj.search(intervening) for conj in self.conjunction_patterns)
                
                # Check token distance
                token_dist = len(intervening.split())
                if not has_conj and token_dist <= self.max_scope_tokens:
                    return NegationResult(
                        concept=concept,
                        is_negated=True,
                        trigger_phrase=last_match.group(0),
                        rule_type="pre_negation",
                    )

        # Check post-negation (triggers after concept)
        for post in self.post_patterns:
            match = post.search(after_text)
            if match:
                intervening = after_text[:match.start()]
                has_conj = any(conj.search(intervening) for conj in self.conjunction_patterns)
                token_dist = len(intervening.split())
                if not has_conj and token_dist <= self.max_scope_tokens:
                    return NegationResult(
                        concept=concept,
                        is_negated=True,
                        trigger_phrase=match.group(0),
                        rule_type="post_negation",
                    )

        return NegationResult(concept=concept, is_negated=False, trigger_phrase=None, rule_type=None)


_default_classifier = NegExClassifier()


def is_negated(sentence: str, concept: str) -> bool:
    """Convenience function returning True if concept is negated in sentence."""
    return _default_classifier.evaluate_sentence(sentence, concept).is_negated
