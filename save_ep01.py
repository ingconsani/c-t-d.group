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
cr, dk = (185, 28, 28), (15, 23, 42)
d.rectangle([24, 24, 1176, 1176], outline=dk, width=10)
d.rectangle([24, 24, 1176, 130], fill=cr)
center_txt(d, 62, 1100, "ANATOMIA DI UNA SERIAL KILLER APP • INNESCO #01", fnt(28), (255,255,255), 34)
d.ellipse([440, 175, 760, 455], fill=(255,255,255), outline=dk, width=8)
center_txt(d, 275, 290, "3 SISTEMI IN 1", fnt(36), cr, 44)
center_txt(d, 325, 290, "100% OFFLINE", fnt(34), dk, 42)
y = center_txt(d, 505, 1020, "QUANTE APP USI OGNI GIORNO CHE NON SI PARLANO TRA LORO?", fnt(52), dk, 64)
d.line([(250, y+20), (950, y+20)], fill=cr, width=5)
center_txt(d, y+42, 1000, "Diagnosi + Esecuzione + Relazioni = 1 Sola Piattaforma Offline.", fnt(34), cr, 44)
d.rectangle([24, 1035, 1176, 1176], fill=dk)
center_txt(d, 1060, 1100, "DOMANI ORE 08:15 LO STUDIO TECNICO QUI SU LINKEDIN", fnt(26), (245,197,24), 32)
center_txt(d, 1108, 1100, "Anteprima immediata (+ 1 Anno Gratis): www.c-t-d.group/news.html", fnt(25), (255,255,255), 32)
for folder in [assets, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_01.png")
for folder in [caroselli, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_01.pdf", "PDF", resolution=150.0)

db_file = f"{repo}/regia_posts.json"
data = json.load(open(db_file)) if os.path.exists(db_file) else {}
data["01"] = {
  "ep_title": "Il Manifesto: 3 Systems in 1 Platform (S = C + P + T + R)",
  "ta": "Connect the DOTS #01-A: Tre App Che Non Si Parlano",
  "ba": """Un'app per annotare le idee.
Un'app per le liste di cose da fare che puntualmente rimandi.
Un social per cercare clienti o fornitori a freddo.

Tre strumenti separati che non si parlano e bruciano il 70% del tuo tempo.
E se Diagnosi, Esecuzione e Relazioni fossero 3 Sistemi integrati in 1 sola Piattaforma 100% offline?

Domani mattina alle 08:15 pubblico la radiografia completa qui su LinkedIn.
Chi vuole studiarla subito in anteprima (e bloccare 1 Anno+ gratis da Gennaio 2027) la trova qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #3SystemsInOnePlatform""",
  "tb": "Connect the DOTS #01: 3 Systems in 1 Platform (Offline)",
  "bb": """🔪 Anatomia di una Serial Killer App — Puntata #01: Il Manifesto dei "3 Systems in 1 Platform" (S = C + P + T + R).
(Hai perso la Puntata #00 Il Trailer? La trovi nella Timeline col Check Verde in Slide 2 e su https://www.c-t-d.group/news.html 👇).

Oggi la nostra Serial Killer App (in arrivo a Gennaio 2027) elimina la sua prima vittima illustre: i software isolati su Cloud che frammentano il lavoro, divorano energia ed espongono i tuoi dati riservati.

Cosa faresti se avessi già oggi Connect the DOTS sul tuo Mac, PC o smartphone?
Avresti 3 Sistemi integrati in 1 sola Piattaforma (3 Systems in 1 Platform) che lavorano al 100% offline dentro il tuo Profilo aggiornato:

1️⃣ 1° Sistema — Diagnosi Strategica (Punti 1..8): il tuo Coach privato, arricchito dall'intelligenza umana degli esperti di dominio (SME), per capire esattamente dove ti trovi oggi attraverso l'equazione proprietaria S = C + P + T + R (Capacità + Potenziale + Traguardo + Risultati).
2️⃣ 2° Sistema — Secondo Cervello Esecutivo (Punti 9..16): per trasformare ogni tuo problema o idea in un cantiere pratico di 21 giorni fino al raggiungimento di un risultato reale certificato.
3️⃣ 3° Sistema — Ingegneria Relazionale Pull (Punti 17..24): per attivare su richiesta solo le competenze, i clienti e le relazioni che ti servono per chiudere i tuoi cantieri, dentro una Community che parla la stessa lingua ("Esperanto").

🎯 IL VANTAGGIO CONCRETO DI QUESTA ARCHITETTURA PER TE:
👤 Se sei una Persona o un Talento: diventi padrone del tuo futuro con un Coach 100% privato che lavora solo per te senza mai cedere i tuoi dati al cloud.
🎓 Se sei un Professionista o Consulente: smetti di rincorrere clienti a freddo (Push) e vieni scelto su richiesta (Pull) grazie ai risultati reali certificati sui tuoi progetti.
🏢 Se sei un Imprenditore, una PMI o un Network: unifichi diagnosi strategica, controllo d'esecuzione e ricerca riservata di partner o fornitori in un'unica plancia a costo server zero.

🎁 VUOI USARLA GRATIS PER UN ANNO O PIÙ DA GENNAIO 2027?
Vai su https://www.c-t-d.group/news.html : lascia il tuo feedback insieme alla tua email per iscriverti alla newsletter delle puntate e blocca subito il tuo posto nel Programma Early Adopter!

Quale dei 3 blocchi ti fa perdere più tempo oggi: capire le priorità, portare a termine i progetti o trovare le persone giuste? 👇

#ConnectTheDOTS #SerialKillerApp #3SystemsInOnePlatform #EdgeAI #StrategiaAziendale #Gennaio2027 #EarlyAdopter"""
}
json.dump(data, open(db_file, "w"), ensure_ascii=False, indent=2)
