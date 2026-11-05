import os, subprocess
from PIL import Image, ImageDraw, ImageFont

repo = "/Users/ingconsani/Development/c-t-d.group"
assets_dir = os.path.join(repo, "assets")
caroselli_web_dir = os.path.join(assets_dir, "caroselli")
out_desktop_dir = "/Users/ingconsani/Desktop/CtD_LinkedIn_Caroselli_PDF"
os.makedirs(caroselli_web_dir, exist_ok=True)
os.makedirs(out_desktop_dir, exist_ok=True)

def li_utf16_len(s):
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

def draw_centered_wrapped(draw, cx, y, max_w, text, font, fill, line_h):
    for ln in wrap_text(text, font, max_w, draw):
        bbox = draw.textbbox((0, 0), ln, font=font)
        w = bbox[2] - bbox[0]
        draw.text((cx - w // 2, y), ln, font=font, fill=fill)
        y += line_h
    return y

# Disegna l'illustrazione vettoriale minimalista al centro del Poster Ancora
def draw_poster_icon(draw, num, cx, cy):
    crimson = (185, 28, 28)
    charcoal = (15, 23, 42)
    gold = (217, 119, 6)
    green = (22, 163, 74)

    # Cerchio di fondo del simbolo
    draw.ellipse([cx - 145, cy - 145, cx + 145, cy + 145], fill=(255, 255, 255), outline=charcoal, width=8)
    draw.ellipse([cx - 128, cy - 128, cx + 128, cy + 128], outline=crimson, width=4)

    if num == 0:
        # Simbolo "NO CLOUD / 100% OFFLINE"
        f = get_font(44, True)
        draw.text((cx - 82, cy - 48), "CLOUD", font=f, fill=charcoal)
        draw.text((cx - 92, cy + 6), "100% OFF", font=get_font(36, True), fill=green)
        draw.line([(cx - 95, cy - 55), (cx + 95, cy - 5)], fill=crimson, width=12)
    elif num == 1:
        # "3 IN 1"
        draw.text((cx - 88, cy - 48), "3 IN 1", font=get_font(64, True), fill=crimson)
        draw.text((cx - 82, cy + 28), "PLATFORM", font=get_font(30, True), fill=charcoal)
    elif num == 2:
        # Punto interrogativo gigante nell'angolo cieco
        draw.text((cx - 38, cy - 82), "?", font=get_font(140, True), fill=crimson)
        draw.text((cx - 95, cy + 58), "ANGOLO CIECO", font=get_font(24, True), fill=charcoal)
    elif num == 3:
        # Simbolo Tasto PAUSA gigante [ || ]
        draw.rounded_rectangle([cx - 65, cy - 65, cx - 20, cy + 45], radius=8, fill=crimson)
        draw.rounded_rectangle([cx + 20, cy - 65, cx + 65, cy + 45], radius=8, fill=crimson)
        draw.text((cx - 85, cy + 62), "TASTO PAUSA", font=get_font(26, True), fill=charcoal)
    elif num == 4:
        # "0 WATT CLOUD"
        draw.text((cx - 90, cy - 52), "0 WATT", font=get_font(52, True), fill=green)
        draw.text((cx - 72, cy + 16), "IN CLOUD", font=get_font(30, True), fill=charcoal)
    elif num == 5:
        # "TO-DO X -> L3"
        draw.text((cx - 85, cy - 52), "TO-DO", font=get_font(50, True), fill=charcoal)
        draw.line([(cx - 90, cy - 25), (cx + 90, cy - 25)], fill=crimson, width=10)
        draw.text((cx - 92, cy + 16), "-> PROGETTO", font=get_font(28, True), fill=green)
    elif num == 6:
        # "21 GIORNI"
        draw.text((cx - 48, cy - 68), "21", font=get_font(86, True), fill=crimson)
        draw.text((cx - 68, cy + 28), "GIORNI VERA", font=get_font(22, True), fill=charcoal)
        draw.text((cx - 52, cy + 54), "PRATICA", font=get_font(24, True), fill=green)
    elif num == 7:
        # "R >>" (Risultati Certificati vs Finti Guru)
        draw.text((cx - 72, cy - 55), "R >>", font=get_font(74, True), fill=crimson)
        draw.text((cx - 88, cy + 32), "PROVEN SME", font=get_font(26, True), fill=charcoal)
    elif num == 8:
        # "1° -> 2° GRADO"
        draw.text((cx - 92, cy - 45), "1° -> 2°", font=get_font(52, True), fill=crimson)
        draw.text((cx - 85, cy + 25), "RISERVATO", font=get_font(28, True), fill=charcoal)
    else:
        # "DOPPIO BINARIO"
        draw.text((cx - 78, cy - 48), "P <-> B", font=get_font(50, True), fill=crimson)
        draw.text((cx - 65, cy + 22), "IN-LIRE", font=get_font(32, True), fill=green)

# Poster Manifesto ad Alto Contrasto (1200x1200) — Stile completamente opposto alle slide tecniche!
def build_editorial_poster(ep):
    num = ep["num"]
    # Sfondo Avorio Editoriale luminosissimo che spacca il feed di LinkedIn
    poster = Image.new("RGB", (1200, 1200), (252, 249, 240))
    dp = ImageDraw.Draw(poster)

    # Cornice esterna Nera + Filetto Rosso Cremisi
    dp.rectangle([24, 24, 1176, 1176], outline=(15, 23, 42), width=10)
    dp.rectangle([40, 40, 1160, 1160], outline=(185, 28, 28), width=3)

    # Top Banner Rosso Cremisi
    dp.rectangle([24, 24, 1176, 130], fill=(185, 28, 28))
    top_txt = f"ANATOMIA DI UNA SERIAL KILLER APP  •  INNESCO #{num:02d}"
    bbox = dp.textbbox((0, 0), top_txt, font=get_font(28, True))
    dp.text((600 - (bbox[2] - bbox[0]) // 2, 62), top_txt, font=get_font(28, True), fill=(255, 255, 255))

    # Illustrazione Simbolica Centrale
    draw_poster_icon(dp, num, 600, 315)

    # DOMANDA / FRASE LAPIDARIA GIGANTE AL CENTRO (Leggibile a 2 metri di distanza)
    y_curr = draw_centered_wrapped(dp, 600, 505, 1020, ep["poster_headline"], get_font(54, True), (15, 23, 42), 66)

    # Linea divisoria rossa
    dp.line([(250, y_curr + 22), (950, y_curr + 22)], fill=(185, 28, 28), width=5)

    # Sottotitolo secco in Rosso/Verde
    draw_centered_wrapped(dp, 600, y_curr + 45, 1000, ep["poster_sub"], get_font(34, True), (185, 28, 28), 44)

    # Bottom Banner Nero Carbone con invito all'azione immediato
    dp.rectangle([24, 1035, 1176, 1176], fill=(15, 23, 42))
    b_txt1 = "DOMANI ORE 08:15 LO STUDIO TECNICO QUI SU LINKEDIN"
    b_txt2 = "Vuoi vederlo subito (+ 1 Anno Gratis)?  ->  www.c-t-d.group/news.html"
    bb1 = dp.textbbox((0, 0), b_txt1, font=get_font(26, True))
    bb2 = dp.textbbox((0, 0), b_txt2, font=get_font(26, True))
    dp.text((600 - (bb1[2] - bb1[0]) // 2, 1060), b_txt1, font=get_font(26, True), fill=(245, 197, 24))
    dp.text((600 - (bb2[2] - bb2[0]) // 2, 1108), b_txt2, font=get_font(26, True), fill=(255, 255, 255))

    return poster

episodes_data = [
    {
        "num": 0,
        "title": "IL TRAILER: Come raccontare la prima 'App-non-App'?",
        "ancora_doc_title": "Connect the DOTS #00-A: La Prima App-non-App (Offline)",
        "doc_title": "Connect the DOTS #00: Anatomia di una Serial Killer App",
        "poster_headline": "NON E' UN'APP. E' LA PRIMA 'APP-NON-APP' (CON AI 100% OFFLINE).",
        "poster_sub": "24 Funzioni Brevettate • Zero Cloud • Per Persone (P) e Aziende (B).",
        "ancora_text": """24 funzioni brevettate.
Intelligenza Artificiale estesa, ma 100% offline.
Zero cloud. Zero canoni server.

Non è un'app. È la prima "App-non-App" (per Persone e Aziende).
Spiegarla in un post normale era impossibile: per questo parte "Anatomia di una Serial Killer App".

Domani mattina alle 08:15 esce il Trailer completo qui su LinkedIn.
Chi vuole vederlo subito in anteprima (e bloccare 1 Anno+ gratis da Gennaio 2027) lo trova già aperto qui:
👉 https://www.c-t-d.group/news.html#news-ep-00

#ConnectTheDOTS #SerialKillerApp #AppNonApp""",
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
        "title": "Il Manifesto: 3 Systems in 1 Platform (S = C + P + T + R)",
        "ancora_doc_title": "Connect the DOTS #01-A: Tre App Che Non Si Parlano",
        "doc_title": "Connect the DOTS #01: 3 Systems in 1 Platform (Offline)",
        "poster_headline": "QUANTE APP USI OGNI GIORNO CHE NON SI PARLANO TRA LORO?",
        "poster_sub": "Diagnosi + Esecuzione + Relazioni = 3 Sistemi in 1 Piattaforma Offline.",
        "ancora_text": """Un'app per le idee.
Un'app per i To-Do che rimandi.
Un social per cercare clienti a freddo.

Tre strumenti che non si parlano e bruciano il 70% del tuo tempo.
E se Diagnosi, Esecuzione e Relazioni fossero 3 Sistemi in 1 sola Piattaforma 100% offline?

Domani alle 08:15 pubblico la radiografia tecnica qui su LinkedIn.
Se vuoi studiarla subito in anteprima (e bloccare 1 Anno+ gratis da Gennaio 2027):
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #Produttivita""",
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
        "title": "Cervello, Orizzonti e Triage Diagnostico Causale",
        "ancora_doc_title": "Connect the DOTS #02-A: Cio' Che Non Sai Di Non Sapere",
        "doc_title": "Connect the DOTS #02: Dal Non So Cosa Non So al DOT L3",
        "poster_headline": "CHATGPT TI RISPONDE SOLO SE SAI GIA' QUALE DOMANDA FARE.",
        "poster_sub": "Ma chi ti salva da cio' che 'Non sai di non sapere'?",
        "ancora_text": """ChatGPT ti risponde solo se sai già quale domanda fare.
Ma i disastri più gravi — nella vita e in azienda — nascono da ciò che "non sai di non sapere".

Come si individua un problema che non sai nemmeno di avere?

Domani alle 08:15 svelo qui su LinkedIn il motore di Triage Causale di Connect the DOTS.
Chi vuole studiarlo in anteprima (e assicurarsi 1 Anno+ gratis da Gennaio 2027) lo trova qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #DecisionMaking""",
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
        "title": "SWOT in RAM (Ignoto = 10/10) e il Tasto Sovrano 'Pausa'",
        "ancora_doc_title": "Connect the DOTS #03-A: Il Cruscotto col Tasto Pausa",
        "doc_title": "Connect the DOTS #03: SWOT in RAM (10/10) e Tasto Pausa",
        "poster_headline": "IN AZIENDA CIO' CHE IGNORI NON VALE ZERO: VALE RISCHIO 10/10.",
        "poster_sub": "Hai mai visto una SWOT in RAM con il tasto sovrano 'Pausa'?",
        "ancora_text": """In azienda ciò che ignori non vale zero.
Vale Rischio Massimo (10/10).

Ma se provi a tenere sotto controllo tutto, impazzisci.
A meno che il tuo cruscotto non abbia il tasto sovrano "Pausa".

Domani alle 08:15 mostro qui su LinkedIn come funziona la SWOT predittiva in RAM.
Anteprima immediata (con 1 Anno+ di licenza gratuita da Gennaio 2027) già aperta qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #Imprenditori""",
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
        "title": "L'Esperanto dei ~1.000 DOT e la Micro-Blockchain Offline",
        "ancora_doc_title": "Connect the DOTS #04-A: Zero Gigawatt Bruciati in Cloud",
        "doc_title": "Connect the DOTS #04: L'Esperanto dei 1.000 DOT Offline",
        "poster_headline": "PERCHE' BRUCIARE GIGAWATT IN CLOUD PER RISPOSTE GIA' NOTE?",
        "poster_sub": "L'Esperanto dei 1.000 DOT gira al 100% Offline sul tuo dispositivo.",
        "ancora_text": """Perché bruciare gigawatt su server cloud remoti (esponendo i tuoi segreti industriali) per rigenerare risposte che gli esperti conoscono già?

La vera rivoluzione AI non è nel Cloud. È 100% offline sul tuo dispositivo.

Domani alle 08:15 i dettagli tecnici qui su LinkedIn.
Anteprima (e prenotazione di 1 Anno+ gratis da Gennaio 2027) disponibile qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #EdgeAI #GDPR""",
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
        "title": "2° Cervello: Proliferazione To-Do -> L3 Progetto & Sinapsi",
        "ancora_doc_title": "Connect the DOTS #05-A: Il Cimitero delle Liste To-Do",
        "doc_title": "Connect the DOTS #05: 2° Cervello, To-Do e Cantieri L3",
        "poster_headline": "LE LISTE DI 'TO-DO' SONO IL CIMITERO DEI BUONI PROPOSITI.",
        "poster_sub": "Trasforma ogni appunto in un cantiere L3 collegato alla strategia.",
        "ancora_text": """Le liste di "To-Do" sono il cimitero dei buoni propositi.
Segni un compito oggi, e tra tre giorni hai già perso il legame con la tua strategia.

Domani alle 08:15 mostro qui su LinkedIn come il Secondo Cervello trasforma ogni appunto in un cantiere collegato ai tuoi obiettivi.
Anteprima (e 1 Anno+ gratis da Gennaio 2027) qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #Execution""",
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
        "title": "Allocazione a 3 Vie, Palestra di 21 Giorni e Certificato PoR",
        "ancora_doc_title": "Connect the DOTS #06-A: 21 Giorni di Pratica Certificata",
        "doc_title": "Connect the DOTS #06: Palestra 21 Giorni e PoR Multi-Sig",
        "poster_headline": "LA TEORIA SENZA 21 GIORNI DI PRATICA LASCIA TUTTO COM'ERA.",
        "poster_sub": "Basta attestati di presenza: benvenuto Proof-of-Result (PoR).",
        "ancora_text": """La formazione teorica senza 21 giorni di pratica lascia tutto esattamente com'era il venerdì prima.

Ecco perché in Connect the DOTS non contano gli attestati di presenza, ma i certificati crittografici di risultato (Proof-of-Result).

Domani alle 08:15 la scheda tecnica qui su LinkedIn.
Studiala in anteprima (e blocca 1 Anno+ gratis da Gennaio 2027) qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #Meritocrazia""",
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
        "title": "Cordone Ombelicale 21gg e Qualifica Proven SME (R>>) NEXUS",
        "ancora_doc_title": "Connect the DOTS #07-A: La Fine dei Finti Guru Social",
        "doc_title": "Connect the DOTS #07: Cordone Ombelicale e Proven SME",
        "poster_headline": "SUI SOCIAL VINCE CHI URLA. SUL MERCATO CHI PORTA RISULTATI.",
        "poster_sub": "Cordone Ombelicale di 21gg + Qualifica Proven SME (R >>).",
        "ancora_text": """Sui social vince chi urla più forte.
Nel mercato reale dovrebbe vincere chi porta risultati certificati ai propri clienti.

Domani alle 08:15 svelo qui su LinkedIn come funziona il "Cordone Ombelicale" di 21 giorni e la qualifica a Proven SME.
Anteprima (e 1 Anno+ gratis da Gennaio 2027) qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #Consulenza""",
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
        "title": "Network Engineering: Score Ponte e 'Salto del 1° Grado'",
        "ancora_doc_title": "Connect the DOTS #08-A: Il Salto del 1° Grado Riservato",
        "doc_title": "Connect the DOTS #08: Score Ponte e Salto del 1° Grado",
        "poster_headline": "COME CHIEDI AIUTO SENZA ESPORRE LE TUE DEBOLEZZE AGLI AMICI?",
        "poster_sub": "Raggiungi il risolutore al 2° grado col 'Salto del 1° Grado'.",
        "ancora_text": """Quando hai un problema serio in azienda (10/10), non vuoi confessarlo agli amici o ai contatti diretti.
Eppure chi può risolverlo è quasi sempre tra i contatti dei tuoi contatti (al 2° grado).

Come ci arrivi senza esporti? Col "Salto del 1° Grado".
Domani alle 08:15 lo schema qui su LinkedIn. Anteprima (e 1 Anno+ gratis) qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #Networking""",
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
        "title": "Compensazione in-Lire Fluida (HTLC) a Doppio Binario",
        "ancora_doc_title": "Connect the DOTS #09-A: Scambio HTLC a Doppio Binario",
        "doc_title": "Connect the DOTS #09: Scambio Fluido in-Lire HTLC B2B",
        "poster_headline": "I CIRCUITI DI SCAMBIO USATI COME CATALOGHI SI BLOCCANO.",
        "poster_sub": "Lo scambio decolla quando parte dai tuoi cantieri reali (P & B).",
        "ancora_text": """I circuiti di scambio usati come semplici cataloghi passivi si bloccano.
Lo scambio decolla solo quando nasce dai cantieri reali che devi realizzare domani mattina.

Domani alle 08:15 svelo il motore di compensazione fluida a Doppio Binario (Persone + Imprese).
Anteprima (e 1 Anno+ gratis da Gennaio 2027) qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #B2B #InLire""",
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

for ep in episodes_data:
    n = ep["num"]
    poster = build_editorial_poster(ep)
    png_name = f"Ancora_LinkedIn_Puntata_{n:02d}.png"
    pdf_name = f"Ancora_LinkedIn_Puntata_{n:02d}.pdf"
    poster.save(os.path.join(assets_dir, png_name))
    poster.save(os.path.join(out_desktop_dir, png_name))
    poster.save(os.path.join(out_desktop_dir, pdf_name), "PDF", resolution=150.0)
    poster.save(os.path.join(caroselli_web_dir, pdf_name), "PDF", resolution=150.0)

print("OK: Generati i 10 Poster Editoriali ad alto contrasto (Avorio/Cremisi/Nero) per lo Stream 1 (Ancora)!")

# ==============================================================================
# COSTRUZIONE DI regia_linkedin.html CON BOTTONI IDENTICI AL 100% NEI DUE STREAM
# ==============================================================================
cards_html = ""
for ep in episodes_data:
    n = ep["num"]
    ta_len = len(ep["ancora_doc_title"])
    pa_len = li_utf16_len(ep["ancora_text"])
    tb_len = len(ep["doc_title"])
    pb_len = li_utf16_len(ep["post_text"])

    cards_html += f"""
        <div class="ep-card" id="regia-ep-{n:02d}" style="background:#141419; border:2px solid #2c2c3a; border-radius:16px; padding:26px; margin-bottom:38px; box-shadow:0 12px 35px rgba(0,0,0,0.6);">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; border-bottom:2px solid #2c2c3a; padding-bottom:14px; margin-bottom:22px;">
                <div>
                    <span style="background:#18112c; color:#f5c518; border:1px solid #f5c518; padding:5px 14px; border-radius:16px; font-size:0.82rem; font-weight:800;">
                        PUNTATA #{n:02d} • Stessi Bottoni Identici per Stream 1 (Ancora Lapidaria) e Stream 2 (Studio Master)
                    </span>
                    <h2 style="color:#fff; font-size:1.5rem; margin:8px 0 0 0;">Puntata #{n:02d} — {ep['title']}</h2>
                </div>
                <div style="display:flex; gap:12px; flex-wrap:wrap;">
                    <label style="display:flex; align-items:center; gap:8px; background:#2a1215; border:2px solid #ef4444; padding:8px 14px; border-radius:10px; cursor:pointer; font-weight:800; color:#fca5a5; font-size:0.85rem;">
                        <input type="checkbox" id="chk-a-{n:02d}" onchange="saveDoneState('{n:02d}')" style="width:18px; height:18px;">
                        <span>Stream 1 (Ancora) Pubblicato [✓]</span>
                    </label>
                    <label style="display:flex; align-items:center; gap:8px; background:#102618; border:2px solid #3cd070; padding:8px 14px; border-radius:10px; cursor:pointer; font-weight:800; color:#3cd070; font-size:0.85rem;">
                        <input type="checkbox" id="chk-b-{n:02d}" onchange="saveDoneState('{n:02d}')" style="width:18px; height:18px;">
                        <span>Stream 2 (Master) Pubblicato [✓]</span>
                    </label>
                </div>
            </div>

            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:24px; align-items:start;">
                <!-- STREAM 1 (SINISTRA): POST-ANCORA LAPIDARIO (PER ATTIRARE TUTTI 10/10) -->
                <div style="background:#0e0e14; border:2px solid #ef4444; border-radius:12px; padding:18px;">
                    <div style="background:#450a0a; color:#fecaca; padding:8px 12px; border-radius:8px; font-weight:800; font-size:0.9rem; margin-bottom:14px;">
                        🎯 STREAM 1 (Giorno 1, ore 08:15) — POST-ANCORA LAPIDARIO (~450 car. • Attira tutti)
                    </div>
                    <div style="display:grid; grid-template-columns: 170px 1fr; gap:14px; margin-bottom:14px; align-items:center;">
                        <img src="assets/Ancora_LinkedIn_Puntata_{n:02d}.png" alt="Poster Ancora {n:02d}" style="width:100%; border-radius:8px; border:2px solid #ef4444;">
                        <div style="font-size:0.82rem; color:#cbd5e1;">
                            <strong>📄 File PDF da allegare su LinkedIn:</strong><br>
                            <code style="color:#f5c518; font-weight:700;">Ancora_LinkedIn_Puntata_{n:02d}.pdf</code><br>
                            <div style="margin-top:10px; display:grid; gap:8px;">
                                <a href="assets/caroselli/Ancora_LinkedIn_Puntata_{n:02d}.pdf" download="Ancora_LinkedIn_Puntata_{n:02d}.pdf" style="display:block; text-align:center; background:#1e293b; color:#38bdf8; border:1px solid #38bdf8; padding:8px; border-radius:6px; text-decoration:none; font-weight:800;">
                                    📥 Scarica / Salva Ancora_LinkedIn_Puntata_{n:02d}.pdf
                                </a>
                                <a href="https://www.linkedin.com/sharing/compose" target="_blank" style="display:block; text-align:center; background:#0a66c2; color:#fff; padding:8px; border-radius:6px; text-decoration:none; font-weight:800;">
                                    🚀 Apri Finestra Post LinkedIn
                                </a>
                            </div>
                        </div>
                    </div>

                    <!-- PASSO 1 IDENTICO -->
                    <div style="background:#14141c; border:1px solid #333; border-radius:8px; padding:12px; margin-bottom:12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.8rem; font-weight:800; color:#f5c518; margin-bottom:6px;">
                            <span>PASSO 1 — Document title* (Max 58 caratteri):</span>
                            <span id="cnt-ta-{n:02d}" style="color:#3cd070;">🟢 {ta_len}/58 caratteri (OK)</span>
                        </div>
                        <div style="display:flex; gap:8px;">
                            <input type="text" id="inp-ta-{n:02d}" value="{ep['ancora_doc_title']}" maxlength="58" oninput="updateCount('inp-ta-{n:02d}','cnt-ta-{n:02d}',58,'ctd_v5_ta_{n:02d}')" style="flex:1; padding:9px; border-radius:6px; border:1px solid #444; background:#0c0c10; color:#fff; font-weight:700; font-size:0.88rem;">
                            <button type="button" onclick="copyField('inp-ta-{n:02d}', this, 58)" style="background:#f5c518; color:#000; border:none; padding:9px 14px; border-radius:6px; font-weight:800; cursor:pointer; white-space:nowrap;">
                                📋 1. Copia Titolo PDF
                            </button>
                        </div>
                    </div>

                    <!-- PASSO 2 IDENTICO -->
                    <div style="background:#14141c; border:1px solid #333; border-radius:8px; padding:12px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; margin-bottom:8px;">
                            <div>
                                <span style="font-size:0.8rem; font-weight:800; color:#38bdf8; display:block;">PASSO 2 — Testo Post ("Share your thoughts..."):</span>
                                <span id="cnt-ba-{n:02d}" style="font-size:0.78rem; font-weight:800; color:#3cd070;">🟢 {pa_len} / 3000 car. (Testo Lapidario • Margine: +{3000 - pa_len})</span>
                            </div>
                            <button type="button" onclick="copyField('inp-ba-{n:02d}', this, 3000)" style="background:#38bdf8; color:#000; border:none; padding:9px 14px; border-radius:6px; font-weight:800; cursor:pointer;">
                                📋 2. Copia Testo Post (Cmd+V su LinkedIn)
                            </button>
                        </div>
                        <textarea id="inp-ba-{n:02d}" rows="13" oninput="updateCount('inp-ba-{n:02d}','cnt-ba-{n:02d}',3000,'ctd_v5_ba_{n:02d}')" style="width:100%; padding:10px; border-radius:6px; border:1px solid #444; background:#0c0c10; color:#f1f5f9; font-family:inherit; font-size:0.9rem; line-height:1.5; box-sizing:border-box;">{ep['ancora_text']}</textarea>
                    </div>
                </div>

                <!-- STREAM 2 (DESTRA): POST MASTER COMPLETO (STUDIO TECNICO 2 SLIDE) -->
                <div style="background:#0e0e14; border:2px solid #38bdf8; border-radius:12px; padding:18px;">
                    <div style="background:#0f2438; color:#bae6fd; padding:8px 12px; border-radius:8px; font-weight:800; font-size:0.9rem; margin-bottom:14px;">
                        📘 STREAM 2 (Giorno 2, ore 08:15) — POST MASTER DI STUDIO (~2.800 car. • 2 Slide)
                    </div>
                    <div style="display:grid; grid-template-columns: 170px 1fr; gap:14px; margin-bottom:14px; align-items:center;">
                        <img src="assets/news_ep_{n:02d}.png" alt="Master {n:02d}" style="width:100%; border-radius:8px; border:2px solid #38bdf8;">
                        <div style="font-size:0.82rem; color:#cbd5e1;">
                            <strong>📄 File PDF da allegare su LinkedIn:</strong><br>
                            <code style="color:#38bdf8; font-weight:700;">Carosello_LinkedIn_Puntata_{n:02d}.pdf</code><br>
                            <div style="margin-top:10px; display:grid; gap:8px;">
                                <a href="assets/caroselli/Carosello_LinkedIn_Puntata_{n:02d}.pdf" download="Carosello_LinkedIn_Puntata_{n:02d}.pdf" style="display:block; text-align:center; background:#1e293b; color:#38bdf8; border:1px solid #38bdf8; padding:8px; border-radius:6px; text-decoration:none; font-weight:800;">
                                    📥 Scarica / Salva Carosello_LinkedIn_Puntata_{n:02d}.pdf
                                </a>
                                <a href="https://www.linkedin.com/sharing/compose" target="_blank" style="display:block; text-align:center; background:#0a66c2; color:#fff; padding:8px; border-radius:6px; text-decoration:none; font-weight:800;">
                                    🚀 Apri Finestra Post LinkedIn
                                </a>
                            </div>
                        </div>
                    </div>

                    <!-- PASSO 1 IDENTICO -->
                    <div style="background:#14141c; border:1px solid #333; border-radius:8px; padding:12px; margin-bottom:12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.8rem; font-weight:800; color:#f5c518; margin-bottom:6px;">
                            <span>PASSO 1 — Document title* (Max 58 caratteri):</span>
                            <span id="cnt-tb-{n:02d}" style="color:#3cd070;">🟢 {tb_len}/58 caratteri (OK)</span>
                        </div>
                        <div style="display:flex; gap:8px;">
                            <input type="text" id="inp-tb-{n:02d}" value="{ep['doc_title']}" maxlength="58" oninput="updateCount('inp-tb-{n:02d}','cnt-tb-{n:02d}',58,'ctd_v5_tb_{n:02d}')" style="flex:1; padding:9px; border-radius:6px; border:1px solid #444; background:#0c0c10; color:#fff; font-weight:700; font-size:0.88rem;">
                            <button type="button" onclick="copyField('inp-tb-{n:02d}', this, 58)" style="background:#f5c518; color:#000; border:none; padding:9px 14px; border-radius:6px; font-weight:800; cursor:pointer; white-space:nowrap;">
                                📋 1. Copia Titolo PDF
                            </button>
                        </div>
                    </div>

                    <!-- PASSO 2 IDENTICO -->
                    <div style="background:#14141c; border:1px solid #333; border-radius:8px; padding:12px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; margin-bottom:8px;">
                            <div>
                                <span style="font-size:0.8rem; font-weight:800; color:#38bdf8; display:block;">PASSO 2 — Testo Post ("Share your thoughts..."):</span>
                                <span id="cnt-bb-{n:02d}" style="font-size:0.78rem; font-weight:800; color:#3cd070;">🟢 {pb_len} / 3000 car. (Testo Master • Margine: +{3000 - pb_len})</span>
                            </div>
                            <button type="button" onclick="copyField('inp-bb-{n:02d}', this, 3000)" style="background:#38bdf8; color:#000; border:none; padding:9px 14px; border-radius:6px; font-weight:800; cursor:pointer;">
                                📋 2. Copia Testo Post (Cmd+V su LinkedIn)
                            </button>
                        </div>
                        <textarea id="inp-bb-{n:02d}" rows="13" oninput="updateCount('inp-bb-{n:02d}','cnt-bb-{n:02d}',3000,'ctd_v5_bb_{n:02d}')" style="width:100%; padding:10px; border-radius:6px; border:1px solid #444; background:#0c0c10; color:#f1f5f9; font-family:inherit; font-size:0.9rem; line-height:1.5; box-sizing:border-box;">{ep['post_text']}</textarea>
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
    <title>Cabina di Regia LinkedIn — Stream 1 (Ancora Lapidaria) & Stream 2 (Studio Master)</title>
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
            <strong style="color:#f5c518; font-size:1.12rem;">🎬 CABINA DI REGIA LINKEDIN — BOTTONI UNIFORMATI (STREAM 1: POSTER LAPIDARIO • STREAM 2: CAROSELLO MASTER)</strong>
            <span style="display:block; font-size:0.8rem; color:#cbd5e1;">In entrambi gli stream usi sempre gli stessi 2 tasti: 📋 1. Copia Titolo PDF • 📋 2. Copia Testo Post (Cmd+V su LinkedIn)</span>
        </div>
        <div class="ep-jump">
            <span>Puntata:</span>
            {"".join(f'<a href="#regia-ep-{ep["num"]:02d}">#{ep["num"]:02d}</a>' for ep in episodes_data)}
            <a href="news.html" style="background:#3cd070; color:#000; border-color:#3cd070; margin-left:10px;">🌐 Pagina Pubblica news.html</a>
        </div>
    </div>

    <main style="max-width: 1380px; margin: 28px auto; padding: 0 20px;">
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
                btn.innerText = '✅ COPIATO (' + len + '/' + maxLimit + ')! Premi Cmd+V su LinkedIn';
                btn.style.background = '#3cd070';
                setTimeout(function() {{
                    btn.innerText = origText;
                    btn.style.background = origBg;
                }}, 3500);
            }});
        }}

        function updateCount(inpId, cntId, maxLimit, storageKey) {{
            var inp = document.getElementById(inpId);
            var cnt = document.getElementById(cntId);
            var len = (maxLimit === 3000) ? countLinkedInChars(inp.value) : inp.value.length;
            var diff = maxLimit - len;
            if (diff >= 0) {{
                cnt.innerText = '🟢 ' + len + ' / ' + maxLimit + (maxLimit === 3000 ? ' car. (Margine: +' + diff + ')' : ' caratteri (OK)');
                cnt.style.color = '#3cd070';
            }} else {{
                cnt.innerText = '🔴 SFORAMENTO DI ' + diff + ' (' + len + '/' + maxLimit + ')';
                cnt.style.color = '#ef4444';
            }}
            localStorage.setItem(storageKey, inp.value);
        }}

        function saveDoneState(epNum) {{
            var ca = document.getElementById('chk-a-' + epNum).checked;
            var cb = document.getElementById('chk-b-' + epNum).checked;
            localStorage.setItem('ctd_v5_done_a_' + epNum, ca ? '1' : '0');
            localStorage.setItem('ctd_v5_done_b_' + epNum, cb ? '1' : '0');
            var card = document.getElementById('regia-ep-' + epNum);
            card.style.borderColor = (ca && cb) ? '#3cd070' : (ca ? '#f5c518' : '#2c2c3a');
        }}

        window.addEventListener('DOMContentLoaded', function() {{
            for (var i = 0; i <= 9; i++) {{
                var k = (i < 10 ? '0' + i : '' + i);
                ['ta', 'ba', 'tb', 'bb'].forEach(function( prefix ) {{
                    var sk = 'ctd_v5_' + prefix + '_' + k;
                    var val = localStorage.getItem(sk);
                    var inpId = 'inp-' + prefix + '-' + k;
                    var cntId = 'cnt-' + prefix + '-' + k;
                    var lim = (prefix === 'ta' || prefix === 'tb') ? 58 : 3000;
                    if (val !== null && document.getElementById(inpId)) {{
                        document.getElementById(inpId).value = val;
                        updateCount(inpId, cntId, lim, sk);
                    }}
                }});
                var da = localStorage.getItem('ctd_v5_done_a_' + k) === '1';
                var db = localStorage.getItem('ctd_v5_done_b_' + k) === '1';
                if (document.getElementById('chk-a-' + k)) document.getElementById('chk-a-' + k).checked = da;
                if (document.getElementById('chk-b-' + k)) document.getElementById('chk-b-' + k).checked = db;
                saveDoneState(k);
            }}
        }});
    </script>
</body>
</html>
"""

open(os.path.join(repo, "regia_linkedin.html"), "w", encoding="utf-8").write(regia_html)
print("OK: regia_linkedin.html aggiornata con bottoni identici e Poster Lapidari!")
