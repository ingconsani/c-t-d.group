import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

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
        "date_a": "Venerdi' 6 Nov 2026 (08:15)",
        "date_b": "Sabato 7 / Lunedi' 9 Nov (08:15)",
        "doc_title": "Connect the DOTS #00: Anatomia di una Serial Killer App",
        "ancora_doc_title": "Connect the DOTS #00-A: Hai 3 Minuti di Concentrazione?",
        "title": "IL TRAILER: Come raccontare la prima 'App-non-App'?",
        "subtitle": "Uso esteso dell'AI ma 100% Offline • 24 Funzioni in 3 Sistemi • Utenti P & B • Nativamente GDPR & EU AI Act Compliant",
        "crop": (0, 0, 1920, 1080),
        "pts": list(range(1, 25)),
        "ancora_b1": "8 LETTORI SU 10 SU LINKEDIN SCORRONO TROPPO IN FRETTA PER LEGGERE 24 FUNZIONI BREVETTATE.",
        "ancora_b2": "MA SE FAI PARTE DI QUEI 2 SU 10: ECCO LA PRIMA 'APP-NON-APP' CON AI 100% OFFLINE (PER UTENTI 'P' E 'B').",
        "ancora_b3": "STUDIA L'ANTEPRIMA SU WWW.C-T-D.GROUP/NEWS.HTML E BLOCCA 1 ANNO+ GRATIS DA GENNAIO 2027!",
        "ancora_text": """Si può presentare in un solo post la prima "App-non-App" che non è mai esistita prima?

Quando abbiamo provato a spiegare Connect the DOTS (in uscita a Gennaio 2027) con i formati tradizionali, ci siamo accorti che 8 lettori su 10 su LinkedIn scorrono troppo in fretta per fermarsi su 24 funzioni brevettate.

Ma se fai parte di quei 2 su 10 che cercano soluzioni strutturali, ecco le 3 domande a cui rispondiamo da oggi con la serie "Anatomia di una Serial Killer App":
👤 Persona (P): come usare l'AI per governare il tuo futuro restando al 100% OFFLINE sul tuo device (zero cloud)?
🎓 Professionista (SME): come farti scegliere dai clienti in modalità Pull grazie ai tuoi risultati certificati (R >>)?
🏢 Imprenditore/PMI (B): come vedere in tempo reale i rischi 10/10 della tua azienda (GDPR e AI Act compliant) a costo server zero?

Nella prossima uscita pubblicherò qui su LinkedIn il Carosello PDF completo del Trailer (#00).
Se però vuoi studiarlo subito in anteprima (e assicurarti 1 Anno+ di licenza gratuita da Gennaio 2027 lasciando un feedback + la tua email per la newsletter), la Puntata #00 è già aperta qui:
👉 https://www.c-t-d.group/news.html#news-ep-00

Quale "falsa promessa" del digitale o della consulenza vorresti veder eliminata per prima? 👇

#ConnectTheDOTS #SerialKillerApp #AppNonApp #EdgeAI #Gennaio2027""",
        "victim": "L'impossibilita' di spiegare una piattaforma rivoluzionaria di 24 componenti con un singolo post tradizionale.",
        "killer_feature": "Una serie aperta ('Anatomia di una Serial Killer App'): ogni puntata isola 1 funzione con 1 Slide da 1.000 parole, Timeline progressiva, Triplo Payoff (P / Prof / B) e 1 Anno+ Gratis da Gennaio 2027.",
        "payoff_persona": "Scopri passo dopo passo come usare un Coach privato e un Secondo Cervello offline senza cedere i tuoi dati al cloud.",
        "payoff_prof": "Scopri come fidelizzare i tuoi clienti per 21 giorni e farti scegliere in modalita' Pull grazie ai tuoi risultati certificati (R >>).",
        "payoff_pmi": "Scopri come unificare SWOT in RAM, cantieri operativi L3 e intersezioni di rete B2B a costo server zero.",
        "next_teaser": "Prossima Puntata (#01): Sveleremo il Manifesto dei '3 Systems in 1 Platform' e l'equazione S = C + P + T + R.",
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
        "date_a": "Fase A (Ex-Ante 08:15)",
        "date_b": "Fase B (Studio 08:15)",
        "doc_title": "Connect the DOTS #01: 3 Systems in 1 Platform (Offline)",
        "ancora_doc_title": "Connect the DOTS #01-A: Quante App Usi Che Non Si Parlano?",
        "title": "Il Manifesto: 3 Systems in 1 Platform (S = C + P + T + R)",
        "subtitle": "Come funzionano i 3 motori integrati nel tuo Profilo aggiornato 100% offline (Lancio Gennaio 2027)",
        "crop": (0, 0, 1920, 1080),
        "pts": list(range(1, 25)),
        "ancora_b1": "USI UN'APP PER LE IDEE, UN'ALTRA PER I TO-DO E UN SOCIAL PER CERCARE CLIENTI O FORNITORI A FREDDO.",
        "ancora_b2": "E SE DIAGNOSI + ESECUZIONE (21GG) + RELAZIONI PULL FOSSERO 3 SISTEMI IN 1 SOLA PIATTAFORMA OFFLINE?",
        "ancora_b3": "SCOPRI L'EQUAZIONE S = C + P + T + R E BLOCCA 1 ANNO+ GRATIS SU WWW.C-T-D.GROUP/NEWS.HTML",
        "ancora_text": """Fai un test rapido sulla tua giornata lavorativa:
Usi un chatbot per cercare risposte, un'altra app per le liste di To-Do che puntualmente rimandi, e un social per cercare clienti o fornitori a freddo.
Tre mondi separati che non si parlano e disperdono il 70% delle tue energie.

Nella Puntata #01 di "Anatomia di una Serial Killer App" sveliamo come a Gennaio 2027 unificheremo questi 3 mondi in 1 sola Piattaforma 100% offline (S = C + P + T + R):
👤 Persona (P): un Coach privato offline che lavora solo per te.
🎓 Professionista (SME): fine delle chiamate a freddo, vieni scelto in Pull per i tuoi risultati (R >>).
🏢 Imprenditore/PMI (B): diagnosi, cantieri L3 e ricerca partner a costo server zero.

Domani pubblicherò qui su LinkedIn il Carosello PDF tecnico della Puntata #01.
Ma se fai parte di quei 2 su 10 che vogliono studiarlo subito in anteprima (e bloccare 1 Anno+ gratis per Gennaio 2027 lasciando un feedback), lo trovi qui:
👉 https://www.c-t-d.group/news.html

Quale dei 3 blocchi ti fa perdere più tempo oggi: capire le priorità, eseguire i progetti o trovare le persone giuste? 👇

#ConnectTheDOTS #SerialKillerApp #3SystemsInOnePlatform #PMI #Professionisti""",
        "victim": "I software isolati in Cloud che standardizzano le persone, divorano energia ed espongono i tuoi segreti industriali.",
        "killer_feature": "3 Sistemi integrati in 1 sola Piattaforma 100% offline dentro il tuo Profilo aggiornato: 1° CtD Base (Diagnosi S=C+P+T+R) + 2° CtD 2°B (Secondo Cervello 21gg) + 3° CtD NE (Network Engineering Pull).",
        "payoff_persona": "Diventi padrone del tuo futuro con un Coach 100% privato sul tuo device che non vende mai i tuoi dati.",
        "payoff_prof": "Smetti di rincorrere clienti a freddo (Push) e vieni attivato in Pull grazie ai tuoi risultati certificati (R >>).",
        "payoff_pmi": "Unifichi diagnosi strategica, cantieri operativi L3 e ricerca riservata di partner a costo server zero.",
        "next_teaser": "Prossima Puntata (#02): Come si uccide l'angolo cieco del 'Non so cosa non so'? Cosa accade premendo il pulsante del Cervello.",
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
        "date_a": "Fase A (Ex-Ante 08:15)",
        "date_b": "Fase B (Studio 08:15)",
        "doc_title": "Connect the DOTS #02: Dal Non So Cosa Non So al DOT L3",
        "ancora_doc_title": "Connect the DOTS #02-A: Il Limite Cieco dei Chatbot",
        "title": "Cervello, Orizzonti e Triage Diagnostico Causale",
        "subtitle": "Dal 'Non so cosa non so' all'individuazione matematica del Next Best Dot (NBD)",
        "crop": (15, 140, 670, 680),
        "pts": [1, 3, 4, 5, 8],
        "ancora_b1": "CHATGPT TI RISPONDE SOLO SE SAI GIA' QUALE DOMANDA FARE.",
        "ancora_b2": "MA CHI TI SALVA DA CIO' CHE 'NON SAI DI NON SAPERE' (DOT L2 PROBLEMA -> DOT L3 SOLUZIONE)?",
        "ancora_b3": "SCOPRI IL TRIAGE DIAGNOSTICO CAUSALE E PRENOTA 1 ANNO+ GRATIS SU WWW.C-T-D.GROUP/NEWS.HTML",
        "ancora_text": """Il limite più pericoloso di ChatGPT e di qualsiasi chatbot generativo?
Per ottenere una risposta utile devi già sapere qual è la domanda giusta da fare.
Ma i disastri più gravi — nella vita come in azienda — nascono sempre da ciò che "non sai di non sapere".

Nella Puntata #02 di "Anatomia di una Serial Killer App" mostriamo come Connect the DOTS uccide il foglio bianco dei chatbot grazie al Triage Diagnostico Causale (che ti guida per nesso causale dal sintomo L2 alla soluzione L3 senza allucinazioni):
👤 Persona (P): individui in 60 secondi la vera causa radice di un blocco.
🎓 Professionista (SME): il cliente arriva da te avendo già qualificato il bisogno sull'L3 Ancora.
🏢 Imprenditore/PMI (B): isoli in 3 minuti il vero collo di bottiglia operativo o finanziario.

Domani uscirà qui su LinkedIn il Carosello PDF completo della Puntata #02.
Se vuoi studiarlo in anteprima (e assicurarti 1 Anno+ gratis da Gennaio 2027 col tuo feedback), vai qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #DecisionMaking #ProblemSolving #Gennaio2027""",
        "victim": "Il foglio bianco dei chatbot generativi (dove devi gia' sapere quale domanda fare) e le risposte probabilistiche con allucinazioni.",
        "killer_feature": "Regola aurea Cervello/Orizzonti (L0 -> L1 -> DOT L2 Problema) + Triage Diagnostico assistito con opzione 'Altro' (da specificare) + Proliferazione causale verso il DOT L3 Soluzione (NBD).",
        "payoff_persona": "Trasformi un disagio confuso nella causa radice esatta e nella prima azione concreta da compiere.",
        "payoff_prof": "Il cliente arriva da te avendo gia' qualificato il proprio bisogno sull'L3 Ancora, azzerando i tempi di pre-analisi.",
        "payoff_pmi": "Isoli in 3 minuti il vero collo di bottiglia operativo o finanziario senza allucinazioni da chatbot.",
        "next_teaser": "Prossima Puntata (#03): Cosa succede ai 900 nodi aziendali che non hai ancora esplorato? Scopriremo la SWOT in RAM e il tasto 'Pausa'.",
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

