
<img title="" src="https://raw.githubusercontent.com/Alessandrostr95/PinkPeachProject/main/site/assets/logo.svg" alt="" width="120" data-align="inline" data-align="center">

# PPP - The Pink Peach Project

Molto spesso a tutti noi capita di lamentarci di qualcosa. Questo è
normale. Anzi, è molto importante sentire ed esprimere la propria
insoddisfazione, in quanto l'umanità è sempre avanzata in eterni
conflitti tra realtà insoddisfacenti e ideali irraggiungibili.

Premesso questo, bisogna anche tenere bene a mente che la cosa
importante, quando si è insoddisfatti, è il cercare di non limitarsi
a critiche e lamentele fine a sé stesse. La critica, quella vera,
non è un modo per disprezzare un qualcosa, o per sfogare la propria
frustrazione e basta. L'intenzione finale di una critica che merita
tale nome infatti dovrebbe essere quella di migliorare l'oggetto che
si sta criticando.

---

Il `Pink Peach Project` nasce da una serie di critiche e da un senso
di insoddisfazione generale rispetto allo stato corrente del sito di
informatica. Apprezziamo tutti gli sforzi che vengono fatti per la
gestione e manutenzione di tale sito, ma purtroppo non li riteniamo
sufficienti per garantire un servizio di qualità che riesca a
reggere la competizione odierna.

L'obiettivo del `Pink Peach Project` è alquanto semplice da esprimere:
**fornire un servizio alternativo al sito ufficiale di
informatica**. Vogliamo, in altre parole, dare una scelta in più agli
studenti iscritti ad informatica.

Per alcuni il nostro servizio sarà peggiore di quello ufficiale. Per
altri, forse, sarà migliore. Ma a prescindere da queste
considerazioni, troppo soggettive per essere di interesse, l'unica
osservazione degna di nota è il fatto che il nostro servizio sarà
unico nel suo genere, perché sarà fatto *dagli studenti per gli
studenti*.

---

### Description

L'idea di base di questo progetto è quella di avere un codice che con 
un solo click *generi in automatico* tutto il sito finale, bello pronto e impacchettato.
Per prima cosa il modulo python `src/scraper.py` scarica tutte le informazioni
utili dal sito ufficiale `http://www.informatica.uniroma2.it/` e li salva nella 
cartella `data/`.
La cartella data ha la seguente struttura
```
  data
  ├── magistrale
  │   └── < Anno Accademico >
  │       ├── annunci
  │       ├── corsi
  │       ├── docenti
  │       ├── esami
  │       └── orario
  └── triennale
      └── < Anno Accademico >
          ├── annunci
          ├── corsi
          ├── docenti
          ├── esami
          └── orario
```

Dopodiche nella cartella `src/site_generator/` ci sono una serie di script python che 
costruiscono le pagine html del sito, basandosi su dei **template** nella cartella
`templates/`.
La libreria usata per la compilazione dei template html è **jinja2** (https://jinja.palletsprojects.com/en/3.0.x/).

I vantaggi di questo approccio sono:
1. Scalabilità del sito
2. Pagine generate dinamicamente lato server, ma viste come pagine statiche lato client, riducento il carico di lavoro dei client
3. Modificare un template in comune per tutti anzichè ogni singola pagina
