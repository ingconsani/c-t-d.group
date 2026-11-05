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
center_txt(d, 62, 1100, "ANATOMIA DI UNA SERIAL KILLER APP • INNESCO #02", fnt(28), (255,255,255), 34)
d.ellipse([440, 175, 760, 455], fill=(255,255,255), outline=dk, width=8)
center_txt(d, 250, 290, "?", fnt(90), cr, 95)
center_txt(d, 355, 290, "ANGOLO CIECO", fnt(30), dk, 36)
y = center_txt(d, 505, 1020, "CHATGPT TI RISPONDE SOLO SE SAI GIA' QUALE DOMANDA FARE.", fnt(52), dk, 64)
d.line([(250, y+20), (950, y+20)], fill=cr, width=5)
center_txt(d, y+42, 1000, "Ma chi ti salva da cio' che 'Non sai di non sapere'?", fnt(34), cr, 44)
d.rectangle([24, 1035, 1176, 1176], fill=dk)
center_txt(d, 1060, 1100, "DOMANI ORE 08:15 LO STUDIO TECNICO QUI SU LINKEDIN", fnt(26), (245,197,24), 32)
center_txt(d, 1108, 1100, "Anteprima immediata (+ 1 Anno Gratis): www.c-t-d.group/news.html", fnt(25), (255,255,255), 32)
for folder in [assets, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_02.png")
for folder in [caroselli, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_02.pdf", "PDF", resolution=150.0)

db_file = f"{repo}/regia_posts.json"
data = json.load(open(db_file)) if os.path.exists(db_file) else {}
data["02"] = {
  "ep_title": "Cervello, Orizzonti e Triage Diagnostico Causale",
  "ta": "Connect the DOTS #02-A: Ciò Che Non Sai Di Non Sapere",
  "ba": """ChatGPT ti dà una risposta utile solo se sai già quale domanda fare.
Ma i disastri più gravi — nella vita e in azienda — nascono sempre da ciò che "non sai di non sapere".

Come fai a individuare un collo di bottiglia che non sai nemmeno di avere?

Domani mattina alle 08:15 mostro qui su LinkedIn il motore di Triage Causale di Connect the DOTS.
Chi vuole studiarlo subito in anteprima (e bloccare 1 Anno+ gratis da Gennaio 2027) lo trova qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #DecisionMaking""",
  "tb": "Connect the DOTS #02: Dal Non So Cosa Non So al DOT L3",
  "bb": """🔪 Anatomia di una Serial Killer App — Puntata #02: Come eliminare il "foglio bianco" dei chatbot e l'angolo cieco del "Non so cosa non so".
(Sfoglia il carosello per la Slide da 1.000 parole e la Timeline col Check Verde delle puntate pubblicate 👇).

Conosci il paradosso di ChatGPT e dei chatbot tradizionali? Per ottenere una risposta utile devi già sapere quale domanda fare. Ma nella vita professionale e in azienda i blocchi più costosi nascono quando:
1. "Non so cosa non so, finché qualcuno non me lo fa notare".
2. "Non so di cosa ho bisogno, finché qualcuno non mi presenta degli aiuti concreti".

Ecco cosa fai al volante di Connect the DOTS (in uscita a Gennaio 2027) in 60 secondi:

🔹 La Filosofia del Cervello (Punti 1 e 3): non puoi guardare fuori (Sinapsi) o agire (Pratica) finché non hai capito dove sei partendo dal Cervello — oppure cliccando su Orizzonti per selezionare direttamente un altro ambito strategico (L0) tra quelli presenti nel mazzo.
🔹 Qualificazione Causale (Punti 4 e 5): navighi tra circa 1.000 ambiti operativi (DOT) fino a isolare il tuo vero Problema radice (DOT L2).
🔹 Triage Diagnostico assistito (Punto 8): quando una domanda aperta non basta a isolare un vettore ad alta probabilità, il motore ti spiega la situazione e ti guida attraverso opzioni pre-confezionate dagli esperti di dominio (SME), affiancate sempre dalla voce "Altro" (con la raccomandazione di specificare la tua unicità). Senza mai ragionare per banale similarità statistica, ma per rigoroso nesso di causa-effetto, CtD accende in verde il nodo Soluzione esatto (DOT L3).

🎯 IL VANTAGGIO CONCRETO DI QUESTA FUNZIONE PER TE:
👤 Se sei una Persona o un Talento: trasformi un dubbio o un blocco confuso nella causa radice esatta e nella prima azione concreta da compiere, 100% offline.
🎓 Se sei un Professionista o Consulente (SME): i clienti arrivano da te avendo già qualificato il proprio bisogno sul nodo L3 in cui sei specialista, azzerando i tempi di pre-analisi.
🏢 Se sei un Imprenditore o una PMI: elimini le decisioni "di pancia" e le allucinazioni dei chatbot isolando in 3 minuti il vero collo di bottiglia operativo o finanziario.

🎁 LASCIA IL TUO FEEDBACK = 1 ANNO+ GRATIS DA GENNAIO 2027
Vai su https://www.c-t-d.group/news.html : dicci cosa ne pensi del Triage Causale insieme alla tua email per la newsletter e assicurati il Programma Early Adopter gratuito!

Qual è l'angolo cieco più pericoloso che hai visto scoprire troppo tardi in un progetto o in un'azienda? 👇

#ConnectTheDOTS #SerialKillerApp #ProblemSolving #DecisionMaking #CoachPrivato #PMI #Gennaio2027"""
}
json.dump(data, open(db_file, "w"), ensure_ascii=False, indent=2)
