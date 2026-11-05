import os, json
from PIL import Image, ImageDraw, ImageFont

repo = "/Users/ingconsani/Development/c-t-d.group"
assets, caroselli = f"{repo}/assets", f"{repo}/assets/caroselli"
desktop = "/Users/ingconsani/Desktop/CtD_LinkedIn_Caroselli_PDF"

def fnt(sz):
    p = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    return ImageFont.truetype(p, sz) if os.path.exists(p) else ImageFont.load_default()

def center_txt(d, y, mw, txt, f, col, lh):
    words, lines, cur = txt.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if d.textbbox((0,0), t, font=f)[2] <= mw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    for ln in lines:
        w = d.textbbox((0,0), ln, font=f)[2]
        d.text((600 - w//2, y), ln, font=f, fill=col); y += lh
    return y

im = Image.new("RGB", (1200, 1200), (252, 249, 240))
d = ImageDraw.Draw(im)
cr, dk, gr = (185, 28, 28), (15, 23, 42), (22, 163, 74)
d.rectangle([24, 24, 1176, 1176], outline=dk, width=10)
d.rectangle([24, 24, 1176, 130], fill=cr)
center_txt(d, 62, 1100, "ANATOMIA DI UNA SERIAL KILLER APP • INNESCO #09", fnt(28), (255,255,255), 34)
d.ellipse([440, 175, 760, 455], fill=(255,255,255), outline=dk, width=8)
center_txt(d, 255, 290, "DOPPIO BINARIO", fnt(34), cr, 42)
center_txt(d, 330, 290, "SCAMBIO FLUIDO", fnt(30), gr, 38)
y = center_txt(d, 505, 1020, "I CIRCUITI DI SCAMBIO USATI COME CATALOGHI SI BLOCCANO.", fnt(52), dk, 64)
d.line([(250, y+20), (950, y+20)], fill=cr, width=5)
center_txt(d, y+42, 1000, "Lo scambio decolla quando parte dai tuoi cantieri reali (Persone & Imprese).", fnt(32), cr, 42)
d.rectangle([24, 1035, 1176, 1176], fill=dk)
center_txt(d, 1060, 1100, "DOMANI ORE 08:15 LO STUDIO TECNICO QUI SU LINKEDIN", fnt(26), (245,197,24), 32)
center_txt(d, 1108, 1100, "Anteprima immediata (+ 1 Anno Gratis): www.c-t-d.group/news.html", fnt(25), (255,255,255), 32)
for folder in [assets, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_09.png")
for folder in [caroselli, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_09.pdf", "PDF", resolution=150.0)

db_file = f"{repo}/regia_posts.json"
data = json.load(open(db_file)) if os.path.exists(db_file) else {}
data["09"] = {
  "ep_title": "Compensazione in-Lire Fluida a Doppio Binario (Persone & Imprese)",
  "ta": "Connect the DOTS #09-A: Scambio Fluido a Doppio Binario",
  "ba": """Perché tanti circuiti di scambio aziendale, quando vengono usati come semplici cataloghi passivi, faticano a generare liquidità continua?
Perché lo scambio vero decolla solo quando nasce dai cantieri operativi che devi realizzare domani mattina.

Domani mattina alle 08:15 mostro qui su LinkedIn come funziona la Compensazione Fluida a Doppio Binario (Persone e Imprese) di Connect the DOTS.
Chi vuole studiarla subito in anteprima (e bloccare 1 Anno+ gratis da Gennaio 2027) la trova qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #B2B #InLire #Networking""",
  "tb": "Connect the DOTS #09: Scambio Fluido in-Lire e Reti B2B",
  "bb": """🔪 Anatomia di una Serial Killer App — Puntata #09: Eliminare la separazione tra network diversi e la staticità dei circuiti usati come cataloghi passivi.
(Sfoglia il carosello per la Slide da 1.000 parole e la Timeline col Check Verde delle puntate pubblicate 👇).

Perché tante aziende iscritte a circuiti di credito commerciale o a network professionali faticano a generare scambi continui? Perché cercano su un catalogo statico un acquisto occasionale, invece di partire dai fabbisogni reali dei propri cantieri strategici (L3).

Ecco cosa accade nei punti 22, 23 e 24 di Connect the DOTS (in arrivo a Gennaio 2027):

1️⃣ Motore di Intersezione e Generazione di Opportunità (Punto 22): lo scambio di beni, servizi e referenze nasce direttamente dai mattoni dei cantieri L3 aperti dagli utenti per migliorare la propria equazione S = C + P + T + R. In questo modo CtD mette in comunicazione attiva circuiti di compensazione (come in-Lire), Capitoli professionali (come BNI), consulenti, talenti e PMI.
2️⃣ Compensazione Fluida a Doppio Binario raccordata al Regime Fiscale (Punto 23): fin dall'input dei dati iniziali nel tuo Profilo aggiornato 100% offline, il sistema richiede la preferenza del tuo Regime Fiscale per regolare in modo automatico e trasparente due binari di scambio:
   - Binario 1 (Ore-Palestra): scambio di tempo, competenze e affiancamento pratico tra individui nei cantieri di 21 giorni.
   - Binario 2 (Crediti B2B): compensazione multilaterale di forniture, consulenze e referenze tra imprese e possessori di partita IVA.
3️⃣ Scambio Diretto Dispositivo-a-Dispositivo (Punto 24): connessione immediata in prossimità a costo server zero, con verifica delle eccellenze tramite il nodo centrale della Community.

🎯 IL VANTAGGIO CONCRETO DI QUESTA FUNZIONE PER TE:
👤 Se sei una Persona o un Talento: valorizzi il tuo tempo col Binario 1 (Ore-Palestra) ottenendo il supporto pratico di altri specialisti senza esborsi monetari.
🎓 Se sei un Professionista o Membro di Network (es. BNI): moltiplichi gli incarichi incrociando le relazioni del tuo Capitolo con la domanda qualificata delle aziende dei circuiti B2B.
🏢 Se sei un Imprenditore, una PMI o un Circuito B2B: finanzi i tuoi cantieri di crescita L3 tramite il Binario 2 (Crediti B2B), acquisendo nuovi clienti e preservando la liquidità di cassa.

🎁 SERIE APERTA + 1 ANNO+ DI LICENZA GRATUITA DA GENNAIO 2027
Vai su https://www.c-t-d.group/news.html : lascia il tuo feedback (usando anche l'opzione "Altro" per proporre quale problema aziendale vuoi veder "eliminato" nelle prossime puntate!) insieme alla tua email per assicurarti 1 Anno+ Gratis nel Programma Early Adopter!

#ConnectTheDOTS #SerialKillerApp #InLire #B2B #EconomiaReale #Networking #PMI #Gennaio2027"""
}
json.dump(data, open(db_file, "w"), ensure_ascii=False, indent=2)
