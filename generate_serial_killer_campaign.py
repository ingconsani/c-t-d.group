import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

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

def draw_wrapped_block(draw, x, y, max_w, text, font, fill, line_h):
    for ln in wrap_text(text, font, max_w, draw):
        draw.text((x, y), ln, font=font, fill=fill)
        y += line_h
    return y

def draw_speech_bubble(draw, box, tail_tip, fill_color, outline_color, width=3):
    x1, y1, x2, y2 = box
    tx, ty = tail_tip
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    # Coda direzionale del fumetto verso il centro grafico
    if ty > y2:
        pts = [(cx - 18, y2 - 4), (cx + 18, y2 - 4), (tx, ty)]
    elif ty < y1:
        pts = [(cx - 18, y1 + 4), (cx + 18, y1 + 4), (tx, ty)]
    elif tx > x2:
        pts = [(x2 - 4, cy - 16), (x2 - 4, cy + 16), (tx, ty)]
    else:
        pts = [(x1 + 4, cy - 16), (x1 + 4, cy + 16), (tx, ty)]
    draw.polygon(pts, fill=outline_color)
    draw.rounded_rectangle(box, radius=18, fill=fill_color, outline=outline_color, width=width)

def draw_badge_pill(draw, x, y, text, bg_color, text_color=(0, 0, 0), font_size=16):
    f = get_font(font_size, True)
    bbox = draw.textbbox((0, 0), text, font=f)
    w = (bbox[2] - bbox[0]) + 24
    h = (bbox[3] - bbox[1]) + 12
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=bg_color)
    draw.text((x + 12, y + 4), text, font=f, fill=text_color)
    return x + w

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

