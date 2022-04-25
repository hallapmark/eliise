from typing import List
from elprotocols import Eliise_Rules

class ENGDecompBrain:

    # Regex patterns to match in the text, and response templates for each pattern
    ELIISE_RULES =  {5: {'i remember (.*)':
                            ['Do you often think of {0}?', 
                            'Does thinking of {0} bring anything else to mind?', 
                            'What else do you remember?', 
                            'Why do you remember {0} just now',
                            'What in the present situation reminds you of {0}',
                            'What is the connection between me and {0}'],
                        'do you remember (.*)': 
                            ['Did you think I would forget {0}?',
                            'Why do you think I should recall {0} now?',
                            'What about {0}?',
                            '=what (.*)',
                            'You mentioned {0}']},
                    4: {},
                    3: {'if (.*)': 
                            ["Do you really think it's likely that {0}?", 
                            'Do you wish that {0}?', 
                            'What do you think about {0}?', 
                            'Really--if {0}']},
                    2: {},
                    1: {},
                    0: {'what (.*)':
                            ['Why do you ask?',
                            'Does that question interest you?',
                            'What is it you really want to know?',
                            'Are such questions much on your mind?',
                            'What answer would please you most?',
                            'What do you think?',
                            'What comes to your mind when you ask that?',
                            'Have you asked such question before?',
                            'Have you asked anyone else?']}}

    def eliise_rules(self) -> Eliise_Rules:
        return self.ELIISE_RULES

    def ordered_ranks(self) -> List[int]:
        return sorted(self.ELIISE_RULES.keys(), reverse = True)
