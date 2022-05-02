import sys
from eliise import *
from est_decomp_brain import *
from est_tokenizer import *
from est_verb_reflector import *
from est_pronoun_reflector import *
from est_content_trimmer import *

# Print a response in the command-line interface
def send_cmdline_message(eliise: Eliise, message: str, echo_user: bool = True):
    if echo_user:
        print()
        print(f"Kasutaja: {message}")
    response = eliise.respond(message)
    print("Eliise:", end=" ")
    print(response)

if __name__ == "__main__":
    if sys.version_info[0:2] != (3, 9):
        raise Exception('Project requires python 3.9')
    s = ''
    eliise = Eliise(ESTDecompBrain(),
                    ESTTokenizer(),
                    ESTVerbReflector(),
                    ESTPronounReflector(),
                    ESTContentTrimmer())
    print("Eliise: Tere! Palun räägi mulle oma murest.")
    while (s != 'quit') and (s != 'sulge'):
        try:
            s = input('> ')
            if s == 'quit' or s == 'sulge':
                break
            send_cmdline_message(eliise, s, echo_user = False)
        except EOFError:
            s = 'quit'

# eliise = Eliise(ESTDecompBrain(),
#                 ESTTokenizer(),
#                 ESTVerbReflector(),
#                 ESTPronounReflector(),
#                 ESTContentTrimmer())
# send_cmdline_message(eliise, "Kõik sõbrad on samasugused.")
# send_cmdline_message(eliise, "Alati nad tülitavad mind millegagi.")
# send_cmdline_message(eliise, "Noh, mu sõber saatis mind siia.")
# send_cmdline_message(eliise, "Ta ütleb, et ma olen enamus ajast õnnetu.")
# send_cmdline_message(eliise, "See on tõsi. Ma olen õnnetu")
# send_cmdline_message(eliise, "Mul on vaja abi, niipalju on kindel.")
# send_cmdline_message(eliise, "Äkki õpiksin oma emaga läbi saama.")
# send_cmdline_message(eliise, "Mu ema hoolitseb minu eest.")
# send_cmdline_message(eliise, "Minu isa.")
# send_cmdline_message(eliise, "Sa oled mõnel viisil minu isaga sarnane.")
# send_cmdline_message(eliise, "Sa oled mitteagressiivne, aga ma arvan, et sa tahad autoriteetne olla.")
# send_cmdline_message(eliise, "Sa ei vaidle minuga.")
# send_cmdline_message(eliise, "Sa kardad mind.")
# send_cmdline_message(eliise, "Mu isa kardab kõiki.")
# send_cmdline_message(eliise, "Kiusajad.")
