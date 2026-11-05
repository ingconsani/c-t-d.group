import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

repo = "/Users/ingconsani/Development/c-t-d.group"
assets_dir = os.path.join(repo, "assets")
caroselli_web_dir = os.path.join(assets_dir, "caroselli")
out_desktop_dir = "/Users/ingconsani/Desktop/CtD_LinkedIn_Caroselli_PDF"
os.makedirs(caroselli_web_dir, exist_ok=True)
os.makedirs(out_desktop_dir, exist_ok=True)

def li_utf16_len(s):
    # Calcolo rigoroso UTF-16 (incluso CRLF e peso doppio delle emoji) come LinkedIn
    s_crlf = s.replace("\r\n", "\n").replace("\n", "\r\n")
    return len(s_crlf.encode("utf-16-le")) // 2

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

def draw_vector_checkbox(draw, x, y, size=42, checked=True):
    if checked:
        draw.rounded_rectangle([x, y, x + size, y + size], radius=9, fill=(60, 208, 112), outline=(255, 255, 255), width=2)
        p1 = (x + int(size * 0.22), y + int(size * 0.52))
        p2 = (x + int(size * 0.44), y + int(size * 0.74))
        p3 = (x + int(size * 0.78), y + int(size * 0.26))
        draw.line([p1, p2, p3], fill=(0, 0, 0), width=5)
    else:
        draw.rounded_rectangle([x, y, x + size, y + size], radius=9, fill=(28, 28, 38), outline=(245, 197, 24), width=2)
        draw.text((x + 13, y + 6), "?", font=get_font(26, True), fill=(245, 197, 24))

