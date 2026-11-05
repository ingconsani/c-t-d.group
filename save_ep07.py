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
center_txt(d, 62, 1100, "ANATOMIA DI UNA SERIAL KILLER APP • INNESCO #07", fnt(28), (255,255,255), 34)
d.ellipse([440, 175, 760, 455], fill=(255,255,255), outline=dk, width=8)
center_txt(d, 255, 290, "R >> VERO", fnt(44), cr, 50)
center_txt(d, 330, 290, "PROVEN SME", fnt(32), gr, 38)
y = center_txt(d, 505, 1020, "SUI SOCIAL VINCE CHI URLA. SUL MERCATO CHI PORTA RISULTATI.", fnt(52), dk, 64)
d.line([(250, y+20), (950, y+20)], fill=cr, width=5)
center_txt(d, y+42, 1000, "Cordone Ombelicale di 21gg + Qualifica Proven SME sul campo.", fnt(34), cr, 44)
d.rectangle([24, 1035, 1176, 1176], fill=dk)
center_txt(d, 1060, 1100, "DOMANI ORE 08:15 LO STUDIO TECNICO QUI SU LINKEDIN", fnt(26), (245,197,24), 32)
center_txt(d, 1108, 1100, "Anteprima immediata (+ 1 Anno Gratis): www.c-t-d.group/news.html", fnt(25), (255,255,255), 32)
for folder in [assets, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_07.png")
for folder in [caroselli, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_07.pdf", "PDF", resolution=150.0)

db_file = f"{repo}/regia_posts.json"
data = json.load(open(db_file)) if os.path.exists(db_file) else {}
data["07"] = {
  "ep_title": "Cordone Ombelicale 21gg e Qualifica Proven SME (R>>) NEXUS",
  "ta": "Connect the DOTS #07-A: La Fine dei Finti Guru Social",
  "ba": """Sui social tradizionali vince chi urla più forte o compra più visibilità.
Nel mercato reale dovrebbe vincere chi porta risultati concreti e verificabili ai propri clienti.

E se fossero i tuoi risultati certificati sul campo a portarti nuovi incarichi su richiesta (senza chiamate a freddo)?

Domani mattina alle 08:15 mostro qui su LinkedIn come funzionano il "Cordone Ombelicale" di 21 giorni e la qualifica meritocratica a Proven SME.
Chi vuole studiarli subito in anteprima (e bloccare 1 Anno+ gratis da Gennaio 2027) li trova qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #Consulenza #Meritocrazia""",
  "tb": "Connect the DOTS #07: Cordone Ombelicale e Proven SME",
  "bb": """🔪 Anatomia di una Serial Killer App — Puntata #07: Eliminare i finti guru da tastiera e l'abbandono del cliente dopo la consulenza.
(Sfoglia il carosello per la Slide da 1.000 parole e la Timeline col Check Verde delle puntate pubblicate 👇).

Sui social tradizionali vince chi urla più forte, anche se non ha mai risolto un caso reale in azienda. E per i professionisti seri c'è un secondo problema cronico: finita la sessione di consulenza o formazione, il cliente torna in ufficio travolto dalle urgenze quotidiane e il legame operativo si spezza.

A Gennaio 2027 Connect the DOTS eliminerà entrambe queste distorsioni (Punti 14, 15, 20 e 24):

1️⃣ Il "Cordone Ombelicale" di 21 Giorni coi tuoi migliori clienti (Punto 14): il professionista o advisor (ad esempio membro di un Capitolo BNI o consulente direzionale) condivide la Palestra pratica di 21 giorni con i propri clienti chiave. Li accompagna passo dopo passo nella messa a terra quotidiana del cantiere progettuale (L3), blindando il risultato e la fidelizzazione nel tempo.
2️⃣ Qualifica Meritocratica a "Proven SME" (Esperto Verificato sul Campo — Punti 15 e 20): ogni volta che un cantiere si chiude con successo certificato nel tuo Profilo aggiornato 100% offline, il parametro R (Risultati) della tua equazione S = C + P + T + R cresce. Quando raggiungi un livello di eccellenza dimostrato (R >>) su uno specifico ambito operativo (DOT), il sistema ti qualifica come Proven SME.
3️⃣ Cooptazione su Richiesta tramite NEXUS (Punto 24): con il tuo consenso scritto, invii la qualifica R >> all'amministrazione di CtD che, dopo verifica tramite il nodo di coordinamento NEXUS, ti inserisce nella lista degli specialisti attivabili su richiesta (in modalità Pull) da chi ha aperto un cantiere esattamente su quel problema.

🎯 IL VANTAGGIO CONCRETO DI QUESTA FUNZIONE PER TE:
👤 Se sei una Persona o un Talento emergente: anche senza budget pubblicitario, se eccelli nella risoluzione pratica di un problema (R >>) vieni valorizzato e reso visibile a chi cerca quella competenza.
🎓 Se sei un Professionista o Consulente: fidelizzi i tuoi clienti attuali col Cordone Ombelicale di 21 giorni e ricevi nuovi incarichi qualificati in modalità Pull sugli ambiti in cui hai dimostrato risultati reali.
🏢 Se sei un Imprenditore o una PMI: quando ti serve uno specialista esterno su un mattone critico (anche specificando esigenze particolari con l'opzione "Altro"), selezioni chi ha già dimostrato risultati certificati sul campo.

🎁 LASCIA IL TUO FEEDBACK PER AVERE 1 ANNO+ GRATIS DA GENNAIO 2027
Vai su https://www.c-t-d.group/news.html : inviaci il tuo parere sul meccanismo meritocratico R >> e iscriviti alla newsletter per assicurarti il Programma Early Adopter!

Quanto cambierebbe il tuo lavoro se i clienti potessero scegliere i consulenti in base ai risultati reali certificati invece che agli slogan pubblicitari? 👇

#ConnectTheDOTS #SerialKillerApp #ProvenSME #Consulenza #ProfessionalServices #Meritocrazia #Gennaio2027"""
}
json.dump(data, open(db_file, "w"), ensure_ascii=False, indent=2)
