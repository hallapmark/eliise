import re, random
from elprotocols import *
from typing import List, Match, ItemsView, Optional
from typing import NamedTuple, Callable

# Eliise class
# TODO Steve grumette eliza 1983
# TODO Reinflection task. Check what's goin on under the hood. 
# TODO NB in the final paper talk a bit about how the reinflection works.

class ELResponse:
    def __init__(self,
                 response: str,
                 match: Optional[Match[str]],
                 decomp_options: Optional[Callable]):
        self.response = response
        self.match = match
        self.decomp_options = decomp_options

class PatternWithOptions(NamedTuple):
    """a docstring"""
    pattern: str

    # map the inputs to the function blocks
    # this is a roundabout way of creating a switch/match statement (unavailable in Py 3.8)
    options: Optional[Callable]

class Eliise:
    def __init__(self,
                 decomp_brain: ELDecompBrain,
                 tokenizer: ELTokenizer,
                 verb_reflector: ELVerbReflector,
                 pronoun_reflector: ELPronounReflector,
                 content_trimmer: ELReflectedContentTrimmer):
        ## Helper classes
        self._decomp_brain = decomp_brain
        self._tokenizer = tokenizer
        self._verb_reflector = verb_reflector
        self._pronoun_reflector = pronoun_reflector
        self._content_trimmer = content_trimmer

        ## State
        # { pattern: index of response to use for pattern next time }
        self._response_index_for_pattern: Dict[str, int] = {} 
        self._memorized_response_stack: List[str] = []
        self._amnesiac = False

    ## Public methods ##
    # Get a response from the chatbot
    def respond(self, message) -> str:
        # TODO: Parametrize content_trimmer
        return self._transform(message, self._decomp_brain, self._response_index_for_pattern)

    ## Private methods ##
    def _transform(self,
                   message: str,
                   decomp_brain: ELDecompBrain,
                   response_index_for_pattern: Dict[str, int]) -> str:
        """ Create a response by transforming the user's input message 
        according to a dictionary of rules."""
        print()
        print(f"User: {message}")
        response = self._response_for_message(message, decomp_brain, response_index_for_pattern)
        return self._fix_punctuation(response.response)

    def _response_for_message(self,
                              message: str,
                              decomp_brain: ELDecompBrain,
                              response_index_for_pattern: Dict[str, int]) -> ELResponse:
        # Some decomposition rules have precedence over others. Loop through
        # possible patterns, starting with the highest ranks, stop when match found.
        for rank in decomp_brain.ordered_ranks():
            rules = decomp_brain.eliise_rules().get(rank)
            response = self._response_for_rank(message,
                                               decomp_brain,
                                               rules.items(),
                                               response_index_for_pattern) if rules else None
            if response: 
                return response
        return ELResponse(self._error_response(), None, None)
    
    def _response_for_rank(self,
                           message: str,
                           decomp_brain: ELDecompBrain,
                           rules: ItemsView[str, List[str]],
                           response_index_for_pattern: Dict[str, int]) -> Optional[ELResponse]:
        for pattern, responses in rules:
            response = self._response_for_pattern(pattern, responses, message, decomp_brain, response_index_for_pattern)
            if not response:
                continue
            # This response does not get used now, it gets stored in memory to be used later
            if response.decomp_options == self._memory_handler:
                print("Memory handler runs!")
                self._memory_handler(response)
                continue
            return response
        return None

    def _response_for_pattern(self,
                              pattern: str,
                              responses: List[str],
                              message: str,
                              decomp_brain: ELDecompBrain,
                              response_index_for_pattern: Dict[str, int]) -> Optional[ELResponse]:
        pattern_with_options = self._cleaned_pattern_with_options(pattern, decomp_brain, self._memory_handler, self._elative_verb_handler)
        decomp_pattern = pattern_with_options.pattern
        decomp_options = pattern_with_options.options
        match = re.search(decomp_pattern, message, re.IGNORECASE)
        if not match:
            return None
        print("Match:", match)
        if pattern == decomp_brain.match_all_key:
            memorized_response = self._pop_from_memory()
            if memorized_response:
                return ELResponse(memorized_response, match, None)
        response_str = self._next_response_for_pattern(decomp_pattern, responses, decomp_brain, response_index_for_pattern)
        print("Response template:", response_str)
        print("Pattern:", decomp_pattern)
        response = ELResponse(response_str, match, decomp_options)
        if not response_str.startswith("="):
            return self._reflect_content(response)
        # We have a redirect request. Pick a response from the specified decomposition pattern
        redir_response_str = self._redir_response_for_key(response_str[1:], decomp_brain, response_index_for_pattern)
        if redir_response_str:
            response.response = redir_response_str
            return self._reflect_content(response)
        return None
        
    def _memory_handler(self, response: ELResponse):
        self._memorized_response_stack.append(response.response)
        # If we just saved a response to memory, we won't use memory this round.
        self._amnesiac = True
    
    def _pop_from_memory(self) -> Optional[str]:
        stack = self._memorized_response_stack
        if self._amnesiac:
            self._amnesiac = False
            return None
        if len(stack) < 1:
            return None
        # Get response from memory and prohibit memory use for next round
        self._amnesiac = True
        return stack.pop(0)

    def _elative_verb_handler(self, response: ELResponse):
        pass
    
    def _cleaned_pattern_with_options(self,
                                      pattern: str,
                                      decomp_brain: ELDecompBrain,
                                      memory_handler: Callable,
                                      elative_verb_handler: Callable) -> PatternWithOptions:
        options_switch = { decomp_brain.memory_flag : memory_handler, decomp_brain.elative_flag: elative_verb_handler }
        for key in options_switch:
            if pattern.startswith(key):
                pattern = pattern.removeprefix(key)
                f = options_switch[key]
                return PatternWithOptions(pattern, f)
        return PatternWithOptions(pattern, None)

    def _next_response_for_pattern(self,
                                   pattern: str,
                                   responses: List[str],
                                   decomp_brain: ELDecompBrain,
                                   response_index_for_pattern: Dict[str, int]) -> str:
        if pattern == decomp_brain.memory_responses_key:
                    return random.choice(responses)
        if not pattern in response_index_for_pattern:
            response_index_for_pattern[pattern] = 1 # Response to use next time pattern is met
            return responses[0]
        i = response_index_for_pattern[pattern]
        if i < len(responses):
            response_index_for_pattern[pattern] += 1
            return responses[i]
        # We've used up all the responses, start over.
        response_index_for_pattern[pattern] = 1 
        return responses[0]
    
    def _redir_response_for_key(self,
                                key: str,
                                decomp_brain: ELDecompBrain,
                                response_index_for_pattern: Dict[str, int]) -> Optional[str]:
        """ This function looks for a response template based on a known key/pattern.
        This enables cross-referencing between patterns. E.g. response n of pattern A might
        be '=B' which is short for 'go pick a response from a related pattern B')"""
        print("redir!")
        for rank in decomp_brain.ordered_ranks():
            rules = decomp_brain.eliise_rules().get(rank)
            if rules and key in rules:
                return self._next_response_for_pattern(key, rules[key], decomp_brain, response_index_for_pattern)  
        return None

    def _error_response(self) -> str:
        return "Bleep bloop, something went wrong. Please continue."

    def _reflect_content(self, response: ELResponse) -> ELResponse:
        if not (response.match and '{0}' in response.response):
            return response
        try:
            captured_content = response.match.group(1)
        except IndexError:
            print("indexerror") # TODO: get rid of print statement
            return response
            # We will get this error if we have indicated in our recomposition 
            # rule that we expect to reflect something in the content, but the 
            # decomposition rule does not capture a corresponding group 
            # (this would be an error in the decomp_brain script).
        else: 
            if not captured_content or not isinstance(captured_content, str):
                # In some scenarios (e.g. in regex patterns including |) it is possible to get None
                # even if there was no error from Match.group().
                print("No captured content!")
                return response
            print("Captured content is:")
            print(captured_content)
            content_to_reflect = self._content_trimmer.shortened_content_to_reflect(captured_content)
            words = self._tokenizer.tokenized(content_to_reflect)
            reflection = self._pronoun_reflector.reflect_pronouns(words)
            reflection = self._verb_reflector.reflect_verbs(reflection)
            reflection_str = " ".join(reflection)
            response.response = response.response.format(reflection_str)
            return response
            # TODO: Handle multiple reflections
    
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
        message = message.replace('!.', '.')
        return message