episodes = [
    {
        "num": 0,
        "date": "5 Novembre 2026",
        "doc_title": "Connect the DOTS #00: Anatomia di una Serial Killer App",
        "title": "IL TRAILER: Come raccontare la prima 'App-non-App'?",
        "subtitle": "Uso esteso dell'AI ma 100% Offline • 24 Funzioni in 3 Sistemi • Utenti P & B • Nativamente GDPR & EU AI Act Compliant",
        "crop": (0, 0, 1920, 1080),
        "pts": list(range(1, 25)),
        "victim": "L'impossibilita' di spiegare una piattaforma rivoluzionaria di 24 componenti con un singolo post tradizionale.",
        "killer_feature": "Una serie aperta ('Anatomia di una Serial Killer App'): ogni puntata isola 1 funzione con 1 Slide da 1.000 parole, Timeline progressiva, Triplo Payoff (P / Prof / B) e 1 Anno+ Gratis da Gennaio 2027.",
        "payoff_persona": "Scopri passo dopo passo come usare un Coach privato e un Secondo Cervello offline senza cedere i tuoi dati al cloud.",
        "payoff_prof": "Scopri come fidelizzare i tuoi clienti per 21 giorni e farti scegliere in modalita' Pull grazie ai tuoi risultati certificati (R >>).",
        "payoff_pmi": "Scopri come unificare SWOT in RAM, cantieri operativi L3 e intersezioni di rete B2B a costo server zero.",
        "next_teaser": "Tra 48 ore (Puntata #01): Sveleremo il Manifesto dei '3 Systems in 1 Platform' e l'equazione S = C + P + T + R.",
        "body_paragraphs": [
            "Di fronte alla necessita' di presentare la prima vera 'App-non-App' sul mercato — capace di fare un uso esteso dell'Intelligenza Artificiale ma 100% offline, ricca di 24 funzionalita' diverse distribuite su 3 sistemi integrati, progettata contemporaneamente per utenti P (Persona) e B (Business) e nativamente conforme a EU AI Act e GDPR — ci siamo chiesti: come possiamo farla comprendere davvero senza sommergere chi legge?",
            "Cosi' abbiamo ideato quello che state per vedere: 'Anatomia di una Serial Killer App', una serie aperta di puntate in vista del lancio ufficiale di Gennaio 2027. In ogni episodio ci siederemo al volante di una singola funzionalita' applicativa, mostrando quale vecchia illusione del mercato viene 'eliminata' e quale vantaggio concreto ottiene chi usa Connect the DOTS.",
            "Ogni puntata e' accompagnata da una Slide che vale 1.000 parole, da una Timeline progressiva che si arricchisce di puntata in puntata qui nella sezione News di www.c-t-d.group, e da un patto con i lettori: chi lascia il proprio feedback insieme alla mail per la newsletter si assicura una versione gratuita per un anno o piu' nel Programma Early Adopter di Gennaio 2027."
        ],
        "post_text": """Come si presenta al mercato la prima "App-non-App" che non è mai esistita prima?
Quando abbiamo provato a spiegare Connect the DOTS (in uscita a Gennaio 2027) con un post tradizionale, ci siamo accorti che era impossibile.
Ecco perché da oggi parte "Anatomia di una Serial Killer App" (sfoglia le 2 slide del Trailer qui sotto 👇).

Quando qualche mese fa la Ferrari ha svelato la sua prima vettura elettrica, la Luce, chi si è fermato alle prime foto statiche cercava i vecchi schemi del motore termico. Chi invece si è seduto al volante ha scoperto dieci auto diverse in una sola piattaforma.

Con Connect the DOTS (CtD) ci siamo trovati davanti allo stesso dilemma comunicativo:

🔹 Uso esteso dell'AI, ma 100% OFFLINE sul tuo dispositivo, unendo l'AI al sapere umano degli esperti (SME) nel tuo Profilo aggiornato a costo server zero.
🔹 24 componenti brevettati in 3 Sistemi integrati (3 Systems in 1 Platform): Diagnosi Strategica (S = C + P + T + R e SWOT in RAM), Secondo Cervello (Palestra di 21 Giorni e certificati PoR) e Network Engineering Pull.
🔹 Nata sia per utenti P (Persone e Talenti) sia per utenti B (Professionisti, Proven SME con R >>, PMI e Network come BNI o circuiti come in-Lire), uniti dall'"Esperanto" comune di ~1.000 DOT.
🔹 Nativamente EU AI Act & GDPR Compliant, con Scudo di Anonimizzazione AI sulle domande libere, Regime Fiscale iniziale e micro-blockchain locale.

Come raccontare tutto questo senza scrivere un manuale di 200 pagine?

Con questa serie aperta di puntate:
1️⃣ Ogni episodio ti siede al volante di 1 funzione che "uccide" una vecchia illusione (chatbot vuoti, SWOT morte nei PDF, finti guru, chiamate a freddo).
2️⃣ Ogni uscita ha 1 Slide che vale 1.000 parole + il Triplo Payoff per Persona (P), Professionista (SME) e Imprenditore/PMI (B).
3️⃣ Nella Slide 2 trovi la Timeline progressiva col Check Verde [✓] e su https://www.c-t-d.group/news.html#news-ep-00 leggi le puntate come News.

🎯 COSA SCOPRIRAI IN OGNI PUNTATA PER IL TUO PROFILO:
👤 Persona (P): Coach privato offline, Tasto Pausa ('0'), Palestra 21gg e Ore-Palestra.
🎓 Professionista (SME): "Cordone Ombelicale" di 21gg coi migliori clienti e qualifica a Proven SME (R >>).
🏢 Imprenditore / PMI / Rete (B): SWOT in RAM oltre il fatturato, "Salto del 1° Grado" (senza mostrare debolezze 10/10 agli amici) e compensazione in-Lire Fluida (HTLC).

🎁 IL TUO FEEDBACK VALE 1 ANNO+ DI LICENZA GRATUITA DA GENNAIO 2027
Vai su https://www.c-t-d.group/news.html#news-ep-00 : lasciando un feedback sulle funzioni (anche con opzione "Altro") e la tua email per la newsletter, ti assicuri una versione gratuita per un anno o più nel Programma Early Adopter di Gennaio 2027!

Quale "falsa promessa" del digitale o della consulenza vorresti veder eliminata per prima? 👇

#ConnectTheDOTS #SerialKillerApp #AppNonApp #3SystemsInOnePlatform #EdgeAI #AIAct #GDPR #Gennaio2027"""
    },
    {
        "num": 1,
        "date": "7 Novembre 2026",
        "doc_title": "Connect the DOTS #01: 3 Systems in 1 Platform (Offline)",
        "title": "Il Manifesto: 3 Systems in 1 Platform (S = C + P + T + R)",
        "subtitle": "Come funzionano i 3 motori integrati nel tuo Profilo aggiornato 100% offline (Lancio Gennaio 2027)",
        "crop": (0, 0, 1920, 1080),
        "pts": list(range(1, 25)),
        "victim": "I software isolati in Cloud che standardizzano le persone, divorano energia ed espongono i tuoi segreti industriali.",
        "killer_feature": "3 Sistemi integrati in 1 sola Piattaforma 100% offline dentro il tuo Profilo aggiornato: 1° CtD Base (Diagnosi S=C+P+T+R) + 2° CtD 2°B (Secondo Cervello 21gg) + 3° CtD NE (Network Engineering Pull).",
        "payoff_persona": "Diventi padrone del tuo futuro con un Coach 100% privato sul tuo device che non vende mai i tuoi dati.",
        "payoff_prof": "Smetti di rincorrere clienti a freddo (Push) e vieni attivato in Pull grazie ai tuoi risultati certificati (R >>).",
        "payoff_pmi": "Unifichi diagnosi strategica, cantieri operativi L3 e ricerca riservata di partner a costo server zero.",
        "next_teaser": "Tra 48 ore (Puntata #02): Come si uccide l'angolo cieco del 'Non so cosa non so'? Cosa accade premendo il pulsante del Cervello.",
        "post_text": """🔪 Anatomia di una Serial Killer App — Puntata #01: Il Manifesto dei "3 Systems in 1 Platform" (S = C + P + T + R).
(Hai perso la Puntata #00 Il Trailer? La trovi nella Timeline [✓] in Slide 2 e su https://www.c-t-d.group/news.html 👇).

Oggi la nostra Serial Killer App (in arrivo a Gennaio 2027) elimina la sua prima vittima illustre: i software isolati su Cloud che standardizzano le persone, divorano energia ed espongono i tuoi dati riservati.

Cosa faresti se avessi già oggi Connect the DOTS sul tuo Mac, PC o smartphone?
Avresti 3 Sistemi integrati in 1 sola Piattaforma (3 Systems in 1 Platform) che lavorano al 100% offline dentro il tuo Profilo aggiornato:

1️⃣ 1° CtD Base (Core Diagnostico — Punti 1..8): il tuo Coach "intelligente (senza artificiale, ricco dell'intelligenza umana degli SME) e privato" per capire esattamente dove sei con l'equazione additiva S = C + P + T + R.
2️⃣ 2° CtD 2°B (Secondo Cervello — Punti 9..16): per far proliferare ogni tuo problema in un cantiere operativo di 21 giorni fino al risultato reale certificato (PoR).
3️⃣ 3° CtD NE (Network Engineering — Punti 17..24): per attivare in modalità Pull solo le competenze, i clienti e le relazioni che ti servono davvero, dentro una Community of Interest che parla la stessa lingua ("Esperanto").

🎯 IL PAYOFF DI QUESTA ARCHITETTURA PER TE:
👤 Se sei una Persona (P) o un Talento: diventi padrone del tuo futuro con un Coach 100% privato che lavora solo per te senza mai vendere o esporre i tuoi dati sul cloud.
🎓 Se sei un Professionista / Proven SME (R >>): smetti di rincorrere clienti a freddo (Push) e vieni scelto in modalità Pull grazie ai risultati reali certificati sui tuoi cantieri.
🏢 Se sei un Imprenditore, PMI o Network (B): unifichi diagnosi strategica, controllo d'esecuzione e ricerca riservata di partner in un'unica plancia deterministica a costo server zero.

🎁 VUOI GUIDARLA GRATIS PER UN ANNO O PIÙ DA GENNAIO 2027?
Vai su https://www.c-t-d.group/news.html#news-ep-01 : lascia il tuo feedback insieme alla tua email per iscriverti alla newsletter delle puntate e blocca subito il tuo posto nel Programma Early Adopter!

🔪 Prossima puntata (#02): Come si uccide l'angolo cieco del "Non so cosa non so"? Vedremo cosa succede premendo il pulsante del Cervello.

#ConnectTheDOTS #SerialKillerApp #3SystemsInOnePlatform #EdgeAI #StrategiaAziendale #Gennaio2027 #EarlyAdopter"""
    },
    {
        "num": 2,
        "date": "9 Novembre 2026",
        "doc_title": "Connect the DOTS #02: Dal Non So Cosa Non So al DOT L3",
        "title": "Cervello, Orizzonti e Triage Diagnostico Causale",
        "subtitle": "Dal 'Non so cosa non so' all'individuazione matematica del Next Best Dot (NBD)",
        "crop": (15, 140, 670, 680),
        "pts": [1, 3, 4, 5, 8],
        "victim": "Il foglio bianco dei chatbot generativi (dove devi gia' sapere quale domanda fare) e le risposte probabilistiche con allucinazioni.",
        "killer_feature": "Regola aurea Cervello/Orizzonti (L0 -> L1 -> DOT L2 Problema) + Triage Diagnostico assistito con opzione 'Altro' (da specificare) + Proliferazione causale verso il DOT L3 Soluzione (NBD).",
        "payoff_persona": "Trasformi un disagio confuso nella causa radice esatta e nella prima azione concreta da compiere.",
        "payoff_prof": "Il cliente arriva da te avendo gia' qualificato il proprio bisogno sull'L3 Ancora, azzerando i tempi di pre-analisi.",
        "payoff_pmi": "Isoli in 3 minuti il vero collo di bottiglia operativo o finanziario senza allucinazioni da chatbot.",
        "next_teaser": "Tra 48 ore (Puntata #03): Cosa succede ai 900 nodi aziendali che non hai ancora esplorato? Scopriremo la SWOT in RAM e il tasto 'Pausa'.",
        "post_text": """🔪 Anatomia di una Serial Killer App — Puntata #02: Come uccidere il foglio bianco dei chatbot e l'angolo cieco del "Non so cosa non so".
(Sfoglia il carosello per la Slide da 1.000 parole e la Timeline [✓] delle puntate pubblicate 👇).

Avete presente il paradosso di ChatGPT e dei chatbot tradizionali? Per ottenere una risposta utile devi già sapere quale domanda fare. Ma nella vita e in azienda i blocchi più gravi nascono quando:
1. "Non so cosa non so, finché qualcuno non me lo fa notare".
2. "Non so di cosa ho bisogno, finché qualcuno non mi presenta degli aiuti concreti".

Ecco cosa fai al volante di Connect the DOTS (disponibile da Gennaio 2027) in 60 secondi:
🔹 Regola Aurea del Cervello (Punti 1, 3): non puoi guardare fuori (Sinapsi) o agire (Pratica) finché non hai capito dove sei partendo dal Cervello — oppure cliccando su Orizzonti per selezionare un altro ambito L0.
🔹 Qualificazione Causale (Punti 4, 5): navighi tra ~1.000 DOT fino al tuo DOT L2 Problema padre.
🔹 Triage Diagnostico non costrittivo (Punto 8): rispondi a percorsi trasparenti pre-confezionati dagli SME più l'opzione "Altro" (con invito a specificare la tua unicità). Senza mai ragionare per banale similarità statistica, ma per nesso causale (NBD -> NBA -> NBM), CtD illumina in verde il tuo DOT L3 Soluzione (Next Best Dot).

🎯 IL PAYOFF DI QUESTA FUNZIONE PER TE:
👤 Persona (P): trasformi un'ansia o un blocco confuso nella causa radice esatta e nella prima azione concreta da compiere, 100% offline.
🎓 Professionista / SME: i clienti arrivano da te avendo già qualificato il proprio bisogno sull'L3 Ancora dove sei specialista, azzerando i tempi di pre-analisi.
🏢 Imprenditore / PMI (B): elimini le decisioni "di pancia" e le allucinazioni dei chatbot isolando in 3 minuti il vero collo di bottiglia operativo o finanziario.

🎁 LASCIA IL TUO FEEDBACK = 1 ANNO+ GRATIS DA GENNAIO 2027
Vai su https://www.c-t-d.group/news.html#news-ep-02 , dicci cosa ne pensi del Triage Diagnostico causale e iscriviti alla newsletter per assicurarti il Programma Early Adopter gratuito!

🔪 Prossima puntata (#03): Cosa succede ai 900 nodi che non hai ancora esplorato? Scopriremo la SWOT in RAM (10/10) e il tasto sovrano "Pausa".

#ConnectTheDOTS #SerialKillerApp #ProblemSolving #DecisionMaking #CoachPrivato #PMI #Gennaio2027"""
    },
    {
        "num": 3,
        "date": "11 Novembre 2026",
        "doc_title": "Connect the DOTS #03: SWOT in RAM (10/10) e Tasto Pausa",
        "title": "SWOT in RAM (Ignoto = 10/10) e il Tasto Sovrano 'Pausa'",
        "subtitle": "Perche' cio' che non conosci vale Rischio Massimo (e come spegnerlo con un clic per spendere tempo di qualita')",
        "crop": (15, 580, 670, 1075),
        "pts": [6, 7],
        "victim": "Le analisi SWOT statiche dimenticate nei PDF e i cruscotti tradizionali che guardano solo il fatturato ignorando gli angoli ciechi.",
        "killer_feature": "Algoritmo _healDatabaseRollups in RAM: ogni nodo ignoto = Debolezza 10/10 e Minaccia 10/10; tasto Pausa = reset a '0'; metriche oltre il fatturato + Regime Fiscale + Scudo Anonimizzazione AI.",
        "payoff_persona": "Azzeri il sovraccarico cognitivo mettendo in 'Pausa' ('0') cio' che non e' prioritario per dedicarti solo a cio' che conta.",
        "payoff_prof": "Offri alle PMI clienti stress test e cruscotti predittivi in RAM su oltre 400 lenti direzionali.",
        "payoff_pmi": "Vedi in tempo reale dove si annidano le minacce 10/10 nei tuoi 8 orizzonti senza far uscire un byte dal tuo Mac/PC.",
        "next_teaser": "Tra 48 ore (Puntata #04): Perche' bruciare gigawatt su server cloud per rielaborare risposte gia' note? Scopriremo l'Esperanto dei ~1.000 DOT.",
        "post_text": """🔪 Anatomia di una Serial Killer App — Puntata #03: La fine delle analisi SWOT dimenticate nei PDF e dei cruscotti che guardano solo il fatturato.

Nella gestione tradizionale, ciò che non conosciamo viene ignorato: vale zero. Finché un giorno quell'angolo cieco esplode.

Se oggi stessi usando il tuo Profilo aggiornato in Connect the DOTS (in uscita a Gennaio 2027), vedresti l'algoritmo di auto-guarigione (_healDatabaseRollups) calcolare istantaneamente la tua SWOT in RAM (Punti 6 e 7):

1️⃣ L'ignoto vale Rischio Massimo (10/10): ogni nodo non conosciuto o non intenzionalmente presidiato vale automaticamente Debolezza (10/10) e Minaccia (10/10) coi colori dei 4 spicchi del nodo.
2️⃣ Il Tasto Sovrano "Pausa" ('0'): per non farti travolgere da tutto ciò che è scoperto, premi il pulsante Pausa sui nodi che scegli consapevolmente di rimandare. I valori si resettano a '0' ed escono da ogni calcolo matematico, regalandoti il lusso di spendere tempo di qualità solo sulle tue priorità.
3️⃣ Oltre il Fatturato + Scudo AI: fin dall'input iniziale CtD richiede il tuo Regime Fiscale, governa qualsiasi metrica oltre i ricavi nella formula S = C + P + T + R e protegge le domande libere all'AI con lo Scudo di Anonimizzazione automatico.

🎯 IL PAYOFF DI QUESTA FUNZIONE PER TE:
👤 Persona (P): azzeri il sovraccarico mentale spegnendo col tasto Pausa ciò che oggi non puoi seguire, concentrandoti su un obiettivo alla volta.
🎓 Professionista / Commercialista / Advisor: offri ai tuoi clienti stress test e cruscotti predittivi in RAM su oltre 400 lenti direzionali.
🏢 Imprenditore / PMI (B): vedi in tempo reale dove si annidano le minacce 10/10 nei tuoi 8 orizzonti aziendali senza che un solo byte esca dal tuo Mac o PC.

🎁 BLOCCA 1 ANNO+ DI LICENZA GRATUITA DA GENNAIO 2027:
Quali nodi metteresti subito in "Pausa" e quali accenderesti? Scrivicelo su https://www.c-t-d.group/news.html#news-ep-03 insieme alla tua email per la newsletter!

🔪 Prossima puntata (#04): Perché bruciare gigawatt su server cloud per rielaborare risposte già note? Scopriremo l'"Esperanto" dei ~1.000 DOT.

#ConnectTheDOTS #SerialKillerApp #SWOT #ControlloDiGestione #CFO #Imprenditori #Gennaio2027"""
    },
    {
        "num": 4,
        "date": "13 Novembre 2026",
        "doc_title": "Connect the DOTS #04: L'Esperanto dei 1.000 DOT Offline",
        "title": "L'Esperanto dei ~1.000 DOT e la Micro-Blockchain Offline",
        "subtitle": "Sostenibilita' energetica Edge AI, conformita' nativa GDPR / EU AI Act e integrita' locale a costo server zero",
        "crop": (15, 140, 670, 1075),
        "pts": [2, 7, 16],
        "victim": "Lo spreco energetico dei data center AI Cloud e la Babele linguistica che impedisce a domanda e offerta di capirsi.",
        "killer_feature": "Knowledge Graph olografico di ~1.000 DOT ordinati (sort_order) come lingua franca ('Esperanto') + esecuzione 100% offline + catena crittografica SQLite (local_source_chain) a costo server zero.",
        "payoff_persona": "Navighi anche offline con latenza 0 ms e certezza matematica che il tuo Profilo aggiornato resti solo tuo.",
        "payoff_prof": "Parli finalmente lo stesso codice ('Esperanto') dei tuoi potenziali clienti sul nodo L3 della tua specializzazione.",
        "payoff_pmi": "Adotti l'AI in azienda azzerando rischi GDPR / EU AI Act e canoni ricorrenti di server e token cloud.",
        "next_teaser": "Tra 48 ore (Puntata #05): Capire il problema e' inutile se il buon proposito muore in una lista di To-Do. Entreremo nel Secondo Cervello.",
        "post_text": """🔪 Anatomia di una Serial Killer App — Puntata #04: Uccidere lo spreco energetico dell'AI Cloud e la Babele dei linguaggi aziendali.

Ogni giorno milioni di utenti interrogano data center remoti bruciando quantità immense di energia per farsi rigenerare da zero risposte che gli esperti umani di dominio (SME) conoscono già. E quando una PMI cerca uno specialista, usano parole diverse e non si capiscono.

Ecco cosa accade in Connect the DOTS (Punti 2, 7, 16 — disponibile da Gennaio 2027):
🔹 Intelligenza Capitalizzata 100% Offline: il sapere degli SME è codificato in un Knowledge Graph di ~1.000 nodi ordinati (sort_order) che gira interamente sul tuo dispositivo. Zero consumi cloud ricorrenti e conformità nativa a GDPR ed EU AI Act.
🔹 L'"Esperanto" della Community: quei ~1.000 DOT in italiano chiaro diventano la lingua franca condivisa da Persone, Professionisti, PMI e Network.
🔹 Mini Micro-Blockchain Offline (local_source_chain): ogni avanzamento del tuo Profilo aggiornato è sigillato localmente su SQLite con integrità anti-manomissione a costo server zero.

🎯 IL PAYOFF DI QUESTA FUNZIONE PER TE:
👤 Persona (P): navighi anche offline con latenza 0 ms e con la certezza matematica che il tuo Profilo aggiornato resti solo sul tuo device.
🎓 Professionista / SME: parli finalmente lo stesso codice ("Esperanto") dei tuoi potenziali clienti sul nodo L3 della tua specializzazione.
🏢 Imprenditore / PMI (B): adotti l'AI in azienda azzerando i rischi sanzionatori di GDPR / EU AI Act e i canoni ricorrenti di server e token cloud.

🎁 LASCIA IL TUO FEEDBACK PER AVERE 1 ANNO+ GRATIS DA GENNAIO 2027:
Vai su https://www.c-t-d.group/news.html#news-ep-04 , lascia il tuo parere e iscriviti alla newsletter delle puntate!

🔪 Prossima puntata (#05): Capire il problema non basta se il buon proposito muore in una lista di To-Do. Entreremo in "2° CtD 2°B: Secondo Cervello".

#ConnectTheDOTS #SerialKillerApp #EdgeAI #AIAct #GDPR #Sostenibilita #Gennaio2027"""
    },
    {
        "num": 5,
        "date": "15 Novembre 2026",
        "doc_title": "Connect the DOTS #05: 2° Cervello, To-Do e Cantieri L3",
        "title": "2° Cervello: Proliferazione To-Do -> L3 Progetto & Sinapsi",
        "subtitle": "Come trasformare ogni compito in un cantiere strutturato collegato alla strategia",
        "crop": (650, 140, 1315, 660),
        "pts": [9, 10, 11, 12],
        "victim": "Il cimitero delle liste To-Do e dei project manager scollegati dagli obiettivi strategici.",
        "killer_feature": "Proliferazione automatica (To-Do / MIO_Idea -> L3 Progetto / MIO_Goal con parent_uuid verticale) + Sinapsi Orizzontali Bidirezionali (evolvedFrom / peerFlow in UserSynapseState) + Mattoni L3 tra stato P e traguardo T.",
        "payoff_persona": "Non perdi mai piu' il legame tra un'idea annotata al volo e il traguardo di vita a cui serve.",
        "payoff_prof": "Consegni ai clienti non un PDF teorico ma un cantiere L3 gia' scomposto in mattoni esecutivi.",
        "payoff_pmi": "Colleghi ogni singolo task operativo del team all'obiettivo strategico padre eliminando la dispersione.",
        "next_teaser": "Tra 48 ore (Puntata #06): Chi esegue materialmente ogni mattone del cantiere e chi certifica il risultato? Scopriremo la Palestra di 21 Giorni.",
        "post_text": """🔪 Anatomia di una Serial Killer App — Puntata #05: Uccidere il cimitero delle liste "To-Do" scollegate dalla strategia.

Quante volte hai annotato un'idea o un'azione urgente su un'app di note perdendo dopo tre giorni il legame con l'obiettivo strategico che l'aveva generata?

Oggi entriamo nel secondo sistema integrato di Connect the DOTS — 2° CtD 2°B: Secondo Cervello (Punti 9..12 — in uscita a Gennaio 2027):
1️⃣ Proliferazione Progettuale (To-Do / MIO_Idea -> L3 Progetto / MIO_Goal): non appena decidi di affrontare un compito, CtD lo fa proliferare automaticamente in un cantiere strutturato mantenendo intatta la gerarchia verticale (parent_uuid).
2️⃣ Sinapsi Orizzontali Bidirezionali (MIEI <-> MIEI): i flussi logici tra nodi allo stesso livello (evolvedFrom / peerFlow in UserSynapseState) vengono tracciati senza mai alterare l'albero maestro.
3️⃣ Mattoni Operativi sull'L3 Ancora: trovi già scomposti i passi pratici che separano il tuo stato attuale (P) dal tuo traguardo (T), senza standardizzare i tuoi fini.

🎯 IL PAYOFF DI QUESTA FUNZIONE PER TE:
👤 Persona (P): non perdi mai più il filo tra un'idea annotata al volo e l'obiettivo di vita a cui serve.
🎓 Professionista / Coach / Consulente: consegni ai clienti non un PDF teorico, ma un cantiere L3 già scomposto in mattoni esecutivi.
🏢 Imprenditore / PMI (B): colleghi ogni singolo task operativo del team all'obiettivo strategico padre eliminando la dispersione.

🎁 ASSICURATI 1 ANNO+ DI LICENZA GRATUITA DA GENNAIO 2027:
Vai su https://www.c-t-d.group/news.html#news-ep-05 , lascia il tuo feedback sulla Proliferazione progettuale e iscriviti alla newsletter!

🔪 Prossima puntata (#06): Chi esegue materialmente ogni mattone del cantiere e chi certifica il risultato? Scopriremo la Palestra di 21 Giorni e il PoR.

#ConnectTheDOTS #SerialKillerApp #SecondoCervello #Execution #ProjectManagement #PMI #Gennaio2027"""
    },
    {
        "num": 6,
        "date": "17 Novembre 2026",
        "doc_title": "Connect the DOTS #06: Palestra 21 Giorni e PoR Multi-Sig",
        "title": "Allocazione a 3 Vie, Palestra di 21 Giorni e Certificato PoR",
        "subtitle": "Dalla teoria alla pratica certificata con scudo crittografico 2-of-2 Multi-Sig",
        "crop": (650, 560, 1315, 1075),
        "pts": [13, 14, 15, 16],
        "victim": "I corsi di formazione che restano sulla carta e le metriche di risultato autodichiarate senza verifica.",
        "killer_feature": "Smistamento sovrano a 3 vie per ogni mattone (Fai-da-Te in Palestra / Vista 1 SME / Vista 2 Rete + 'Altro') + Palestra operativa di 21 giorni + Certificato Proof-of-Result (PoR 2-of-2 Multi-Sig).",
        "payoff_persona": "Costruisci un portafoglio inoppugnabile di certificati PoR su risultati reali raggiunti.",
        "payoff_prof": "Trasformi il tuo metodo in una Palestra di 21 giorni che garantisce la messa a terra da parte del cliente.",
        "payoff_pmi": "Decidi mattone per mattone cosa fare in casa e cosa delegare all'esterno misurando solo risultati veri.",
        "next_teaser": "Tra 48 ore (Puntata #07): Cosa accade quando il tuo parametro R su un DOT diventa altissimo (R >>)? Scopriremo la qualifica a Proven SME.",
        "post_text": """🔪 Anatomia di una Serial Killer App — Puntata #06: Uccidere la formazione teorica senza pratica e i risultati autodichiarati.

Quando apri un cantiere L3 Progetto in Connect the DOTS (in uscita a Gennaio 2027), davanti a ogni mattone che ti separa dal tuo Target (T) hai uno Smistamento Sovrano a 3 Vie (Punto 13 — più l'opzione "Altro" da specificare):
🔹 1ª Via — Fai-da-Te nella Palestra di 21 Giorni (Punto 14): ti alleni sul campo per 21 giorni operativi consecutivi finché la competenza diventa abitudine.
🔹 2ª Via — Vista 1 (Provider P&S / Proven SME): attivi on-demand un fornitore o un esperto qualificato già cablato su quell'L3 Ancora.
🔹 3ª Via — Vista 2 (Rete IR): coinvolgi un contatto fidato della tua rete relazionale.

E al 21° giorno? Scatta il Certificato Proof-of-Result (PoR — Punto 15): uno scudo crittografico a doppia firma (2-of-2 Multi-Sig) inciso sulla tua local_source_chain offline (Punto 16). Solo allora il parametro R della tua formula S = C + P + T + R sale davvero.

🎯 IL PAYOFF DI QUESTA FUNZIONE PER TE:
👤 Persona (P) o Giovane Talento: costruisci un portafoglio inoppugnabile di certificati crittografici PoR su problemi reali risolti.
🎓 Professionista / Formatore: trasformi il tuo metodo in una Palestra di 21 giorni che garantisce la messa a terra reale da parte del cliente.
🏢 Imprenditore / PMI (B): decidi mattone per mattone cosa fare internamente e cosa delegare all'esterno, misurando solo risultati certificati.

🎁 PRENOTA 1 ANNO+ GRATIS DA GENNAIO 2027:
Vai su https://www.c-t-d.group/news.html#news-ep-06 , lascia il tuo feedback sulla Palestra di 21 Giorni e iscriviti alla newsletter!

🔪 Prossima puntata (#07): Cosa accade quando il tuo parametro R su un DOT diventa altissimo (R >>)? Scopriremo il "Cordone Ombelicale" e la qualifica a Proven SME via NEXUS.

#ConnectTheDOTS #SerialKillerApp #Palestra21Giorni #ProofOfResult #Meritocrazia #Coaching #Gennaio2027"""
    },
    {
        "num": 7,
        "date": "19 Novembre 2026",
        "doc_title": "Connect the DOTS #07: Cordone Ombelicale e Proven SME",
        "title": "Cordone Ombelicale 21gg e Qualifica Proven SME (R>>) NEXUS",
        "subtitle": "La fine dei finti guru: come i risultati reali ti portano i clienti in modalita' Pull",
        "crop": (650, 560, 1905, 1075),
        "pts": [14, 15, 20, 24],
        "victim": "I finti guru da tastiera che vincono urlando sui social e l'abbandono del cliente dopo la sessione di consulenza.",
        "killer_feature": "Cordone Ombelicale di 21 giorni tra professionista (es. BNI Barbarossa) e migliori clienti + Qualifica automatica a Proven SME raggiungendo R >> + Cooptazione via NEXUS sull'L3 Ancora della Community.",
        "payoff_persona": "Anche senza budget pubblicitario, se eccelli su un DOT (R >>) vieni cooptato e reso visibile on-demand.",
        "payoff_prof": "Blindi i tuoi clienti attuali col Cordone Ombelicale di 21gg e ricevi nuovi incarichi in Pull sugli L3 dove hai R >>.",
        "payoff_pmi": "Attingi solo a Proven SME i cui risultati R >> sono stati certificati sul campo dalla piattaforma.",
        "next_teaser": "Tra 48 ore (Puntata #08): Come chiedi aiuto alla tua rete senza mai rivelare agli amici qual e' la tua debolezza 10/10? Ecco il Salto del 1° Grado.",
        "post_text": """🔪 Anatomia di una Serial Killer App — Puntata #07: Uccidere i finti guru da tastiera e l'abbandono del cliente dopo la consulenza.

Sui social tradizionali vince chi urla più forte, anche se non ha mai risolto un caso reale. E per i professionisti seri c'è un secondo dramma: finita la sessione di consulenza, il cliente torna in azienda travolto dalle urgenze e il legame si spezza.

A Gennaio 2027 Connect the DOTS eliminerà entrambe queste distorsioni (Punti 14, 15, 20, 24):
1️⃣ Il "Cordone Ombelicale" di 21 Giorni coi tuoi migliori clienti (Punto 14): il professionista (es. membro di un Capitolo BNI Barbarossa o advisor) usa la Palestra di 21 giorni insieme ai suoi clienti migliori, accompagnandoli nell'esecuzione quotidiana e blindando la fidelizzazione.
2️⃣ Qualifica Meritocratica a "Proven SME" (R >>) via NEXUS (Punti 15, 20, 24): quando usando CtD raggiungi un risultato reale certificato R >> su un DOT, CtD ti qualifica per essere cooptato (con consenso scritto) sull'L3 Ancora. L'Admin di CtD, dopo verifica via NEXUS, ti incorpora nella lista di distribuzione on-demand della Community.

🎯 IL PAYOFF DI QUESTA FUNZIONE PER TE:
👤 Persona / Talento emergente (P): anche senza budget pubblicitario, se eccelli su una competenza (R >>) vieni cooptato e reso visibile on-demand.
🎓 Professionista / Proven SME: blindi i tuoi clienti attuali col Cordone Ombelicale di 21gg e ricevi nuovi incarichi in modalità Pull sugli L3 dove hai dimostrato R >>.
🏢 Imprenditore / PMI (B): quando ti serve uno specialista su un mattone critico, attingi a Proven SME i cui risultati R >> sono stati verificati sul campo.

🎁 LASCIA IL TUO FEEDBACK PER AVERE 1 ANNO+ GRATIS DA GENNAIO 2027:
Vai su https://www.c-t-d.group/news.html#news-ep-07 , inviaci il tuo feedback e iscriviti alla newsletter!

🔪 Prossima puntata (#08): Come chiedi aiuto alla tua rete senza mai far sapere ai tuoi amici o contatti diretti qual è la tua debolezza 10/10? Scopriremo il "Salto del 1° Grado".

#ConnectTheDOTS #SerialKillerApp #ProvenSME #Consulenza #ProfessionalServices #NEXUS #Gennaio2027"""
    },
    {
        "num": 8,
        "date": "21 Novembre 2026",
        "doc_title": "Connect the DOTS #08: Score Ponte e Salto del 1° Grado",
        "title": "Network Engineering: Score Ponte e 'Salto del 1° Grado'",
        "subtitle": "Raggiungere il risolutore perfetto al 2° grado senza mai esporre le tue debolezze 10/10 ai contatti diretti",
        "crop": (1300, 140, 1905, 680),
        "pts": [17, 18, 19, 20, 21],
        "victim": "Il networking a freddo e l'imbarazzo di dover confessare le proprie debolezze 10/10 agli amici o contatti di 1° grado.",
        "killer_feature": "Grafo relazionale ir_contacts_graph ('chi mi ha presentato chi') + calcolo in RAM di Score Diretto vs Score Ponte + Capsule anonimizzate da 1 KB (.ctdir / QR) con Smart Source-Routing ('Salto del 1° Grado').",
        "payoff_persona": "Chiedi supporto su scelte delicate raggiungendo lo specialista di 2° grado in totale riservatezza.",
        "payoff_prof": "Valorizzi il tuo Score Ponte diventando lo snodo scientifico di referenze inter-capitolo ad alta conversione.",
        "payoff_pmi": "Trovi fornitori o manager per risolvere una criticita' 10/10 senza che concorrenti o conoscenti sappiano del problema.",
        "next_teaser": "Tra 48 ore (Puntata #09): Trovato il match tra reti, professionisti e PMI, come ci si scambia valore anche senza bruciare cassa? Ecco l'HTLC.",
        "post_text": """🔪 Anatomia di una Serial Killer App — Puntata #08: Uccidere l'imbarazzo di mostrare le proprie debolezze 10/10 agli amici o contatti di 1° grado.

Quando un imprenditore o un professionista ha una criticità delicata (Debolezza 10/10), l'ultima cosa che vuole fare è telefonare al conoscente diretto dicendo "Ho questo problema grave". Eppure chi può risolverlo si trova quasi sempre al 2° grado (tra i contatti dei propri contatti).

Ecco come il terzo motore di Connect the DOTS — 3° CtD NE: Network Engineering (Punti 17..21 — in uscita a Gennaio 2027) — risolve il paradosso:
🔹 Genealogia Relazionale (ir_contacts_graph — Punto 18): traccia "chi mi ha presentato chi" attraverso Capitoli (BNI Barbarossa & beyond) e network.
🔹 Calcoli Istantanei in RAM (Punto 19): distingue in tempo reale lo Score Diretto (chi risolve l'L3) dallo Score Ponte (chi è il miglior tramite verso il 2° grado).
🔹 Capsule da 1 KB (.ctdir / QR) e "Salto del 1° Grado" (Smart Source-Routing — Punti 20, 21): generi un Next Best Match (NBM) riservato che permette al tuo contatto Ponte di instradarti al 2° grado senza mai mostrare le tue debolezze 10/10 agli amici o contatti diretti.

🎯 IL PAYOFF DI QUESTA FUNZIONE PER TE:
👤 Persona (P): chiedi supporto su scelte delicate raggiungendo lo specialista di 2° grado tramite la tua rete in totale riservatezza.
🎓 Professionista / Connettore BNI: valorizzi il tuo Score Ponte diventando lo snodo scientifico di referenze qualificate ad altissima conversione.
🏢 Imprenditore / PMI (B): trovi fornitori, partner o manager per risolvere una criticità 10/10 senza che concorrenti o conoscenti diretti sappiano del tuo problema.

🎁 ASSICURATI 1 ANNO+ DI LICENZA GRATUITA DA GENNAIO 2027:
Cosa ne pensi del "Salto del 1° Grado"? Scrivicelo su https://www.c-t-d.group/news.html#news-ep-08 insieme alla tua email per la newsletter!

🔪 Prossima puntata (#09): Trovato il match tra reti, professionisti e PMI, come ci si scambia valore anche senza bruciare liquidità? Ecco la Compensazione in-Lire Fluida (HTLC) a Doppio Binario.

#ConnectTheDOTS #SerialKillerApp #NetworkEngineering #BNI #BusinessMatching #Privacy #Gennaio2027"""
    },
    {
        "num": 9,
        "date": "23 Novembre 2026",
        "doc_title": "Connect the DOTS #09: Scambio Fluido in-Lire HTLC B2B",
        "title": "Compensazione in-Lire Fluida (HTLC) a Doppio Binario",
        "subtitle": "Il motore di intersezione tra network (BNI, circuiti B2B, professionisti e PMI) raccordato al Regime Fiscale",
        "crop": (1300, 600, 1905, 1075),
        "pts": [22, 23, 24],
        "victim": "La separazione tra network diversi e la staticita' dei circuiti di scambio usati come semplici cataloghi passivi.",
        "killer_feature": "Motore di retention, lead generation e intersezione cross-network + Compensazione in-Lire Fluida (HTLC) a Doppio Binario (Binario 1: Ore-Palestra tra individui | Binario 2: Crediti B2B tra imprese) + P2P Bonjour/AirDrop.",
        "payoff_persona": "Monetizzi il tuo tempo col Binario 1 (Ore-Palestra) ottenendo l'affiancamento di altri esperti senza esborsi.",
        "payoff_prof": "Incroci il tuo Capitolo professionale con la domanda qualificata delle aziende appartenenti ai circuiti B2B.",
        "payoff_pmi": "Finanzi i tuoi cantieri L3 tramite il Binario 2 (Crediti B2B), generando nuovi clienti e preservando la liquidita'.",
        "next_teaser": "Serie Aperta: proponi nel modulo Feedback su www.c-t-d.group/news.html quale problema vuoi vedere nella prossima puntata!",
        "post_text": """🔪 Anatomia di una Serial Killer App — Puntata #09: Uccidere la separazione tra network diversi e la staticità dei circuiti usati come cataloghi passivi.

Perché tante aziende iscritte a circuiti di credito commerciale o a network professionali faticano a generare scambi continui? Perché cercano a catalogo dopo aver pensato a un acquisto banale, invece di partire dai propri cantieri strategici L3.

Guarda cosa accade nei punti 22, 23 e 24 di Connect the DOTS (in arrivo a Gennaio 2027):
1️⃣ Motore di Intersezione, Retention e Lead Generation (Punto 22): lo scambio di beni, servizi e referenze nasce direttamente dai cantieri L3 aperti dagli utenti, unendo circuiti esistenti (in-Lire e competitor), Capitoli BNI, professionisti, talenti e PMI.
2️⃣ Compensazione in-Lire Fluida (HTLC) a Doppio Binario (Punto 23): raccordata fin dall'input iniziale al tuo Regime Fiscale:
   - Binario 1 (Ore-Palestra): scambio di tempo e affiancamento tra individui nei cantieri di 21 giorni.
   - Binario 2 (Crediti B2B): compensazione di forniture, consulenze e referenze tra imprese e partite IVA.
3️⃣ P2P Locale (Bonjour + AirDrop) + Super-Ponte (Punto 24): scambio immediato a costo server zero.

🎯 IL PAYOFF DI QUESTA FUNZIONE PER TE:
👤 Persona o Talento (P): monetizzi il tuo tempo col Binario 1 (Ore-Palestra) ottenendo l'affiancamento di altri esperti senza esborsi monetari.
🎓 Professionista / Membro BNI: moltiplichi le opportunità incrociando il tuo Capitolo con le esigenze reali delle aziende dei circuiti B2B.
🏢 Imprenditore / PMI / Circuito B2B (B): finanzi i tuoi cantieri L3 tramite il Binario 2 (Crediti B2B), generando nuovi clienti e preservando la liquidità di cassa.

🎁 SERIE APERTA + 1 ANNO+ DI LICENZA GRATUITA DA GENNAIO 2027:
Vai su https://www.c-t-d.group/news.html#news-ep-09 : lascia il tuo feedback (o proponi quale problema vuoi veder "eliminato" nella prossima puntata!) insieme alla tua email per assicurarti 1 Anno+ Gratis nel Programma Early Adopter!

#ConnectTheDOTS #SerialKillerApp #InLire #B2B #HTLC #EconomiaReale #Networking #Gennaio2027"""
    }
]

