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
center_txt(d, 62, 1100, "ANATOMIA DI UNA SERIAL KILLER APP • INNESCO #06", fnt(28), (255,255,255), 34)
d.ellipse([440, 175, 760, 455], fill=(255,255,255), outline=dk, width=8)
center_txt(d, 255, 290, "21 GIORNI", fnt(44), cr, 50)
center_txt(d, 330, 290, "PRATICA VERA", fnt(30), gr, 36)
y = center_txt(d, 505, 1020, "LA TEORIA SENZA 21 GIORNI DI PRATICA LASCIA TUTTO COM'ERA.", fnt(52), dk, 64)
d.line([(250, y+20), (950, y+20)], fill=cr, width=5)
center_txt(d, y+42, 1000, "Basta attestati di presenza: benvenuto Risultato Certificato.", fnt(34), cr, 44)
d.rectangle([24, 1035, 1176, 1176], fill=dk)
center_txt(d, 1060, 1100, "DOMANI ORE 08:15 LO STUDIO TECNICO QUI SU LINKEDIN", fnt(26), (245,197,24), 32)
center_txt(d, 1108, 1100, "Anteprima immediata (+ 1 Anno Gratis): www.c-t-d.group/news.html", fnt(25), (255,255,255), 32)
for folder in [assets, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_06.png")
for folder in [caroselli, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_06.pdf", "PDF", resolution=150.0)

db_file = f"{repo}/regia_posts.json"
data = json.load(open(db_file)) if os.path.exists(db_file) else {}
data["06"] = {
  "ep_title": "Allocazione a 3 Vie, Palestra di 21 Giorni e Certificato PoR",
  "ta": "Connect the DOTS #06-A: 21 Giorni di Pratica Certificata",
  "ba": """La formazione teorica senza 21 giorni di pratica lascia tutto esattamente com'era il venerdì prima.

Ecco perché in Connect the DOTS non contano i semplici attestati di partecipazione, ma i certificati crittografici di risultato reale (Proof-of-Result).

Domani mattina alle 08:15 mostro qui su LinkedIn come funzionano la Palestra di 21 Giorni e lo Smistamento a 3 Vie.
Chi vuole studiarli subito in anteprima (e bloccare 1 Anno+ gratis da Gennaio 2027) li trova qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #Palestra21Giorni #Meritocrazia""",
  "tb": "Connect the DOTS #06: Palestra 21 Giorni e PoR Multi-Sig",
  "bb": """🔪 Anatomia di una Serial Killer App — Puntata #06: Eliminare la formazione teorica senza pratica e i risultati autodichiarati.
(Sfoglia il carosello per la Slide da 1.000 parole e la Timeline col Check Verde delle puntate pubblicate 👇).

Quanti corsi di formazione o sessioni di consulenza restano sulla carta il lunedì mattina successivo perché manca un binario esecutivo quotidiano?

Quando apri un cantiere progettuale (L3) in Connect the DOTS (in uscita a Gennaio 2027), davanti a ogni mattone che separa il tuo stato attuale (P) dal tuo Traguardo (T) hai uno Smistamento Sovrano a 3 Vie (Punto 13 — affiancato sempre dall'opzione "Altro" con invito a specificare):

🔹 1ª Via — Fai-da-Te nella Palestra di 21 Giorni (Punto 14): ti alleni sul campo per 21 giorni operativi consecutivi finché la nuova competenza si trasforma in abitudine consolidata.
🔹 2ª Via — Esperto o Fornitore Qualificato (Vista 1): attivi su richiesta uno specialista di dominio (SME) o un fornitore già collegato a quello specifico mattone L3.
🔹 3ª Via — Rete Relazionale Fiducia (Vista 2): coinvolgi un contatto qualificato della tua rete personale o professionale.

E al termine dei 21 giorni? Scatta il Certificato di Risultato Reale (Proof-of-Result — Punti 15 e 16): uno scudo crittografico a doppia firma registrato sulla tua catena locale offline. Solo allora il parametro R (Risultati) della tua equazione S = C + P + T + R sale davvero.

🎯 IL VANTAGGIO CONCRETO DI QUESTA FUNZIONE PER TE:
👤 Se sei una Persona o un Giovane Talento: costruisci nel tuo Profilo aggiornato un portafoglio inoppugnabile di certificati su problemi reali risolti, molto più forte di un CV tradizionale.
🎓 Se sei un Professionista o Formatore: trasformi il tuo metodo in una Palestra pratica di 21 giorni che garantisce la messa a terra reale da parte del cliente.
🏢 Se sei un Imprenditore o una PMI: decidi mattone per mattone cosa eseguire internamente e cosa delegare all'esterno, premiando solo i risultati certificati.

🎁 PRENOTA 1 ANNO+ GRATIS DA GENNAIO 2027
Vai su https://www.c-t-d.group/news.html : lascia il tuo feedback sulla Palestra di 21 Giorni e iscriviti alla newsletter per assicurarti il Programma Early Adopter!

Quanta differenza fa, nella tua esperienza, avere una guida pratica per 21 giorni consecutivi rispetto a un corso teorico isolato? 👇

#ConnectTheDOTS #SerialKillerApp #Palestra21Giorni #ProofOfResult #Meritocrazia #Coaching #Gennaio2027"""
}
json.dump(data, open(db_file, "w"), ensure_ascii=False, indent=2)
