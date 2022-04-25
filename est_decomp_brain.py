from typing import List
from elprotocols import Eliise_Rules

class ESTDecompBrain:

    ## Regex helpers ##

    # Easy matching of verbs when we do not care about the conjugation. Can only be used 
    # on verbs where the stem does not change.
    verb_endings_regex = r'(?:d|sid|b|s|vad)' 

    """ Use these to test 'IndexError: no such group' error"""
    #verb_endings_regex = r'(?:d|sid|b|s|vad)'
    #rf'(?:(?:meenuta{verb_endings_regex} mulle)|(?:ka selline))'
    #send_cmdline_message(eliise, "Meenutasid mulle toredaid inimesi!")

    # Easy matching of common -ne adjectives when we care neither about the case nor whether they are in sg. or pl.
    # 14 cases in sg. and pl.
    ne_regex = r'(?:ne\b|sed\b|se\b|ste\b|st\b|seid\b|st?esse\b|st?es\b|st?est\b|st?ele\b|st?el\b|st?elt\b|st?eks\b|st?eni\b|st?ena\b|st?eta\b|st?ega\b)'  
    def ne_regex_constructor(endings: List[str]):
        regex_str = r'?:'
        pass
    ## Regex patterns to match in the text, and response templates for each pattern ##
    # Use (?:) for creating a non-capturing group that will not be reflected back in the reply.
    ELIISE_RULES = {10: {'sarnane(.*)':
                                ['Mismoodi?', 'Mil moel sarnane?', 'Mil viisil?'
                                'Milles sarnasus seisneb?', 'Millist sarnasust sa siin näed?',
                                'Millele see sarnasus sinu arvates viitab?',
                                'Kas sul tulevad veel mingid seosed pähe?',
                                'Mida see sarnasus sinu arvates tähendada võiks?',
                                'Mis seos siin sinu arvates on?',
                                'Kas siin võiks tõesti mingi seos olla?',
                                'Kuidas nii?'], 
                        rf'(?:sarna{ne_regex}|samad?|samasugu{ne_regex})(.*)': # TODO: Replace test string
                                ["TEST. REPLACE. Millele see sarnasus sinu arvates viitab? Kas seda, et see on {0}?", 
                                '=sarnane'], # TODO: don't we need (.*)? Also, sama(d)?
                        rf'(?:(?:meenuta{verb_endings_regex} mulle)|(?:ka selline))': # TODO: Test all these
                                ['TEST. REPLACE. Kas see meenutab sulle {0}?', 
                                '=sarnane']},
                    5:  {'mäletan(.*)':
                                ['Kas sa mõtled tihti {0}?',
                                'Kas midagi tuleb veel mõttesse, kui sa mõtled {0}?',
                                'Mis sul veel meelde tuleb?',
                                'Mis sulle praeguses olukorras meenutab {0}?',
                                'Mis on seos minu ja {0} vahel?'],
                        'kas .*mäletad(.*)':
                                ['Kas sa arvasid, et ma unustan {0}?',
                                'Miks ma peaksin praegu mõtlema sellest {0}',
                                'Mis sellest {0}?',
                                '=mis',
                                'Sa mainisid {0}']},
                    4:  {'nägin unes(.*)':
                                ['Tõesti, {0}?',
                                'Kas sa oled kunagi ärkvel olles fantaseerinud {0}',
                                'Kas sa oled varem unes näinud {0}',
                                '=unenägu']},
                    3:  {r'\bkui\b(.*)':
                                ['Kas sa pead tõenäoliseks, et {0}?',
                                'Kas sa soovid, et {0}?',
                                'Mida sina sellest arvad, kui {0}?',
                                'No tõesti--kui {0}?'],
                        '(?:unenägu|unenäod|unenäos|unenägudes)': # TODO: don't we need (.*)? TEST
                                ['Mida see unenägu sinu arvates tähendab?',
                                'Kas sa näed tihti unenägusid?',
                                'Millised inimesed sinu unenägudes on?',
                                'Kas sa ei leia, et see unenägu on kuidagi sinu murega seotud?']},
                    0:  {'kuidas(.*)': 
                                ['=mis'], # TODO: add keyword 'mis'
                        'millal(.*)':
                                ['=mis'],
                        'vabandust(.*)':
                                ['Palun ära vabanda.',
                                'Vabandada pole vaja.',
                                'Mida sa vabandades tunned?',
                                'Ma ütlesin sulle, et vabandada pole vaja.'],
                         '(?:tahan|vajan)(.*)':
                                ['Kui sa saaksid {0}, siis mida see sulle tähendaks?',
                                'Miks sa tahad {0}?',
                                'Mis siis, kui sa juba õige pea saaksidki {0}?',
                                'Mis siis, kui sa mitte kunagi ei saa {0}?',
                                'Mida sulle tähendaks, kui sa saaksid {0}',
                                'Kuidas {0} soovimine meie vestlusse puutub?']},
                    -1: {'.*': 
                                ['Ma pole kindel, kas ma mõistan täielikult, mida sa öelda tahad.',
                                'Palun jätka.',
                                'Mida see sinu arvates tähendab?',
                                'Kas sellistest asjadest rääkimine tekitab sinus tugevaid emotsioone?']}
                    }

    def eliise_rules(self) -> Eliise_Rules:
        return self.ELIISE_RULES

    def ordered_ranks(self) -> List[int]:
        return sorted(self.ELIISE_RULES.keys(), reverse = True)

if __name__ == "__main__":
    decomp_brain = ESTDecompBrain()
    print(decomp_brain.ordered_ranks())
    print(decomp_brain.eliise_rules())