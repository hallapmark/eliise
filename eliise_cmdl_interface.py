from eliise import *
from est_decomp_brain import *
from est_tokenizer import *
from est_verb_reflector import *
from est_pronoun_reflector import *
from est_content_trimmer import *

# Print a response in the command-line interface
def send_cmdline_message(eliise: Eliise, message: str):
    response = eliise.respond(message)
    print("Eliise:", end=" ")
    print(response)

# if __name__ == "__main__":
#     s = ''
#     eliise = Eliise(ESTDecompBrain(),
#                     ESTTokenizer(),
#                     ESTVerbReflector(),
#                     ESTPronounReflector(),
#                     ESTContentTrimmer())
#     print("Eliise: Tere! Palun räägi mulle oma murest.")
#     while (s != 'quit') and (s != 'sulge'):
#         try:
#             s = input('> ')
#             if s == 'quit' or s == 'sulge':
#                 break
#             send_cmdline_message(eliise, s)
#         except EOFError:
#             s = 'quit'

eliise = Eliise(ESTDecompBrain(),
                ESTTokenizer(),
                ESTVerbReflector(),
                ESTPronounReflector(),
                ESTContentTrimmer())
send_cmdline_message(eliise, "See on tõsi. Ma olen õnnetu")
