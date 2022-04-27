import re

class ESTContentTrimmer:
    def shortened_content_to_reflect(self, content: str) -> str:
        # For now only clean up the simplest cases of munged punctuation
        content = content.replace(',,', ',')
        content = content.replace('..', '.')

        # First we do a rough split along all commas and dots
        all_clauses = [clause for clause in re.split('([,.])', content) if clause != ""]

        # We did not get any splits, just return the content intact
        if not len(all_clauses) > 1:
            return content
        
        clauses_to_reflect = [all_clauses[0]]
        for i, next_cl in enumerate(all_clauses):
            if i == 0:
                continue
            previous_cl = all_clauses[i-1]
            # If it's the second clause and we have the connective ", et" we keep the second clause
            if i == 1 and previous_cl.endswith(",") and True in [next_cl.find(x) for x in [" et", "et"]]:
                clauses_to_reflect.append(next_cl)
            elif len(previous_cl) < 9: # ~2 words. 
                # This also weeds out false splits e.g. abbreviations with a dot in them.
                clauses_to_reflect.append(next_cl)
            else:
                break
        return "".join(clauses_to_reflect)  
