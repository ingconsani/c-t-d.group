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
center_txt(d, 62, 1100, "ANATOMIA DI UNA SERIAL KILLER APP • INNESCO #04", fnt(28), (255,255,255), 34)
d.ellipse([440, 175, 760, 455], fill=(255,255,255), outline=dk, width=8)
center_txt(d, 270, 290, "0 WATT", fnt(48), gr, 54)
center_txt(d, 335, 290, "IN CLOUD", fnt(32), dk, 38)
y = center_txt(d, 505, 1020, "PERCHE' BRUCIARE GIGAWATT IN CLOUD PER RISPOSTE GIA' NOTE?", fnt(52), dk, 64)
d.line([(250, y+20), (950, y+20)], fill=cr, width=5)
center_txt(d, y+42, 1000, "L'Esperanto dei 1.000 DOT gira al 100% Offline sul tuo dispositivo.", fnt(34), cr, 44)
d.rectangle([24, 1035, 1176, 1176], fill=dk)
center_txt(d, 1060, 1100, "DOMANI ORE 08:15 LO STUDIO TECNICO QUI SU LINKEDIN", fnt(26), (245,197,24), 32)
center_txt(d, 1108, 1100, "Anteprima immediata (+ 1 Anno Gratis): www.c-t-d.group/news.html", fnt(25), (255,255,255), 32)
for folder in [assets, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_04.png")
for folder in [caroselli, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_04.pdf", "PDF", resolution=150.0)

db_file = f"{repo}/regia_posts.json"
data = json.load(open(db_file)) if os.path.exists(db_file) else {}
data["04"] = {
  "ep_title": "L'Esperanto dei ~1.000 DOT e la Micro-Blockchain Offline",
  "ta": "Connect the DOTS #04-A: Zero Gigawatt Bruciati in Cloud",
  "ba": """Perché bruciare gigawatt su server cloud remoti (esponendo i tuoi segreti industriali) per rigenerare da zero risposte che gli esperti di dominio conoscono già?

La vera rivoluzione dell'Intelligenza Artificiale non è nel Cloud. È 100% offline sul tuo dispositivo.

Domani mattina alle 08:15 mostro qui su LinkedIn come funziona l'"Esperanto" dei 1.000 DOT di Connect the DOTS.
Chi vuole studiarlo subito in anteprima (e bloccare 1 Anno+ gratis da Gennaio 2027) lo trova qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #EdgeAI #GDPR""",
  "tb": "Connect the DOTS #04: L'Esperanto dei 1.000 DOT Offline",
  "bb": """🔪 Anatomia di una Serial Killer App — Puntata #04: Eliminare lo spreco energetico dell'AI Cloud e la Babele dei linguaggi aziendali.
(Sfoglia il carosello per la Slide da 1.000 parole e la Timeline col Check Verde delle puntate pubblicate 👇).

Ogni giorno milioni di utenti interrogano data center remoti bruciando quantità immense di energia per farsi rigenerare da zero risposte che gli esperti umani di dominio (SME) conoscono già. E quando un'impresa cerca uno specialista, spesso usano linguaggi diversi e non riescono a capirsi.

Ecco cosa accade al volante di Connect the DOTS (Punti 2, 7 e 16 — disponibile da Gennaio 2027):

🔹 Intelligenza Capitalizzata 100% Offline: CtD funziona anche senza connessione a internet, sia per motivi di privacy assoluta sia per azzerare i costi ricorrenti di server e token. Il sapere degli esperti (SME) è codificato in una mappa strutturata e ordinata di circa 1.000 nodi che gira interamente sul tuo dispositivo, garantendo conformità nativa a GDPR ed EU AI Act.
🔹 L'"Esperanto" della Community: quei ~1.000 ambiti operativi (DOT), scritti in italiano chiaro e univoco, diventano la lingua franca condivisa da Persone, Professionisti, PMI e Network per capirsi al volo senza ambiguità.
🔹 Micro-Blockchain Locale Offline: ogni avanzamento, metrica e certificato del tuo Profilo aggiornato viene sigillato localmente sul tuo database con una catena crittografica anti-manomissione a costo server zero.

🎯 IL VANTAGGIO CONCRETO DI QUESTA FUNZIONE PER TE:
👤 Se sei una Persona o un Talento: lavori anche in aereo o offline con risposta istantanea e con la certezza matematica che il tuo Profilo aggiornato resti solo sul tuo dispositivo.
🎓 Se sei un Professionista o Consulente (SME): parli finalmente lo stesso identico codice ("Esperanto") dei tuoi potenziali clienti sul nodo esatto della tua specializzazione.
🏢 Se sei un Imprenditore o una PMI: porti l'Intelligenza Artificiale in azienda azzerando i rischi sanzionatori di GDPR / EU AI Act e i canoni mensili dei servizi cloud.

🎁 LASCIA IL TUO FEEDBACK PER AVERE 1 ANNO+ GRATIS DA GENNAIO 2027
Vai su https://www.c-t-d.group/news.html : lascia il tuo parere sull'architettura 100% offline e iscriviti alla newsletter per bloccare il Programma Early Adopter!

Quanto pesa oggi nella tua azienda il timore di caricare dati sensibili su piattaforme AI in cloud? 👇

#ConnectTheDOTS #SerialKillerApp #EdgeAI #AIAct #GDPR #Sostenibilita #Gennaio2027"""
}
json.dump(data, open(db_file, "w"), ensure_ascii=False, indent=2)