episodes = [
    {
        "num": 0,
        "date": "5 Novembre 2026",
        "title": "IL TRAILER: Come raccontare la prima 'App-non-App'?",
        "subtitle": "Uso esteso dell'AI ma 100% Offline • 24 Funzioni in 3 Sistemi • Utenti P & B • Nativamente GDPR & EU AI Act Compliant",
        "crop": (0, 0, 1920, 1080),
        "pts": list(range(1, 25)),
        "victim": "L'impossibilità di spiegare una piattaforma rivoluzionaria di 24 componenti con un singolo post o una brochure tradizionale.",
        "killer_feature": "Una serie aperta ('Anatomia di una Serial Killer App'): ogni puntata isola 1 funzione con 1 Slide da 1.000 parole, Timeline [✓], Triplo Payoff (P / Prof / B) e 1 Anno+ Gratis da Gennaio 2027 per chi dà feedback.",
        "payoff_persona": "Scopri passo dopo passo come usare un Coach privato e un Secondo Cervello offline senza cedere i tuoi dati al cloud.",
        "payoff_prof": "Scopri come fidelizzare i tuoi clienti per 21 giorni e farti scegliere in modalità Pull grazie ai tuoi risultati certificati (R >>).",
        "payoff_pmi": "Scopri come unificare SWOT in RAM, cantieri operativi L3 e intersezioni di rete B2B a costo server zero.",
        "next_teaser": "Puntata #01: Il Manifesto dei '3 Systems in 1 Platform' e l'equazione deterministica S = C + P + T + R.",
        "body_paragraphs": [
            "Di fronte alla necessità di presentare la prima vera 'App-non-App' sul mercato — capace di fare un uso esteso dell'Intelligenza Artificiale ma 100% offline, ricca di 24 funzionalità diverse distribuite su 3 sistemi integrati, progettata contemporaneamente per utenti P (Persona) e B (Business) e nativamente conforme a EU AI Act e GDPR — ci siamo chiesti: come possiamo farla comprendere davvero senza sommergere chi legge?",
            "Così abbiamo ideato quello che state per vedere: 'Anatomia di una Serial Killer App', una serie aperta di puntate in vista del lancio ufficiale di Gennaio 2027. In ogni episodio ci siederemo al volante di una singola funzionalità applicativa, mostrando quale vecchia illusione del mercato viene 'eliminata' e quale vantaggio concreto ottiene chi usa Connect the DOTS.",
            "Ogni puntata è accompagnata da una Slide che vale 1.000 parole, da una Timeline progressiva con Check Box Verde [✓] per recuperare gli episodi passati qui nella sezione News di www.c-t-d.group, e da un patto con i lettori: chi lascia il proprio feedback insieme alla mail per la newsletter si assicura una versione gratuita per un anno o più nel Programma Early Adopter di Gennaio 2027."
        ]
    },
    {
        "num": 1,
        "date": "7 Novembre 2026",
        "title": "Il Manifesto: 3 Systems in 1 Platform (S = C + P + T + R)",
        "subtitle": "Come funzionano i 3 motori integrati nel tuo Profilo aggiornato 100% offline (Lancio Gennaio 2027)",
        "crop": (0, 0, 1920, 1080),
        "pts": list(range(1, 25)),
        "victim": "I software isolati in Cloud che standardizzano le persone, divorano energia ed espongono i tuoi segreti industriali.",
        "killer_feature": "3 Sistemi integrati in 1 sola Piattaforma 100% offline dentro il tuo Profilo aggiornato: 1° CtD Base (Diagnosi S=C+P+T+R) + 2° CtD 2°B (Secondo Cervello 21gg) + 3° CtD NE (Network Engineering Pull).",
        "payoff_persona": "Diventi padrone del tuo futuro con un Coach 100% privato sul tuo device che non vende mai i tuoi dati.",
        "payoff_prof": "Smetti di rincorrere clienti a freddo (Push) e vieni attivato in Pull grazie ai tuoi risultati certificati (R >>).",
        "payoff_pmi": "Unifichi diagnosi strategica, cantieri operativi L3 e ricerca riservata di partner a costo server zero.",
        "next_teaser": "Puntata #02: Come si uccide l'angolo cieco del 'Non so cosa non so'? Cosa accade premendo il pulsante del Cervello.",
        "body_paragraphs": [
            "Quando la Ferrari ha svelato la sua prima vettura elettrica, la Luce, molti osservatori hanno commesso l'errore di giudicarla dalle prime foto statiche cercando il vecchio motore termico. Chi poi si è seduto davvero al volante ha capito che non era un'auto tradizionale elettrificata, ma dieci auto diverse in una sola piattaforma, cucita intorno al guidatore.",
            "Con Connect the DOTS hai 3 Sistemi integrati in 1 sola Piattaforma (3 Systems in 1 Platform) che lavorano al 100% offline dentro il tuo Profilo aggiornato: 1° CtD Base (Core Diagnostico con formula S = C + P + T + R), 2° CtD 2°B (Secondo Cervello con Palestra di 21 Giorni) e 3° CtD NE (Network Engineering in modalità Pull)."
        ]
    },
    {
        "num": 2,
        "date": "9 Novembre 2026",
        "title": "Cervello, Orizzonti e Triage Diagnostico Causale",
        "subtitle": "Dal 'Non so cosa non so' all'individuazione matematica del Next Best Dot (NBD)",
        "crop": (15, 140, 670, 680),
        "pts": [1, 3, 4, 5, 8],
        "victim": "Il foglio bianco dei chatbot generativi (dove devi già sapere quale domanda fare) e le risposte probabilistiche con allucinazioni.",
        "killer_feature": "Regola aurea Cervello/Orizzonti (L0 -> L1 -> DOT L2 Problema) + Triage Diagnostico assistito con opzione 'Altro' (da specificare) + Proliferazione causale verso il DOT L3 Soluzione (NBD).",
        "payoff_persona": "Trasformi un disagio confuso nella causa radice esatta e nella prima azione concreta da compiere.",
        "payoff_prof": "Il cliente arriva da te avendo già qualificato il proprio bisogno sull'L3 Ancora, azzerando i tempi di pre-analisi.",
        "payoff_pmi": "Isoli in 3 minuti il vero collo di bottiglia operativo o finanziario senza allucinazioni da chatbot.",
        "next_teaser": "Puntata #03: Cosa succede ai 900 nodi aziendali che non hai ancora esplorato? Scopriremo la SWOT in RAM e il tasto 'Pausa'.",
        "body_paragraphs": [
            "In Connect the DOTS non ti trovi davanti a una casella vuota che aspetta un prompt, ma a una filosofia rigorosa: non puoi guardare fuori (Sinapsi) o buttarti nell'azione (Pratica) finché non hai capito dove sei partendo dal Cervello — oppure cliccando su Orizzonti per selezionare direttamente un altro ambito L0.",
            "Navigando tra circa 1.000 DOT fino al tuo DOT L2 Problema padre, apri il Triage Diagnostico: percorsi assistiti trasparenti con risposte pre-confezionate dagli SME più l'opzione 'Altro' (con invito a specificare). Senza mai ragionare per banale similarità statistica ma per nesso causale (NBD -> NBA -> NBM), CtD accende il tuo DOT L3 Soluzione (L3 Ancora)."
        ]
    },
    {
        "num": 3,
        "date": "11 Novembre 2026",
        "title": "SWOT in RAM (Ignoto = 10/10) e il Tasto Sovrano 'Pausa'",
        "subtitle": "Perché ciò che non conosci vale Rischio Massimo (e come spegnerlo con un clic per spendere tempo di qualità)",
        "crop": (15, 580, 670, 1075),
        "pts": [6, 7],
        "victim": "Le analisi SWOT statiche dimenticate nei PDF e i cruscotti tradizionali che guardano solo il fatturato ignorando gli angoli ciechi.",
        "killer_feature": "Algoritmo _healDatabaseRollups in RAM: ogni nodo ignoto = Debolezza 10/10 e Minaccia 10/10; tasto Pausa = reset a '0'; metriche oltre il fatturato + Regime Fiscale + Scudo Anonimizzazione AI.",
        "payoff_persona": "Azzeri il sovraccarico cognitivo mettendo in 'Pausa' ('0') ciò che non è prioritario per dedicarti solo a ciò che conta.",
        "payoff_prof": "Offri alle PMI clienti stress test e cruscotti predittivi in RAM su oltre 400 lenti direzionali.",
        "payoff_pmi": "Vedi in tempo reale dove si annidano le minacce 10/10 nei tuoi 8 orizzonti senza far uscire un byte dal tuo Mac/PC.",
        "next_teaser": "Puntata #04: Perché bruciare gigawatt su server cloud per rielaborare risposte già note? Scopriremo l'Esperanto dei ~1.000 DOT.",
        "body_paragraphs": [
            "In Connect the DOTS le analisi SWOT prendono i dati direttamente dalla memoria RAM (_healDatabaseRollups), dove ogni nodo non conosciuto o non intenzionalmente presidiato vale automaticamente Debolezza 10/10 e Minaccia 10/10.",
            "Premendo il pulsante Pausa su un nodo, i suoi valori si resettano a '0' e il nodo esce da qualsiasi calcolo, permettendoti di spendere tempo di qualità solo sulle tue vere priorità, governando qualsiasi metrica oltre il solo fatturato con Regime Fiscale iniziale e Scudo di Anonimizzazione AI."
        ]
    },
    {
        "num": 4,
        "date": "13 Novembre 2026",
        "title": "L'Esperanto dei ~1.000 DOT e la Micro-Blockchain Offline",
        "subtitle": "Sostenibilità energetica Edge AI, conformità nativa GDPR / EU AI Act e integrità locale a costo server zero",
        "crop": (15, 140, 670, 1075),
        "pts": [2, 7, 16],
        "victim": "Lo spreco energetico dei data center AI Cloud e la Babele linguistica che impedisce a domanda e offerta di capirsi.",
        "killer_feature": "Knowledge Graph olografico di ~1.000 DOT ordinati (sort_order) come lingua franca ('Esperanto') + esecuzione 100% offline + catena crittografica SQLite (local_source_chain) a costo server zero.",
        "payoff_persona": "Navighi anche offline con latenza 0 ms e certezza matematica che il tuo Profilo aggiornato resti solo tuo.",
        "payoff_prof": "Parli finalmente lo stesso codice ('Esperanto') dei tuoi potenziali clienti sul nodo L3 della tua specializzazione.",
        "payoff_pmi": "Adotti l'AI in azienda azzerando rischi GDPR / EU AI Act e canoni ricorrenti di server e token cloud.",
        "next_teaser": "Puntata #05: Capire il problema è inutile se il buon proposito muore in una lista di To-Do. Entreremo in 2° CtD 2°B: Secondo Cervello.",
        "body_paragraphs": [
            "Connect the DOTS capitalizza il sapere degli SME in un Knowledge Graph di circa 1.000 nodi in italiano chiaro ordinati con sort_order: un vero 'Esperanto' comune che abilita un'Intelligenza Relazionale ecologica e sostenibile, 100% offline e nativamente conforme a GDPR ed EU AI Act.",
            "Ogni avanzamento del tuo Profilo aggiornato viene inoltre blindato localmente da una mini micro-blockchain offline (local_source_chain su SQLite) a costo server zero."
        ]
    },
    {
        "num": 5,
        "date": "15 Novembre 2026",
        "title": "2° Cervello: Proliferazione To-Do -> L3 Progetto & Sinapsi",
        "subtitle": "Come trasformare ogni compito in un cantiere strutturato collegato alla strategia",
        "crop": (650, 140, 1315, 660),
        "pts": [9, 10, 11, 12],
        "victim": "Il cimitero delle liste To-Do e dei project manager scollegati dagli obiettivi strategici.",
        "killer_feature": "Proliferazione automatica (To-Do / MIO_Idea -> L3 Progetto / MIO_Goal con parent_uuid verticale) + Sinapsi Orizzontali Bidirezionali (evolvedFrom / peerFlow in UserSynapseState) + Mattoni L3 tra stato P e traguardo T.",
        "payoff_persona": "Non perdi mai più il legame tra un'idea annotata al volo e il traguardo di vita a cui serve.",
        "payoff_prof": "Consegni ai clienti non un PDF teorico ma un cantiere L3 già scomposto in mattoni esecutivi.",
        "payoff_pmi": "Colleghi ogni singolo task operativo del team all'obiettivo strategico padre eliminando la dispersione.",
        "next_teaser": "Puntata #06: Chi esegue materialmente ogni mattone del cantiere e chi certifica il risultato? Scopriremo la Palestra di 21 Giorni.",
        "body_paragraphs": [
            "Quando crei un obiettivo (MIO_Goal / L3 Progetto) a partire da un'idea o da un To-Do pre-esistente, CtD mantiene intatta la gerarchia verticale nel database (parent_uuid) e genera in parallelo una Sinapsi Orizzontale Bidirezionale (MIEI <-> MIEI con relazione evolvedFrom o peerFlow in UserSynapseState), scomponendo i passi pratici che separano P da T."
        ]
    },
    {
        "num": 6,
        "date": "17 Novembre 2026",
        "title": "Allocazione a 3 Vie, Palestra di 21 Giorni e Certificato PoR",
        "subtitle": "Dalla teoria alla pratica certificata con scudo crittografico 2-of-2 Multi-Sig",
        "crop": (650, 560, 1315, 1075),
        "pts": [13, 14, 15, 16],
        "victim": "I corsi di formazione che restano sulla carta e le metriche di risultato autodichiarate senza verifica.",
        "killer_feature": "Smistamento sovrano a 3 vie per ogni mattone (Fai-da-Te in Palestra / Vista 1 SME / Vista 2 Rete + 'Altro') + Palestra operativa di 21 giorni + Certificato Proof-of-Result (PoR 2-of-2 Multi-Sig).",
        "payoff_persona": "Costruisci un portafoglio inoppugnabile di certificati PoR su risultati reali raggiunti.",
        "payoff_prof": "Trasformi il tuo metodo in una Palestra di 21 giorni che garantisce la messa a terra da parte del cliente.",
        "payoff_pmi": "Decidi mattone per mattone cosa fare in casa e cosa delegare all'esterno misurando solo risultati veri.",
        "next_teaser": "Puntata #07: Cosa accade quando il tuo parametro R su un DOT diventa altissimo (R >>)? Scopriremo la qualifica a Proven SME.",
        "body_paragraphs": [
            "Per ogni mattone del tuo cantiere L3 hai uno Smistamento Sovrano a 3 vie (Fai-da-Te in Palestra, Vista 1 Provider P&S / Proven SME, Vista 2 Rete IR + 'Altro'). La Palestra di 21 Giorni culmina nel Certificato Proof-of-Result (PoR) con scudo crittografico 2-of-2 Multi-Sig."
        ]
    },
    {
        "num": 7,
        "date": "19 Novembre 2026",
        "title": "Cordone Ombelicale 21gg e Qualifica Proven SME (R>>) NEXUS",
        "subtitle": "La fine dei finti guru: come i risultati reali ti portano i clienti in modalità Pull",
        "crop": (650, 560, 1905, 1075),
        "pts": [14, 15, 20, 24],
        "victim": "I finti guru da tastiera che vincono urlando sui social e l'abbandono del cliente dopo la sessione di consulenza.",
        "killer_feature": "Cordone Ombelicale di 21 giorni tra professionista (es. BNI Barbarossa) e migliori clienti + Qualifica automatica a Proven SME raggiungendo R >> + Cooptazione via NEXUS sull'L3 Ancora della Community.",
        "payoff_persona": "Anche senza budget pubblicitario, se eccelli su un DOT (R >>) vieni cooptato e reso visibile on-demand.",
        "payoff_prof": "Blindi i tuoi clienti attuali col Cordone Ombelicale di 21gg e ricevi nuovi incarichi in Pull sugli L3 dove hai R >>.",
        "payoff_pmi": "Attingi solo a Proven SME i cui risultati R >> sono stati certificati sul campo dalla piattaforma.",
        "next_teaser": "Puntata #08: Come chiedi aiuto alla tua rete senza mai rivelare agli amici qual è la tua debolezza 10/10? Ecco il Salto del 1° Grado.",
        "body_paragraphs": [
            "La Palestra di 21 giorni crea un 'Cordone Ombelicale' che lega il professionista ai suoi migliori clienti. Raggiungendo R >> su un DOT, CtD qualifica l'utente come Proven SME per essere cooptato (con consenso scritto) via NEXUS sull'L3 Ancora della Community."
        ]
    },
    {
        "num": 8,
        "date": "21 Novembre 2026",
        "title": "Network Engineering: Score Ponte e 'Salto del 1° Grado'",
        "subtitle": "Raggiungere il risolutore perfetto al 2° grado senza mai esporre le tue debolezze 10/10 ai contatti diretti",
        "crop": (1300, 140, 1905, 680),
        "pts": [17, 18, 19, 20, 21],
        "victim": "Il networking a freddo e l'imbarazzo di dover confessare le proprie debolezze 10/10 agli amici o contatti di 1° grado.",
        "killer_feature": "Grafo relazionale ir_contacts_graph ('chi mi ha presentato chi') + calcolo in RAM di Score Diretto vs Score Ponte + Capsule anonimizzate da 1 KB (.ctdir / QR) con Smart Source-Routing ('Salto del 1° Grado').",
        "payoff_persona": "Chiedi supporto su scelte delicate raggiungendo lo specialista di 2° grado in totale riservatezza.",
        "payoff_prof": "Valorizzi il tuo Score Ponte diventando lo snodo scientifico di referenze inter-capitolo ad alta conversione.",
        "payoff_pmi": "Trovi fornitori o manager per risolvere una criticità 10/10 senza che concorrenti o conoscenti sappiano del problema.",
        "next_teaser": "Puntata #09: Trovato il match tra reti, professionisti e PMI, come ci si scambia valore anche senza bruciare cassa? Ecco l'HTLC.",
        "body_paragraphs": [
            "Il sistema 3° CtD NE traccia 'chi mi ha presentato chi' (ir_contacts_graph), calcola in tempo reale Score Diretto vs Score Ponte e permette il Next Best Match (NBM) riservato tramite il 'Salto del 1° Grado' senza mai mostrare le proprie debolezze 10/10 agli amici o contatti diretti."
        ]
    },
    {
        "num": 9,
        "date": "23 Novembre 2026",
        "title": "Compensazione in-Lire Fluida (HTLC) a Doppio Binario",
        "subtitle": "Il motore di intersezione tra network (BNI, circuiti B2B, professionisti e PMI) raccordato al Regime Fiscale",
        "crop": (1300, 600, 1905, 1075),
        "pts": [22, 23, 24],
        "victim": "La separazione tra network diversi e la staticità dei circuiti di scambio usati come semplici cataloghi passivi.",
        "killer_feature": "Motore di retention, lead generation e intersezione cross-network + Compensazione in-Lire Fluida (HTLC) a Doppio Binario (Binario 1: Ore-Palestra tra individui | Binario 2: Crediti B2B tra imprese) + P2P Bonjour/AirDrop.",
        "payoff_persona": "Monetizzi il tuo tempo col Binario 1 (Ore-Palestra) ottenendo l'affiancamento di altri esperti senza esborsi.",
        "payoff_prof": "Incroci il tuo Capitolo professionale con la domanda qualificata delle aziende appartenenti ai circuiti B2B.",
        "payoff_pmi": "Finanzi i tuoi cantieri L3 tramite il Binario 2 (Crediti B2B), generando nuovi clienti e preservando la liquidità.",
        "next_teaser": "Serie Aperta: proponi nel modulo Feedback qui sotto quale caso d'uso o problema vuoi vedere nella prossima puntata!",
        "body_paragraphs": [
            "Lo scambio di beni, servizi e referenze diventa un motore di retention, lead generation e intersezione tra circuiti esistenti (in-Lire e competitor), Capitoli BNI, professionisti e PMI, regolato su Doppio Binario (Ore-Palestra tra individui e Crediti B2B tra imprese) raccordato al Regime Fiscale richiesto in input iniziale."
        ]
    }
]