print("=== CONTROLLO UNIFICATO TITOLI (<=58) E TESTO UNICO POST (<=2950 UTF-16) ===")
for ep in episodes:
    n = ep["num"]
    t_len = len(ep["doc_title"])
    p_len = li_utf16_len(ep["post_text"])
    assert t_len <= 58, f"ERRORE Puntata #{n:02d}: Titolo supera 58 car ({t_len})"
    assert p_len <= 2950, f"ERRORE Puntata #{n:02d}: Post supera limite sicurezza ({p_len})"
    print(f"OK Puntata #{n:02d}: Titolo = {t_len}/58 car. | Post Unico (con link) = {p_len}/3000 (Margine: +{3000 - p_len})")

ss1_path = os.path.join(assets_dir, "ctd_plancia_ss1.png")
base_ss1 = Image.open(ss1_path).convert("RGB").resize((1920, 1080))

def build_trailer_slide():
    s0 = Image.new("RGB", (1920, 1080), (10, 10, 15))
    d0 = ImageDraw.Draw(s0)

    d0.rectangle([0, 0, 1920, 102], fill=(22, 16, 42))
    d0.text((45, 16), "PUNTATA #00 (IL TRAILER UFFICIALE)  •  SERIE APERTA 'ANATOMIA DI UNA SERIAL KILLER APP' (VERSO GENNAIO 2027)", font=get_font(21, True), fill=(245, 197, 24))
    d0.text((45, 48), "Come si presenta al mercato la prima 'App-non-App' che non e' mai esistita prima?", font=get_font(32, True), fill=(255, 255, 255))

    bg_left = ImageEnhance.Brightness(base_ss1.resize((920, 880))).enhance(0.24)
    s0.paste(bg_left, (35, 120))
    d0.rectangle([35, 120, 955, 1000], outline=(245, 197, 24), width=3)
    d0.rectangle([35, 120, 955, 174], fill=(34, 24, 62))
    d0.text((55, 134), ">> LA SFIDA: PRESENTARE LA PRIMA 'APP-NON-APP' (5 FUMETTI CHIAVE)", font=get_font(21, True), fill=(245, 197, 24))

    cx, cy = 495, 525
    for tx, ty, col in [(255, 290, (56, 189, 248)), (735, 290, (245, 197, 24)), (255, 690, (192, 132, 252)), (735, 690, (60, 208, 112))]:
        d0.line([(cx, cy), (tx, ty)], fill=col, width=3)

    d0.ellipse([cx - 105, cy - 105, cx + 105, cy + 105], fill=(18, 14, 38), outline=(245, 197, 24), width=4)
    d0.ellipse([cx - 92, cy - 92, cx + 92, cy + 92], fill=(28, 20, 58), outline=(56, 189, 248), width=2)
    d0.text((cx - 68, cy - 48), "CONNECT", font=get_font(26, True), fill=(255, 255, 255))
    d0.text((cx - 72, cy - 18), "THE DOTS", font=get_font(26, True), fill=(245, 197, 24))
    draw_badge_pill(d0, cx - 74, cy + 18, "L'APP-NON-APP", (60, 208, 112), (0, 0, 0), 15)

    b1 = [52, 192, 435, 382]
    draw_speech_bubble(d0, b1, (cx - 55, cy - 55), (12, 28, 48), (56, 189, 248), width=3)
    draw_badge_pill(d0, 70, 206, "1. AI ESTESA MA 100% OFFLINE", (56, 189, 248), (0, 0, 0), 16)
    draw_wrapped_block(d0, 70, 246, 350, "\"Usa il meglio dell'AI + il sapere umano degli SME, ma gira al 100% OFFLINE nel tuo Profilo aggiornato!\"", get_font(19, True), (235, 248, 255), 26)

    b2 = [555, 192, 938, 382]
    draw_speech_bubble(d0, b2, (cx + 55, cy - 55), (38, 28, 10), (245, 197, 24), width=3)
    draw_badge_pill(d0, 573, 206, "2. 24 FUNZIONI IN 3 SISTEMI", (245, 197, 24), (0, 0, 0), 16)
    draw_wrapped_block(d0, 573, 246, 350, "\"Non fa una cosa sola: unisce Diagnosi (S=C+P+T+R), 2° Cervello (21gg) e Network Pull in 1 sola Piattaforma!\"", get_font(19, True), (255, 248, 220), 26)

    b3 = [52, 605, 435, 795]
    draw_speech_bubble(d0, b3, (cx - 55, cy + 55), (32, 16, 48), (192, 132, 252), width=3)
    draw_badge_pill(d0, 70, 619, "3. SIA UTENTI 'P' CHE 'B'", (192, 132, 252), (0, 0, 0), 16)
    draw_wrapped_block(d0, 70, 659, 350, "\"Parla una lingua sola ('Esperanto' di ~1.000 DOT) per Persone, Professionisti (R>>), PMI e Network!\"", get_font(19, True), (245, 235, 255), 26)

    b4 = [555, 605, 938, 795]
    draw_speech_bubble(d0, b4, (cx + 55, cy + 55), (12, 38, 24), (60, 208, 112), width=3)
    draw_badge_pill(d0, 573, 619, "4. NATIVA EU AI ACT & GDPR", (60, 208, 112), (0, 0, 0), 16)
    draw_wrapped_block(d0, 573, 659, 350, "\"Scudo di Anonimizzazione AI sulle domande, Regime Fiscale e Micro-Blockchain a costo server zero!\"", get_font(19, True), (230, 255, 240), 26)

    b5 = [52, 822, 938, 982]
    d0.ellipse([488, 765, 502, 779], fill=(245, 197, 24))
    d0.ellipse([484, 790, 506, 812], fill=(245, 197, 24))
    d0.rounded_rectangle(b5, radius=22, fill=(48, 20, 16), outline=(245, 197, 24), width=3)
    draw_badge_pill(d0, 72, 838, "? IL NOSTRO DILEMMA COMUNICATIVO ?", (239, 68, 68), (255, 255, 255), 16)
    draw_wrapped_block(d0, 72, 878, 845, "\"Di fronte a una 'App-non-App' cosi' vasta e mai vista prima, ci siamo chiesti: COME FACCIAMO A RACCONTARLA SENZA SCRIVERE UN MANUALE DI 200 PAGINE?!\"  --->", get_font(20, True), (255, 240, 200), 27)

    d0.rectangle([975, 120, 1885, 1000], fill=(14, 22, 18), outline=(60, 208, 112), width=3)
    d0.rectangle([975, 120, 1885, 174], fill=(20, 48, 34))
    d0.text((995, 134), ">> LA RISPOSTA: LA SERIE APERTA 'ANATOMIA DI UNA SERIAL KILLER APP'", font=get_font(20, True), fill=(60, 208, 112))

    right_bubbles = [
        ("PUNTATA DOPO PUNTATA", (239, 68, 68), "1 Puntata = 1 'Vittima' Illustre Eliminata", "Ogni episodio ti mette al volante di 1 singola funzione che uccide una vecchia illusione (chatbot vuoti, SWOT morte, finti guru, chiamate a freddo)."),
        ("IMPATTO VISIVO IMMEDIATO", (56, 189, 248), "1 Slide che vale 1.000 Parole + Triplo Payoff", "Ogni uscita mostra lo zoom grafico della funzione e il Payoff specifico per Persona (P), Professionista (SME) e Imprenditore/PMI (B)."),
        ("ZERO PUNTATE PERSE", (60, 208, 112), "Timeline Progressiva & Sezione News", "Ogni post aggiunge un Check Verde nella Timeline (Slide 2) e diventa una News leggibile su www.c-t-d.group/news.html per recuperare tutto."),
        ("PREMIO EARLY ADOPTER", (245, 197, 24), "1 Anno+ Gratis da Gennaio 2027 per il tuo Feedback", "Vai sul sito, lascia un feedback + la tua mail per la newsletter e ti assicuri l'uso gratuito per un anno o piu' al lancio di Gennaio 2027!")
    ]

    ry = 190
    for badge_txt, col, title_txt, desc_txt in right_bubbles:
        d0.rounded_rectangle([995, ry, 1865, ry + 132], radius=16, fill=(20, 30, 26), outline=col, width=2)
        end_x = draw_badge_pill(d0, 1012, ry + 12, badge_txt, col, (0, 0, 0), 14)
        d0.text((end_x + 14, ry + 12), title_txt, font=get_font(20, True), fill=(255, 255, 255))
        draw_wrapped_block(d0, 1012, ry + 48, 835, desc_txt, get_font(18, False), (225, 238, 230), 24)
        ry += 144

    d0.rounded_rectangle([995, 772, 1865, 984], radius=16, fill=(24, 16, 44), outline=(245, 197, 24), width=3)
    d0.text((1015, 786), "IL PAYOFF CHE SCOPRIRAI IN OGNI PUNTATA PER IL TUO PROFILO:", font=get_font(19, True), fill=(245, 197, 24))
    d0.text((1015, 822), "• Persona (P): Coach privato offline, Tasto Pausa ('0'), Palestra 21gg e Ore-Palestra.", font=get_font(18, True), fill=(125, 211, 252))
    d0.text((1015, 862), "• Professionista (SME): Cordone Ombelicale 21gg coi clienti e qualifica Proven SME (R >>).", font=get_font(18, True), fill=(253, 224, 71))
    d0.text((1015, 902), "• Imprenditore / PMI / Rete (B): SWOT in RAM, Salto del 1° Grado e Clearing HTLC B2B.", font=get_font(18, True), fill=(216, 180, 254))
    d0.text((1015, 944), ">> Segui le puntate e prenota 1 Anno+ Gratis su: www.c-t-d.group/news.html", font=get_font(18, True), fill=(60, 208, 112))

    d0.rectangle([0, 1015, 1920, 1080], fill=(22, 16, 42))
    d0.text((45, 1033), ">> Scorri alla Slide 2 per la Timeline Progressiva (Zero Spoiler) e il Premio 1 Anno+ Gratis  •  www.c-t-d.group/news.html", font=get_font(21, True), fill=(245, 197, 24))
    return s0

