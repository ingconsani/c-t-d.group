import os, subprocess
from PIL import Image, ImageDraw, ImageFont

repo = "/Users/ingconsani/Development/c-t-d.group"
assets_dir = os.path.join(repo, "assets")
caroselli_web_dir = os.path.join(assets_dir, "caroselli")
out_desktop_dir = "/Users/ingconsani/Desktop/CtD_LinkedIn_Caroselli_PDF"
os.makedirs(caroselli_web_dir, exist_ok=True)
os.makedirs(out_desktop_dir, exist_ok=True)

def get_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf"
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines, current = [], ""
    for w in words:
        test = (current + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines

vp_24_clean = [
    (1, '1 - Coach "intelligente (senza artificiale, ricco dell\'intelligenza umana degli SME) e privato": partire dal Cervello prima di Sinapsi o Pratica.'),
    (2, '2 - L\'"Esperanto" comune (in italiano chiaro e ordinato con sort_order) che abilita un\'Intelligenza Relazionale ecologica e sostenibile.'),
    (3, '3 - Navigazione flessibile: partenza dal Cervello o selezione diretta di un altro nodo L0 cliccando su Orizzonti.'),
    (4, '4 - Qualificazione dell\'esigenza: passaggio dal "non so cosa non so" al riconoscimento del vero problema L2 padre.'),
    (5, '5 - Meccanismo della Proliferazione (NBD -> NBA -> NBM): individuazione dell\'L3 Ancora risolutivo del problema L2 padre.'),
    (6, '6 - Calcolo in RAM (_healDatabaseRollups): nodi ignoti = Debolezza 10 e Minaccia 10; tasto Pausa = reset a \'0\' per spendere tempo di qualità.'),
    (7, '7 - Profilo aggiornato 100% offline: metriche generalizzate oltre il fatturato, Scudo di Anonimizzazione AI e compliance GDPR / EU AI Act.'),
    (8, '8 - Profilazione propedeutica e non costrittiva: percorsi assistiti trasparenti e risposte pre-confezionate + "Altro" (con invito a specificare).'),
    (9, '9 - Dalla teoria alla pratica: aiutare Persona, Professionista o PMI a diventare padroni del proprio futuro senza standardizzarne i fini.'),
    (10, '10 - Proliferazione progettuale: trasformazione automatica del compito in cantiere mantenendo la gerarchia verticale (parent_uuid).'),
    (11, '11 - Workflow orizzontale (MIEI <-> MIEI): tracciamento logico (evolvedFrom / peerFlow in UserSynapseState) senza alterare la struttura.'),
    (12, '12 - Aiuti concreti sull\'L3 Ancora: scomposizione dei passi pratici che separano lo stato attuale (P) dal traguardo (T).'),
    (13, '13 - Smistamento sovrano: scelta per ogni mattone tra Fai-da-Te (Palestra), Vista 1 (Provider P&S / Proven SME), Vista 2 (Rete IR) + "Altro".'),
    (14, '14 - Costruzione di R e "Cordone Ombelicale": 21 giorni operativi che legano anche il professionista (es. Barbarossa) ai suoi migliori clienti.'),
    (15, '15 - Qualifica a "Proven SME": raggiungendo R >> su un DOT, CtD qualifica l\'utente per essere cooptato (con consenso scritto) sull\'L3 Ancora.'),
    (16, '16 - Mini micro-blockchain offline (local_source_chain): integrità locale dei punteggi e dei certificati anti-manomissione SQLite a costo server zero.'),
    (17, '17 - Rivoluzione da Push a Pull: inimitabilità garantita da +50 anni di esperienza, +2 anni di sviluppo AI e doppio brevetto.'),
    (18, '18 - Genealogia relazionale (ir_contacts_graph): tracciamento di "chi mi ha presentato chi" tra Capitoli (BNI Barbarossa & beyond) e network.'),
    (19, '19 - Calcoli in tempo reale in RAM: Score Diretto (chi risolve direttamente l\'L3) vs Score Ponte (chi introduce al 2° grado).'),
    (20, '20 - "Prodotti / Servizi / Relazioni personalizzate a disposizione on-demand": cablate sul singolo L3 Ancora per essere oggetto di Pull.'),
    (21, '21 - Next Best Match (NBM) riservato ("Salto del 1° Grado"): inoltro mirato senza mai mostrare le proprie debolezze 10/10 agli amici o contatti diretti.'),
    (22, '22 - Scambio di beni, servizi e referenze (in-Lire Fluida HTLC): motore di retention e lead generation per circuiti esistenti (in-Lire e competitor).'),
    (23, '23 - Doppio binario transattivo: Ore-Palestra tra individui e Crediti B2B raccordati al Regime Fiscale richiesto in input iniziale.'),
    (24, '24 - Invio del profilo con R >> all\'Admin di CtD via NEXUS che, dopo verifica, lo incorpora nella lista di distribuzione della Community.')
]

# Struttura APERTA delle Puntate (puoi aggiungerne o modificarne quante vuoi in qualsiasi momento)
episodes = [
    {
        "num": 1,
        "date": "5 Novembre 2026",
        "title": "Il Manifesto: 3 Systems in 1 Platform (S = C + P + T + R)",
        "subtitle": "Come nasce una 'Serial Killer App' progettata per restituirti il controllo del futuro (Lancio Gennaio 2027)",
        "crop": (0, 0, 1920, 1080),
        "pts": list(range(1, 25)),
        "victim": "I software isolati in Cloud che standardizzano le persone, divorano energia ed espongono i tuoi segreti industriali.",
        "killer_feature": "3 Sistemi integrati in 1 sola Piattaforma 100% offline dentro il tuo Profilo aggiornato: 1° CtD Base (Diagnosi S=C+P+T+R) + 2° CtD 2°B (Secondo Cervello 21gg) + 3° CtD NE (Network Engineering Pull).",
        "payoff_persona": "Diventi padrone del tuo futuro con un Coach 100% privato sul tuo device che non vende mai i tuoi dati.",
        "payoff_prof": "Smetti di rincorrere clienti a freddo (Push) e vieni attivato in Pull grazie ai tuoi risultati certificati (R >>).",
        "payoff_pmi": "Unifichi diagnosi strategica, cantieri operativi L3 e ricerca riservata di partner a costo server zero.",
        "next_teaser": "Come si uccide l'angolo cieco del 'Non so cosa non so'? Scopriremo cosa accade premendo il pulsante del Cervello.",
        "body_paragraphs": [
            "Quando la Ferrari ha svelato la sua prima vettura elettrica, la Luce, molti osservatori hanno commesso l'errore di giudicarla dalle prime foto statiche cercando il vecchio motore termico. Chi poi si è seduto davvero al volante ha capito che non era un'auto tradizionale elettrificata, ma dieci auto diverse in una sola piattaforma, cucita intorno al guidatore.",
            "Negli ultimi due anni, lavorando in simbiosi con l'AI e capitalizzando oltre 50 anni di esperienza sul campo, abbiamo costruito qualcosa di altrettanto radicale nel software. Sarà disponibile a partire da Gennaio 2027, ma da oggi — attraverso questa serie aperta di puntate — vogliamo farvi sedere al volante di Connect the DOTS (CtD).",
            "L'abbiamo ribattezzata una 'Serial Killer App' perché i suoi 24 componenti brevettati eliminano serialmente le grandi illusioni del digitale e della consulenza a cui ci siamo rassegnati: l'AI su cloud che divora energia ed espone dati riservati, i finti guru autoreferenziali senza risultati certificati (R >>), le liste di To-Do scollegate dalla strategia e il networking Push fatto di chiamate a freddo.",
            "Con Connect the DOTS hai 3 Sistemi integrati in 1 sola Piattaforma (3 Systems in 1 Platform) che lavorano al 100% offline dentro il tuo Profilo aggiornato: 1° CtD Base (Core Diagnostico con formula S = C + P + T + R), 2° CtD 2°B (Secondo Cervello con Palestra di 21 Giorni) e 3° CtD NE (Network Engineering in modalità Pull)."
        ]
    },
    {
        "num": 2,
        "date": "7 Novembre 2026",
        "title": "Cervello, Orizzonti e Triage Diagnostico Causale",
        "subtitle": "Dal 'Non so cosa non so' all'individuazione matematica del Next Best Dot (NBD)",
        "crop": (15, 140, 670, 680),
        "pts": [1, 3, 4, 5, 8],
        "victim": "Il foglio bianco dei chatbot generativi (dove devi già sapere quale domanda fare) e le risposte probabilistiche con allucinazioni.",
        "killer_feature": "Regola aurea Cervello/Orizzonti (L0 -> L1 -> DOT L2 Problema) + Triage Diagnostico assistito con opzione 'Altro' (da specificare) + Proliferazione causale verso il DOT L3 Soluzione (NBD).",
        "payoff_persona": "Trasformi un disagio confuso nella causa radice esatta e nella prima azione concreta da compiere.",
        "payoff_prof": "Il cliente arriva da te avendo già qualificato il proprio bisogno sull'L3 Ancora, azzerando i tempi di pre-analisi.",
        "payoff_pmi": "Isoli in 3 minuti il vero collo di bottiglia operativo o finanziario senza allucinazioni da chatbot.",
        "next_teaser": "Cosa succede ai 900 nodi aziendali che non hai ancora esplorato? Scopriremo la SWOT in RAM e il tasto sovrano 'Pausa'.",
        "body_paragraphs": [
            "Il paradosso dei chatbot generativi tradizionali è che per ottenere una risposta utile devi già sapere quale domanda fare. Ma nella vita reale e in azienda i disastri nascono da due blocchi cognitivi precisi: 'Non so cosa non so, finché qualcuno non me lo fa notare' e 'Non so di cosa ho bisogno, finché qualcuno non mi presenta degli aiuti concreti'.",
            "In Connect the DOTS non ti trovi davanti a una casella vuota che aspetta un prompt, ma a una filosofia rigorosa: non puoi guardare fuori (Sinapsi) o buttarti nell'azione (Pratica) finché non hai capito dove sei partendo dal Cervello — oppure cliccando su Orizzonti per selezionare direttamente un altro ambito L0.",
            "Navigando tra circa 1.000 DOT fino al tuo DOT L2 Problema padre, apri il Triage Diagnostico: percorsi assistiti trasparenti con risposte pre-confezionate dagli SME più l'opzione 'Altro' (con invito a specificare). Senza mai ragionare per banale similarità statistica ma per nesso causale (NBD -> NBA -> NBM), CtD accende il tuo DOT L3 Soluzione (L3 Ancora)."
        ]
    },
    {
        "num": 3,
        "date": "9 Novembre 2026",
        "title": "SWOT in RAM (Ignoto = 10/10) e il Tasto Sovrano 'Pausa'",
        "subtitle": "Perché ciò che non conosci vale Rischio Massimo (e come spegnerlo con un clic per spendere tempo di qualità)",
        "crop": (15, 580, 670, 1075),
        "pts": [6, 7],
        "victim": "Le analisi SWOT statiche dimenticate nei PDF e i cruscotti tradizionali che guardano solo il fatturato ignorando gli angoli ciechi.",
        "killer_feature": "Algoritmo _healDatabaseRollups in RAM: ogni nodo ignoto = Debolezza 10/10 e Minaccia 10/10; tasto Pausa = reset a '0'; metriche oltre il fatturato + Regime Fiscale + Scudo Anonimizzazione AI.",
        "payoff_persona": "Azzeri il sovraccarico cognitivo mettendo in 'Pausa' ('0') ciò che non è prioritario per dedicarti solo a ciò che conta.",
        "payoff_prof": "Offri alle PMI clienti stress test e cruscotti predittivi in RAM su oltre 400 lenti direzionali.",
        "payoff_pmi": "Vedi in tempo reale dove si annidano le minacce 10/10 nei tuoi 8 orizzonti senza far uscire un byte dal tuo Mac/PC.",
        "next_teaser": "Perché bruciare gigawatt su server cloud per rielaborare risposte già note? Scopriremo l'Esperanto dei ~1.000 DOT.",
        "body_paragraphs": [
            "Nella gestione tradizionale, ciò che non conosciamo viene ignorato e considerato pari a zero, finché un giorno quell'angolo cieco esplode. In Connect the DOTS le analisi SWOT prendono i dati direttamente dalla memoria RAM (_healDatabaseRollups), dove ogni nodo non conosciuto o non intenzionalmente presidiato vale automaticamente Debolezza 10/10 e Minaccia 10/10.",
            "Per non restare schiacciati da tutto ciò che è scoperto, CtD introduce un comando sovrano: premendo il pulsante Pausa su un nodo, i suoi valori si resettano a '0' e il nodo esce da qualsiasi calcolo, permettendoti di spendere tempo di qualità solo sulle tue vere priorità.",
            "Tutto questo avviene governando qualsiasi metrica oltre il solo fatturato, acquisendo il Regime Fiscale in fase di input iniziale e proteggendo le domande a testo libero all'AI con lo Scudo di Anonimizzazione automatico nel tuo Profilo aggiornato 100% offline."
        ]
    },
    {
        "num": 4,
        "date": "11 Novembre 2026",
        "title": "L'Esperanto dei ~1.000 DOT e la Micro-Blockchain Offline",
        "subtitle": "Sostenibilità energetica Edge AI, conformità nativa GDPR / EU AI Act e integrità locale a costo server zero",
        "crop": (15, 140, 670, 1075),
        "pts": [2, 7, 16],
        "victim": "Lo spreco energetico dei data center AI Cloud e la Babele linguistica che impedisce a domanda e offerta di capirsi.",
        "killer_feature": "Knowledge Graph olografico di ~1.000 DOT ordinati (sort_order) come lingua franca ('Esperanto') + esecuzione 100% offline + catena crittografica SQLite (local_source_chain) a costo server zero.",
        "payoff_persona": "Navighi anche offline con latenza 0 ms e certezza matematica che il tuo Profilo aggiornato resti solo tuo.",
        "payoff_prof": "Parli finalmente lo stesso codice ('Esperanto') dei tuoi potenziali clienti sul nodo L3 della tua specializzazione.",
        "payoff_pmi": "Adotti l'AI in azienda azzerando rischi GDPR / EU AI Act e canoni ricorrenti di server e token cloud.",
        "next_teaser": "Capire il problema è inutile se il buon proposito muore in una lista di To-Do. Entreremo in 2° CtD 2°B: Secondo Cervello.",
        "body_paragraphs": [
            "Oggi milioni di utenti interrogano data center remoti bruciando quantità immense di energia per farsi rigenerare da zero risposte che gli esperti umani di dominio (SME) conoscono già. E quando una PMI cerca uno specialista, usano parole diverse e non si incontrano.",
            "Connect the DOTS capitalizza il sapere degli SME in un Knowledge Graph di circa 1.000 nodi in italiano chiaro ordinati con sort_order: un vero 'Esperanto' comune che abilita un'Intelligenza Relazionale ecologica e sostenibile, 100% offline e nativamente conforme a GDPR ed EU AI Act.",
            "Ogni avanzamento del tuo Profilo aggiornato viene inoltre blindato localmente da una mini micro-blockchain offline (local_source_chain su SQLite) che garantisce l'integrità anti-manomissione dei punteggi e dei certificati a costo server zero."
        ]
    },
    {
        "num": 5,
        "date": "13 Novembre 2026",
        "title": "2° Cervello: Proliferazione To-Do -> L3 Progetto & Sinapsi",
        "subtitle": "Come trasformare ogni compito in un cantiere strutturato collegato alla strategia",
        "crop": (650, 140, 1315, 660),
        "pts": [9, 10, 11, 12],
        "victim": "Il cimitero delle liste To-Do e dei project manager scollegati dagli obiettivi strategici.",
        "killer_feature": "Proliferazione automatica (To-Do / MIO_Idea -> L3 Progetto / MIO_Goal con parent_uuid verticale) + Sinapsi Orizzontali Bidirezionali (evolvedFrom / peerFlow in UserSynapseState) + Mattoni L3 tra stato P e traguardo T.",
        "payoff_persona": "Non perdi mai più il legame tra un'idea annotata al volo e il traguardo di vita a cui serve.",
        "payoff_prof": "Consegni ai clienti non un PDF teorico ma un cantiere L3 già scomposto in mattoni esecutivi.",
        "payoff_pmi": "Colleghi ogni singolo task operativo del team all'obiettivo strategico padre eliminando la dispersione.",
        "next_teaser": "Chi esegue materialmente ogni mattone del cantiere e chi certifica il risultato? Scopriremo la Palestra di 21 Giorni.",
        "body_paragraphs": [
            "Il secondo sistema integrato nella piattaforma — 2° CtD 2°B: Secondo Cervello — nasce per portare Persona, Professionista e PMI dalla teoria alla pratica, aiutandoli a diventare padroni del proprio futuro senza mai standardizzarne i fini.",
            "Quando crei un obiettivo (MIO_Goal / L3 Progetto) a partire da un'idea o da un To-Do pre-esistente, CtD mantiene intatta la gerarchia verticale nel database (parent_uuid) e genera in parallelo una Sinapsi Orizzontale Bidirezionale (MIEI <-> MIEI con relazione evolvedFrom o peerFlow in UserSynapseState).",
            "Sull'L3 Ancora trovi così già scomposti i mattoni operativi concreti che separano il tuo stato attuale (P) dal tuo traguardo (T)."
        ]
    },
    {
        "num": 6,
        "date": "15 Novembre 2026",
        "title": "Allocazione a 3 Vie, Palestra di 21 Giorni e Certificato PoR",
        "subtitle": "Dalla teoria alla pratica certificata con scudo crittografico 2-of-2 Multi-Sig",
        "crop": (650, 560, 1315, 1075),
        "pts": [13, 14, 15, 16],
        "victim": "I corsi di formazione che restano sulla carta e le metriche di risultato autodichiarate senza verifica.",
        "killer_feature": "Smistamento sovrano a 3 vie per ogni mattone (Fai-da-Te in Palestra / Vista 1 SME / Vista 2 Rete + 'Altro') + Palestra operativa di 21 giorni + Certificato Proof-of-Result (PoR 2-of-2 Multi-Sig).",
        "payoff_persona": "Costruisci un portafoglio inoppugnabile di certificati PoR su risultati reali raggiunti.",
        "payoff_prof": "Trasformi il tuo metodo in una Palestra di 21 giorni che garantisce la messa a terra da parte del cliente.",
        "payoff_pmi": "Decidi mattone per mattone cosa fare in casa e cosa delegare all'esterno misurando solo risultati veri.",
        "next_teaser": "Cosa accade quando il tuo parametro R su un DOT diventa altissimo (R >>)? Scopriremo la qualifica a Proven SME.",
        "body_paragraphs": [
            "Per ogni mattone del tuo cantiere L3, Connect the DOTS ti offre uno Smistamento Sovrano a 3 vie (più l'opzione 'Altro' da specificare): puoi eseguirlo in modalità Fai-da-Te nella Palestra, attivare la Vista 1 (Provider P&S / Proven SME on-demand) o coinvolgere la Vista 2 (la tua Rete di relazioni).",
            "Scegliendo la Palestra di 21 Giorni, affronti un percorso esecutivo quotidiano che trasforma la competenza in risultato reale e culmina nel Certificato Proof-of-Result (PoR) protetto da scudo crittografico a doppia firma (2-of-2 Multi-Sig), facendo crescere la variabile R nella formula S = C + P + T + R."
        ]
    },
    {
        "num": 7,
        "date": "17 Novembre 2026",
        "title": "Cordone Ombelicale 21gg e Qualifica Proven SME (R>>) NEXUS",
        "subtitle": "La fine dei finti guru: come i risultati reali ti portano i clienti in modalità Pull",
        "crop": (650, 560, 1905, 1075),
        "pts": [14, 15, 20, 24],
        "victim": "I finti guru da tastiera che vincono urlando sui social e l'abbandono del cliente dopo la sessione di consulenza.",
        "killer_feature": "Cordone Ombelicale di 21 giorni tra professionista (es. BNI Barbarossa) e migliori clienti + Qualifica automatica a Proven SME raggiungendo R >> + Cooptazione via NEXUS sull'L3 Ancora della Community.",
        "payoff_persona": "Anche senza budget pubblicitario, se eccelli su un DOT (R >>) vieni cooptato e reso visibile on-demand.",
        "payoff_prof": "Blindi i tuoi clienti attuali col Cordone Ombelicale di 21gg e ricevi nuovi incarichi in Pull sugli L3 dove hai R >>.",
        "payoff_pmi": "Attingi solo a Proven SME i cui risultati R >> sono stati certificati sul campo dalla piattaforma.",
        "next_teaser": "Come chiedi aiuto alla tua rete senza mai rivelare agli amici qual è la tua debolezza 10/10? Ecco il Salto del 1° Grado.",
        "body_paragraphs": [
            "La Palestra di 21 giorni crea un vero 'Cordone Ombelicale' che lega il professionista (ad esempio i membri di un Capitolo BNI come il Barbarossa) ai suoi migliori clienti, accompagnandoli nell'esecuzione quotidiana tra una sessione e l'altra.",
            "Inoltre, raggiungendo risultati reali eccellenti (R >>) su uno specifico DOT, CtD qualifica l'utente come 'Proven SME': con il suo consenso scritto, il profilo con R >> viene inviato via NEXUS all'Admin di CtD che, dopo verifica, lo incorpora nella lista di distribuzione on-demand cablata sull'L3 Ancora di tutta la Community."
        ]
    },
    {
        "num": 8,
        "date": "19 Novembre 2026",
        "title": "Network Engineering: Score Ponte e 'Salto del 1° Grado'",
        "subtitle": "Raggiungere il risolutore perfetto al 2° grado senza mai esporre le tue debolezze 10/10 ai contatti diretti",
        "crop": (1300, 140, 1905, 680),
        "pts": [17, 18, 19, 20, 21],
        "victim": "Il networking a freddo e l'imbarazzo di dover confessare le proprie debolezze 10/10 agli amici o contatti di 1° grado.",
        "killer_feature": "Grafo relazionale ir_contacts_graph ('chi mi ha presentato chi') + calcolo in RAM di Score Diretto vs Score Ponte + Capsule anonimizzate da 1 KB (.ctdir / QR) con Smart Source-Routing ('Salto del 1° Grado').",
        "payoff_persona": "Chiedi supporto su scelte delicate raggiungendo lo specialista di 2° grado in totale riservatezza.",
        "payoff_prof": "Valorizzi il tuo Score Ponte diventando lo snodo scientifico di referenze inter-capitolo ad alta conversione.",
        "payoff_pmi": "Trovi fornitori o manager per risolvere una criticità 10/10 senza che concorrenti o conoscenti sappiano del problema.",
        "next_teaser": "Trovato il match tra reti, professionisti e PMI, come ci si scambia valore anche senza bruciare cassa? Ecco l'HTLC a Doppio Binario.",
        "body_paragraphs": [
            "Il terzo sistema della piattaforma — 3° CtD NE: Network Engineering — ribalta il paradigma da Push a Pull grazie alla genealogia relazionale (ir_contacts_graph), che traccia 'chi mi ha presentato chi' attraverso Capitoli e network calcolando in tempo reale in RAM lo Score Diretto e lo Score Ponte.",
            "Quando hai una debolezza critica 10/10 che non vuoi mostrare agli amici o contatti diretti, il meccanismo Next Best Match (NBM) riservato invia una Capsula anonimizzata da 1 KB (.ctdir / QR) con Smart Source-Routing ('Salto del 1° Grado'), raggiungendo il risolutore di 2° grado senza mai esporre la tua vulnerabilità al 1° grado."
        ]
    },
    {
        "num": 9,
        "date": "21 Novembre 2026",
        "title": "Compensazione in-Lire Fluida (HTLC) a Doppio Binario",
        "subtitle": "Il motore di intersezione tra network (BNI, circuiti B2B, professionisti e PMI) raccordato al Regime Fiscale",
        "crop": (1300, 600, 1905, 1075),
        "pts": [22, 23, 24],
        "victim": "La separazione tra network diversi e la staticità dei circuiti di scambio usati come semplici cataloghi passivi.",
        "killer_feature": "Motore di retention, lead generation e intersezione cross-network + Compensazione in-Lire Fluida (HTLC) a Doppio Binario (Binario 1: Ore-Palestra tra individui | Binario 2: Crediti B2B tra imprese) + P2P Bonjour/AirDrop.",
        "payoff_persona": "Monetizzi il tuo tempo col Binario 1 (Ore-Palestra) ottenendo l'affiancamento di altri esperti senza esborsi.",
        "payoff_prof": "Incroci il tuo Capitolo professionale con la domanda qualificata delle aziende appartenenti ai circuiti B2B.",
        "payoff_pmi": "Finanzi i tuoi cantieri L3 tramite il Binario 2 (Crediti B2B), generando nuovi clienti e preservando la liquidità.",
        "next_teaser": "Quale sarà la prossima vittima della Serial Killer App? Segnalaci il tuo caso nel form Feedback su www.c-t-d.group/news.html!",
        "body_paragraphs": [
            "Lo scambio di beni, servizi e referenze in Connect the DOTS diventa un potente motore di retention, lead generation e intersezione tra circuiti esistenti (come in-Lire e oltre), Capitoli BNI, liberi professionisti, talenti e PMI.",
            "Ogni transazione è regolata dalla Compensazione in-Lire Fluida (HTLC) a Doppio Binario, raccordata fin dall'input iniziale al Regime Fiscale dell'utente: il Binario 1 (Ore-Palestra) per gli scambi tra individui e il Binario 2 (Crediti B2B) per le transazioni tra imprese."
        ]
    }
]

ss1_path = os.path.join(assets_dir, "ctd_plancia_ss1.png")
base_ss1 = Image.open(ss1_path).convert("RGB").resize((1920, 1080))

# Generazione Slide Master Pulita SS2 (per asset generale)
slide_ss2_master = Image.new("RGB", (1920, 1080), (10, 10, 14))
dm = ImageDraw.Draw(slide_ss2_master)
dm.text((60, 28), "Connect the DOTS — 3 Systems in 1 Platform (Lancio Gennaio 2027)", font=get_font(34, True), fill=(255, 255, 255))
dm.text((60, 72), "Riferimenti ai 24 Componenti della Value Proposition (1° CtD Base [1-8]  •  2° CtD 2°B [9-16]  •  3° CtD NE [17-24])", font=get_font(22, True), fill=(245, 197, 24))
ym = 115
for idx, line in vp_24_clean:
    col = (180, 225, 255) if idx <= 8 else ((255, 235, 150) if idx <= 16 else (170, 245, 195))
    dm.text((60, ym), line, font=get_font(19, False), fill=col)
    ym += 37
dm.text((60, 1028), "Confidential & Proprietary Information. Patents Pending. © 2026 Visimplement di Alberto Consani e C. SaS.  |  www.c-t-d.group/news.html", font=get_font(16, True), fill=(245, 197, 24))
slide_ss2_master.save(os.path.join(assets_dir, "ctd_legenda_ss2.png"))

def draw_wrapped_block(draw, x, y, max_w, text, font, fill, line_h):
    for ln in wrap_text(text, font, max_w, draw):
        draw.text((x, y), ln, font=font, fill=fill)
        y += line_h
    return y

for ep in episodes:
    ep_num = ep["num"]

    # ==========================================================================
    # SLIDE 1: "LA SLIDE CHE VALE 1.000 PAROLE" (Visual Spotlight + Triplo Payoff)
    # ==========================================================================
    s1 = Image.new("RGB", (1920, 1080), (10, 10, 15))
    ds1 = ImageDraw.Draw(s1)

    # Top Header
    ds1.rectangle([0, 0, 1920, 105], fill=(22, 16, 42))
    ds1.text((45, 16), f"🔪 ANATOMIA DI UNA SERIAL KILLER APP  •  PUNTATA #{ep_num:02d} ({ep['date']})  •  SERIE APERTA VERSO GENNAIO 2027", font=get_font(21, True), fill=(245, 197, 24))
    ds1.text((45, 48), ep["title"], font=get_font(33, True), fill=(255, 255, 255))

    # Left Box: High-Res Visual Zoom ("1 Immagine = 1.000 Parole")
    ds1.rectangle([40, 125, 900, 995], fill=(16, 16, 24), outline=(245, 197, 24), width=3)
    ds1.rectangle([40, 125, 900, 175], fill=(32, 24, 58))
    pts_str = "Tutti (1..24)" if len(ep["pts"]) > 10 else ", ".join(str(p) for p in ep["pts"])
    ds1.text((60, 138), f"🔍 FOCUS VISIVO SULLA PLANCIA CtD  •  Componenti attivati: [{pts_str}]", font=get_font(20, True), fill=(245, 197, 24))

    cropped = base_ss1.crop(ep["crop"])
    cw, ch = cropped.size
    scale = min(830 / cw, 780 / ch)
    nw, nh = int(cw * scale), int(ch * scale)
    resized = cropped.resize((nw, nh))
    s1.paste(resized, (55 + (830 - nw) // 2, 190 + (780 - nh) // 2))

    # Right Column: 3 Cards (Vittima Eliminata | Killer Feature CtD | Triplo Payoff)
    rx1, rx2 = 930, 1880
    rw = rx2 - rx1 - 40

    # Card A: Vittima Eliminata
    ds1.rectangle([rx1, 125, rx2, 305], fill=(36, 14, 20), outline=(239, 68, 68), width=2)
    ds1.text((rx1 + 20, 140), "❌ LA VITTIMA ELIMINATA (VECCHIO MONDO)", font=get_font(21, True), fill=(252, 165, 165))
    draw_wrapped_block(ds1, rx1 + 20, 175, rw, ep["victim"], get_font(20, False), (255, 235, 235), 28)

    # Card B: Killer Feature CtD
    ds1.rectangle([rx1, 325, rx2, 545], fill=(16, 28, 46), outline=(56, 189, 248), width=2)
    ds1.text((rx1 + 20, 340), "⚡ LA KILLER FEATURE CtD (COSA FAI AL VOLANTE DELL'APP)", font=get_font(21, True), fill=(56, 189, 248))
    draw_wrapped_block(ds1, rx1 + 20, 375, rw, ep["killer_feature"], get_font(20, False), (235, 248, 255), 28)

    # Card C: Triplo Payoff Differenziato
    ds1.rectangle([rx1, 565, rx2, 995], fill=(16, 34, 24), outline=(60, 208, 112), width=3)
    ds1.text((rx1 + 20, 580), "🎯 IL PAYOFF CONCRETO PER IL TUO PROFILO:", font=get_font(22, True), fill=(60, 208, 112))

    py = 620
    for badge_lbl, badge_col, p_txt in [
        ("👤 SE SEI UNA PERSONA O UN TALENTO:", (56, 189, 248), ep["payoff_persona"]),
        ("🎓 SE SEI UN PROFESSIONISTA / PROVEN SME (R >>):", (245, 197, 24), ep["payoff_prof"]),
        ("🏢 SE SEI UN IMPRENDITORE / PMI O NETWORK:", (192, 132, 252), ep["payoff_pmi"])
    ]:
        ds1.text((rx1 + 20, py), badge_lbl, font=get_font(19, True), fill=badge_col)
        py = draw_wrapped_block(ds1, rx1 + 20, py + 25, rw, p_txt, get_font(19, False), (240, 245, 240), 25) + 14

    # Bottom Bar
    ds1.rectangle([0, 1015, 1920, 1080], fill=(22, 16, 42))
    ds1.text((45, 1033), "👉 Scorri le slide per la Mappa Completa e la Timeline [✓]  •  Leggi la News integrale su: www.c-t-d.group/news.html", font=get_font(21, True), fill=(245, 197, 24))

    # Salva Slide 1 anche come immagine Hero per la pagina news.html
    hero_img_path = os.path.join(assets_dir, f"news_ep_{ep_num:02d}.png")
    s1.save(hero_img_path)

    # ==========================================================================
    # SLIDE 2: MAPPA GENERALE CON MIRINO ORO SUL QUADRANTE DELLA PUNTATA
    # ==========================================================================
    s2 = Image.new("RGB", (1920, 1080), (10, 10, 14))
    s2.paste(base_ss1.resize((1920, 990)), (0, 90))
    ds2 = ImageDraw.Draw(s2)
    ds2.rectangle([0, 0, 1920, 90], fill=(22, 16, 42))
    ds2.text((45, 16), f"DOVE SI COLLOCA NEI '3 SYSTEMS IN 1 PLATFORM'  •  PUNTATA #{ep_num:02d}", font=get_font(24, True), fill=(245, 197, 24))
    ds2.text((45, 50), f"Nel riquadro oro: i componenti [{pts_str}] approfonditi nella puntata di oggi", font=get_font(19, False), fill=(230, 230, 240))
    if len(ep["pts"]) < 24:
        cx1, cy1, cx2, cy2 = ep["crop"]
        sy1 = int(cy1 * (990 / 1080)) + 90
        sy2 = int(cy2 * (990 / 1080)) + 90
        ds2.rectangle([cx1, sy1, cx2, sy2], outline=(245, 197, 24), width=6)

    # ==========================================================================
    # SLIDE 3: I 24 COMPONENTI CON EVIDENZIAZIONE ORO DEI PUNTI DI OGGI
    # ==========================================================================
    s3 = Image.new("RGB", (1920, 1080), (10, 10, 14))
    ds3 = ImageDraw.Draw(s3)
    ds3.text((60, 26), f"I 24 Componenti della Value Proposition  •  Evidenziati i Punti della Puntata #{ep_num:02d}", font=get_font(31, True), fill=(255, 255, 255))
    ds3.text((60, 68), "I punti con freccia (►) in Oro brillante sono i protagonisti dell'episodio di oggi:", font=get_font(21, True), fill=(245, 197, 24))
    y3 = 112
    for idx, line in vp_24_clean:
        is_active = idx in ep["pts"]
        if is_active and len(ep["pts"]) < 24:
            ds3.rectangle([48, y3 - 3, 1875, y3 + 31], fill=(45, 34, 10), outline=(245, 197, 24), width=1)
            ds3.text((56, y3), "► " + line, font=get_font(19, True), fill=(245, 197, 24))
        else:
            col = (175, 215, 245) if idx <= 8 else ((235, 220, 155) if idx <= 16 else (165, 230, 190))
            ds3.text((60, y3), line, font=get_font(18, False), fill=col)
        y3 += 37
    ds3.text((60, 1028), "Archivio completo delle News e dei 24 Componenti su: www.c-t-d.group/news.html  |  www.c-t-d.group/founders.html", font=get_font(16, True), fill=(245, 197, 24))

    # ==========================================================================
    # SLIDE 4: TIMELINE PROGRESSIVA APERTA CON CHECK BOX VERDE [✓] + CTA NEWS
    # ==========================================================================
    s4 = Image.new("RGB", (1920, 1080), (10, 10, 14))
    ds4 = ImageDraw.Draw(s4)
    ds4.rectangle([0, 0, 1920, 105], fill=(22, 16, 42))
    ds4.text((50, 18), f"TIMELINE DELLA SERIE APERTA  •  PUNTATA #{ep_num:02d} ATTIVA (CHECK VERDI [✓] SULLE USCITE PUBBLICATE)", font=get_font(27, True), fill=(245, 197, 24))
    ds4.text((50, 58), "Ti sei perso una puntata? Leggi tutte le News integrali su www.c-t-d.group/news.html", font=get_font(20, False), fill=(210, 210, 225))

    ty = 118
    for item in episodes:
        num = item["num"]
        dt = item["date"]
        tit = item["title"]
        vic = item["victim"]
        is_done = num < ep_num
        is_curr = (num == ep_num)
        bg = (18, 42, 28) if is_done else ((44, 32, 12) if is_curr else (20, 20, 26))
        border = (60, 208, 112) if is_done else ((245, 197, 24) if is_curr else (45, 45, 58))
        ds4.rectangle([50, ty, 1870, ty + 68], fill=bg, outline=border, width=2)

        bx, by = 68, ty + 12
        if is_done:
            ds4.rectangle([bx, by, bx + 42, by + 42], fill=(60, 208, 112), outline=(255, 255, 255), width=2)
            ds4.text((bx + 9, by + 3), "✓", font=get_font(30, True), fill=(0, 0, 0))
            status_lbl = f"PUNTATA #{num:02d} ({dt}) — PUBBLICATA SU WWW.C-T-D.GROUP/NEWS.HTML"
            t_col = (140, 245, 175)
        elif is_curr:
            ds4.rectangle([bx, by, bx + 42, by + 42], fill=(245, 197, 24), outline=(255, 255, 255), width=2)
            ds4.text((bx + 10, by + 5), "★", font=get_font(26, True), fill=(0, 0, 0))
            status_lbl = f"PUNTATA #{num:02d} ({dt}) — IN EVIDENZA OGGI"
            t_col = (245, 197, 24)
        else:
            ds4.rectangle([bx, by, bx + 42, by + 42], fill=(28, 28, 36), outline=(110, 110, 130), width=2)
            ds4.text((bx + 12, by + 7), str(num), font=get_font(20, True), fill=(130, 130, 150))
            status_lbl = f"PUNTATA #{num:02d} ({dt}) — PROSSIMAMENTE"
            t_col = (155, 155, 170)

        ds4.text((130, ty + 8), f"{status_lbl}:  {tit}", font=get_font(20, True), fill=t_col)
        ds4.text((130, ty + 36), f"🔪 Elimina: {vic[:112]}", font=get_font(17, False), fill=(220, 220, 230))
        ty += 75

    # Riga Serie Aperta Dinamica
    ds4.rectangle([50, ty, 1870, ty + 64], fill=(20, 26, 44), outline=(56, 189, 248), width=2)
    ds4.text((70, ty + 10), "➕ SERIE APERTA IN CONTINUA EVOLUZIONE  •  NUOVE PUNTATE E CASI D'USO AGGIUNTI IN CORSA", font=get_font(20, True), fill=(56, 189, 248))
    ds4.text((70, ty + 36), "Quale problema o processo vorresti veder 'eliminato' nelle prossime puntate? Scrivicelo nel modulo Feedback su www.c-t-d.group/news.html!", font=get_font(17, False), fill=(225, 240, 255))

    # Footer CTA Early Adopter Gennaio 2027
    ds4.rectangle([50, 948, 1870, 1060], fill=(26, 16, 48), outline=(245, 197, 24), width=3)
    ds4.text((75, 960), "🎁 VUOI USARE CONNECT THE DOTS GRATIS (PER UN ANNO O PIÙ) A PARTIRE DA GENNAIO 2027?", font=get_font(23, True), fill=(245, 197, 24))
    ds4.text((75, 994), "Vai su www.c-t-d.group/news.html o founders.html • Lascia il tuo Feedback + la tua Email per la Newsletter delle puntate", font=get_font(19, False), fill=(255, 255, 255))
    ds4.text((75, 1024), "e blocca subito il tuo posto nel Programma Early Adopter (Persona • Professionista/Proven SME • Imprenditore/PMI • Network).", font=get_font(18, False), fill=(60, 208, 112))

    pdf_name = f"Carosello_LinkedIn_Puntata_{ep_num:02d}.pdf"
    s1.save(os.path.join(out_desktop_dir, pdf_name), "PDF", resolution=150.0, save_all=True, append_images=[s2, s3, s4])
    s1.save(os.path.join(caroselli_web_dir, pdf_name), "PDF", resolution=150.0, save_all=True, append_images=[s2, s3, s4])

print("OK: Generati tutti i Caroselli PDF a 4 Slide (con Slide 1 da 1.000 parole + Timeline Aperta)!")

# ==============================================================================
# GENERAZIONE DELLA PAGINA NEWS (news.html e en/news.html) SU WWW.C-T-D.GROUP
# ==============================================================================
def build_news_page(is_en=False):
    prefix = "../" if is_en else ""
    lang_switch = '<a href="../news.html" style="color: #FAE100; font-weight: bold;">IT</a>' if is_en else '<a href="en/news.html" style="color: #FAE100; font-weight: bold;">EN</a>'

    timeline_rows_html = ""
    articles_html = ""

    for ep in episodes:
        num = ep["num"]
        is_published = (num == 1)  # Puntata #01 pubblicata oggi, le altre pronte in calendario aperto
        badge_status = "✅ PUBBLICATA" if is_published else f"📌 IN USCITA ({ep['date']})"
        border_col = "var(--green-secure)" if is_published else "var(--accent-gold)"
        bg_row = "rgba(60, 208, 112, 0.1)" if is_published else "#181822"

        timeline_rows_html += f"""
                <a href="#news-ep-{num:02d}" style="text-decoration: none; display: block; padding: 13px 16px; background: {bg_row}; border-left: 4px solid {border_col}; border-radius: 6px; color: #fff; transition: transform 0.15s;">
                    <strong style="color: {border_col};">[{badge_status} • Puntata #{num:02d}]</strong> <strong>{ep['title']}</strong>
                    <span style="display: block; font-size: 0.82rem; color: var(--text-gray); margin-top: 3px;">🔪 Vittima eliminata: {ep['victim']}</span>
                </a>
        """

        paras = "".join(f"<p style='color: #dedee8; font-size: 0.98rem; line-height: 1.65; margin-bottom: 14px;'>{p}</p>" for p in ep["body_paragraphs"])
        pts_str = "Tutti (1..24)" if len(ep["pts"]) > 10 else ", ".join(str(p) for p in ep["pts"])

        articles_html += f"""
            <article id="news-ep-{num:02d}" style="background: #141419; border: 1px solid var(--border-color); border-top: 3px solid {border_col}; border-radius: 14px; padding: 28px; margin-bottom: 36px; box-shadow: 0 10px 30px rgba(0,0,0,0.45);">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 14px;">
                    <span style="background: #18112c; color: var(--accent-gold); border: 1px solid var(--accent-gold); padding: 5px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">
                        🔪 Puntata #{num:02d} • {ep['date']} • Componenti CtD: [{pts_str}]
                    </span>
                    <a href="{prefix}assets/caroselli/Carosello_LinkedIn_Puntata_{num:02d}.pdf" target="_blank" style="background: rgba(245, 197, 24, 0.15); color: var(--accent-gold); border: 1px solid var(--accent-gold); padding: 6px 14px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; text-decoration: none;">
                        📥 Scarica il Carosello PDF (4 Slide)
                    </a>
                </div>

                <h2 style="color: #ffffff; font-size: 1.75rem; margin: 0 0 6px 0;">{ep['title']}</h2>
                <p style="color: var(--accent-gold); font-size: 1.02rem; font-weight: 600; margin: 0 0 20px 0;">{ep['subtitle']}</p>

                <!-- LA SLIDE CHE VALE 1.000 PAROLE -->
                <div style="margin-bottom: 24px; border-radius: 10px; overflow: hidden; border: 1px solid #2c2c3a;">
                    <img src="{prefix}assets/news_ep_{num:02d}.png" alt="Slide 1000 Parole - Puntata {num:02d}" style="width: 100%; height: auto; display: block;" loading="lazy" />
                </div>

                {paras}

                <!-- TRIPLO PAYOFF DIFFERENZIATO -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; margin: 22px 0;">
                    <div style="background: #101824; border: 1px solid #38bdf8; border-radius: 8px; padding: 14px;">
                        <strong style="color: #38bdf8; font-size: 0.82rem; text-transform: uppercase; display: block; margin-bottom: 6px;">👤 Payoff Persona &amp; Talento</strong>
                        <p style="color: #e2e8f0; font-size: 0.88rem; margin: 0;">{ep['payoff_persona']}</p>
                    </div>
                    <div style="background: #1f190c; border: 1px solid var(--accent-gold); border-radius: 8px; padding: 14px;">
                        <strong style="color: var(--accent-gold); font-size: 0.82rem; text-transform: uppercase; display: block; margin-bottom: 6px;">🎓 Payoff Professionista / Proven SME</strong>
                        <p style="color: #fef9c3; font-size: 0.88rem; margin: 0;">{ep['payoff_prof']}</p>
                    </div>
                    <div style="background: #1a1228; border: 1px solid #b085f5; border-radius: 8px; padding: 14px;">
                        <strong style="color: #b085f5; font-size: 0.82rem; text-transform: uppercase; display: block; margin-bottom: 6px;">🏢 Payoff Imprenditore, PMI &amp; Network</strong>
                        <p style="color: #f3e8ff; font-size: 0.88rem; margin: 0;">{ep['payoff_pmi']}</p>
                    </div>
                </div>

                <div style="background: #18112c; border-left: 4px solid var(--accent-gold); padding: 12px 16px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                    <span style="font-size: 0.88rem; color: #dedee8;"><strong>🔪 Prossima Puntata:</strong> {ep['next_teaser']}</span>
                    <a href="#early-adopter-feedback-box" style="background: var(--accent-gold); color: #000; font-weight: 800; font-size: 0.84rem; padding: 8px 16px; border-radius: 6px; text-decoration: none;">
                        🎁 Lascia Feedback &amp; Prenota 1 Anno+ Gratis
                    </a>
                </div>
            </article>
        """

    return f"""<!DOCTYPE html>
<html lang="{'en' if is_en else 'it'}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connect the DOTS (CtD) - News &amp; Serie "Serial Killer App" (Verso Gennaio 2027)</title>
    <link rel="stylesheet" href="{prefix}style.css">
    <style>
        :root {{
            --bg-dark: #0a0a0d;
            --card-bg: #141419;
            --accent-gold: #f5c518;
            --accent-purple: #7042d2;
            --accent-purple-light: #b085f5;
            --text-gray: #a0a0aa;
            --border-color: #242038;
            --green-secure: #3cd070;
        }}
        body {{
            background-color: var(--bg-dark);
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <header>
        <nav class="main-nav">
            <a href="{prefix}index.html" class="nav-logo">Connect the DOTS (CtD)</a>
            <div class="nav-links">
                <a href="{prefix}index.html">Home</a>
                <a href="{prefix}platform.html">Platform</a>
                <a href="{prefix}services.html">Services</a>
                <a href="{prefix}business.html">Business</a>
                <a href="{prefix}news.html" class="active" style="color: var(--accent-gold); font-weight: 800;">News &amp; Serie</a>
                <a href="{prefix}founders.html">Founders</a>
                <a href="{prefix}leadership.html">Leadership</a>
                | {lang_switch}
            </div>
        </nav>
    </header>

    <main style="max-width: 1080px; margin: 40px auto; padding: 0 20px;">
        <div style="text-align: center; margin-bottom: 36px;">
            <div style="display: inline-flex; align-items: center; background: #18112c; color: var(--accent-gold); border: 1px solid var(--accent-gold); padding: 6px 18px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; margin-bottom: 14px;">
                🔪 Serie Aperta Verso il Lancio di Gennaio 2027 • 1 Slide da 1.000 Parole per Puntata
            </div>
            <h1 style="font-size: 2.4rem; margin: 0 0 12px 0; color: #fff;">News &amp; Puntate: <span style="color: var(--accent-gold);">"Anatomia di una Serial Killer App"</span></h1>
            <p style="color: var(--text-gray); max-width: 860px; margin: 0 auto; font-size: 1.02rem;">
                Segui qui tutte le puntate della serie LinkedIn in formato articolo integrale, scarica i Caroselli PDF con la <strong>Slide che vale 1.000 parole</strong> e lascia il tuo feedback per assicurarti la <strong>Licenza Gratuita Estesa (per un anno o più)</strong> al lancio di <strong>Gennaio 2027</strong>.
            </p>
        </div>

        <!-- TIMELINE INTERATTIVA APERTA CON CHECK BOX VERDE -->
        <section style="background: #141419; border: 1px solid var(--border-color); border-radius: 14px; padding: 24px; margin-bottom: 40px;">
            <h3 style="color: var(--accent-gold); margin: 0 0 8px 0; font-size: 1.3rem;">📋 Timeline Interattiva delle Puntate (Struttura Aperta)</h3>
            <p style="color: var(--text-gray); font-size: 0.9rem; margin: 0 0 16px 0;">
                Clicca su qualsiasi puntata per leggere subito la News completa, oppure proponi nel modulo in fondo quale problema vorresti veder affrontato nelle prossime uscite:
            </p>
            <div style="display: grid; gap: 10px;">
                {timeline_rows_html}
                <div style="padding: 13px 16px; background: rgba(56, 189, 248, 0.1); border-left: 4px solid #38bdf8; border-radius: 6px; color: #e0f2fe;">
                    <strong style="color: #38bdf8;">[➕ CANTIERE APERTO — PROSSIME PUNTATE SU RICHIESTA]</strong> Nuovi episodi e casi d'uso aggiunti in corsa anche a partire dai vostri feedback!
                </div>
            </div>
        </section>

        <!-- ARTICOLI INTEGRALI DELLE PUNTATE -->
        <section>
            {articles_html}
        </section>

        <!-- BOX FEEDBACK + NEWSLETTER PER LICENZA GRATUITA ESTESA GENNAIO 2027 -->
        <section id="early-adopter-feedback-box" style="background: #141419; border: 2px solid var(--accent-gold); border-radius: 14px; padding: 30px; margin-top: 40px;">
            <h2 style="color: #fff; font-size: 1.7rem; margin: 0 0 10px 0;">🎁 Lascia il Tuo Feedback, Iscriviti alla Newsletter e Assicurati 1 Anno+ Gratis da Gennaio 2027</h2>
            <p style="color: var(--text-gray); font-size: 0.95rem; margin-bottom: 20px;">
                Chi partecipa lasciando un feedback sulle puntate (o suggerendo il prossimo argomento della serie aperta) insieme alla propria email per la newsletter si assicura l'accesso al <strong>Programma Early Adopter di Gennaio 2027 con licenza gratuita estesa (per un anno o più)</strong>.
            </p>
            <form onsubmit="submitNewsFeedback(event)" style="display: grid; gap: 14px;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px;">
                    <input type="text" id="nw-name" required placeholder="Nome e Cognome *" style="width:100%; padding:12px; border-radius:6px; border:1px solid #333; background:#0c0c10; color:#fff; box-sizing:border-box;">
                    <input type="email" id="nw-email" required placeholder="La tua Email (per Newsletter & Licenza Gratis 1 Anno+) *" style="width:100%; padding:12px; border-radius:6px; border:1px solid #333; background:#0c0c10; color:#fff; box-sizing:border-box;">
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px;">
                    <select id="nw-role" onchange="document.getElementById('nw-other-wrap').style.display=(this.value==='Altro'?'block':'none')" style="width:100%; padding:12px; border-radius:6px; border:1px solid #333; background:#0c0c10; color:#fff; box-sizing:border-box;">
                        <option value="Persona / Talento / Executive">1. Persona / Talento / Executive</option>
                        <option value="Professionista / Consulente / Aspirante Proven SME (R>>)">2. Professionista / Consulente / Aspirante Proven SME (R&gg;)</option>
                        <option value="Imprenditore / PMI (SME)">3. Imprenditore / PMI (SME)</option>
                        <option value="Network (Capitolo BNI) / Circuito B2B (es. in-Lire)">4. Network (Capitolo BNI) / Circuito B2B (es. in-Lire)</option>
                        <option value="Advisory Firm / Corporate / Investitore">5. Advisory Firm / Corporate / Investitore</option>
                        <option value="Altro">Altro (specificare sotto)</option>
                    </select>
                    <input type="text" id="nw-topic" placeholder="Su quale Puntata o nuova funzione vuoi dare feedback?" style="width:100%; padding:12px; border-radius:6px; border:1px solid #333; background:#0c0c10; color:#fff; box-sizing:border-box;">
                </div>
                <div id="nw-other-wrap" style="display:none;">
                    <input type="text" id="nw-role-other" placeholder="Hai scelto 'Altro': specifica qui il tuo profilo o esigenza..." style="width:100%; padding:12px; border-radius:6px; border:1px solid #38bdf8; background:#0c0c10; color:#fff; box-sizing:border-box;">
                </div>
                <textarea id="nw-msg" required rows="3" placeholder="Scrivi qui il tuo feedback o suggerisci la prossima 'vittima' da eliminare nella serie aperta..." style="width:100%; padding:12px; border-radius:6px; border:1px solid #333; background:#0c0c10; color:#fff; box-sizing:border-box;"></textarea>
                <button type="submit" style="background: var(--accent-gold); color: #000; font-weight: 800; font-size: 1rem; padding: 14px 24px; border: none; border-radius: 8px; cursor: pointer;">
                    ✅ Invia Feedback, Iscriviti alla Newsletter e Blocca la Licenza Gratuita Estesa (Gennaio 2027)
                </button>
            </form>
        </section>
    </main>

    <footer>
        <p>&copy; 2026 Connect the DOTS (CtD). Tutti i diritti riservati. Brevetto per Invenzione Industriale n. 102025000001002.</p>
    </footer>

    <script>
        function submitNewsFeedback(e) {{
            e.preventDefault();
            var name = document.getElementById('nw-name').value;
            var email = document.getElementById('nw-email').value;
            var role = document.getElementById('nw-role').value;
            if (role === 'Altro') role = 'Altro: ' + document.getElementById('nw-role-other').value;
            var topic = document.getElementById('nw-topic').value;
            var msg = document.getElementById('nw-msg').value;
            var subj = encodeURIComponent('Feedback News & Early Adopter Gennaio 2027 - ' + name);
            var body = encodeURIComponent('Nome: ' + name + '\\nEmail: ' + email + '\\nProfilo: ' + role + '\\nPuntata/Tema: ' + topic + '\\n\\nFeedback:\\n' + msg);
            window.location.href = 'mailto:alberto.consani@gmail.com?subject=' + subj + '&body=' + body;
        }}
    </script>
</body>
</html>"""

open(os.path.join(repo, "news.html"), "w", encoding="utf-8").write(build_news_page(is_en=False))
open(os.path.join(repo, "en", "news.html"), "w", encoding="utf-8").write(build_news_page(is_en=True))
print("OK: Generate news.html e en/news.html!")

# Aggiunta link "News & Serie" nella barra di navigazione di tutte le pagine del sito
for root_dir, _, files in os.walk(repo):
    if "/.git" in root_dir:
        continue
    for fn in sorted(files):
        if not fn.endswith(".html") or fn == "news.html":
            continue
        p = os.path.join(root_dir, fn)
        txt = open(p, encoding="utf-8").read()
        if 'href="news.html"' not in txt:
            txt = txt.replace('<a href="founders.html">', '<a href="news.html" style="color: var(--accent-gold); font-weight: 700;">News &amp; Serie</a>\n                <a href="founders.html">')
            open(p, "w", encoding="utf-8").write(txt)

print("OK: Link 'News & Serie' aggiunto alla navbar di tutte le pagine!")