ss1_path = os.path.join(assets_dir, "ctd_plancia_ss1.png")
base_ss1 = Image.open(ss1_path).convert("RGB").resize((1920, 1080))

# ==============================================================================
# NUOVA SLIDE "PUNTATA #00 — IL TRAILER" (100% GRAFICA CON FUMETTI)
# ==============================================================================
def build_trailer_slide(as_context_slide=False):
    s0 = Image.new("RGB", (1920, 1080), (10, 10, 15))
    d0 = ImageDraw.Draw(s0)

    # Top Header (Zero emoji -> zero quadratini [])
    d0.rectangle([0, 0, 1920, 102], fill=(22, 16, 42))
    if as_context_slide:
        d0.text((45, 16), "★ IL CONTESTO DELLA SERIE (PUNTATA #00 — TRAILER)  •  PERCHÉ QUESTA È UNA 'SERIAL KILLER APP'", font=get_font(21, True), fill=(60, 208, 112))
    else:
        d0.text((45, 16), "★ PUNTATA #00 (IL TRAILER UFFICIALE)  •  SERIE APERTA 'ANATOMIA DI UNA SERIAL KILLER APP' (VERSO GENNAIO 2027)", font=get_font(21, True), fill=(245, 197, 24))
    d0.text((45, 48), "Come si presenta al mercato la prima 'App-non-App' che non è mai esistita prima?", font=get_font(32, True), fill=(255, 255, 255))

    # ==========================================================================
    # LATO SINISTRO (x=35..955): 100% GRAFICO CON SFONDO PLANCIA + NUCLEO + 5 FUMETTI
    # ==========================================================================
    # Sfondo olografico scuro della plancia dentro il pannello di sinistra
    bg_left = ImageEnhance.Brightness(base_ss1.resize((920, 880))).enhance(0.24)
    s0.paste(bg_left, (35, 120))
    d0.rectangle([35, 120, 955, 1000], outline=(245, 197, 24), width=3)
    d0.rectangle([35, 120, 955, 174], fill=(34, 24, 62))
    d0.text((55, 134), "► LA SFIDA: PRESENTARE LA PRIMA 'APP-NON-APP' (5 FUMETTI CHIAVE)", font=get_font(21, True), fill=(245, 197, 24))

    # Nucleo Grafico Centrale ("CtD APP-NON-APP") a (cx=495, cy=525)
    cx, cy = 495, 525
    # Raggi luminosi verso i 4 fumetti
    for tx, ty, col in [(255, 290, (56, 189, 248)), (735, 290, (245, 197, 24)), (255, 690, (192, 132, 252)), (735, 690, (60, 208, 112))]:
        d0.line([(cx, cy), (tx, ty)], fill=col, width=3)

    # Cerchi concentrici del Nucleo CtD
    d0.ellipse([cx - 105, cy - 105, cx + 105, cy + 105], fill=(18, 14, 38), outline=(245, 197, 24), width=4)
    d0.ellipse([cx - 92, cy - 92, cx + 92, cy + 92], fill=(28, 20, 58), outline=(56, 189, 248), width=2)
    d0.text((cx - 68, cy - 48), "CONNECT", font=get_font(26, True), fill=(255, 255, 255))
    d0.text((cx - 72, cy - 18), "THE DOTS", font=get_font(26, True), fill=(245, 197, 24))
    draw_badge_pill(d0, cx - 74, cy + 18, "L'APP-NON-APP", (60, 208, 112), (0, 0, 0), 15)

    # FUMETTO 1 (Alto Sinistra — Ciano)
    b1 = [52, 192, 435, 382]
    draw_speech_bubble(d0, b1, (cx - 55, cy - 55), (12, 28, 48), (56, 189, 248), width=3)
    draw_badge_pill(d0, 70, 206, "1. AI ESTESA MA 100% OFFLINE", (56, 189, 248), (0, 0, 0), 16)
    draw_wrapped_block(d0, 70, 246, 350, "\"Usa il meglio dell'AI + il sapere umano degli SME, ma gira al 100% OFFLINE nel tuo Profilo aggiornato!\"", get_font(19, True), (235, 248, 255), 26)

    # FUMETTO 2 (Alto Destra — Oro)
    b2 = [555, 192, 938, 382]
    draw_speech_bubble(d0, b2, (cx + 55, cy - 55), (38, 28, 10), (245, 197, 24), width=3)
    draw_badge_pill(d0, 573, 206, "2. 24 FUNZIONI IN 3 SISTEMI", (245, 197, 24), (0, 0, 0), 16)
    draw_wrapped_block(d0, 573, 246, 350, "\"Non fa una cosa sola: unisce Diagnosi (S=C+P+T+R), 2° Cervello (21gg) e Network Pull in 1 sola Piattaforma!\"", get_font(19, True), (255, 248, 220), 26)

    # FUMETTO 3 (Basso Sinistra — Viola)
    b3 = [52, 605, 435, 795]
    draw_speech_bubble(d0, b3, (cx - 55, cy + 55), (32, 16, 48), (192, 132, 252), width=3)
    draw_badge_pill(d0, 70, 619, "3. SIA UTENTI 'P' CHE 'B'", (192, 132, 252), (0, 0, 0), 16)
    draw_wrapped_block(d0, 70, 659, 350, "\"Parla una lingua sola ('Esperanto' di ~1.000 DOT) per Persone, Professionisti (R>>), PMI e Network!\"", get_font(19, True), (245, 235, 255), 26)

    # FUMETTO 4 (Basso Destra — Verde)
    b4 = [555, 605, 938, 795]
    draw_speech_bubble(d0, b4, (cx + 55, cy + 55), (12, 38, 24), (60, 208, 112), width=3)
    draw_badge_pill(d0, 573, 619, "4. NATIVA EU AI ACT & GDPR", (60, 208, 112), (0, 0, 0), 16)
    draw_wrapped_block(d0, 573, 659, 350, "\"Scudo di Anonimizzazione AI sulle domande, Regime Fiscale e Micro-Blockchain a costo server zero!\"", get_font(19, True), (230, 255, 240), 26)

    # FUMETTO PENSIERO 5 (In Basso a tutta larghezza sinistra — Ambra/Rosso con freccia verso Destra)
    b5 = [52, 822, 938, 982]
    # Pallini di pensiero dal nucleo centrale verso il fumetto 5
    d0.ellipse([488, 765, 502, 779], fill=(245, 197, 24))
    d0.ellipse([484, 790, 506, 812], fill=(245, 197, 24))
    d0.rounded_rectangle(b5, radius=22, fill=(48, 20, 16), outline=(245, 197, 24), width=3)
    draw_badge_pill(d0, 72, 838, "? IL NOSTRO DILEMMA COMUNICATIVO ?", (239, 68, 68), (255, 255, 255), 16)
    draw_wrapped_block(d0, 72, 878, 845, "\"Di fronte a una 'App-non-App' così vasta e mai vista prima, ci siamo chiesti: COME FACCIAMO A RACCONTARLA SENZA SCRIVERE UN MANUALE DI 200 PAGINE?!\"  ══►", get_font(20, True), (255, 240, 200), 27)

    # ==========================================================================
    # LATO DESTRO (x=975..1885): LA RISPOSTA IN 4 FUMETTI SINTETICI + BOX PAYOFF
    # ==========================================================================
    d0.rectangle([975, 120, 1885, 1000], fill=(14, 22, 18), outline=(60, 208, 112), width=3)
    d0.rectangle([975, 120, 1885, 174], fill=(20, 48, 34))
    d0.text((995, 134), "► LA RISPOSTA: LA SERIE APERTA 'ANATOMIA DI UNA SERIAL KILLER APP'", font=get_font(20, True), fill=(60, 208, 112))

    right_bubbles = [
        ("PUNTATA DOPO PUNTATA", (239, 68, 68), "1 Puntata = 1 'Vittima' Illustre Eliminata", "Ogni episodio ti mette al volante di 1 singola funzione che uccide una vecchia illusione (chatbot vuoti, SWOT morte, finti guru, chiamate a freddo)."),
        ("IMPATTO VISIVO IMMEDIATO", (56, 189, 248), "1 Slide che vale 1.000 Parole + Triplo Payoff", "Ogni uscita mostra lo zoom grafico della funzione e il Payoff specifico per Persona (P), Professionista (SME) e Imprenditore/PMI (B)."),
        ("ZERO PUNTATE PERSE", (60, 208, 112), "Timeline col Check Verde [✓] & Sezione News", "Ogni post accende un Check Verde [✓] nella Timeline e diventa una News leggibile su www.c-t-d.group/news.html per recuperare tutto."),
        ("PREMIO EARLY ADOPTER", (245, 197, 24), "1 Anno+ Gratis da Gennaio 2027 per il tuo Feedback", "Vai sul sito, lascia un feedback + la tua mail per la newsletter e ti assicuri l'uso gratuito per un anno o più al lancio di Gennaio 2027!")
    ]

    ry = 190
    for badge_txt, col, title_txt, desc_txt in right_bubbles:
        d0.rounded_rectangle([995, ry, 1865, ry + 132], radius=16, fill=(20, 30, 26), outline=col, width=2)
        end_x = draw_badge_pill(d0, 1012, ry + 12, badge_txt, col, (0, 0, 0), 14)
        d0.text((end_x + 14, ry + 12), title_txt, font=get_font(20, True), fill=(255, 255, 255))
        draw_wrapped_block(d0, 1012, ry + 48, 835, desc_txt, get_font(18, False), (225, 238, 230), 24)
        ry += 144

    # Box Finale Triplo Payoff P / SME / B
    d0.rounded_rectangle([995, 772, 1865, 984], radius=16, fill=(24, 16, 44), outline=(245, 197, 24), width=3)
    d0.text((1015, 786), "★ IL PAYOFF CHE SCOPRIRAI IN OGNI PUNTATA PER IL TUO PROFILO:", font=get_font(19, True), fill=(245, 197, 24))
    d0.text((1015, 822), "● Persona (P): Coach privato offline, Tasto Pausa ('0'), Palestra 21gg e Ore-Palestra.", font=get_font(18, True), fill=(125, 211, 252))
    d0.text((1015, 862), "● Professionista (SME): Cordone Ombelicale 21gg coi clienti e qualifica Proven SME (R >>).", font=get_font(18, True), fill=(253, 224, 71))
    d0.text((1015, 902), "● Imprenditore / PMI / Rete (B): SWOT in RAM, Salto del 1° Grado e Clearing HTLC B2B.", font=get_font(18, True), fill=(216, 180, 254))
    d0.text((1015, 944), "► Leggi le puntate e prenota 1 Anno+ Gratis su: www.c-t-d.group/news.html", font=get_font(18, True), fill=(60, 208, 112))

    # Bottom Bar
    d0.rectangle([0, 1015, 1920, 1080], fill=(22, 16, 42))
    d0.text((45, 1033), "► Scorri le slide per la Mappa dei 3 Sistemi, i 24 Componenti e la Timeline [✓]  •  www.c-t-d.group/news.html", font=get_font(21, True), fill=(245, 197, 24))
    return s0