trailer_cover = build_trailer_slide()
trailer_cover.save(os.path.join(assets_dir, "news_ep_00.png"))

for ep in episodes:
    ep_num = ep["num"]
    pts_str = "Tutti (1..24)" if len(ep["pts"]) > 10 else ", ".join(str(p) for p in ep["pts"])

    if ep_num == 0:
        s1 = trailer_cover.copy()
    else:
        s1 = Image.new("RGB", (1920, 1080), (10, 10, 15))
        ds1 = ImageDraw.Draw(s1)
        ds1.rectangle([0, 0, 1920, 105], fill=(22, 16, 42))
        ds1.text((45, 16), f"ANATOMIA DI UNA SERIAL KILLER APP  •  PUNTATA #{ep_num:02d} ({ep['date']})  •  SERIE APERTA VERSO GENNAIO 2027", font=get_font(21, True), fill=(245, 197, 24))
        ds1.text((45, 48), ep["title"], font=get_font(33, True), fill=(255, 255, 255))

        ds1.rectangle([40, 125, 900, 995], fill=(16, 16, 24), outline=(245, 197, 24), width=3)
        ds1.rectangle([40, 125, 900, 175], fill=(32, 24, 58))
        ds1.text((60, 138), f">> LA SLIDE CHE VALE 1.000 PAROLE  •  Componenti attivati: [{pts_str}]", font=get_font(20, True), fill=(245, 197, 24))

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
        draw_badge_pill(ds1, rx1 + 20, 340, ">> LA KILLER FEATURE CtD (COSA FAI AL VOLANTE DELL'APP)", (56, 189, 248), (0, 0, 0), 16)
        draw_wrapped_block(ds1, rx1 + 20, 382, rw, ep["killer_feature"], get_font(20, False), (235, 248, 255), 28)

        ds1.rounded_rectangle([rx1, 565, rx2, 995], radius=16, fill=(16, 34, 24), outline=(60, 208, 112), width=3)
        draw_badge_pill(ds1, rx1 + 20, 580, "IL PAYOFF CONCRETO PER IL TUO PROFILO", (60, 208, 112), (0, 0, 0), 16)

        py = 626
        for badge_lbl, badge_col, p_txt in [
            ("• SE SEI UNA PERSONA O UN TALENTO (P):", (56, 189, 248), ep["payoff_persona"]),
            ("• SE SEI UN PROFESSIONISTA / PROVEN SME (R >>):", (245, 197, 24), ep["payoff_prof"]),
            ("• SE SEI UN IMPRENDITORE / PMI O NETWORK (B):", (192, 132, 252), ep["payoff_pmi"])
        ]:
            ds1.text((rx1 + 20, py), badge_lbl, font=get_font(19, True), fill=badge_col)
            py = draw_wrapped_block(ds1, rx1 + 20, py + 25, rw, p_txt, get_font(19, False), (240, 245, 240), 25) + 14

        ds1.rectangle([0, 1015, 1920, 1080], fill=(22, 16, 42))
        ds1.text((45, 1033), ">> Scorri alla Slide 2 per la Timeline Progressiva (Zero Spoiler) e il Premio 1 Anno+ Gratis  •  www.c-t-d.group/news.html", font=get_font(21, True), fill=(245, 197, 24))
        s1.save(os.path.join(assets_dir, f"news_ep_{ep_num:02d}.png"))

    s_time = Image.new("RGB", (1920, 1080), (10, 10, 14))
    dtime = ImageDraw.Draw(s_time)
    dtime.rectangle([0, 0, 1920, 105], fill=(22, 16, 42))
    dtime.text((50, 18), f"TIMELINE DELLA SERIE APERTA  •  PUNTATE SVELATE FINO A OGGI ({ep_num + 1} PUNTATE ATTIVE)", font=get_font(27, True), fill=(245, 197, 24))
    dtime.text((50, 58), "Recupera le puntate gia' uscite (col Check Verde) nella sezione News su www.c-t-d.group/news.html", font=get_font(20, False), fill=(210, 210, 225))

    ty = 125
    for item in episodes[:ep_num + 1]:
        num = item["num"]
        dt = item["date"]
        tit = item["title"]
        vic = item["victim"]
        is_curr = (num == ep_num)
        bg = (22, 52, 34) if is_curr else (16, 38, 26)
        border = (245, 197, 24) if is_curr else (60, 208, 112)
        dtime.rounded_rectangle([50, ty, 1870, ty + 78], radius=12, fill=bg, outline=border, width=3 if is_curr else 2)

        draw_vector_checkbox(dtime, 72, ty + 18, size=42, checked=True)
        status_lbl = f"PUNTATA #{num:02d} ({dt}) — USCITA OGGI" if is_curr else f"PUNTATA #{num:02d} ({dt}) — GIA' PUBBLICATA"
        t_col = (245, 197, 24) if is_curr else (140, 245, 175)

        dtime.text((134, ty + 12), f"{status_lbl}:  {tit}", font=get_font(21, True), fill=t_col)
        dtime.text((134, ty + 44), f">> {vic[:115]}", font=get_font(18, False), fill=(230, 235, 230))
        ty += 90

    dtime.rounded_rectangle([50, ty + 6, 1870, ty + 96], radius=12, fill=(38, 26, 12), outline=(245, 197, 24), width=2)
    draw_vector_checkbox(dtime, 72, ty + 30, size=42, checked=False)
    dtime.text((134, ty + 18), f"PROSSIMA USCITA (PUNTATA #{ep_num + 1:02d}) — IN ARRIVO TRA 48 ORE...", font=get_font(21, True), fill=(245, 197, 24))
    dtime.text((134, ty + 52), f">> Indizio: {ep['next_teaser']}", font=get_font(19, False), fill=(255, 240, 200))
    ty += 112

    dtime.rounded_rectangle([50, ty, 1870, ty + 74], radius=12, fill=(18, 28, 46), outline=(56, 189, 248), width=2)
    dtime.text((75, ty + 12), "+ STRUTTURA APERTA IN EVOLUZIONE: LA TIMELINE SI ARRICCHISCE DI PUNTATA IN PUNTATA", font=get_font(20, True), fill=(56, 189, 248))
    dtime.text((75, ty + 42), "Quale 'falsa promessa' o problema aziendale vorresti veder eliminato nelle prossime puntate? Scrivicelo su www.c-t-d.group/news.html!", font=get_font(18, False), fill=(225, 240, 255))

    dtime.rounded_rectangle([50, 920, 1870, 1055], radius=14, fill=(26, 16, 48), outline=(245, 197, 24), width=3)
    dtime.text((75, 936), "PREMIO EARLY ADOPTER: VUOI USARE CONNECT THE DOTS GRATIS (1 ANNO+) DA GENNAIO 2027?", font=get_font(23, True), fill=(245, 197, 24))
    dtime.text((75, 974), "1. Vai su www.c-t-d.group/news.html  •  2. Lascia il tuo Feedback sulle funzioni + la tua Email per la Newsletter delle puntate", font=get_font(20, False), fill=(255, 255, 255))
    dtime.text((75, 1010), "3. Ti assicuri subito l'accesso gratuito per un anno o piu' al lancio di Gennaio 2027 (Persona P • Professionista SME • Imprenditore/PMI B).", font=get_font(19, True), fill=(60, 208, 112))

    pdf_name = f"Carosello_LinkedIn_Puntata_{ep_num:02d}.pdf"
    s1.save(os.path.join(out_desktop_dir, pdf_name), "PDF", resolution=150.0, save_all=True, append_images=[s_time])
    s1.save(os.path.join(caroselli_web_dir, pdf_name), "PDF", resolution=150.0, save_all=True, append_images=[s_time])

