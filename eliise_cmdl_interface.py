from eliise import *
from est_decomp_brain import *
from est_tokenizer import *
from est_verb_reflector import *
from est_pronoun_reflector import *
from est_content_trimmer import *

from eng_decomp_brain import *
from eng_tokenizer import *
from eng_pronoun_reflector import *
from elprotocols import ELDefaultVerbReflector

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
#                     ESTPronounReflector())
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

# send_cmdline_message(eliise, "Mulle nii meeldib, et me saime need sarnastelt toredatelt inimestelt!")
# send_cmdline_message(eliise, "Ohhoo – me hindame samasuguseid looduspilte!")
# send_cmdline_message(eliise, "Meenutad mulle toredaid inimesi!")
# send_cmdline_message(eliise, "Ma usun, et ma olen ka taoline, kes eriti ise midagi öelda ei julge!")
# send_cmdline_message(eliise, "Minu unenägudes juhtub palju toredaid asju!")
# send_cmdline_message(eliise, "Minu unenägudesse – juhtub palju toredaid asju!")
# send_cmdline_message(eliise, "Minu unenägudesse – juhtub palju toredaid asju!")
# send_cmdline_message(eliise, "Aga millest see tuleb?")
# send_cmdline_message(eliise, "Aga milleni see kõik meid viib?")
# send_cmdline_message(eliise, "Ja millal nemad siis nii tähtsaks said?")
# send_cmdline_message(eliise, "Kuidas sina sellest tead?")
# send_cmdline_message(eliise, "Kindlasti arvad sa, et ma olen tobu.")
# send_cmdline_message(eliise, "Tartu on täna kindlapeale vihmane!")
# send_cmdline_message(eliise, "Äkki ma ei olegi osav!")
# send_cmdline_message(eliise, "Seal võib olla inimene!")
# send_cmdline_message(eliise, "Võib-olla olla niisama?")
# send_cmdline_message(eliise, "Võibolla Hegeliga pole mõtet juttu puhuda?")
# send_cmdline_message(eliise, "Jaa, nii see on")
# send_cmdline_message(eliise, "Jaaaa, nii see on")
# send_cmdline_message(eliise, "Jahhh, nii see on")
# send_cmdline_message(eliise, "Jah, nii see on")
# send_cmdline_message(eliise, "Kas sa mäletad, et ma sind eelmisel aastal aitasin, et sul hea oleks?")

# send_cmdline_message(eliise, "Kas sa ikka mäletad, et jah, ma nagu aitasin sind eelmisel aastal?")
# send_cmdline_message(eliise, "Need on minu rohulibled!")
# send_cmdline_message(eliise, "Kas sa mäletad, kuidas ma sind eelmisel aastal aitasin, et sul hea oleks?")
# send_cmdline_message(eliise, "Appi, see on tore inimene!")
# send_cmdline_message(eliise, "Ma tean, et minu suur vend ei usu minu võimetesse.")
# send_cmdline_message(eliise, "Mu õde tahab, et ma enda eest rohkem vastutaksin.")
send_cmdline_message(eliise, "Minu isa.")
send_cmdline_message(eliise, "See on minu õun.")
send_cmdline_message(eliise, "Appi, see on tore inimene!")
send_cmdline_message(eliise, "Ma mäletan oma sõpru.")
send_cmdline_message(eliise, "See on minu kiivi.")
send_cmdline_message(eliise, "Appi, see on kahtlane arvuti!")
send_cmdline_message(eliise, "Masinad on alati liiga emotsionaalsed.")
send_cmdline_message(eliise, "Seal on igasugu saiakesi.")
send_cmdline_message(eliise, "Leivakesi.")



# eliza = Eliise(ENGDecompBrain(),
#                ENGTokenizer(),
#                ELDefaultVerbReflector(),
#                ENGPronounReflector())

# Send the messages
# for _ in range(7):
#     send_cmdline_message(eliise, "Ma mälEtan, kui väga ma Helgi heakskiitu tahtsin, aga ma ei saanud seda kunagi.")
# print()
# for _ in range(7):
#     send_cmdline_message(eliise, "Ma mäletan oma sõpru.")
# for _ in range(2):
#     send_cmdline_message(eliise, "Kas mäletad, et ma Helgi heakskiitu tahtsin, aga ma ei saanud seda kunagi?")

#send_cmdline_message(eliise, "kui ma Helgi heakskiitu tahtsin, aga ma ei saanud seda kunagi.")

#send_cmdline_message(eliise, "Ma vajan tema toetust.")
# send_cmdline_message(eliise, "Ma tahan tema toetust.")
# send_cmdline_message(eliise, "Mb tahn tema toetust.")

# for _ in range(5):
#     send_cmdline_message(eliise, "Ma jooksin muudkui edasi.")

# send_cmdline_message(eliise, "mis siis, kui ma võidan selle mängu?")
# send_cmdline_message(eliise, "mis siis saab, kui su, su suurepärane auto, on katki?")
# send_cmdline_message(eliise, "mis siis saab, kui sina, meie kallikene, kaduma lähed?")
# send_cmdline_message(eliise, "kas sa mäletad oma eelmist sünnipäeva?")
# send_cmdline_message("kas sa arvad, et inimesed peaksid muretsema tehiskrattide pärast?")
# send_cmdline_message("ma tahan robotsõpra")
#eliise.send_cmdline_message("mis oleks, kui sina saaksid ükskõik milline olla?")
#eliise.send_cmdline_message("mis oleks, kui nemad saaksid ükskõik millised olla?")
#send_cmdline_message("kas sa arvad, et minu kass on vinge?")

# Send the messages
# send_cmdline_message(eliza, "do you remember your last birthday")
# send_cmdline_message(eliza, "if I say that you remember your last birthday")
# send_cmdline_message(eliza, "do you think humans should be worried about AI")
# send_cmdline_message(eliza, "I want a robot friend")
# send_cmdline_message(eliza, "what if you could be anything you wanted")
# send_cmdline_message(eliza, "what if your car is broken?")
# send_cmdline_message(eliza, "do you think my cat is awesome?")

