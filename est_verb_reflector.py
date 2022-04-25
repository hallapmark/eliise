from typing import List
from estnltk.vabamorf.morf import synthesize
from estnltk.vabamorf.morf import analyze

class ESTVerbReflector:
    VERB_REFLECTIONS = {
        'n': 'd',  # ind. pres. sg. 1 act. positive -- to -- ind. pres. sg. 2 act. pos.
        'd': 'n',  # And the reverse
        'sin': 'sid'
    }

    def reflect_verbs(self, word_list: List[str]) -> List[str]:
        d = self.VERB_REFLECTIONS
        analysed_word_l = analyze(" ".join(word_list))
        new_words: List[str] = []
        for i, word_obj in enumerate(analysed_word_l):
            morph_analysis = word_obj['analysis'][0]
            # not a verb, skip to next word without reflection
            if morph_analysis['partofspeech'] != 'V':
                new_words.append(word_obj['text'])
                continue
            form = morph_analysis['form']
            lemma = morph_analysis['lemma']
            # BASIC REFLECTION.
            # Verb conjugations in verb_reflection_dict always get applied regardless of context
            if form in d:  
                reflected_verb = synthesize(lemma = lemma, form = d[form])[0]
                new_words.append(reflected_verb)
            # CONTEXT-SENSITIVE REFLECTION
            # 'ksid' is ambiguous between 3rd and 2nd person conditional mood
            elif form == 'ksid' and new_words[i-1] in ('mina', 'ma', 'mina ise', 'ma ise'):
                reflected_verb = synthesize(lemma = lemma, form = 'ksin')[0]
                new_words.append(reflected_verb)
            else:
                new_words.append(word_obj['text'])
        return new_words