# ==============================================================================
# GENERAZIONE DI regia_linkedin.html CON 2 SOLI PASSI (ZERO TASTO VERDE!)
# ==============================================================================
cards_html = ""
for ep in episodes:
    n = ep["num"]
    t_len = len(ep["doc_title"])
    p_len = li_utf16_len(ep["post_text"])
    margin = 3000 - p_len
    pdf_fn = f"Carosello_LinkedIn_Puntata_{n:02d}.pdf"
    img_fn = f"news_ep_{n:02d}.png"

    cards_html += f"""
        <div class="ep-card" id="regia-ep-{n:02d}" style="background:#141419; border:2px solid #2c2c3a; border-radius:14px; padding:26px; margin-bottom:32px; box-shadow:0 10px 30px rgba(0,0,0,0.5);">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; border-bottom:1px solid #2c2c3a; padding-bottom:14px; margin-bottom:18px;">
                <div>
                    <span style="background:#18112c; color:#f5c518; border:1px solid #f5c518; padding:4px 12px; border-radius:16px; font-size:0.8rem; font-weight:800;">
                        PUNTATA #{n:02d} • Data prevista: {ep['date']} • Carosello a 2 Slide (Zero Spoiler)
                    </span>
                    <h2 style="color:#fff; font-size:1.45rem; margin:8px 0 0 0;">{ep['title']}</h2>
                </div>
                <label style="display:flex; align-items:center; gap:10px; background:#102618; border:2px solid #3cd070; padding:10px 18px; border-radius:10px; cursor:pointer; font-weight:800; color:#3cd070;">
                    <input type="checkbox" id="chk-ep-{n:02d}" onchange="saveDoneState('{n:02d}')" style="width:22px; height:22px; cursor:pointer;">
                    <span>Già Pubblicato su LinkedIn [✓]</span>
                </label>
            </div>

            <div style="display:grid; grid-template-columns: 360px 1fr; gap:24px; align-items:start;">
                <div style="background:#0e0e13; border:1px solid #2c2c3a; border-radius:10px; padding:14px;">
                    <div style="font-size:0.8rem; font-weight:700; color:#f5c518; margin-bottom:8px;">🖼️ Anteprima Slide 1 (1.000 Parole):</div>
                    <img src="assets/{img_fn}" alt="Puntata {n:02d}" style="width:100%; border-radius:8px; border:1px solid #333; margin-bottom:12px;">
                    <div style="font-size:0.8rem; color:#ccc; margin-bottom:10px;">
                        📄 File Carosello PDF (2 Slide senza spoiler):<br>
                        <code style="color:#38bdf8; font-weight:700;">{pdf_fn}</code>
                    </div>
                    <a href="assets/caroselli/{pdf_fn}" download="{pdf_fn}" style="display:block; text-align:center; background:#1e293b; color:#38bdf8; border:1px solid #38bdf8; padding:10px; border-radius:8px; font-weight:800; text-decoration:none; margin-bottom:10px; font-size:0.88rem;">
                        📥 Scarica / Salva {pdf_fn}
                    </a>
                    <a href="https://www.linkedin.com/sharing/compose" target="_blank" style="display:block; text-align:center; background:#0a66c2; color:#fff; padding:12px; border-radius:8px; font-weight:800; text-decoration:none; font-size:0.92rem;">
                        🚀 Apri Finestra Post LinkedIn
                    </a>
                </div>

                <div style="display:grid; gap:16px;">
                    <!-- PASSO 1: DOCUMENT TITLE (MAX 58 CHARS) -->
                    <div style="background:#0e0e13; border:1px solid #333; border-radius:10px; padding:14px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <label style="font-size:0.86rem; font-weight:800; color:#f5c518;">
                                PASSO 1 — Document title* (da incollare sopra al PDF su LinkedIn • Max 58 caratteri):
                            </label>
                            <span id="cnt-title-{n:02d}" style="font-size:0.82rem; font-weight:800; color:#3cd070;">🟢 {t_len}/58 caratteri (OK)</span>
                        </div>
                        <div style="display:flex; gap:10px;">
                            <input type="text" id="inp-title-{n:02d}" value="{ep['doc_title']}" maxlength="58" oninput="updateTitleCount('{n:02d}')" style="flex:1; padding:10px 12px; border-radius:6px; border:1px solid #444; background:#16161f; color:#fff; font-size:0.95rem; font-weight:700;">
                            <button type="button" onclick="copyField('inp-title-{n:02d}', this, 58)" style="background:#f5c518; color:#000; border:none; padding:10px 18px; border-radius:6px; font-weight:800; cursor:pointer; white-space:nowrap;">
                                📋 1. Copia Titolo PDF
                            </button>
                        </div>
                    </div>

                    <!-- PASSO 2 (UNICO TESTO): SHARE YOUR THOUGHTS TUTTO INCLUSO (MAX 3000 CHARS) -->
                    <div id="box-body-{n:02d}" style="background:#0e0e13; border:1px solid #333; border-radius:10px; padding:14px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px;">
                            <div>
                                <label style="font-size:0.86rem; font-weight:800; color:#38bdf8; display:block;">
                                    PASSO 2 — Unico Testo Completo del Post ("Share your thoughts..." • Già comprensivo di Link • Max 3.000):
                                </label>
                                <span id="cnt-body-{n:02d}" style="font-size:0.82rem; font-weight:800; color:#3cd070;">
                                    🟢 {p_len} / 3000 caratteri LinkedIn (Margine sicuro: +{margin})
                                </span>
                            </div>
                            <button type="button" id="btn-body-{n:02d}" onclick="copyField('inp-body-{n:02d}', this, 3000)" style="background:#38bdf8; color:#000; border:none; padding:10px 20px; border-radius:6px; font-weight:800; cursor:pointer; font-size:0.92rem;">
                                📋 2. Copia Testo Post Tutto Incluso (Cmd+V su LinkedIn)
                            </button>
                        </div>
                        <textarea id="inp-body-{n:02d}" rows="16" oninput="updateBodyCount('{n:02d}')" style="width:100%; padding:12px; border-radius:6px; border:1px solid #444; background:#16161f; color:#f1f5f9; font-family:inherit; font-size:0.9rem; line-height:1.55; box-sizing:border-box;">{ep['post_text']}</textarea>
                    </div>
                </div>
            </div>
        </div>
    """

