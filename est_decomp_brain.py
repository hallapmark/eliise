from typing import List
from elprotocols import Eliise_Rules

class ESTDecompBrain:

    ## Regex helpers ##

    # Matching of verbs when we do not care about the conjugation. Can only be used 
    # on verbs where the stem does not change. Not a complete list of all possible endings.
    _verb_endings_regex = r'(?:d|sid|b|s|vad|ksin|ksid)' 

    ## NOUN DECLENSION MATCHING ##
    # 14 cases in sg. and pl. plus parallel variants. We are ignoring comparatives for now.

    # declension type 00 / tüüpsõna 00
    _decl_00_mis_regex = '(?:s|lle|llede|da|llesse|lledesse|lles|lledes|llest|lledest|llele|lledele|l|llel|lledel|llelt|lledelt|lleks|lledeks|lleni|lledeni|llena|lledena|lleta|lledeta|llega|lledega)' 
    _decl_01e_regex_sg = '(?:i|i|it|isse|is|ist|ile|il|ilt|iks|ini|ina|ita|iga)'
    _decl_01e_regex_pl = '(?:id|ite|eid|itesse|eisse|ites|eis|itest|eist|itele|eile|itel|eil|itelt|eilt|iteks|eiks|iteni|itena|iteta|itega)'
    _decl_02_regex_sg = '(?:a|at|asse|as|ast|ale|al|alt|aks|ani|ana|ata|aga)'
    _decl_02_regex_pl = '(?:ad|ate|aid|atesse|aisse|ates|ais|atest|aist|atele|aile|atel|ail|atelt|ailt|ateks|aiks|ateni|atena|ateta|atega)'
    _decl_10_ne_regex_sg = '(?:ne|se|st|sesse|ses|sest|sele|sel|selt|seks|seni|sena|seta|sega)'
    _decl_10_ne_regex_pl = '(?:sed|ste|seid|stesse|seisse|stes|stest|stele|stel|stelt|steks|steni|stena|steta|stega)'
    _decl_18_gu_regex = '(?:gu|o|gu|gusse|kku|osse|os|ost|ole|ol|lt|oni|ona|ota|oga|od|gude|gusid|gudesse|gudes|gudest|gudele|gudel|gudelt|gudeni)'
    _decl_20_regex_sg = '(?:i|e|e|esse|es|est|ele|el|elt|eks|eni|ena|eta|ega)'
    _decl_20_regex_pl = '(?:ed|ede|esid|edesse|edes|edest|edele|edel|edelt|edeks|edeni|edena|edeta|edega)'

    ## Flags that trigger special processing rules
    memory_flag = '[memory]'
    elative_flag = '[elative_flag]'
    check_verb_in_reflection_flag = '[check_verb_in_reflection_flag]'

    ## Keys that need to be referenced in the eliise.py class
    memory_responses_key = 'memory_responses'
    match_all_key = '.*'
    
    ## Equivalence classes/synonyms
    def _family_synons_regex(self) -> str:
        # TODO: add recognition for all cases? 
        synons = ['perekond', 'ema', 'emme', 'mamps', 'mamma', 'isa', 'paps', 'õde', 'vend', 'abikaasa', 'lapsed', 'laps']
        return rf'(?:{"|".join(synons)})'

    def _belief_synons_regex(self) -> str:
        synons = ['uskumus', r'\busk\b','tunnen', 'mõtlen', 'arvan', 'usun', 'soovin'] # But not 'tahan' (want), it has its own set of rules
        return rf'(?:{"|".join(synons)})'

    ## Interface
    def ordered_ranks(self) -> List[int]:
        return sorted(self.eliise_rules().keys(), reverse = True)

    # Regex patterns to match in the text, and response templates for each pattern ##
    # Use (?:) for creating a non-capturing group that will not be reflected back in the reply.
    def eliise_rules(self) -> Eliise_Rules:
        return {50:     {rf'arvut(?:{self._decl_01e_regex_sg}|{self._decl_01e_regex_pl})': 
                                ['=arvuti'],
                        'arvuti': 
                                ['Kas arvutid teevad sind murelikuks?',
                                'Miks sa arvuteid mainid?',
                                'Kuidas sinu arvates masinad sinu murega seotud on?',
                                'Kas sa ei arva, et masinad võivad inimesi aidata?',
                                'Mis sind masinate juures häirib?',
                                'Mida sa masinatest arvad?'],
                        rf'masin(?:{self._decl_02_regex_sg}|{self._decl_02_regex_sg})?': 
                                ['=arvuti']},
                15:     {rf'nim(?:{self._decl_20_regex_sg}|{self._decl_20_regex_pl})\b(.*)': 
                                ['Nimed mind ei huvita.',
                                'Ma juba ütlesin, et nimed mind ei huvita – palun jätka.']},
                10:     {'sarnane(.*)':
                                ['Milles sarnasus seisneb?', 'Mismoodi?', 'Mil moel sarnane?',
                                'Millist sarnasust sa siin näed?',
                                'Millele see sarnasus sinu arvates viitab?',
                                'Kas sul tulevad veel mingid seosed pähe?',
                                'Mida see sarnasus sinu arvates tähendada võiks?',
                                'Mis seos siin sinu arvates on?',
                                'Kas siin võiks tõesti mingi seos olla?',
                                'Kuidas nii?'],
                        'sarnased(.*)':
                                ['Mil moel sarnased?', 'Millele see sarnasus sinu arvates viitab?', 
                                'Kas sul tulevad veel mingid seosed pähe?'],
                        rf'sarna{self._decl_10_ne_regex_sg}(.*)': 
                                ['=sarnane(.*)'], 
                        rf'(?:\bsama\b|samasugu{self._decl_10_ne_regex_sg})(.*)':
                                ['Mil viisil samasugune?', '=sarnane(.*)'],
                        rf'(?:\bsamad\b|samasugu{self._decl_10_ne_regex_pl})(.*)':
                                ['Mil viisil samasugused?',
                                '=sarnased(.*)'], # TODO: re-test the sg and pl variants       
                        rf'meenutad mulle(.*)': # note: this is in sg. 2 only as in the original Eliza
                                ['=sarnane(.*)'],
                        r'ka (?:selline|taoline)\b(.*)':
                                ['=sarnane(.*)']},
                5:      {'mäletan(.*)':
                                [rf'{self.elative_flag}Kas sa mõtled tihti {0}?', # alternatively a tuple # Maybe check out if estnlk has a solution for this. But heuristics fine. Some sort of syntactic parsing or tagging in estnlk. Something to check whether the object is a noun phrase or a subordinate clause
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
                4:      {'nägin unes(.*)':
                                ['Tõesti, {0}?',
                                'Kas sa oled kunagi ärkvel olles fantaseerinud {0}?',
                                'Kas sa oled varem unes näinud {0}?',
                                '=__unenägu__']},
                3:      {r'\bkui\b(.*)':
                                ['Kas sa pead tõenäoliseks, et {0}?',
                                'Kas sa soovid, et {0}?',
                                'Mida sina sellest arvad, kui {0}?',
                                'No tõesti--kui {0}?'],
                        rf'unenä{self._decl_18_gu_regex}\b(.*)':
                                ['=unenägu(.*)'],
                        'unenägu(.*)': 
                                ['Mida see unenägu sinu arvates tähendab?',
                                'Kas sa näed tihti unenägusid?',
                                'Millised inimesed sinu unenägudes on?',
                                'Kas sa ei leia, et see unenägu on kuidagi sinu murega seotud?']},
                2:      {'kas ma olin)(.*)': 
                                ['Mis siis oleks, kui sa olid {0}?',
                                'Kas sa arvad, et olid {0}?',
                                'Kas sa olid {0}',
                                'Mida see tähendaks, kui sa olid {0}',
                                'Millele viitab sinu arvates \"{0}\"?',
                                '=__mis__'],
                        'ma olin(.*)':
                                ['Kas tõesti olid?',
                                'Miks sa mulle nüüd ütled, et sa olid {0}',
                                'Äkki ma juba teadsin, et sa olid {0}'],
                        'kas sa olid(.*)': 
                                ['Kas sulle meeldiks uskuda, et ma olin {0}?',
                                'Mis sellele viitab, et ma olin {0}?',
                                'Mida sina arvad?',
                                'Võib-olla ma olin {0}.',
                                'Mis siis oleks, kui ma olin {0}'],
                        rf'{self.memory_flag}\b(?:minu|mu)\b(.*)':
                                [f'={self.memory_responses_key}'],
                        rf'\b(?:minu|mu)\b.*({self._family_synons_regex()})(.*)': # 2 captured groups! 
                                ['Räägi mulle veel oma perekonnast.',
                                'Kes su perekonnas veel {1}?',
                                'Sinu {0}.',
                                'Mis sul veel mõttesse tuleb, kui sa mõtled oma {0}?'],
                        rf'{self.check_verb_in_reflection_flag}\b(?:minu|mu)\b(.*)': # TODO: that-clause detector would be good here. Or maybe a verb detector?
                                ['Sinu {0}?',
                                'Miks sa ütled – sinu {0}',
                                'Kas see vihjab veel millelegi sinule kuuluvale?',
                                'Kas sulle on tähtis, et sinu {0}'],
                        f'{self.memory_responses_key}':
                                ['Räägime lähemalt, miks sinu {0}.', # TODO: that-clause or verb detector needed here as well
                                'Enne ütlesid sa, et {0}.',
                                'Aga sinu {0}?',
                                'Kas sel on midagi pistmist faktiga, et sinu {0}?']},
                0:      {'vabandust(.*)':
                                ['Palun ära vabanda.',
                                'Vabandada pole vaja.',
                                'Mida sa vabandades tunned?',
                                'Ma ütlesin sulle, et vabandada pole vaja.'],
                        'kuidas(.*)': 
                                ['=__mis__'], 
                        'millal(.*)':
                                ['=__mis__'],
                        'kindlasti|kindlapeale(.*)':
                                ['=__jah__'],
                        r'(?:võib-?olla)|(?:võib olla)|(?:\bäkki\b)(.*)':
                                ['Sa ei tundu selles päris kindel.',
                                'Miks sa seda ebakindlalt ütled?',
                                'Kas sa ei võiks olla positiivsem?',
                                'Sa pole kindel.',
                                'Kas sa siis ei tea?'],
                        'english': ['=__võõrkeel__'],
                        'francais': ['=__võõrkeel__'],
                        'italiano': ['=__võõrkeel__'],
                        'espanol': ['=__võõrkeel__'],
                        '__võõrkeel__': ['Vabandust, aga ma räägin ainult eesti keelt.'],
                        r'tere|tervist|(?:\bhei\b)(.*)':
                                ['Tere. Palun räägi oma murest.'],
                        r'((?:kas ma olen)|(?:olen ma\b))(.*)':
                                ['Kas sa usud, et sa oled {0}?',
                                'Kas sa tahaksid olla {0}',
                                'Sa soovid, et ma ütleksin, et sa oled {0}',
                                'Mida see sulle tähendaks, kui sa oleksid {0}',
                                '=__mis__'],
                        #r'olen\b(.*)': ['Miks sa ütled "olen"?', 'Ma ei saa sellest aru.'], can skip this in Estonian
                        r'((?:kas sa oled)|(?:oled sa\b))(.*)':
                                ['Miks sind huvitab, kas ma olen {0} või mitte?',
                                'Kas sa eelistaksid, et ma ei oleks {0}?',
                                'Võib-olla ma olen {0} sinu fantaasiates.',
                                'Kas sa mõnikord mõtled, et ma olen {0}',
                                '=__mis__'],
                        r'\bon\b(.*)': 
                                ['Kas sa arvasid, et nad ehk ei ole {0}?',
                                'Kas sulle meeldiks, kui nad ei oleks {0}?',
                                'Mis siis, kui nad ei oleks {0}?',
                                'On võimalik, et nad on {0}.'],
                        r'sinu\b(.*)':
                                ['Miks sind huvitab minu {0}?',
                                'Kuidas on sinu enda {0}?',
                                'Kas sulle valmistab muret kellegi teise {0}?',
                                'Tõesti, minu {0}?'],
                        r'(?:tahan|vajan)(.*)':
                                ['Kui sa saaksid {0}, siis mida see sulle tähendaks?',
                                'Miks sa tahad {0}?',
                                'Mis siis, kui sa juba õige pea saaksidki {0}?',
                                'Mis siis, kui sa mitte kunagi ei saa {0}?',
                                'Mida sulle tähendaks, kui sa saaksid {0}?',
                                'Kuidas {0} soovimine meie vestlusse puutub?'],
                        'olen.*(kurb|õnnetu|depressivne|haige)(.*)': # 2 captured groups, second likely not used
                                ['Mul on kahju kuulda, et sa oled {0}?',
                                'Kas sa arvad, et siin olemine aitab sul mitte olla {0}?',
                                'Ma usun, et pole meeldiv olla {0}',
                                'Kas sa selgitaksid, mis juhtus, et sa oled {0}'], # TODO: iffy translation
                        'olen.*(õnnelik|elevil|rõõmus)(.*)': # 2 captured groups, second likely not used
                                ['=__õnnelik__'],
                        '__õnnelik__':
                                ['Kuidas ma olen aidanud sul olla {0}?',
                                'Kas teraapia on aidanud sul olla {0}', # TODO: iffy translation
                                'Miks sa nüüd {0} oled?',
                                'Kas sa saaksid selgitada, miks sa järsku {0} oled?'],
                        r'tunnen(?:.*)(paremini|õnnelikult\b)(.*)':
                                ['Kuidas ma olen aidanud sul tunda end {0}?'],
                        'rõõmustan(.*)':
                                ['Kas teraapia on aidanud sul rõõmustada?'],
                        rf'{self._belief_synons_regex}.*(?:ma|mina)(.*)':
                                ['Kas sa tõesti usud seda?',
                                'Aga sa pole kindel, et sa {0}.',
                                'Kas sa tõesti kahtled, et sa {0}?'],
                        rf'{self._belief_synons_regex}.*(?:sa|sina)(.*)':
                                ['=sina'], # TODO: check reference validity!
                        r'\bolen\b(.*)':
                                ['Kas sa tulid minu juurde sellepärast, et sa oled {0}?',
                                'Kui kaua oled sa olnud {0}',
                                'Kas sa usud, et on normaalne olla {0}',
                                'Kas sa naudid olla {0}'], # TODO: more idiomatic translation
                        r'(ma|mina) ei saa(.*)':
                                ['Kuidas sa tead, et sa ei saa {0}?',
                                'Kas sa oled proovinud?',
                                'Võib-olla saaksid sa praegu {0}.',
                                'Kas sa tõesti tahad olla võimeline {0}?'],
                        r'ma ei\b(.*)':
                                ['Kas sa tõesti ei {0}?',
                                'Miks sa ei {0}?',
                                'Kas sa soovid olla võimeline {0}',
                                'Kas see häirib sind?'],
                        'kas ma tunnen(.*)':
                                ['Räägi mulle veel sellistest tunnetest.',
                                'Kas sa tunned tihti {0}?',
                                'Kas sa naudid seda, kui tunned {0}?',
                                'Mida sulle {0} tundmine meenutab?'],
                        r'ma(.*)sind\b.*': # TODO: we want an infinitive flag here?
                                ['Võib-olla sinu fantaasiates me {0} üksteist.',
                                'Kas sa tahad mind {0}?',
                                'Sul tundub olevat vajadus mind {0}',
                                'Kas sa {0} kedagi kedagi veel?'],
                        r'(.*\b(ma|mina)\b.*)':
                                ['Sa ütled {0}',
                                'Kas sa saaksid täpsustada?',
                                'Kas sul on mingi eriline põhjus öelda "{0}"',
                                'See on päris huvitav.'],
                        r'\b(?:sa|sina) oled(.*)':
                                ['Miks sa arvad, et ma olen {0}?',
                                'Kas sulle valmistab rõõmu uskuda, et ma olen {0}?',
                                'Kas sa mõnikord soovid, et sa oleksid {0}',
                                'Võib-olla sulle meeldiks olla {0}'],
                        r'\b(?:sa|sina)(.*)mind.*':
                                ['MIks sa arvad, et ma {0} sind?',
                                'Sulle meeldib arvata, et ma {0} sind – kas pole nii?',
                                'Miks sa arvad, et ma {0} sind?',
                                'Tõesti, mina {0} sind?',
                                'Kas sa tahad uskuda, et ma {0} sind?',
                                'Oletame, et ma {0} sind – mida see tähendaks?',
                                'Kas keegi veel usub, et ma {0} sind?'],
                        r'\b(?:sa|sina)\b(.*)':
                                ['Me rääkisime sinust – mitte minust.',
                                'Ah nii, mina {0}?',
                                'Sa ei räägi tegelikult minust – või mis?',
                                'Millised tunded sind praegu valdavad?'],
                        r'\b(jah+|jaa+)\b(.*)':
                                ['=__jah__'],
                        '__jah__':
                                ['Sa tundud selles päris kindel.',
                                'Sa oled selles veendunud.',
                                'Või nii.',
                                'Ma mõistan.'],
                        r'\beip?\b(.*)':
                                ['Kas sa ütled \"ei\" lihtsalt selleks, et olla negatiivne?',
                                'Sa oled praegu natuke negatiivne.',
                                'Miks mitte?',
                                'Miks \"ei\"?'],
                        r'kas.*(?:suudad|oskad|oled võimeline)(.*)': # TODO: check disjunction
                                ['Kas pole nii, et sa usud, et ma suudan {0}?',
                                '=__mis__',
                                'Sa tahad, et ma oskaksin {0}.',
                                'Võib-olla sa tahad ise olla võimeline {0}.'],
                        r'kas.*(?:suudan|oskan|olen võimeline)(.*)':
                                ['Kas sa suudad {0} või mitte sõltub rohkem sinust kui minust.',
                                'Kas sa tahad olla võimeline {0}?',
                                'Võib-olla sa ei taha {0}',
                                '=__mis__'],
                        rf'\bmi{self._decl_00_mis_regex}\b(.*)':
                                ['=__mis__'],
                        '__mis__':
                                ['Miks sa seda küsid?',
                                'Kas see teema paelub sind?',
                                'Mida sa selle küsimusega tegelikult teada saada tahtsid?',
                                'Kas sa mõtled tihti sellistele küsimustele?',
                                'Milline vastus sulle kõige rohkem meelehead teeks?',
                                'Mida sina arvad?',
                                'Kui sa seda küsid, siis mis sul mõttesse tuleb?',
                                'Kas sa oled selliseid küsimusi varem küsinud?',
                                'Kas sa oled kelleltki veel küsinud?']},
                -1:     {f'{self.match_all_key}': 
                                ['Ma pole kindel, kas ma mõistan täielikult, mida sa öelda tahad.',
                                'Palun jätka.',
                                'Mida see sinu arvates tähendab?',
                                'Kas sellistest asjadest rääkimine tekitab sinus tugevaid emotsioone?']}
                        }

if __name__ == "__main__":
    decomp_brain = ESTDecompBrain()
    #print(decomp_brain.ordered_ranks())
    #print(decomp_brain.eliise_rules())
