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
center_txt(d, 62, 1100, "ANATOMIA DI UNA SERIAL KILLER APP • INNESCO #08", fnt(28), (255,255,255), 34)
d.ellipse([440, 175, 760, 455], fill=(255,255,255), outline=dk, width=8)
center_txt(d, 255, 290, "1° -> 2° GRADO", fnt(36), cr, 44)
center_txt(d, 330, 290, "RISERVATO", fnt(32), gr, 38)
y = center_txt(d, 505, 1020, "COME CHIEDI AIUTO SENZA ESPORRE LE TUE DEBOLEZZE AGLI AMICI?", fnt(52), dk, 64)
d.line([(250, y+20), (950, y+20)], fill=cr, width=5)
center_txt(d, y+42, 1000, "Raggiungi il risolutore al 2° grado col 'Salto del 1° Grado'.", fnt(34), cr, 44)
d.rectangle([24, 1035, 1176, 1176], fill=dk)
center_txt(d, 1060, 1100, "DOMANI ORE 08:15 LO STUDIO TECNICO QUI SU LINKEDIN", fnt(26), (245,197,24), 32)
center_txt(d, 1108, 1100, "Anteprima immediata (+ 1 Anno Gratis): www.c-t-d.group/news.html", fnt(25), (255,255,255), 32)
for folder in [assets, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_08.png")
for folder in [caroselli, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_08.pdf", "PDF", resolution=150.0)

db_file = f"{repo}/regia_posts.json"
data = json.load(open(db_file)) if os.path.exists(db_file) else {}
data["08"] = {
  "ep_title": "Network Engineering: Score Ponte e 'Salto del 1° Grado'",
  "ta": "Connect the DOTS #08-A: Il Salto del 1° Grado Riservato",
  "ba": """Quando hai un problema delicato in azienda (rischio 10/10), l'ultima cosa che vuoi fare è confessarlo agli amici o ai contatti diretti di 1° grado.
Eppure la persona capace di risolverlo si trova quasi sempre al 2° grado (tra i contatti dei tuoi contatti).

Come ci arrivi senza mai esporre il tuo punto debole? Col "Salto del 1° Grado".

Domani mattina alle 08:15 mostro qui su LinkedIn come funziona l'Ingegneria Relazionale di Connect the DOTS.
Chi vuole studiarla subito in anteprima (e bloccare 1 Anno+ gratis da Gennaio 2027) la trova qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #Networking #Privacy""",
  "tb": "Connect the DOTS #08: Score Ponte e Salto del 1° Grado",
  "bb": """🔪 Anatomia di una Serial Killer App — Puntata #08: Eliminare l'imbarazzo di mostrare le proprie debolezze 10/10 agli amici o ai contatti diretti.
(Sfoglia il carosello per la Slide da 1.000 parole e la Timeline col Check Verde delle puntate pubblicate 👇).

Quando un imprenditore, un professionista o una persona individua una criticità delicata (Debolezza 10/10 e Minaccia 10/10), l'ultima cosa che desidera è telefonare al conoscente diretto dicendo: "Ho questo problema grave in azienda". Eppure lo specialista capace di risolverlo si trova quasi sempre al 2° grado, cioè tra i contatti dei propri contatti.

Ecco come il terzo sistema integrato di Connect the DOTS — Ingegneria Relazionale (Network Engineering, Punti 17..21 — in uscita a Gennaio 2027) — risolve questo paradosso:

🔹 Genealogia Relazionale (Punto 18): dentro il tuo Profilo aggiornato 100% offline, il sistema mappa nel tempo "chi ha presentato chi", valorizzando i legami fiduciari nati nei Capitoli professionali (come BNI) e nei network aziendali.
🔹 Calcolo Istantaneo in RAM di Score Diretto e Score Ponte (Punto 19): per ogni esigenza emersa nei tuoi cantieri (L3), il motore distingue in tempo reale chi può risolvere direttamente il problema (Score Diretto) da chi è il miglior tramite fiduciario per introdurti al 2° grado (Score Ponte).
🔹 Micro-Capsule da 1 KB e "Salto del 1° Grado" (Punti 20 e 21): tramite leggerissime capsule crittografate (scambiabili anche via codice QR), attivi un instradamento intelligente che permette al tuo contatto Ponte di metterti in comunicazione con il risolutore di 2° grado senza mai conoscere né vedere le tue debolezze 10/10.

🎯 IL VANTAGGIO CONCRETO DI QUESTA FUNZIONE PER TE:
👤 Se sei una Persona o un Talento: chiedi supporto su scelte delicate raggiungendo lo specialista di 2° grado attraverso la tua rete in totale riservatezza.
🎓 Se sei un Professionista o Membro di Network (es. BNI): valorizzi il tuo Score Ponte diventando lo snodo scientifico di segnalazioni qualificate ad altissima conversione.
🏢 Se sei un Imprenditore o una PMI: trovi fornitori, partner o manager per risolvere una criticità 10/10 senza che concorrenti o conoscenti diretti sappiano del tuo problema.

🎁 ASSICURATI 1 ANNO+ DI LICENZA GRATUITA DA GENNAIO 2027
Cosa ne pensi del "Salto del 1° Grado"? Scrivicelo su https://www.c-t-d.group/news.html (usando anche l'opzione "Altro" per specificare il tuo caso) insieme alla tua email per la newsletter!

Quante volte hai rinunciato a chiedere un'introduzione utile solo per non esporre un problema interno ai tuoi contatti diretti? 👇

#ConnectTheDOTS #SerialKillerApp #NetworkEngineering #BNI #BusinessMatching #Privacy #Gennaio2027"""
}
json.dump(data, open(db_file, "w"), ensure_ascii=False, indent=2)