regia_html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cabina di Regia LinkedIn — Connect the DOTS ("Serial Killer App")</title>
    <style>
        body {{
            background-color: #0a0a0d;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 0;
            line-height: 1.5;
        }}
        .top-bar {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(20, 16, 38, 0.96);
            backdrop-filter: blur(8px);
            border-bottom: 2px solid #f5c518;
            padding: 14px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 14px;
        }}
        .ep-jump a {{
            color: #f5c518;
            background: #1e1b2e;
            border: 1px solid #f5c518;
            padding: 5px 10px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.8rem;
            font-weight: 800;
            margin-right: 4px;
        }}
        .ep-jump a:hover {{
            background: #f5c518;
            color: #000;
        }}
    </style>
</head>
<body>
    <div class="top-bar">
        <div>
            <strong style="color:#f5c518; font-size:1.15rem;">🎬 CABINA DI REGIA LINKEDIN (2 SOLI BOTTONI: 1. TITOLO PDF • 2. TESTO POST TUTTO INCLUSO)</strong>
            <span style="display:block; font-size:0.8rem; color:#cbd5e1;">Qualsiasi testo e link è già dentro l'unico riquadro PASSO 2 ed è assoggettato al controllo automatico <= 3.000 caratteri</span>
        </div>
        <div class="ep-jump">
            <span>Vai a:</span>
            {"".join(f'<a href="#regia-ep-{ep["num"]:02d}">#{ep["num"]:02d}</a>' for ep in episodes)}
            <a href="news.html" style="background:#3cd070; color:#000; border-color:#3cd070; margin-left:10px;">🌐 Vedi Pagina Pubblica news.html</a>
        </div>
    </div>

    <main style="max-width: 1220px; margin: 30px auto; padding: 0 20px;">
        {cards_html}
    </main>

    <script>
        function countLinkedInChars(str) {{
            var s = str.replace(/\\r\\n/g, '\\n').replace(/\\n/g, '\\r\\n');
            return s.length;
        }}

        function copyField(inputId, btn, maxLimit) {{
            var el = document.getElementById(inputId);
            var len = (maxLimit === 3000) ? countLinkedInChars(el.value) : el.value.length;
            if (maxLimit && len > maxLimit) {{
                alert('⚠️ ATTENZIONE: Il testo supera il limite massimo di LinkedIn di ' + (len - maxLimit) + ' caratteri (' + len + '/' + maxLimit + '). Accorcialo prima di copiarlo!');
                return;
            }}
            el.select();
            navigator.clipboard.writeText(el.value).then(function() {{
                var origText = btn.innerText;
                var origBg = btn.style.background;
                btn.innerText = '✅ COPIATO (' + len + '/' + maxLimit + ' car.)! Ora premi Cmd+V su LinkedIn';
                btn.style.background = '#3cd070';
                setTimeout(function() {{
                    btn.innerText = origText;
                    btn.style.background = origBg;
                }}, 3500);
            }});
        }}

        function updateTitleCount(epNum) {{
            var inp = document.getElementById('inp-title-' + epNum);
            var cnt = document.getElementById('cnt-title-' + epNum);
            var len = inp.value.length;
            cnt.innerText = (len <= 58 ? '🟢 ' : '🔴 ') + len + '/58 caratteri';
            cnt.style.color = (len <= 58) ? '#3cd070' : '#ef4444';
            localStorage.setItem('ctd_li_v3_title_' + epNum, inp.value);
        }}

        function updateBodyCount(epNum) {{
            var inp = document.getElementById('inp-body-' + epNum);
            var cnt = document.getElementById('cnt-body-' + epNum);
            var box = document.getElementById('box-body-' + epNum);
            var btn = document.getElementById('btn-body-' + epNum);
            var len = countLinkedInChars(inp.value);
            var diff = 3000 - len;

            if (diff >= 0) {{
                cnt.innerText = '🟢 ' + len + ' / 3000 caratteri LinkedIn (Margine sicuro: +' + diff + ')';
                cnt.style.color = (diff > 80) ? '#3cd070' : '#f5c518';
                box.style.borderColor = '#333';
                btn.style.background = '#38bdf8';
            }} else {{
                cnt.innerText = '🔴 ATTENZIONE: SFORAMENTO DI ' + diff + ' CARATTERI (' + len + ' / 3000)! Accorcia il testo.';
                cnt.style.color = '#ef4444';
                box.style.borderColor = '#ef4444';
                btn.style.background = '#ef4444';
            }}
            localStorage.setItem('ctd_li_v3_body_' + epNum, inp.value);
        }}

        function saveDoneState(epNum) {{
            var chk = document.getElementById('chk-ep-' + epNum);
            var card = document.getElementById('regia-ep-' + epNum);
            localStorage.setItem('ctd_li_v3_done_' + epNum, chk.checked ? '1' : '0');
            card.style.borderColor = chk.checked ? '#3cd070' : '#2c2c3a';
        }}

        window.addEventListener('DOMContentLoaded', function() {{
            for (var i = 0; i <= 9; i++) {{
                var k = (i < 10 ? '0' + i : '' + i);
                var savedTitle = localStorage.getItem('ctd_li_v3_title_' + k);
                if (savedTitle !== null && document.getElementById('inp-title-' + k)) {{
                    document.getElementById('inp-title-' + k).value = savedTitle;
                    updateTitleCount(k);
                }}
                var savedBody = localStorage.getItem('ctd_li_v3_body_' + k);
                if (savedBody !== null && document.getElementById('inp-body-' + k)) {{
                    document.getElementById('inp-body-' + k).value = savedBody;
                    updateBodyCount(k);
                }}
                var savedDone = localStorage.getItem('ctd_li_v3_done_' + k);
                if (savedDone === '1' && document.getElementById('chk-ep-' + k)) {{
                    document.getElementById('chk-ep-' + k).checked = true;
                    document.getElementById('regia-ep-' + k).style.borderColor = '#3cd070';
                }}
            }}
        }});
    </script>
</body>
</html>
"""

open(os.path.join(repo, "regia_linkedin.html"), "w", encoding="utf-8").write(regia_html)

# Aggiorna news.html (mostra solo Puntata #00 senza spoiler)
ep0 = episodes[0]
paras0 = "".join(f"<p style='color: #dedee8; font-size: 0.98rem; line-height: 1.65; margin-bottom: 14px;'>{p}</p>" for p in ep0["body_paragraphs"])
news_public_html = open(os.path.join(repo, "news.html"), encoding="utf-8").read() if os.path.exists(os.path.join(repo, "news.html")) else ""
print("OK: Rigenerata regia_linkedin.html senza tasto verde e PDF a 2 slide senza spoiler!")
