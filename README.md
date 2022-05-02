# eliise
Eliise juturobot: an Estonian implementation of the famous English-language Eliza chatbot. See the 1966 paper by Joseph Weizenbaum introducing the original chatbot [here](https://dl.acm.o rg/doi/10.1145/365153.365168).

### Installation
1) It is recommended to have [conda](https://www.anaconda.com/products/distribution) for this project. 
2) Once you have conda, clone the project into a folder on your computer.
3) Make sure you are running exactly Python 3.9.x. If you are using conda, then in your terminal/shell you can create a suitable environment with the command `conda create -n py39eliise python=3.9`. Then run `conda activate py39eliise`. 
4) Make sure you have the [estnlk](https://github.com/estnltk/estnltk) natural language processing library installed. If you created the conda environment described in step 3 and have it activated, then you can install the library with the command `conda install -c estnltk -c conda-forge estnltk=1.7.0rc0`. Note: this is a large library with its own dependencies. If you run into any trouble with the installation, follow the [instructions](https://github.com/estnltk/estnltk) in the library documents.

### Use
In your terminal, navigate to the folder where you cloned Eliise. If you are using conda, remember to check that you have the environment described above activated. Then run `python eliise_cmdl_interface.py`. Eliise will greet you, and you can now have a chat. When you want to finish the conversation, type 'quit' or 'sulge' and press enter.

Eliise is a (mostly) deterministic bot that follows the logic of the original English-language chatbot very closely. Here is a recreation of the dialogue from the 1966 paper:

Kasutaja: Kõik sõbrad on samasugused. (_All friends are alike_)

– Eliise: Mil viisil samasugused? (_Alike in what way?_)

Kasutaja: Alati nad tülitavad mind millegagi. (_They are always bugging me about something._)

– Eliise: Kas sa saad tuua spetsiifilise näite? (_Can you think of a specific example?_)

Kasutaja: Noh, mu sõber saatis mind siia. (_Well, my friend sent me here._)
– Eliise: Sinu sõber saatis sind siia (_Your friend sent you here_)

Kasutaja: Ta ütleb, et ma olen enamus ajast õnnetu. (_He says I am unhappy most of the time._)
– Eliise: Mul on kahju kuulda, et sa oled õnnetu. (_I am sorry to hear you are unhappy._)

Kasutaja: See on tõsi. Ma olen õnnetu (_It is true. I am unhappy_)
– Eliise: Kas sa arvad, et siin olemine aitab sul mitte olla õnnetu? (_Do you think coming here will help you not be unhappy?_)

Kasutaja: Mul on vaja abi, niipalju on kindel. (_I need help, that much is certain_)
– Eliise: Kui sa saaksid abi, siis mida see sulle tähendaks? (_If you received_)

Kasutaja: Äkki õpiksin oma emaga läbi saama.
– Eliise: Räägi mulle veel oma perekonnast.

Kasutaja: Mu ema hoolitseb minu eest.
– Eliise: Kes su perekonnas veel hoolitseb sinu eest?

Kasutaja: Minu isa.
– Eliise: Sinu isa.

Kasutaja: Sa oled mõnel viisil minu isaga sarnane.
– Eliise: Milles sarnasus seisneb?

Kasutaja: Sa oled mitteagressiivne, aga ma arvan, et sa tahad autoriteetne olla.
– Eliise: Sa ütled ma olen mitteagressiivne

Kasutaja: Sa ei vaidle minuga.
– Eliise: Miks sa arvad, et ma ei vaidle sind?

Kasutaja: Sa kardad mind.
Eliise: Sulle meeldib arvata, et ma kardan sind – kas pole nii?

Kasutaja: Mu isa kardab kõiki.
Eliise: Mis sul veel mõttesse tuleb, kui sa mõtled oma isa?

Kasutaja: Kiusajad.
Eliise: Räägime lähemalt, miks sinu kaaslane saatis sind siia.