trailer_cover = build_trailer_slide(as_context_slide=False)
trailer_context = build_trailer_slide(as_context_slide=True)
trailer_cover.save(os.path.join(assets_dir, "news_ep_00.png"))

# Slide Master Pulita SS2
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

for ep in episodes:
    ep_num = ep["num"]
    pts_str = "Tutti (1..24)" if len(ep["pts"]) > 10 else ", ".join(str(p) for p in ep["pts"])

    if ep_num == 0:
        s1 = trailer_cover.copy()
    else:
        s1 = Image.new("RGB", (1920, 1080), (10, 10, 15))
        ds1 = ImageDraw.Draw(s1)
        ds1.rectangle([0, 0, 1920, 105], fill=(22, 16, 42))
        ds1.text((45, 16), f"★ ANATOMIA DI UNA SERIAL KILLER APP  •  PUNTATA #{ep_num:02d} ({ep['date']})  •  SERIE APERTA VERSO GENNAIO 2027", font=get_font(21, True), fill=(245, 197, 24))
        ds1.text((45, 48), ep["title"], font=get_font(33, True), fill=(255, 255, 255))

        ds1.rectangle([40, 125, 900, 995], fill=(16, 16, 24), outline=(245, 197, 24), width=3)
        ds1.rectangle([40, 125, 900, 175], fill=(32, 24, 58))
        ds1.text((60, 138), f"► LA SLIDE CHE VALE 1.000 PAROLE  •  Componenti attivati: [{pts_str}]", font=get_font(20, True), fill=(245, 197, 24))

        cropped = base_ss1.crop(ep["crop"])
        cw, ch = cropped.size
        scale = min(830 / cw, 780 / ch)
        nw, nh = int(cw * scale), int(ch * scale)
        resized = cropped.resize((nw, nh))
        s1.paste(resized, (55 + (830 - nw) // 2, 190 + (780 - nh) // 2))

        rx1, rx2 = 930, 1880
        rw = rx2 - rx1 - 40

        ds1.rounded_rectangle([rx1, 125, rx2, 305], radius=16, fill=(36, 14, 20), outline=(239, 68, 68), width=2)
        draw_badge_pill(ds1, rx1 + 20, 140, "X LA VITTIMA ELIMINATA (VECCHIO MONDO)", (239, 68, 68), (255, 255, 255), 16)
        draw_wrapped_block(ds1, rx1 + 20, 182, rw, ep["victim"], get_font(20, False), (255, 235, 235), 28)

        ds1.rounded_rectangle([rx1, 325, rx2, 545], radius=16, fill=(16, 28, 46), outline=(56, 189, 248), width=2)
        draw_badge_pill(ds1, rx1 + 20, 340, "► LA KILLER FEATURE CtD (COSA FAI AL VOLANTE DELL'APP)", (56, 189, 248), (0, 0, 0), 16)
        draw_wrapped_block(ds1, rx1 + 20, 382, rw, ep["killer_feature"], get_font(20, False), (235, 248, 255), 28)

        ds1.rounded_rectangle([rx1, 565, rx2, 995], radius=16, fill=(16, 34, 24), outline=(60, 208, 112), width=3)
        draw_badge_pill(ds1, rx1 + 20, 580, "★ IL PAYOFF CONCRETO PER IL TUO PROFILO", (60, 208, 112), (0, 0, 0), 16)

        py = 626
        for badge_lbl, badge_col, p_txt in [
            ("● SE SEI UNA PERSONA O UN TALENTO (P):", (56, 189, 248), ep["payoff_persona"]),
            ("● SE SEI UN PROFESSIONISTA / PROVEN SME (R >>):", (245, 197, 24), ep["payoff_prof"]),
            ("● SE SEI UN IMPRENDITORE / PMI O NETWORK (B):", (192, 132, 252), ep["payoff_pmi"])
        ]:
            ds1.text((rx1 + 20, py), badge_lbl, font=get_font(19, True), fill=badge_col)
            py = draw_wrapped_block(ds1, rx1 + 20, py + 25, rw, p_txt, get_font(19, False), (240, 245, 240), 25) + 14

        ds1.rectangle([0, 1015, 1920, 1080], fill=(22, 16, 42))
        ds1.text((45, 1033), "► Scorri per il Trailer 'App-non-App', la Mappa Generale e la Timeline [✓]  •  www.c-t-d.group/news.html", font=get_font(21, True), fill=(245, 197, 24))
        s1.save(os.path.join(assets_dir, f"news_ep_{ep_num:02d}.png"))

    # SLIDE MAPPA GENERALE
    s_map = Image.new("RGB", (1920, 1080), (10, 10, 14))
    s_map.paste(base_ss1.resize((1920, 990)), (0, 90))
    dmap = ImageDraw.Draw(s_map)
    dmap.rectangle([0, 0, 1920, 90], fill=(22, 16, 42))
    dmap.text((45, 16), f"LA PLANCIA GENERALE: '3 SYSTEMS IN 1 PLATFORM'  •  PUNTATA #{ep_num:02d}", font=get_font(24, True), fill=(245, 197, 24))
    dmap.text((45, 50), f"Componenti attivati in questo episodio: [{pts_str}]", font=get_font(19, False), fill=(230, 230, 240))
    if len(ep["pts"]) < 24:
        cx1, cy1, cx2, cy2 = ep["crop"]
        sy1 = int(cy1 * (990 / 1080)) + 90
        sy2 = int(cy2 * (990 / 1080)) + 90
        dmap.rectangle([cx1, sy1, cx2, sy2], outline=(245, 197, 24), width=6)

    # SLIDE 24 COMPONENTI
    s_list = Image.new("RGB", (1920, 1080), (10, 10, 14))
    dlist = ImageDraw.Draw(s_list)
    dlist.text((60, 26), f"I 24 Componenti della Value Proposition  •  Puntata #{ep_num:02d}", font=get_font(31, True), fill=(255, 255, 255))
    dlist.text((60, 68), "1° CtD Base [1-8]  •  2° CtD 2°B: Secondo Cervello [9-16]  •  3° CtD NE: Network Engineering [17-24]", font=get_font(21, True), fill=(245, 197, 24))
    y3 = 112
    for idx, line in vp_24_clean:
        is_active = idx in ep["pts"]
        if is_active and len(ep["pts"]) < 24:
            dlist.rectangle([48, y3 - 3, 1875, y3 + 31], fill=(45, 34, 10), outline=(245, 197, 24), width=1)
            dlist.text((56, y3), "► " + line, font=get_font(19, True), fill=(245, 197, 24))
        else:
            col = (175, 215, 245) if idx <= 8 else ((235, 220, 155) if idx <= 16 else (165, 230, 190))
            dlist.text((60, y3), line, font=get_font(18, False), fill=col)
        y3 += 37
    dlist.text((60, 1028), "Archivio completo delle News e dei 24 Componenti su: www.c-t-d.group/news.html  |  www.c-t-d.group/founders.html", font=get_font(16, True), fill=(245, 197, 24))

    # SLIDE TIMELINE APERTA (ZERO EMOJI -> SOLO SIMBOLI NITIDI ✓, ★, +)
    s_time = Image.new("RGB", (1920, 1080), (10, 10, 14))
    dtime = ImageDraw.Draw(s_time)
    dtime.rectangle([0, 0, 1920, 98], fill=(22, 16, 42))
    dtime.text((50, 16), f"TIMELINE DELLA SERIE APERTA  •  PUNTATA #{ep_num:02d} IN EVIDENZA (CHECK VERDI [✓] SULLE USCITE PUBBLICATE)", font=get_font(26, True), fill=(245, 197, 24))
    dtime.text((50, 54), "Ti sei perso il Trailer (#00) o una puntata precedente? Leggi tutte le News su www.c-t-d.group/news.html", font=get_font(19, False), fill=(210, 210, 225))

    ty = 108
    for item in episodes:
        num = item["num"]
        dt = item["date"]
        tit = item["title"]
        vic = item["victim"]
        is_done = num < ep_num
        is_curr = (num == ep_num)
        bg = (18, 42, 28) if is_done else ((44, 32, 12) if is_curr else (20, 20, 26))
        border = (60, 208, 112) if is_done else ((245, 197, 24) if is_curr else (45, 45, 58))
        dtime.rectangle([50, ty, 1870, ty + 62], fill=bg, outline=border, width=2)

        bx, by = 68, ty + 11
        if is_done:
            dtime.rectangle([bx, by, bx + 40, by + 40], fill=(60, 208, 112), outline=(255, 255, 255), width=2)
            dtime.text((bx + 8, by + 2), "✓", font=get_font(28, True), fill=(0, 0, 0))
            status_lbl = f"PUNTATA #{num:02d} ({dt}) — PUBBLICATA"
            t_col = (140, 245, 175)
        elif is_curr:
            dtime.rectangle([bx, by, bx + 40, by + 40], fill=(245, 197, 24), outline=(255, 255, 255), width=2)
            dtime.text((bx + 9, by + 4), "★", font=get_font(24, True), fill=(0, 0, 0))
            status_lbl = f"PUNTATA #{num:02d} ({dt}) — ATTIVA OGGI"
            t_col = (245, 197, 24)
        else:
            dtime.rectangle([bx, by, bx + 40, by + 40], fill=(28, 28, 36), outline=(110, 110, 130), width=2)
            dtime.text((bx + 5, by + 8), f"#{num:02d}", font=get_font(17, True), fill=(130, 130, 150))
            status_lbl = f"PUNTATA #{num:02d} ({dt}) — IN ARRIVO"
            t_col = (155, 155, 170)

        dtime.text((126, ty + 6), f"{status_lbl}:  {tit}", font=get_font(19, True), fill=t_col)
        dtime.text((126, ty + 33), f"► Focus: {vic[:115]}", font=get_font(16, False), fill=(220, 220, 230))
        ty += 68

    dtime.rectangle([50, ty, 1870, ty + 56], fill=(20, 26, 44), outline=(56, 189, 248), width=2)
    dtime.text((70, ty + 8), "+ SERIE APERTA IN CONTINUA EVOLUZIONE  •  NUOVE PUNTATE AGGIUNTE IN CORSA DAI VOSTRI FEEDBACK", font=get_font(18, True), fill=(56, 189, 248))
    dtime.text((70, ty + 31), "Suggerisci il prossimo caso d'uso su www.c-t-d.group/news.html e blocca 1 Anno+ Gratis da Gennaio 2027!", font=get_font(16, False), fill=(225, 240, 255))

    dtime.rectangle([50, 952, 1870, 1062], fill=(26, 16, 48), outline=(245, 197, 24), width=3)
    dtime.text((75, 962), "★ VUOI USARE CONNECT THE DOTS GRATIS (PER UN ANNO O PIÙ) A PARTIRE DA GENNAIO 2027?", font=get_font(22, True), fill=(245, 197, 24))
    dtime.text((75, 994), "Vai su www.c-t-d.group/news.html • Lascia il tuo Feedback + la tua Email per iscriverti alla Newsletter delle puntate", font=get_font(19, False), fill=(255, 255, 255))
    dtime.text((75, 1024), "e assicurati subito il Programma Early Adopter (Persona P • Professionista/Proven SME • Imprenditore/PMI/Network B).", font=get_font(18, False), fill=(60, 208, 112))

    pdf_name = f"Carosello_LinkedIn_Puntata_{ep_num:02d}.pdf"
    extra_slides = [s_map, s_list, s_time] if ep_num == 0 else [trailer_context, s_map, s_list, s_time]
    s1.save(os.path.join(out_desktop_dir, pdf_name), "PDF", resolution=150.0, save_all=True, append_images=extra_slides)
    s1.save(os.path.join(caroselli_web_dir, pdf_name), "PDF", resolution=150.0, save_all=True, append_images=extra_slides)

print("OK: Rigenerati tutti i Caroselli PDF con Fumetti vettoriali e ZERO quadratini []!")

# ==============================================================================
# AGGIORNAMENTO DI news.html CON BOTTONE "1-CLICK LINKEDIN"
# ==============================================================================
def build_news_page(is_en=False):
    prefix = "../" if is_en else ""
    lang_switch = '<a href="../news.html" style="color: #FAE100; font-weight: bold;">IT</a>' if is_en else '<a href="en/news.html" style="color: #FAE100; font-weight: bold;">EN</a>'

    timeline_rows_html = ""
    articles_html = ""

    for ep in episodes:
        num = ep["num"]
        is_published = (num == 0)
        badge_status = "🎬 TRAILER PUBBLICATO OGGI" if is_published else f"📌 IN USCITA ({ep['date']})"
        border_col = "var(--green-secure)" if is_published else "var(--accent-gold)"
        bg_row = "rgba(60, 208, 112, 0.12)" if is_published else "#181822"
        n_slides = 4 if num == 0 else 5

        timeline_rows_html += f"""
                <a href="#news-ep-{num:02d}" style="text-decoration: none; display: block; padding: 13px 16px; background: {bg_row}; border-left: 4px solid {border_col}; border-radius: 6px; color: #fff;">
                    <strong style="color: {border_col};">[{badge_status} • Puntata #{num:02d}]</strong> <strong>{ep['title']}</strong>
                    <span style="display: block; font-size: 0.82rem; color: var(--text-gray); margin-top: 3px;">🔪 Focus: {ep['victim']}</span>
                </a>
        """

        paras = "".join(f"<p style='color: #dedee8; font-size: 0.98rem; line-height: 1.65; margin-bottom: 14px;'>{p}</p>" for p in ep["body_paragraphs"])
        pts_str = "Tutti (1..24)" if len(ep["pts"]) > 10 else ", ".join(str(p) for p in ep["pts"])

        # Testo pronto per LinkedIn per il bottone 1-Click
        li_text_lines = [
            f"🔪 Anatomia di una Serial Killer App — Puntata #{num:02d}: {ep['title']}",
            f"({ep['subtitle']})",
            "",
            "\n\n".join(ep["body_paragraphs"]),
            "",
            "🎯 IL PAYOFF DI QUESTA FUNZIONE PER IL TUO PROFILO:",
            f"👤 Se sei una Persona (P) o un Talento: {ep['payoff_persona']}",
            f"🎓 Se sei un Professionista / Proven SME (R >>): {ep['payoff_prof']}",
            f"🏢 Se sei un Imprenditore, PMI o Network (B): {ep['payoff_pmi']}",
            "",
            "🎁 VUOI USARE CONNECT THE DOTS GRATIS (PER UN ANNO O PIÙ) DA GENNAIO 2027?",
            "Leggi tutte le puntate su https://www.c-t-d.group/news.html : lasciando un feedback sulle funzioni insieme alla tua email per iscriverti alla newsletter, ti assicuri il Programma Early Adopter con versione gratuita per un anno o più!",
            "",
            f"🔪 Prossimo passo: {ep['next_teaser']}",
            "",
            "#ConnectTheDOTS #SerialKillerApp #AppNonApp #3SystemsInOnePlatform #EdgeAI #AIAct #GDPR #Gennaio2027"
        ]
        li_full_text = "\n".join(li_text_lines).replace('"', '&quot;')

        articles_html += f"""
            <article id="news-ep-{num:02d}" style="background: #141419; border: 1px solid var(--border-color); border-top: 3px solid {border_col}; border-radius: 14px; padding: 28px; margin-bottom: 36px; box-shadow: 0 10px 30px rgba(0,0,0,0.45);">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 14px;">
                    <span style="background: #18112c; color: var(--accent-gold); border: 1px solid var(--accent-gold); padding: 5px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">
                        {'🎬 Puntata #00 (Il Trailer)' if num == 0 else f'🔪 Puntata #{num:02d}'} • {ep['date']} • Componenti CtD: [{pts_str}]
                    </span>
                    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                        <a href="{prefix}assets/caroselli/Carosello_LinkedIn_Puntata_{num:02d}.pdf" target="_blank" style="background: rgba(245, 197, 24, 0.15); color: var(--accent-gold); border: 1px solid var(--accent-gold); padding: 7px 14px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; text-decoration: none;">
                            📥 1. Scarica Carosello PDF ({n_slides} Slide)
                        </a>
                        <button type="button" data-litext="{li_full_text}" onclick="copyAndOpenLinkedIn(this, '{num:02d}')" style="background: var(--accent-gold); color: #000; border: none; padding: 7px 14px; border-radius: 6px; font-size: 0.82rem; font-weight: 800; cursor: pointer;">
                            📋 2. Copia Testo Post + Apri LinkedIn
                        </button>
                    </div>
                </div>

                <h2 style="color: #ffffff; font-size: 1.75rem; margin: 0 0 6px 0;">Puntata #{num:02d} — {ep['title']}</h2>
                <p style="color: var(--accent-gold); font-size: 1.02rem; font-weight: 600; margin: 0 0 20px 0;">{ep['subtitle']}</p>

                <div style="margin-bottom: 24px; border-radius: 10px; overflow: hidden; border: 1px solid #2c2c3a;">
                    <img src="{prefix}assets/news_ep_{num:02d}.png" alt="Slide 1000 Parole - Puntata {num:02d}" style="width: 100%; height: auto; display: block;" loading="lazy" />
                </div>

                {paras}

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; margin: 22px 0;">
                    <div style="background: #101824; border: 1px solid #38bdf8; border-radius: 8px; padding: 14px;">
                        <strong style="color: #38bdf8; font-size: 0.82rem; text-transform: uppercase; display: block; margin-bottom: 6px;">👤 Payoff Persona &amp; Talento (P)</strong>
                        <p style="color: #e2e8f0; font-size: 0.88rem; margin: 0;">{ep['payoff_persona']}</p>
                    </div>
                    <div style="background: #1f190c; border: 1px solid var(--accent-gold); border-radius: 8px; padding: 14px;">
                        <strong style="color: var(--accent-gold); font-size: 0.82rem; text-transform: uppercase; display: block; margin-bottom: 6px;">🎓 Payoff Professionista / Proven SME</strong>
                        <p style="color: #fef9c3; font-size: 0.88rem; margin: 0;">{ep['payoff_prof']}</p>
                    </div>
                    <div style="background: #1a1228; border: 1px solid #b085f5; border-radius: 8px; padding: 14px;">
                        <strong style="color: #b085f5; font-size: 0.82rem; text-transform: uppercase; display: block; margin-bottom: 6px;">🏢 Payoff Imprenditore, PMI &amp; Network (B)</strong>
                        <p style="color: #f3e8ff; font-size: 0.88rem; margin: 0;">{ep['payoff_pmi']}</p>
                    </div>
                </div>

                <div style="background: #18112c; border-left: 4px solid var(--accent-gold); padding: 12px 16px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                    <span style="font-size: 0.88rem; color: #dedee8;"><strong>🔪 Prossimo Passo:</strong> {ep['next_teaser']}</span>
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
                🎬 Dalla Puntata #00 (Il Trailer della prima "App-non-App") • Serie Aperta verso Gennaio 2027
            </div>
            <h1 style="font-size: 2.4rem; margin: 0 0 12px 0; color: #fff;">News &amp; Puntate: <span style="color: var(--accent-gold);">"Anatomia di una Serial Killer App"</span></h1>
            <p style="color: var(--text-gray); max-width: 860px; margin: 0 auto; font-size: 1.02rem;">
                Di fronte alla sfida di presentare la prima <strong>"App-non-App"</strong> — con uso esteso dell'AI ma <strong>100% offline</strong>, 24 funzionalità in 3 sistemi, per utenti <strong>P</strong> e <strong>B</strong>, nativamente <strong>EU AI Act e GDPR compliant</strong> — abbiamo ideato questa serie aperta di puntate. Leggi gli episodi, scarica le <strong>Slide da 1.000 parole</strong> e lascia il tuo feedback per assicurarti <strong>un anno o più di licenza gratuita</strong> da Gennaio 2027.
            </p>
        </div>

        <section style="background: #141419; border: 1px solid var(--border-color); border-radius: 14px; padding: 24px; margin-bottom: 40px;">
            <h3 style="color: var(--accent-gold); margin: 0 0 8px 0; font-size: 1.3rem;">📋 Timeline Interattiva delle Puntate (a partire da Puntata #00 — Il Trailer)</h3>
            <p style="color: var(--text-gray); font-size: 0.9rem; margin: 0 0 16px 0;">
                Clicca su qualsiasi puntata per leggere subito la News completa o scaricare il Carosello PDF:
            </p>
            <div style="display: grid; gap: 10px;">
                {timeline_rows_html}
                <div style="padding: 13px 16px; background: rgba(56, 189, 248, 0.1); border-left: 4px solid #38bdf8; border-radius: 6px; color: #e0f2fe;">
                    <strong style="color: #38bdf8;">[➕ CANTIERE APERTO — PROSSIME PUNTATE SU RICHIESTA]</strong> Nuovi episodi aggiunti in corsa anche a partire dai vostri feedback!
                </div>
            </div>
        </section>

        <section>
            {articles_html}
        </section>

        <section id="early-adopter-feedback-box" style="background: #141419; border: 2px solid var(--accent-gold); border-radius: 14px; padding: 30px; margin-top: 40px;">
            <h2 style="color: #fff; font-size: 1.7rem; margin: 0 0 10px 0;">🎁 Lascia il Tuo Feedback, Iscriviti alla Newsletter e Assicurati 1 Anno+ Gratis da Gennaio 2027</h2>
            <p style="color: var(--text-gray); font-size: 0.95rem; margin-bottom: 20px;">
                Chi partecipa lasciando un feedback sulle puntate (o suggerendo il prossimo argomento della serie aperta) insieme alla propria email per la newsletter si assicura l'accesso al <strong>Programma Early Adopter di Gennaio 2027 con una versione gratuita per un anno o più</strong>.
            </p>
            <form onsubmit="submitNewsFeedback(event)" style="display: grid; gap: 14px;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px;">
                    <input type="text" id="nw-name" required placeholder="Nome e Cognome *" style="width:100%; padding:12px; border-radius:6px; border:1px solid #333; background:#0c0c10; color:#fff; box-sizing:border-box;">
                    <input type="email" id="nw-email" required placeholder="La tua Email (per Newsletter & Licenza Gratis 1 Anno+) *" style="width:100%; padding:12px; border-radius:6px; border:1px solid #333; background:#0c0c10; color:#fff; box-sizing:border-box;">
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px;">
                    <select id="nw-role" onchange="document.getElementById('nw-other-wrap').style.display=(this.value==='Altro'?'block':'none')" style="width:100%; padding:12px; border-radius:6px; border:1px solid #333; background:#0c0c10; color:#fff; box-sizing:border-box;">
                        <option value="Persona / Talento / Executive (P)">1. Persona / Talento / Executive (P)</option>
                        <option value="Professionista / Consulente / Aspirante Proven SME (R>>)">2. Professionista / Consulente / Aspirante Proven SME (R&gg;)</option>
                        <option value="Imprenditore / PMI (B)">3. Imprenditore / PMI (B)</option>
                        <option value="Network (Capitolo BNI) / Circuito B2B (es. in-Lire)">4. Network (Capitolo BNI) / Circuito B2B (es. in-Lire)</option>
                        <option value="Advisory Firm / Corporate / Investitore">5. Advisory Firm / Corporate / Investitore</option>
                        <option value="Altro">Altro (specificare sotto)</option>
                    </select>
                    <input type="text" id="nw-topic" placeholder="Su quale Puntata o funzione della 'App-non-App' vuoi dare feedback?" style="width:100%; padding:12px; border-radius:6px; border:1px solid #333; background:#0c0c10; color:#fff; box-sizing:border-box;">
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
        function copyAndOpenLinkedIn(btn, epNum) {{
            var txt = btn.getAttribute('data-litext');
            navigator.clipboard.writeText(txt).then(function() {{
                var orig = btn.innerText;
                btn.innerText = '✅ Testo Copiato! Ora premi Cmd+V su LinkedIn e allega Puntata_' + epNum + '.pdf';
                btn.style.background = '#3cd070';
                setTimeout(function() {{
                    window.open('https://www.linkedin.com/feed/?shareActive=true', '_blank');
                }}, 350);
                setTimeout(function() {{
                    btn.innerText = orig;
                    btn.style.background = '#f5c518';
                }}, 7000);
            }});
        }}
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
print("OK: Aggiornate news.html e en/news.html con bottone 1-Click LinkedIn!")
