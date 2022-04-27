from typing import Protocol, List, Dict

Eliise_Rules = Dict[int, Dict[str, List[str]]]
"""Dict[rank, Dict[regex pattern, List[response templates]]]"""

## Protocols
class ELTokenizer(Protocol):
    def tokenized(self, message: str) -> List[str]:  # type: ignore (silence Pylance)
        """Return a list of tokens/words."""

class ELVerbReflector(Protocol):
    def reflect_verbs(self, word_list: List[str]) -> List[str]: # type: ignore
        """Return a list of reflected verbs (e.g. sg. 1 act. -> sg. 2 act.)."""

class ELPronounReflector(Protocol):
    def reflect_pronouns(self,
                         word_list: List[str]) -> List[str]:  # type: ignore
        """ Return a list of reflected pronouns (e.g. sg. 1 -> sg. 2)."""

class ELDecompBrain(Protocol):
    def eliise_rules(self) -> Eliise_Rules: # type: ignore
        """ Returns ranked regex patterns to match in the text, and response templates for each pattern."""
        
    def ordered_ranks(self) -> List[int]: # type: ignore
        """ Returns a list of the possible ranks of the regex patterns, highest ranks first."""

class ELReflectedContentTrimmer(Protocol):
    def shortened_content_to_reflect(self, content: str) -> str: # type: ignore
        """ Returns a shortened string with some clauses cut."""

## Default implementations
# Empty implementation of ELVerbReflector languages like English where we do not need to reflect 
# verbs other than the copula.
class ELDefaultVerbReflector:
    def reflect_verbs(self, word_list: List[str]) -> List[str]: 
        return word_list