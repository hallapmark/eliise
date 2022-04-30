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
    _ne_regex_sg = '(?:ne|se|st|sesse|ses|sest|sele|sel|selt|seks|seni|sena|seta|sega)'
    _ne_regex_pl = '(?:sed|ste|seid|stesse|seisse|stes|stest|stele|stel|stelt|steks|steni|stena|steta|stega)'

    # declension type 18
    _gu_regex = '(?:gu|o|gu|gusse|kku|osse|os|ost|ole|ol|lt|oni|ona|ota|oga|od|gude|gusid|gudesse|gudes|gudest|gudele|gudel|gudelt|gudeni)'

    memory_flag = '[memory]'
    think_verb_flag = '[think_verb_flag]'
    memory_responses_key = 'memory_responses'
    match_all_key = '.*'

    def ordered_ranks(self) -> List[int]:
        return sorted(self.eliise_rules().keys(), reverse = True)

    ## Regex patterns to match in the text, and response templates for each pattern ##
    # Use (?:) for creating a non-capturing group that will not be reflected back in the reply.
    def eliise_rules(self) -> Eliise_Rules:
        return {10:     {'sarnane(.*)':
                                ['Mil moel sarnane?', 'Mismoodi?',
                                'Milles sarnasus seisneb?', 'Millist sarnasust sa siin näed?',
                                'Millele see sarnasus sinu arvates viitab?',
                                'Kas sul tulevad veel mingid seosed pähe?',
                                'Mida see sarnasus sinu arvates tähendada võiks?',
                                'Mis seos siin sinu arvates on?',
                                'Kas siin võiks tõesti mingi seos olla?',
                                'Kuidas nii?'],
                        'sarnased(.*)':
                                ['Mil moel sarnased?', 'Millele see sarnasus sinu arvates viitab?', 
                                'Kas sul tulevad veel mingid seosed pähe?'],
                        rf'sarna{self._ne_regex_sg}(.*)': 
                                ['=sarnane(.*)'], 
                        rf'(?:\bsama\b|samasugu{self._ne_regex_sg})(.*)':
                                ['Mil viisil samasugune?', '=sarnane(.*)'],
                        rf'(?:\bsamad\b|samasugu{self._ne_regex_pl})(.*)':
                                ['Mil viisil samasugused?',
                                '=sarnased(.*)'], # TODO: re-test the sg and pl variants       
                        rf'meenutad mulle(.*)': # note: this is in sg. 2 only as in the original Eliza
                                ['=sarnane(.*)'],
                        r'ka (?:selline|taoline)\b(.*)':
                                ['=sarnane(.*)']},
                    5:  {'mäletan(.*)':
                                [rf'{self.think_verb_flag}Kas sa mõtled tihti {0}?', # alternatively a tuple # Maybe check out if estnlk has a solution for this. But heuristics fine. Some sort of syntactic parsing or tagging in estnlk. Something to check whether the object is a noun phrase or a subordinate clause
                                'Kas midagi tuleb veel mõttesse, kui sa mõtled {0}?',
                                'Mis sul veel meelde tuleb?',
                                'Mis sulle praeguses olukorras meenutab {0}?',
                                'Mis on seos minu ja {0} vahel?'],
                        'kas .*mäletad(.*)':
                                ['Kas sa arvasid, et ma unustan {0}?',
                                'Miks ma peaksin praegu mõtlema sellest {0}?',
                                'Mis sellest {0}?',
                                '=__mis__',
                                'Sa mainisid {0}']},
                    4:  {'nägin unes(.*)':
                                ['Tõesti, {0}?',
                                'Kas sa oled kunagi ärkvel olles fantaseerinud {0}?',
                                'Kas sa oled varem unes näinud {0}?',
                                '=__unenägu__']},
                    3:  {r'\bkui\b(.*)':
                                ['Kas sa pead tõenäoliseks, et {0}?',
                                'Kas sa soovid, et {0}?',
                                'Mida sina sellest arvad, kui {0}?',
                                'No tõesti--kui {0}?'],
                        rf'unenä{self._gu_regex}\b(.*)':
                                ['=unenägu'],
                        'unenägu': 
                                ['Mida see unenägu sinu arvates tähendab?',
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
                                'Mida sulle tähendaks, kui sa saaksid {0}?',
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
                        rf'\bmi{self._mis_regex}\b(.*)':
                                ['=__mis__'],
                        rf'{self.memory_flag}\b(?:minu|mu)\b(.*)':
                                [f'={self.memory_responses_key}']},
                    -1: {f'{self.match_all_key}': 
                                ['Ma pole kindel, kas ma mõistan täielikult, mida sa öelda tahad.',
                                'Palun jätka.',
                                'Mida see sinu arvates tähendab?',
                                'Kas sellistest asjadest rääkimine tekitab sinus tugevaid emotsioone?'],
                        f'{self.memory_responses_key}':
                                ['Räägime lähemalt, miks sinu {0}.',
                                'Enne ütlesid sa, et {0}.',
                                'Aga sinu {0}?',
                                'Kas sel on midagi pistmist faktiga, et sinu {0}?']}
                        }

if __name__ == "__main__":
    decomp_brain = ESTDecompBrain()
    #print(decomp_brain.ordered_ranks())
    print(decomp_brain.eliise_rules())

