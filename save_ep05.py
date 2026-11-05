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
center_txt(d, 62, 1100, "ANATOMIA DI UNA SERIAL KILLER APP • INNESCO #05", fnt(28), (255,255,255), 34)
d.ellipse([440, 175, 760, 455], fill=(255,255,255), outline=dk, width=8)
center_txt(d, 265, 290, "TO-DO", fnt(48), dk, 54)
d.line([(505, 290), (695, 290)], fill=cr, width=8)
center_txt(d, 335, 290, "-> CANTIERE", fnt(32), gr, 38)
y = center_txt(d, 505, 1020, "LE LISTE DI 'TO-DO' SONO IL CIMITERO DEI BUONI PROPOSITI.", fnt(52), dk, 64)
d.line([(250, y+20), (950, y+20)], fill=cr, width=5)
center_txt(d, y+42, 1000, "Trasforma ogni appunto in un cantiere L3 collegato alla strategia.", fnt(34), cr, 44)
d.rectangle([24, 1035, 1176, 1176], fill=dk)
center_txt(d, 1060, 1100, "DOMANI ORE 08:15 LO STUDIO TECNICO QUI SU LINKEDIN", fnt(26), (245,197,24), 32)
center_txt(d, 1108, 1100, "Anteprima immediata (+ 1 Anno Gratis): www.c-t-d.group/news.html", fnt(25), (255,255,255), 32)
for folder in [assets, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_05.png")
for folder in [caroselli, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_05.pdf", "PDF", resolution=150.0)

db_file = f"{repo}/regia_posts.json"
data = json.load(open(db_file)) if os.path.exists(db_file) else {}
data["05"] = {
  "ep_title": "2° Cervello: Proliferazione To-Do -> L3 Progetto & Sinapsi",
  "ta": "Connect the DOTS #05-A: Il Cimitero delle Liste To-Do",
  "ba": """Le liste di "To-Do" sono il cimitero dei buoni propositi.
Segni un'idea o un'urgenza oggi, e dopo tre giorni hai già perso il legame con l'obiettivo strategico che l'aveva generata.

Come si trasforma un semplice appunto in un cantiere esecutivo che arriva fino in fondo?

Domani mattina alle 08:15 mostro qui su LinkedIn come funziona il Secondo Cervello di Connect the DOTS.
Chi vuole studiarlo subito in anteprima (e bloccare 1 Anno+ gratis da Gennaio 2027) lo trova qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #SecondoCervello #Execution""",
  "tb": "Connect the DOTS #05: 2° Cervello, To-Do e Cantieri L3",
  "bb": """🔪 Anatomia di una Serial Killer App — Puntata #05: Eliminare il cimitero delle liste "To-Do" scollegate dalla strategia.
(Sfoglia il carosello per la Slide da 1.000 parole e la Timeline col Check Verde delle puntate pubblicate 👇).

Quante volte hai annotato un'idea brillante o un'azione urgente su un'app di note, perdendo dopo tre giorni il legame con l'obiettivo strategico che l'aveva generata?

Oggi entriamo nel secondo sistema integrato di Connect the DOTS — il Secondo Cervello Esecutivo (Punti 9..12 — in uscita a Gennaio 2027):

1️⃣ Proliferazione Progettuale (da Compito o Idea a Cantiere L3): non appena decidi di affrontare un'attività o di far evolvere una tua Idea in un Traguardo (Goal), CtD la trasforma automaticamente in un cantiere strutturato, mantenendo intatta la gerarchia verticale con l'obiettivo padre che la raggruppa.
2️⃣ Sinapsi Orizzontali Bidirezionali: mentre la gerarchia verticale tiene ordine nella struttura, CtD crea un collegamento logico bidirezionale (Sinapsi personalizzata) tra i tuoi nodi allo stesso livello — ad esempio tra un'Idea e il Traguardo che ne è nato, o tra un Compito e una Routine — tracciando l'intero flusso di lavoro senza mai alterare l'albero maestro.
3️⃣ I Mattoni Operativi sul Nodo Soluzione (L3): sotto ogni cantiere trovi già scomposti i passi pratici che separano il tuo stato attuale (P) dal tuo traguardo (T), aiutandoti a passare dalla teoria alla pratica senza mai standardizzare i tuoi fini.

🎯 IL VANTAGGIO CONCRETO DI QUESTA FUNZIONE PER TE:
👤 Se sei una Persona o un Talento: non perdi mai più il filo tra un'intuizione annotata al volo, le tue routine quotidiane e il traguardo di vita a cui servono.
🎓 Se sei un Professionista, Coach o Consulente: consegni ai tuoi clienti non un documento teorico, ma un cantiere L3 già scomposto in mattoni esecutivi pronti da mettere a terra.
🏢 Se sei un Imprenditore o una PMI: colleghi ogni singolo compito operativo del team all'obiettivo strategico aziendale, azzerando la dispersione.

🎁 ASSICURATI 1 ANNO+ DI LICENZA GRATUITA DA GENNAIO 2027
Vai su https://www.c-t-d.group/news.html : lascia il tuo feedback sul Secondo Cervello insieme alla tua email per la newsletter e blocca il Programma Early Adopter!

Qual è la percentuale di idee o compiti che oggi si perdono per strada tra i tuoi appunti e l'esecuzione reale? 👇

#ConnectTheDOTS #SerialKillerApp #SecondoCervello #Execution #ProjectManagement #PMI #Gennaio2027"""
}
json.dump(data, open(db_file, "w"), ensure_ascii=False, indent=2)
