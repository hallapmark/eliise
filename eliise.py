from multiprocessing.sharedctypes import Value
import re
import random
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
                 pronoun_reflector: ELPronounReflector):
        self._decomp_brain = decomp_brain
        self._tokenizer = tokenizer
        self._verb_reflector = verb_reflector
        self._pronoun_reflector = pronoun_reflector
        # { pattern: index of response to use for pattern next time }
        self._response_memdict: Dict[str, int] = {} 

    ## Public methods ##
    # Get a response from the chatbot
    def respond(self, message) -> str:
        return self._transform(message, self._decomp_brain, self._response_memdict)

    ## Private methods ##
    def _transform(self,
                   message: str,
                   decomp_brain: ELDecompBrain,
                   response_memdict: Dict[str, int]) -> str:
        """ Create a response by transforming the user's input message 
        according to a dictionary of rules."""
        response = self._get_response_template(message, decomp_brain, response_memdict)
        response_str = response.response
        # We plug in a reflection of what the user said
        if response.match and '{0}' in response_str:
            try:
                reflection = self._reflect_content(response.match)
            except IndexError:
                pass
                # TODO: In the future, we might want to LOG an error to a file or 
                # remote server so that we can keep an eye on any inconsistencies in our 
                # regex. We will get this error if we have indicated in our recomposition 
                # rule that we expect to reflect something in the content, but the 
                # decomposition rule does not capture a corresponding group 
                # (this would be an error in the decomp_brain script).
            else: 
                response_str = response_str.format(reflection)
            finally:
                response_str = self._fix_punctuation(response_str)
             # TODO: Handle multiple reflections
        return response_str

    def _get_response_template(self,
                               message: str,
                               decomp_brain: ELDecompBrain,
                               response_memdict: Dict[str, int]) -> ELResponse:
        # Some decomposition rules have precedence over others. Loop through
        # possible patterns, starting with the highest ranks, stop when match found.
        for rank in decomp_brain.ordered_ranks():
            rules = decomp_brain.eliise_rules().get(rank)
            response = self._response_for_rank(message, rules.items(), response_memdict) if rules else None
            # TODO: pick the leftmost response from the same rank?
            if response:
                return response
        return self._error_response()
    
    def _response_for_rank(self,
                           message: str,
                           rules: ItemsView[str, List[str]],
                           response_memdict: Dict[str, int]) -> Optional[ELResponse]:
        for pattern, responses in rules:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                print("Match:")
                print(match)
                response = self._response_for_pattern(pattern, responses, response_memdict)
                print("Response template:")
                print(response)
                return ELResponse(response, match)
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
        response_memdict[pattern] = 1 # We've used up all the responses, start over.
        return responses[0]

    def _error_response(self) -> ELResponse:
        return ELResponse("Bleep bloop, something went wrong. Please continue.", None)

    def _reflect_content(self, regex_match: Match[str]) -> str:
        try:
            captured_content = regex_match.group(1)
        except IndexError:
            raise
        else:
            # all_clauses = self._all_clauses(captured_content)
            # content_to_reflect = "".join(self._clauses_to_reflect(all_clauses))
            if not captured_content:
                # In some scenarios (e.g. in regex patterns including |) it is possible not 
                # to have an error from Match.group() yet the returned content can still be None.
                # TODO: Consider logging error (possibly need the user's permission for this)
                print("No captured content!")
                return ""
            print("Captured content is:")
            print(captured_content)
            words = self._tokenizer.tokenized(captured_content) # TODO: change to content_to_reflect
            reflection = self._pronoun_reflector.reflect_pronouns(words)
            reflection = self._verb_reflector.reflect_verbs(reflection)  
            return " ".join(reflection)
    
    # def _all_clauses(self, message: str) -> List[str]:
    #     # TODO: This is not a language-universal solution. Move to a protocol?
    #     all_clauses = re.split('[,.]', message)
    #     print(f'All clauses{all_clauses}')
    #     return re.split('[,.]', message)
    
    # TODO: This is not working as expected
    def _clauses_to_reflect(self, all_clauses: List[str]) -> List[str]:
        # Todo: make a recursive function here?
        clauses_to_reflect = [all_clauses[0]]
        for i, clause in enumerate(clauses_to_reflect[1:]):
            if len(clauses_to_reflect[i-1]) < 10: # ~2 words
                clauses_to_reflect.append(clause)  
        return clauses_to_reflect

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
