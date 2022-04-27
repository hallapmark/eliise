from doctest import run_docstring_examples
from multiprocessing.sharedctypes import Value
import re
from elprotocols import *
from typing import List, Match, ItemsView, Optional

# Eliise class
# TODO Steve grumette eliza 1983
# TODO Reinflection task. Check what's goin on under the hood. 
# TODO NB in the final paper talk a bit about how the reinflection works.

class ELResponse:
    def __init__(self,
                 response: str,
                 match: Optional[Match[str]]):
        self.response = response
        self.match = match

class Eliise:
    def __init__(self,
                 decomp_brain: ELDecompBrain,
                 tokenizer: ELTokenizer,
                 verb_reflector: ELVerbReflector,
                 pronoun_reflector: ELPronounReflector,
                 content_trimmer: ELReflectedContentTrimmer):
        self._decomp_brain = decomp_brain
        self._tokenizer = tokenizer
        self._verb_reflector = verb_reflector
        self._pronoun_reflector = pronoun_reflector
        self._content_trimmer = content_trimmer
        # { pattern: index of response to use for pattern next time }
        self._response_memdict: Dict[str, int] = {} 

    ## Public methods ##
    # Get a response from the chatbot
    def respond(self, message) -> str:
        # TODO: Parametrize content_trimmer
        return self._transform(message, self._decomp_brain, self._response_memdict)

    ## Private methods ##
    def _transform(self,
                   message: str,
                   decomp_brain: ELDecompBrain,
                   response_memdict: Dict[str, int]) -> str:
        """ Create a response by transforming the user's input message 
        according to a dictionary of rules."""
        print()
        print(f"User: {message}")
        response = self._response_template_for_message(message, decomp_brain, response_memdict)
        response_str = response.response
        # We plug in a reflection of what the user said
        if response.match and '{0}' in response_str:
            try:
                reflection = self._reflect_content(response.match)
            except IndexError:
                print("indexerror") # TODO: get rid of print statement
                pass
                # We will get this error if we have indicated in our recomposition 
                # rule that we expect to reflect something in the content, but the 
                # decomposition rule does not capture a corresponding group 
                # (this would be an error in the decomp_brain script).
            else: 
                response_str = response_str.format(reflection)
            finally:
                response_str = self._fix_punctuation(response_str)
             # TODO: Handle multiple reflections
        return response_str

    def _response_template_for_message(self,
                                       message: str,
                                       decomp_brain: ELDecompBrain,
                                       response_memdict: Dict[str, int]) -> ELResponse:
        # Some decomposition rules have precedence over others. Loop through
        # possible patterns, starting with the highest ranks, stop when match found.
        for rank in decomp_brain.ordered_ranks():
            rules = decomp_brain.eliise_rules().get(rank)
            response = self._response_for_rank(message,
                                               decomp_brain,
                                               rules.items(),
                                               response_memdict) if rules else None
            if response: 
                return response
        return ELResponse(self._error_response(), None)
    
    def _response_for_rank(self,
                           message: str,
                           decomp_brain: ELDecompBrain,
                           rules: ItemsView[str, List[str]],
                           response_memdict: Dict[str, int]) -> Optional[ELResponse]:
        for pattern, responses in rules:
            match = re.search(pattern, message, re.IGNORECASE)
            if not match:
                continue
            print("Match:", match)
            response_str = self._response_for_pattern(pattern, responses, response_memdict)
            print("Response template:", response_str)
            print("Pattern:", pattern)
            if not response_str.startswith("="):
                return ELResponse(response_str, match)
            # We have a redirect request. Pick a response from the specified decomposition pattern
            redir_response_str = self._redir_response_for_key(response_str[1:], decomp_brain, response_memdict)
            if redir_response_str:
                return ELResponse(redir_response_str, match)
        return None

    def _response_for_pattern(self,
                              pattern: str,
                              responses: List[str],
                              response_memdict: Dict[str, int]) -> str:
        if not pattern in response_memdict:
            response_memdict[pattern] = 1 # Response to use next time pattern is met
            return responses[0]
        i = response_memdict[pattern]
        if i < len(responses):
            response_memdict[pattern] += 1
            return responses[i]
        # We've used up all the responses, start over.
        response_memdict[pattern] = 1 
        return responses[0]
    
    def _redir_response_for_key(self,
                                key: str,
                                decomp_brain: ELDecompBrain,
                                response_memdict: Dict[str, int]) -> Optional[str]:
        """ This function looks for a response template based on a known key/pattern.
        This enables cross-referencing between patterns. E.g. response n of pattern A might
        be '=B' which is short for 'go pick a response from a related pattern B')"""
        for rank in decomp_brain.ordered_ranks():
            rules = decomp_brain.eliise_rules().get(rank)
            if rules and key in rules:
                return self._response_for_pattern(key, rules[key], response_memdict)  
        return None

    def _error_response(self) -> str:
        return "Bleep bloop, something went wrong. Please continue."

    def _reflect_content(self, regex_match: Match[str]) -> str:
        try:
            captured_content = regex_match.group(1)
        except IndexError:
            print("Raising indexerror")
            raise
        else:
            # all_clauses = self._all_clauses(captured_content)
            # content_to_reflect = "".join(self._clauses_to_reflect(all_clauses))
            if not captured_content or not isinstance(captured_content, str):
                # In some scenarios (e.g. in regex patterns including |) it is possible to get None
                # even if there was no error from Match.group().
                # TODO: Consider logging error (possibly need the user's permission for this)
                print("No captured content!")
                return ""
            print("Captured content is:")
            print(captured_content)
            content_to_reflect = self._content_trimmer.shortened_content_to_reflect(captured_content)
            words = self._tokenizer.tokenized(content_to_reflect)
            reflection = self._pronoun_reflector.reflect_pronouns(words)
            reflection = self._verb_reflector.reflect_verbs(reflection)
            return " ".join(reflection)
    
    def _fix_punctuation(self, message: str) -> str:
        message = message.replace('?.', '.')
        message = message.replace('.?', '?')
        message = message.replace('??', '?')
        message = message.replace(' .', '.')
        message = message.replace('.,',',')
        message = message.replace(' ,', ',')
        message = message.replace(' ?', '?')
        message = message.replace(' !', '!')
        message = message.replace('!?', '?')
        return message
