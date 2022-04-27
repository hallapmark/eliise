from typing import List
from elprotocols import Eliise_Rules

class ESTDecompBrain:

    ## Regex helpers ##

    # Easy matching of verbs when we do not care about the conjugation. Can only be used 
    # on verbs where the stem does not change.
    _verb_endings_regex = r'(?:d|sid|b|s|vad)' 

    """ Use these to test 'IndexError: no such group' error"""
    #verb_endings_regex = r'(?:d|sid|b|s|vad)'
    #rf'(?:(?:meenuta{verb_endings_regex} mulle)|(?:ka selline))'
    #send_cmdline_message(eliise, "Meenutasid mulle toredaid inimesi!")

    ## NOUN DECLENSION MATCHING ##
    # 14 cases in sg. and pl. plus parallel variants. We are ignoring comparatives for now.

    # declension type 00
    _mis_regex = '(?:s|lle|llede|da|llesse|lledesse|lles|lledes|llest|lledest|llele|lledele|l|llel|lledel|llelt|lledelt|lleks|lledeks|lleni|lledeni|llena|lledena|lleta|lledeta|llega|lledega)' 
    # declension type 10 / tüüpsõna 10
    _ne_regex = '(?:ne|sed|se|ste|st|seid|st?esse|seisse|st?es|st?est|st?ele|st?el|st?elt|st?eks|st?eni|st?ena|st?eta|st?ega)'  
    
    # declension type 18
    _gu_regex = '(?:gu|o|gu|gusse|kku|osse|os|ost|ole|ol|lt|oni|ona|ota|oga|od|gude|gusid|gudesse|gudes|gudest|gudele|gudel|gudelt|gudeni)'

    def ordered_ranks(self) -> List[int]:
        return sorted(self.eliise_rules().keys(), reverse = True)

    ## Regex patterns to match in the text, and response templates for each pattern ##
    # Use (?:) for creating a non-capturing group that will not be reflected back in the reply.
    def eliise_rules(self) -> Eliise_Rules:
        return {10:     {'sarnane(.*)':
                                ['Mismoodi?', 'Mil moel sarnane?', 'Mil viisil?'
                                'Milles sarnasus seisneb?', 'Millist sarnasust sa siin näed?',
                                'Millele see sarnasus sinu arvates viitab?',
                                'Kas sul tulevad veel mingid seosed pähe?',
                                'Mida see sarnasus sinu arvates tähendada võiks?',
                                'Mis seos siin sinu arvates on?',
                                'Kas siin võiks tõesti mingi seos olla?',
                                'Kuidas nii?'], 
                        rf'(?:sarna{self._ne_regex}|\bsamad?\b|samasugu{self._ne_regex})(.*)': # TODO: 'samasugune' should actually have its own rules
                                ['=sarnane(.*)'], 
                        rf'meenuta{self._verb_endings_regex} mulle(.*)': # Replace 
                                ['TEST. REPLACE. Kas see meenutab sulle {0}?', 
                                '=sarnane(.*)'],
                        r'ka (?:selline|taoline)\b(.*)':
                                ['=sarnane(.*)']},
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
                                '=__mis__',
                                'Sa mainisid {0}']},
                    4:  {'nägin unes(.*)':
                                ['Tõesti, {0}?',
                                'Kas sa oled kunagi ärkvel olles fantaseerinud {0}',
                                'Kas sa oled varem unes näinud {0}',
                                '=__unenägu__']},
                    3:  {r'\bkui\b(.*)':
                                ['Kas sa pead tõenäoliseks, et {0}?',
                                'Kas sa soovid, et {0}?',
                                'Mida sina sellest arvad, kui {0}?',
                                'No tõesti--kui {0}?'],
                        rf'unenä{self._gu_regex}\b(.*)':
                                ['=unenägu'],
                        'unenägu': 
                                ['Mida see unenägu sinu arvates tähendab? {0}',
                                'Kas sa näed tihti unenägusid?',
                                'Millised inimesed sinu unenägudes on?',
                                'Kas sa ei leia, et see unenägu on kuidagi sinu murega seotud?']},
                    0:  {'vabandust(.*)':
                                ['Palun ära vabanda.',
                                'Vabandada pole vaja.',
                                'Mida sa vabandades tunned?',
                                'Ma ütlesin sulle, et vabandada pole vaja.'],
                        'kuidas(.*)': 
                                ['=__mis__'], 
                        'millal(.*)':
                                ['=__mis__'],
                        'kindlasti|kindlapeale':
                                ['=__jah__'],
                        r'(?:võib-?olla)|(?:võib olla)|(?:äkki\b)':
                                ['Sa ei tundu selles päris kindel.',
                                'Miks sa seda ebakindlalt ütled?',
                                'Kas sa ei võiks olla positiivsem?',
                                'Sa pole kindel.',
                                'Kas sa siis ei tea?'],
                        '(?:tahan|vajan)(.*)':
                                ['Kui sa saaksid {0}, siis mida see sulle tähendaks?',
                                'Miks sa tahad {0}?',
                                'Mis siis, kui sa juba õige pea saaksidki {0}?',
                                'Mis siis, kui sa mitte kunagi ei saa {0}?',
                                'Mida sulle tähendaks, kui sa saaksid {0}',
                                'Kuidas {0} soovimine meie vestlusse puutub?'],
                        '__jah__':
                                ['Sa tundud selles päris kindel.',
                                'Sa oled selles veendunud.',
                                'Või nii.',
                                'Ma mõistan.'],
                        r'\b(jah+|jaa+)\b':
                                ['=__jah__'], 
                        '__mis__':
                                ['Miks sa seda küsid?',
                                'Kas see teema paelub sind?',
                                'Mida sa selle küsimusega tegelikult teada saada tahtsid?',
                                'Kas sa mõtled tihti sellistele küsimustele?',
                                'Milline vastus sulle kõige rohkem meelehead teeks?',
                                'Mida sina arvad?',
                                'Kui sa seda küsid, siis mis sul mõttesse tuleb?',
                                'Kas sa oled selliseid küsimusi varem küsinud?',
                                'Kas sa oled kelleltki veel küsinud?'],
                        rf'\bmi{self._mis_regex}\b':
                                ['=__mis__']},
                    -1: {'.*': 
                                ['Ma pole kindel, kas ma mõistan täielikult, mida sa öelda tahad.',
                                'Palun jätka.',
                                'Mida see sinu arvates tähendab?',
                                'Kas sellistest asjadest rääkimine tekitab sinus tugevaid emotsioone?']}
                        }

if __name__ == "__main__":
    decomp_brain = ESTDecompBrain()
    #print(decomp_brain.ordered_ranks())
    print(decomp_brain.eliise_rules())