🔪 Prossima puntata (#03): Cosa succede ai 900 nodi aziendali che non hai ancora esplorato? Scopriremo la SWOT in RAM (10/10) e il tasto sovrano "Pausa".

#ConnectTheDOTS #SerialKillerApp #ProblemSolving #DecisionMaking #CoachPrivato #PMI #Gennaio2027"""
    },
    {
        "num": 3,
        "date_a": "Fase A (Ex-Ante 08:15)",
        "date_b": "Fase B (Studio 08:15)",
        "doc_title": "Connect the DOTS #03: SWOT in RAM (10/10) e Tasto Pausa",
        "ancora_doc_title": "Connect the DOTS #03-A: Ignoto = 10/10 + Tasto Pausa",
        "title": "SWOT in RAM (Ignoto = 10/10) e il Tasto Sovrano 'Pausa'",
        "subtitle": "Perche' cio' che non conosci vale Rischio Massimo (e come spegnerlo con un clic per spendere tempo di qualita')",
        "crop": (15, 580, 670, 1075),
        "pts": [6, 7],
        "ancora_b1": "IN AZIENDA CIO' CHE NON CONOSCI NON VALE ZERO: VALE RISCHIO MASSIMO (10/10).",
        "ancora_b2": "MA COME FAI A NON IMPAZZIRE? CON IL TASTO SOVRANO 'PAUSA' ('0') DELLA SWOT IN RAM!",
        "ancora_b3": "STUDIA LA PUNTATA #03 E PRENOTA 1 ANNO+ GRATIS DA GENNAIO 2027 SU WWW.C-T-D.GROUP/NEWS.HTML",
        "ancora_text": """Nei cruscotti aziendali tradizionali, ciò che non monitori vale zero. Finché un giorno quell'angolo cieco esplode.
Se invece provi a controllare tutto, finisci paralizzato dal sovraccarico.

Nella Puntata #03 di "Anatomia di una Serial Killer App" sveliamo come Connect the DOTS risolve questo paradosso direttamente in memoria RAM:
1️⃣ Ogni nodo ignoto vale automaticamente Debolezza 10/10 e Minaccia 10/10.
2️⃣ Premendo il tasto sovrano "Pausa", i valori scendono a '0' ed escono dai calcoli per farti spendere tempo di qualità solo sulle tue vere priorità.

Domani pubblicherò qui su LinkedIn il Carosello PDF della Puntata #03.
Se vuoi studiarla subito in anteprima (e bloccare 1 Anno+ gratis per Gennaio 2027 col tuo feedback), la trovi qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #SWOT #ControlloDiGestione #CFO #Imprenditori #Gennaio2027""",
        "victim": "Le analisi SWOT statiche dimenticate nei PDF e i cruscotti tradizionali che guardano solo il fatturato ignorando gli angoli ciechi.",
        "killer_feature": "Algoritmo _healDatabaseRollups in RAM: ogni nodo ignoto = Debolezza 10/10 e Minaccia 10/10; tasto Pausa = reset a '0'; metriche oltre il fatturato + Regime Fiscale + Scudo Anonimizzazione AI.",
        "payoff_persona": "Azzeri il sovraccarico cognitivo mettendo in 'Pausa' ('0') cio' che non e' prioritario per dedicarti solo a cio' che conta.",
        "payoff_prof": "Offri alle PMI clienti stress test e cruscotti predittivi in RAM su oltre 400 lenti direzionali.",
        "payoff_pmi": "Vedi in tempo reale dove si annidano le minacce 10/10 nei tuoi 8 orizzonti senza far uscire un byte dal tuo Mac/PC.",
        "next_teaser": "Prossima Puntata (#04): Perche' bruciare gigawatt su server cloud per rielaborare risposte gia' note? Scopriremo l'Esperanto dei ~1.000 DOT.",
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
        "date_a": "Fase A (Ex-Ante 08:15)",
        "date_b": "Fase B (Studio 08:15)",
        "doc_title": "Connect the DOTS #04: L'Esperanto dei 1.000 DOT Offline",
        "ancora_doc_title": "Connect the DOTS #04-A: Basta Bruciare Gigawatt in Cloud",
        "title": "L'Esperanto dei ~1.000 DOT e la Micro-Blockchain Offline",
        "subtitle": "Sostenibilita' energetica Edge AI, conformita' nativa GDPR / EU AI Act e integrita' locale a costo server zero",
        "crop": (15, 140, 670, 1075),
        "pts": [2, 7, 16],
        "ancora_b1": "PERCHE' BRUCIARE GIGAWATT SU SERVER CLOUD PER RIGENERARE RISPOSTE CHE GLI ESPERTI CONOSCONO GIA'?",
        "ancora_b2": "1.000 DOT IN ITALIANO CHIARO ('ESPERANTO') + MICRO-BLOCKCHAIN 100% OFFLINE A COSTO SERVER ZERO.",
        "ancora_b3": "SCOPRI LA PUNTATA #04 E BLOCCA 1 ANNO+ GRATIS SU WWW.C-T-D.GROUP/NEWS.HTML",
        "ancora_text": """Perché bruciare gigawatt su server cloud remoti (esponendo i tuoi dati aziendali) per farsi rigenerare da zero risposte che gli esperti umani di dominio (SME) conoscono già?

Nella Puntata #04 di "Anatomia di una Serial Killer App" sveliamo come Connect the DOTS unisce sostenibilità energetica, privacy totale (GDPR / EU AI Act) e un "Esperanto" comune di ~1.000 DOT che fa finalmente capirsi Persone, Professionisti e PMI.

Domani pubblicherò qui su LinkedIn il Carosello PDF della Puntata #04.
Se vuoi studiarla subito in anteprima (e assicurarti 1 Anno+ gratis per Gennaio 2027 lasciando il tuo feedback), vai qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #EdgeAI #AIAct #GDPR #Sostenibilita #Gennaio2027""",
        "victim": "Lo spreco energetico dei data center AI Cloud e la Babele linguistica che impedisce a domanda e offerta di capirsi.",
        "killer_feature": "Knowledge Graph olografico di ~1.000 DOT ordinati (sort_order) come lingua franca ('Esperanto') + esecuzione 100% offline + catena crittografica SQLite (local_source_chain) a costo server zero.",
        "payoff_persona": "Navighi anche offline con latenza 0 ms e certezza matematica che il tuo Profilo aggiornato resti solo tuo.",
        "payoff_prof": "Parli finalmente lo stesso codice ('Esperanto') dei tuoi potenziali clienti sul nodo L3 della tua specializzazione.",
        "payoff_pmi": "Adotti l'AI in azienda azzerando rischi GDPR / EU AI Act e canoni ricorrenti di server e token cloud.",
        "next_teaser": "Prossima Puntata (#05): Capire il problema e' inutile se il buon proposito muore in una lista di To-Do. Entreremo nel Secondo Cervello.",
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
        "date_a": "Fase A (Ex-Ante 08:15)",
        "date_b": "Fase B (Studio 08:15)",
        "doc_title": "Connect the DOTS #05: 2° Cervello, To-Do e Cantieri L3",
        "ancora_doc_title": "Connect the DOTS #05-A: Il Cimitero delle Liste To-Do",
        "title": "2° Cervello: Proliferazione To-Do -> L3 Progetto & Sinapsi",
        "subtitle": "Come trasformare ogni compito in un cantiere strutturato collegato alla strategia",
        "crop": (650, 140, 1315, 660),
        "pts": [9, 10, 11, 12],
        "ancora_b1": "QUANTE IDEE E BUONI PROPOSITI MUOIONO OGNI SETTIMANA NELLA TUA LISTA DI 'TO-DO'?",
        "ancora_b2": "IL 2° CERVELLO CtD FA PROLIFERARE OGNI COMPITO IN UN CANTIERE 'L3 PROGETTO' CON SINAPSI ORIZZONTALI.",
        "ancora_b3": "STUDIA LA PUNTATA #05 E PRENOTA 1 ANNO+ GRATIS SU WWW.C-T-D.GROUP/NEWS.HTML",
        "ancora_text": """Quante idee brillanti o compiti urgenti hai segnato in una lista di "To-Do" che dopo una settimana si è trasformata in un cimitero di buoni propositi scollegati dalla strategia?

Nella Puntata #05 di "Anatomia di una Serial Killer App" entriamo nel Secondo Cervello di Connect the DOTS: vedremo come un compito prolifera automaticamente in un cantiere L3 Progetto mantenendo la gerarchia verticale (parent_uuid) e le Sinapsi Orizzontali Bidirezionali.

Domani uscirà qui su LinkedIn il Carosello PDF completo della Puntata #05.
Se vuoi studiarlo subito in anteprima (e assicurarti 1 Anno+ gratis da Gennaio 2027 col tuo feedback), vai qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #SecondoCervello #Execution #ProjectManagement #PMI #Gennaio2027""",
        "victim": "Il cimitero delle liste To-Do e dei project manager scollegati dagli obiettivi strategici.",
        "killer_feature": "Proliferazione automatica (To-Do / MIO_Idea -> L3 Progetto / MIO_Goal con parent_uuid verticale) + Sinapsi Orizzontali Bidirezionali (evolvedFrom / peerFlow in UserSynapseState) + Mattoni L3 tra stato P e traguardo T.",
        "payoff_persona": "Non perdi mai piu' il legame tra un'idea annotata al volo e il traguardo di vita a cui serve.",
        "payoff_prof": "Consegni ai clienti non un PDF teorico ma un cantiere L3 gia' scomposto in mattoni esecutivi.",
        "payoff_pmi": "Colleghi ogni singolo task operativo del team all'obiettivo strategico padre eliminando la dispersione.",
        "next_teaser": "Prossima Puntata (#06): Chi esegue materialmente ogni mattone del cantiere e chi certifica il risultato? Scopriremo la Palestra di 21 Giorni.",
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
        "date_a": "Fase A (Ex-Ante 08:15)",
        "date_b": "Fase B (Studio 08:15)",
        "doc_title": "Connect the DOTS #06: Palestra 21 Giorni e PoR Multi-Sig",
        "ancora_doc_title": "Connect the DOTS #06-A: Palestra 21gg e Risultati Veri",
        "title": "Allocazione a 3 Vie, Palestra di 21 Giorni e Certificato PoR",
        "subtitle": "Dalla teoria alla pratica certificata con scudo crittografico 2-of-2 Multi-Sig",
        "crop": (650, 560, 1315, 1075),
        "pts": [13, 14, 15, 16],
        "ancora_b1": "LA FORMAZIONE TEORICA SENZA 21 GIORNI DI PRATICA LASCIA TUTTO COM'ERA PRIMA.",
        "ancora_b2": "SMISTAMENTO A 3 VIE + PALESTRA DI 21 GIORNI + CERTIFICATO CRITTOGRAFICO PROOF-OF-RESULT (PoR).",
        "ancora_b3": "SCOPRI LA PUNTATA #06 E PRENOTA 1 ANNO+ GRATIS SU WWW.C-T-D.GROUP/NEWS.HTML",
        "ancora_text": """Quanti corsi di formazione o consulenze restano lettera morta il lunedì mattina successivo perché manca un binario esecutivo di 21 giorni?

Nella Puntata #06 di "Anatomia di una Serial Killer App" sveliamo lo Smistamento Sovrano a 3 Vie di Connect the DOTS (Fai-da-Te in Palestra, Vista 1 SME o Vista 2 Rete) e il Certificato crittografico Proof-of-Result (PoR a doppia firma 2-of-2 Multi-Sig).

Domani pubblicherò qui su LinkedIn il Carosello PDF della Puntata #06.
Se vuoi studiarlo subito in anteprima (e assicurarti 1 Anno+ gratis per Gennaio 2027 lasciando il tuo feedback), vai qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #Palestra21Giorni #ProofOfResult #Meritocrazia #Gennaio2027""",
        "victim": "I corsi di formazione che restano sulla carta e le metriche di risultato autodichiarate senza verifica.",
        "killer_feature": "Smistamento sovrano a 3 vie per ogni mattone (Fai-da-Te in Palestra / Vista 1 SME / Vista 2 Rete + 'Altro') + Palestra operativa di 21 giorni + Certificato Proof-of-Result (PoR 2-of-2 Multi-Sig).",
        "payoff_persona": "Costruisci un portafoglio inoppugnabile di certificati PoR su risultati reali raggiunti.",
        "payoff_prof": "Trasformi il tuo metodo in una Palestra di 21 giorni che garantisce la messa a terra da parte del cliente.",
        "payoff_pmi": "Decidi mattone per mattone cosa fare in casa e cosa delegare all'esterno misurando solo risultati veri.",
        "next_teaser": "Prossima Puntata (#07): Cosa accade quando il tuo parametro R su un DOT diventa altissimo (R >>)? Scopriremo la qualifica a Proven SME.",
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
        "date_a": "Fase A (Ex-Ante 08:15)",
        "date_b": "Fase B (Studio 08:15)",
        "doc_title": "Connect the DOTS #07: Cordone Ombelicale e Proven SME",
        "ancora_doc_title": "Connect the DOTS #07-A: Fine dei Finti Guru da Tastiera",
        "title": "Cordone Ombelicale 21gg e Qualifica Proven SME (R>>) NEXUS",
        "subtitle": "La fine dei finti guru: come i risultati reali ti portano i clienti in modalita' Pull",
        "crop": (650, 560, 1905, 1075),
        "pts": [14, 15, 20, 24],
        "ancora_b1": "SUI SOCIAL VINCE CHI URLA PIU' FORTE. NEL MONDO REALE VINCE CHI HA RISULTATI CERTIFICATI (R >>).",
        "ancora_b2": "CORDONE OMBELICALE DI 21 GIORNI COI CLIENTI + COOPTAZIONE MERITOCRATICA A 'PROVEN SME' VIA NEXUS.",
        "ancora_b3": "CANDIDATI COME EARLY ADOPTER (1 ANNO+ GRATIS) SU WWW.C-T-D.GROUP/NEWS.HTML",
        "ancora_text": """Sui social tradizionali vince chi urla più forte o compra più pubblicità, anche senza aver mai risolto un caso reale.
E se invece i clienti ti scegliessero in modalità Pull solo sulla base dei risultati certificati (R >>) che hai fatto ottenere sul campo?

Nella Puntata #07 di "Anatomia di una Serial Killer App" sveliamo il "Cordone Ombelicale" di 21 giorni coi tuoi migliori clienti e il meccanismo di cooptazione meritocratica a Proven SME via NEXUS.

Domani uscirà qui su LinkedIn il Carosello PDF della Puntata #07.
Se vuoi studiarlo subito in anteprima (e bloccare 1 Anno+ gratis per Gennaio 2027 lasciando un feedback), vai qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #ProvenSME #Consulenza #ProfessionalServices #NEXUS #Gennaio2027""",
        "victim": "I finti guru da tastiera che vincono urlando sui social e l'abbandono del cliente dopo la sessione di consulenza.",
        "killer_feature": "Cordone Ombelicale di 21 giorni tra professionista (es. BNI Barbarossa) e migliori clienti + Qualifica automatica a Proven SME raggiungendo R >> + Cooptazione via NEXUS sull'L3 Ancora della Community.",
        "payoff_persona": "Anche senza budget pubblicitario, se eccelli su un DOT (R >>) vieni cooptato e reso visibile on-demand.",
        "payoff_prof": "Blindi i tuoi clienti attuali col Cordone Ombelicale di 21gg e ricevi nuovi incarichi in Pull sugli L3 dove hai R >>.",
        "payoff_pmi": "Attingi solo a Proven SME i cui risultati R >> sono stati certificati sul campo dalla piattaforma.",
        "next_teaser": "Prossima Puntata (#08): Come chiedi aiuto alla tua rete senza mai rivelare agli amici qual e' la tua debolezza 10/10? Ecco il Salto del 1° Grado.",
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
        "date_a": "Fase A (Ex-Ante 08:15)",
        "date_b": "Fase B (Studio 08:15)",
        "doc_title": "Connect the DOTS #08: Score Ponte e Salto del 1° Grado",
        "ancora_doc_title": "Connect the DOTS #08-A: Il Salto del 1° Grado Riservato",
        "title": "Network Engineering: Score Ponte e 'Salto del 1° Grado'",
        "subtitle": "Raggiungere il risolutore perfetto al 2° grado senza mai esporre le tue debolezze 10/10 ai contatti diretti",
        "crop": (1300, 140, 1905, 680),
        "pts": [17, 18, 19, 20, 21],
        "ancora_b1": "COME CHIEDI AIUTO ALLA TUA RETE SENZA MAI CONFESSARE LE TUE DEBOLEZZE 10/10 AGLI AMICI DI 1° GRADO?",
        "ancora_b2": "SCORE PONTE IN RAM + CAPSULE DA 1 KB (.CTDIR) COL 'SALTO DEL 1° GRADO' FINO AL RISOLUTORE DI 2° GRADO!",
        "ancora_b3": "SCOPRI LA PUNTATA #08 E BLOCCA 1 ANNO+ GRATIS SU WWW.C-T-D.GROUP/NEWS.HTML",
        "ancora_text": """Quando hai una criticità delicata in azienda o nella vita privata (Debolezza 10/10), non vuoi raccontarla al tuo amico o contatto diretto di 1° grado. Eppure la persona che può risolverla si trova quasi sempre al 2° grado (tra i contatti dei tuoi contatti).

Nella Puntata #08 di "Anatomia di una Serial Killer App" sveliamo come il Network Engineering di Connect the DOTS calcola in RAM lo Score Ponte e realizza il "Salto del 1° Grado" in totale riservatezza.

Domani pubblicherò qui su LinkedIn il Carosello PDF della Puntata #08.
Se vuoi studiarlo subito in anteprima (e assicurarti 1 Anno+ gratis per Gennaio 2027 col tuo feedback), vai qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #NetworkEngineering #BNI #BusinessMatching #Privacy #Gennaio2027""",
        "victim": "Il networking a freddo e l'imbarazzo di dover confessare le proprie debolezze 10/10 agli amici o contatti di 1° grado.",
        "killer_feature": "Grafo relazionale ir_contacts_graph ('chi mi ha presentato chi') + calcolo in RAM di Score Diretto vs Score Ponte + Capsule anonimizzate da 1 KB (.ctdir / QR) con Smart Source-Routing ('Salto del 1° Grado').",
        "payoff_persona": "Chiedi supporto su scelte delicate raggiungendo lo specialista di 2° grado in totale riservatezza.",
        "payoff_prof": "Valorizzi il tuo Score Ponte diventando lo snodo scientifico di referenze inter-capitolo ad alta conversione.",
        "payoff_pmi": "Trovi fornitori o manager per risolvere una criticita' 10/10 senza che concorrenti o conoscenti sappiano del problema.",
        "next_teaser": "Prossima Puntata (#09): Trovato il match tra reti, professionisti e PMI, come ci si scambia valore anche senza bruciare cassa? Ecco l'HTLC.",
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
        "date_a": "Fase A (Ex-Ante 08:15)",
        "date_b": "Fase B (Studio 08:15)",
        "doc_title": "Connect the DOTS #09: Scambio Fluido in-Lire HTLC B2B",
        "ancora_doc_title": "Connect the DOTS #09-A: Scambio HTLC a Doppio Binario",
        "title": "Compensazione in-Lire Fluida (HTLC) a Doppio Binario",
        "subtitle": "Il motore di intersezione tra network (BNI, circuiti B2B, professionisti e PMI) raccordato al Regime Fiscale",
        "crop": (1300, 600, 1905, 1075),
        "pts": [22, 23, 24],
        "ancora_b1": "PERCHE' I CIRCUITI DI SCAMBIO USATI COME SEMPLICI CATALOGHI FATICANO A GENERARE LIQUIDITA' CONTINUA?",
        "ancora_b2": "COMPENSAZIONE IN-LIRE FLUIDA (HTLC) A DOPPIO BINARIO: ORE-PALESTRA (P) + CREDITI B2B TRA IMPRESE (B)!",
        "ancora_b3": "SCOPRI LA PUNTATA #09 E PRENOTA 1 ANNO+ GRATIS SU WWW.C-T-D.GROUP/NEWS.HTML",
        "ancora_text": """Come si fa a far incrociare la domanda di cantieri reali di Persone, Professionisti, Capitoli BNI e PMI con circuiti di compensazione come in-Lire senza intaccare la liquidità di cassa?

Nella Puntata #09 di "Anatomia di una Serial Killer App" sveliamo la Compensazione Transattiva Fluida (HTLC) a Doppio Binario (Binario 1: Ore-Palestra tra individui | Binario 2: Crediti B2B tra imprese, raccordati al Regime Fiscale).

Domani uscirà qui su LinkedIn il Carosello PDF della Puntata #09.
Se vuoi studiarlo subito in anteprima (e assicurarti 1 Anno+ gratis per Gennaio 2027 lasciando il tuo feedback), vai qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #InLire #B2B #HTLC #EconomiaReale #Networking #Gennaio2027""",
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

ss1_path = os.path.join(assets_dir, "ctd_plancia_ss1.png")
base_ss1 = Image.open(ss1_path).convert("RGB").resize((1920, 1080))

# ==============================================================================
# COSTRUZIONE DELLE 10 CARD ANCORA (1200x1200 QUADRATA MOBILE-FIRST A 3 FUMETTI GIGANTI)
# ==============================================================================
def build_ancora_card(ep):
    num = ep["num"]
    card = Image.new("RGB", (1200, 1200), (10, 10, 15))
    bg_sq = ImageEnhance.Brightness(base_ss1.resize((1200, 1200))).enhance(0.18)
    card.paste(bg_sq, (0, 0))
    dc = ImageDraw.Draw(card)

    # Header
    dc.rectangle([0, 0, 1200, 115], fill=(22, 16, 42))
    dc.text((40, 20), f"CONNECT THE DOTS (GENNAIO 2027)  •  INNESCO PUNTATA #{num:02d}", font=get_font(22, True), fill=(245, 197, 24))
    dc.text((40, 56), ep["title"][:62], font=get_font(31, True), fill=(255, 255, 255))

    # Fumetto Gigante 1 (Rosso/Ambra: Il Problema L2)
    b1 = [50, 155, 1150, 435]
    draw_speech_bubble(dc, b1, (600, 470), (42, 16, 22), (239, 68, 68), width=4)
    draw_badge_pill(dc, 80, 178, "1. IL PROBLEMA CHE L'80% IGNORA", (239, 68, 68), (255, 255, 255), 18)
    draw_wrapped_block(dc, 80, 232, 1040, ep["ancora_b1"], get_font(32, True), (255, 240, 240), 44)

    # Fumetto Gigante 2 (Ciano/Blu: La Soluzione CtD L3)
    b2 = [50, 480, 1150, 775]
    draw_speech_bubble(dc, b2, (600, 810), (14, 30, 52), (56, 189, 248), width=4)
    draw_badge_pill(dc, 80, 503, "2. LA SVOLTA CONNECT THE DOTS (100% OFFLINE)", (56, 189, 248), (0, 0, 0), 18)
    draw_wrapped_block(dc, 80, 558, 1040, ep["ancora_b2"], get_font(31, True), (235, 248, 255), 43)

    # Fumetto Gigante 3 (Verde/Oro: L'Azione Immediata + 1 Anno+ Gratis)
    b3 = [50, 815, 1150, 1095]
    dc.rounded_rectangle(b3, radius=22, fill=(16, 40, 28), outline=(60, 208, 112), width=4)
    draw_badge_pill(dc, 80, 838, "3. LA SFIDA DEI 3 MINUTI (PREMIO EARLY ADOPTER)", (60, 208, 112), (0, 0, 0), 18)
    draw_wrapped_block(dc, 80, 892, 1040, ep["ancora_b3"], get_font(30, True), (245, 197, 24), 42)

    # Footer
    dc.rectangle([0, 1125, 1200, 1200], fill=(22, 16, 42))
    dc.text((40, 1148), ">> Persona (P) • Professionista (SME) • Imprenditore/PMI (B)  |  www.c-t-d.group/news.html", font=get_font(22, True), fill=(255, 255, 255))
    return card

for ep in episodes:
    n = ep["num"]
    assert len(ep["doc_title"]) <= 58
    assert len(ep["ancora_doc_title"]) <= 58
    assert li_utf16_len(ep["ancora_text"]) <= 2950
    assert li_utf16_len(ep["post_text"]) <= 2950

    acard = build_ancora_card(ep)
    png_name = f"Ancora_LinkedIn_Puntata_{n:02d}.png"
    pdf_anc_name = f"Ancora_LinkedIn_Puntata_{n:02d}.pdf"
    acard.save(os.path.join(assets_dir, png_name))
    acard.save(os.path.join(out_desktop_dir, png_name))
    acard.save(os.path.join(out_desktop_dir, pdf_anc_name), "PDF", resolution=150.0)
    acard.save(os.path.join(caroselli_web_dir, pdf_anc_name), "PDF", resolution=150.0)

print("OK: Generate tutte le 10 Card Ancora Ex-Ante (.png e .pdf)!")

# ==============================================================================
# AGGIORNAMENTO DI regia_linkedin.html CON DOPPIA COLONNA: FASE A (ANCORA) + FASE B (MASTER)
# ==============================================================================
cards_html = ""
for ep in episodes:
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
                        PUNTATA #{n:02d} • Strategia a Doppio Stadio (Fase A Ex-Ante + Fase B Studio Master)
                    </span>
                    <h2 style="color:#fff; font-size:1.5rem; margin:8px 0 0 0;">Puntata #{n:02d} — {ep['title']}</h2>
                </div>
                <div style="display:flex; gap:12px; flex-wrap:wrap;">
                    <label style="display:flex; align-items:center; gap:8px; background:#1e1b2e; border:2px solid #f5c518; padding:8px 14px; border-radius:10px; cursor:pointer; font-weight:800; color:#f5c518; font-size:0.85rem;">
                        <input type="checkbox" id="chk-a-{n:02d}" onchange="saveDoneState('{n:02d}')" style="width:18px; height:18px;">
                        <span>Fase A (Ancora) Pubblicata [✓]</span>
                    </label>
                    <label style="display:flex; align-items:center; gap:8px; background:#102618; border:2px solid #3cd070; padding:8px 14px; border-radius:10px; cursor:pointer; font-weight:800; color:#3cd070; font-size:0.85rem;">
                        <input type="checkbox" id="chk-b-{n:02d}" onchange="saveDoneState('{n:02d}')" style="width:18px; height:18px;">
                        <span>Fase B (Master) Pubblicata [✓]</span>
                    </label>
                </div>
            </div>

            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:24px; align-items:start;">
                <!-- COLONNA SINISTRA: FASE A (POST-ANCORA EX-ANTE BREVE PER 8 SU 10) -->
                <div style="background:#0e0e14; border:2px solid #f5c518; border-radius:12px; padding:18px;">
                    <div style="background:#2a1f0d; color:#f5c518; padding:8px 12px; border-radius:8px; font-weight:800; font-size:0.9rem; margin-bottom:14px;">
                        ⚡ FASE A (Giorno 1, ore 08:15) — IL POST-ANCORA EX-ANTE (Lettura 10 sec)
                    </div>
                    <div style="display:grid; grid-template-columns: 165px 1fr; gap:14px; margin-bottom:14px; align-items:center;">
                        <img src="assets/Ancora_LinkedIn_Puntata_{n:02d}.png" alt="Ancora {n:02d}" style="width:100%; border-radius:8px; border:1px solid #f5c518;">
                        <div style="font-size:0.82rem; color:#cbd5e1;">
                            <strong>Allegato Fase A (Scrivania/CtD_LinkedIn_Caroselli_PDF):</strong><br>
                            • Immagine: <code style="color:#f5c518;">Ancora_LinkedIn_Puntata_{n:02d}.png</code><br>
                            • Oppure PDF: <code style="color:#f5c518;">Ancora_LinkedIn_Puntata_{n:02d}.pdf</code><br>
                            <div style="margin-top:8px; display:flex; gap:8px; flex-wrap:wrap;">
                                <a href="assets/Ancora_LinkedIn_Puntata_{n:02d}.png" download="Ancora_LinkedIn_Puntata_{n:02d}.png" style="background:#1e293b; color:#f5c518; border:1px solid #f5c518; padding:6px 10px; border-radius:6px; text-decoration:none; font-weight:700;">📥 PNG</a>
                                <a href="assets/caroselli/Ancora_LinkedIn_Puntata_{n:02d}.pdf" download="Ancora_LinkedIn_Puntata_{n:02d}.pdf" style="background:#1e293b; color:#f5c518; border:1px solid #f5c518; padding:6px 10px; border-radius:6px; text-decoration:none; font-weight:700;">📥 PDF</a>
                                <a href="https://www.linkedin.com/sharing/compose" target="_blank" style="background:#0a66c2; color:#fff; padding:6px 12px; border-radius:6px; text-decoration:none; font-weight:800;">🚀 Apri LinkedIn</a>
                            </div>
                        </div>
                    </div>

                    <div style="margin-bottom:12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.78rem; font-weight:800; color:#f5c518; margin-bottom:4px;">
                            <span>Titolo (se carichi il PDF • Max 58 car.):</span>
                            <span id="cnt-ta-{n:02d}" style="color:#3cd070;">🟢 {ta_len}/58</span>
                        </div>
                        <div style="display:flex; gap:8px;">
                            <input type="text" id="inp-ta-{n:02d}" value="{ep['ancora_doc_title']}" maxlength="58" oninput="updateCount('inp-ta-{n:02d}','cnt-ta-{n:02d}',58,'ctd_v4_ta_{n:02d}')" style="flex:1; padding:8px; border-radius:6px; border:1px solid #444; background:#16161f; color:#fff; font-weight:700; font-size:0.85rem;">
                            <button type="button" onclick="copyField('inp-ta-{n:02d}', this, 58)" style="background:#f5c518; color:#000; border:none; padding:8px 12px; border-radius:6px; font-weight:800; cursor:pointer; font-size:0.8rem;">📋 Copia Titolo A</button>
                        </div>
                    </div>

                    <div id="box-ba-{n:02d}">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <span id="cnt-ba-{n:02d}" style="font-size:0.8rem; font-weight:800; color:#3cd070;">🟢 {pa_len} / 3000 car. (Margine: +{3000 - pa_len})</span>
                            <button type="button" onclick="copyField('inp-ba-{n:02d}', this, 3000)" style="background:#f5c518; color:#000; border:none; padding:8px 14px; border-radius:6px; font-weight:800; cursor:pointer; font-size:0.84rem;">
                                📋 Copia Testo Breve Ancora (FASE A)
                            </button>
                        </div>
                        <textarea id="inp-ba-{n:02d}" rows="14" oninput="updateCount('inp-ba-{n:02d}','cnt-ba-{n:02d}',3000,'ctd_v4_ba_{n:02d}')" style="width:100%; padding:10px; border-radius:6px; border:1px solid #444; background:#16161f; color:#f1f5f9; font-family:inherit; font-size:0.86rem; line-height:1.5; box-sizing:border-box;">{ep['ancora_text']}</textarea>
                    </div>
                </div>

                <!-- COLONNA DESTRA: FASE B (POST MASTER CON CAROSELLO PDF A 2 SLIDE) -->
                <div style="background:#0e0e14; border:2px solid #38bdf8; border-radius:12px; padding:18px;">
                    <div style="background:#0f2438; color:#38bdf8; padding:8px 12px; border-radius:8px; font-weight:800; font-size:0.9rem; margin-bottom:14px;">
                        📘 FASE B (Giorno 2, ore 08:15) — IL POST MASTER COMPLETO (Carosello 2 Slide)
                    </div>
                    <div style="display:grid; grid-template-columns: 165px 1fr; gap:14px; margin-bottom:14px; align-items:center;">
                        <img src="assets/news_ep_{n:02d}.png" alt="Master {n:02d}" style="width:100%; border-radius:8px; border:1px solid #38bdf8;">
                        <div style="font-size:0.82rem; color:#cbd5e1;">
                            <strong>Carosello PDF a 2 Slide (Zero Spoiler):</strong><br>
                            <code style="color:#38bdf8;">Carosello_LinkedIn_Puntata_{n:02d}.pdf</code><br>
                            <div style="margin-top:8px; display:flex; gap:8px; flex-wrap:wrap;">
                                <a href="assets/caroselli/Carosello_LinkedIn_Puntata_{n:02d}.pdf" download="Carosello_LinkedIn_Puntata_{n:02d}.pdf" style="background:#1e293b; color:#38bdf8; border:1px solid #38bdf8; padding:6px 10px; border-radius:6px; text-decoration:none; font-weight:700;">📥 Scarica PDF Master</a>
                                <a href="https://www.linkedin.com/sharing/compose" target="_blank" style="background:#0a66c2; color:#fff; padding:6px 12px; border-radius:6px; text-decoration:none; font-weight:800;">🚀 Apri LinkedIn</a>
                            </div>
                        </div>
                    </div>

                    <div style="margin-bottom:12px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.78rem; font-weight:800; color:#38bdf8; margin-bottom:4px;">
                            <span>PASSO 1 — Document title* (Max 58 car.):</span>
                            <span id="cnt-tb-{n:02d}" style="color:#3cd070;">🟢 {tb_len}/58</span>
                        </div>
                        <div style="display:flex; gap:8px;">
                            <input type="text" id="inp-tb-{n:02d}" value="{ep['doc_title']}" maxlength="58" oninput="updateCount('inp-tb-{n:02d}','cnt-tb-{n:02d}',58,'ctd_v4_tb_{n:02d}')" style="flex:1; padding:8px; border-radius:6px; border:1px solid #444; background:#16161f; color:#fff; font-weight:700; font-size:0.85rem;">
                            <button type="button" onclick="copyField('inp-tb-{n:02d}', this, 58)" style="background:#38bdf8; color:#000; border:none; padding:8px 12px; border-radius:6px; font-weight:800; cursor:pointer; font-size:0.8rem;">📋 1. Copia Titolo B</button>
                        </div>
                    </div>

                    <div id="box-bb-{n:02d}">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <span id="cnt-bb-{n:02d}" style="font-size:0.8rem; font-weight:800; color:#3cd070;">🟢 {pb_len} / 3000 car. (Margine: +{3000 - pb_len})</span>
                            <button type="button" onclick="copyField('inp-bb-{n:02d}', this, 3000)" style="background:#38bdf8; color:#000; border:none; padding:8px 14px; border-radius:6px; font-weight:800; cursor:pointer; font-size:0.84rem;">
                                📋 2. Copia Testo Master (FASE B)
                            </button>
                        </div>
                        <textarea id="inp-bb-{n:02d}" rows="14" oninput="updateCount('inp-bb-{n:02d}','cnt-bb-{n:02d}',3000,'ctd_v4_bb_{n:02d}')" style="width:100%; padding:10px; border-radius:6px; border:1px solid #444; background:#16161f; color:#f1f5f9; font-family:inherit; font-size:0.86rem; line-height:1.5; box-sizing:border-box;">{ep['post_text']}</textarea>
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
    <title>Cabina di Regia LinkedIn (Doppio Stadio Ex-Ante + Master) — Connect the DOTS</title>
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
            <strong style="color:#f5c518; font-size:1.12rem;">🎬 CABINA DI REGIA LINKEDIN — STRATEGIA DOPPIO STADIO (FASE A: ANCORA EX-ANTE • FASE B: STUDIO MASTER)</strong>
            <span style="display:block; font-size:0.8rem; color:#cbd5e1;">Orario Best Practice: 08:00 – 08:30 • A sinistra il Post-Ancora breve (per 8 su 10), a destra il Post Master completo (per 2 su 10)</span>
        </div>
        <div class="ep-jump">
            <span>Puntata:</span>
            {"".join(f'<a href="#regia-ep-{ep["num"]:02d}">#{ep["num"]:02d}</a>' for ep in episodes)}
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
                cnt.innerText = '🟢 ' + len + ' / ' + maxLimit + (maxLimit === 3000 ? ' car. (Margine: +' + diff + ')' : '');
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
            localStorage.setItem('ctd_v4_done_a_' + epNum, ca ? '1' : '0');
            localStorage.setItem('ctd_v4_done_b_' + epNum, cb ? '1' : '0');
            var card = document.getElementById('regia-ep-' + epNum);
            card.style.borderColor = (ca && cb) ? '#3cd070' : (ca ? '#f5c518' : '#2c2c3a');
        }}

        window.addEventListener('DOMContentLoaded', function() {{
            for (var i = 0; i <= 9; i++) {{
                var k = (i < 10 ? '0' + i : '' + i);
                ['ta', 'ba', 'tb', 'bb'].forEach(function( prefix ) {{
                    var sk = 'ctd_v4_' + prefix + '_' + k;
                    var val = localStorage.getItem(sk);
                    var inpId = 'inp-' + prefix + '-' + k;
                    var cntId = 'cnt-' + prefix + '-' + k;
                    var lim = (prefix === 'ta' || prefix === 'tb') ? 58 : 3000;
                    if (val !== null && document.getElementById(inpId)) {{
                        document.getElementById(inpId).value = val;
                        updateCount(inpId, cntId, lim, sk);
                    }}
                }});
                var da = localStorage.getItem('ctd_v4_done_a_' + k) === '1';
                var db = localStorage.getItem('ctd_v4_done_b_' + k) === '1';
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
print("OK: Console regia_linkedin.html aggiornata con Fase A (Ex-Ante) + Fase B (Master)!")
