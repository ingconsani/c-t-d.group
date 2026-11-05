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
center_txt(d, 62, 1100, "ANATOMIA DI UNA SERIAL KILLER APP • INNESCO #03", fnt(28), (255,255,255), 34)
d.ellipse([440, 175, 760, 455], fill=(255,255,255), outline=dk, width=8)
d.rounded_rectangle([535, 235, 580, 345], radius=8, fill=cr)
d.rounded_rectangle([620, 235, 665, 345], radius=8, fill=cr)
center_txt(d, 365, 290, "TASTO PAUSA", fnt(30), dk, 36)
y = center_txt(d, 505, 1020, "IN AZIENDA CIO' CHE IGNORI NON VALE ZERO: VALE RISCHIO 10/10.", fnt(52), dk, 64)
d.line([(250, y+20), (950, y+20)], fill=cr, width=5)
center_txt(d, y+42, 1000, "Hai mai visto una SWOT in RAM con il tasto sovrano 'Pausa'?", fnt(34), cr, 44)
d.rectangle([24, 1035, 1176, 1176], fill=dk)
center_txt(d, 1060, 1100, "DOMANI ORE 08:15 LO STUDIO TECNICO QUI SU LINKEDIN", fnt(26), (245,197,24), 32)
center_txt(d, 1108, 1100, "Anteprima immediata (+ 1 Anno Gratis): www.c-t-d.group/news.html", fnt(25), (255,255,255), 32)
for folder in [assets, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_03.png")
for folder in [caroselli, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_03.pdf", "PDF", resolution=150.0)

db_file = f"{repo}/regia_posts.json"
data = json.load(open(db_file)) if os.path.exists(db_file) else {}
data["03"] = {
  "ep_title": "SWOT in RAM (Ignoto = 10/10) e il Tasto Sovrano 'Pausa'",
  "ta": "Connect the DOTS #03-A: Il Cruscotto col Tasto Pausa",
  "ba": """In azienda ciò che ignori non vale zero.
Vale Rischio Massimo (10/10).

Ma se provi a tenere sotto controllo cento fronti contemporaneamente, finisci paralizzato.
A meno che il tuo cruscotto direzionale non abbia il tasto sovrano "Pausa".

Domani mattina alle 08:15 mostro qui su LinkedIn come funziona la SWOT predittiva in RAM di Connect the DOTS.
Chi vuole studiarla subito in anteprima (e bloccare 1 Anno+ gratis da Gennaio 2027) la trova qui:
👉 https://www.c-t-d.group/news.html

#ConnectTheDOTS #SerialKillerApp #SWOT #Imprenditori""",
  "tb": "Connect the DOTS #03: SWOT in RAM (10/10) e Tasto Pausa",
  "bb": """🔪 Anatomia di una Serial Killer App — Puntata #03: La fine delle analisi SWOT dimenticate nei PDF e dei cruscotti che guardano solo il fatturato.
(Sfoglia il carosello per la Slide da 1.000 parole e la Timeline col Check Verde delle puntate pubblicate 👇).

Nella gestione tradizionale, ciò che non conosciamo o non monitoriamo viene ignorato: nei fogli di calcolo vale zero. Finché un giorno quell'angolo cieco esplode.

Se oggi stessi usando il tuo Profilo aggiornato in Connect the DOTS (in uscita a Gennaio 2027), vedresti l'algoritmo di auto-guarigione ricalcolare istantaneamente la tua SWOT direttamente in memoria RAM (evitando i dati grezzi non consolidati su disco):

1️⃣ L'ignoto vale Rischio Massimo (10/10): quando un nodo non è conosciuto o non è stato intenzionalmente escluso, CtD lo considera automaticamente una Debolezza (10/10) e una Minaccia (10/10), riflettendo visivamente questi valori con gli stessi colori usati per i 4 segmenti del nodo.
2️⃣ Il Tasto Sovrano "Pausa" ('0'): per non farti travolgere dall'ansia di dover presidiare tutto subito, ti basta premere il pulsante Pausa sui nodi che scegli consapevolmente di rimandare. I valori si resettano istantaneamente a '0' e il nodo non viene considerato in alcun calcolo matematico, regalandoti il lusso di dedicare tempo di qualità solo alle tue vere priorità.
3️⃣ Oltre il Fatturato + Regime Fiscale + Scudo AI: fin dall'input dei dati iniziali CtD richiede la preferenza del tuo Regime Fiscale, governa non solo il fatturato ma qualsiasi altra informazione strategica o personale nella formula S = C + P + T + R, e identifica e anonimizza in automatico ogni dato sensibile nelle tue domande a testo libero all'AI.

🎯 IL VANTAGGIO CONCRETO DI QUESTA FUNZIONE PER TE:
👤 Se sei una Persona o un Talento: azzeri il sovraccarico mentale spegnendo col tasto Pausa ciò che oggi non puoi seguire, concentrandoti su un solo obiettivo alla volta.
🎓 Se sei un Professionista, Commercialista o Advisor: offri ai tuoi clienti stress test e cruscotti predittivi in RAM su oltre 400 lenti direzionali.
🏢 Se sei un Imprenditore o una PMI: vedi in tempo reale dove si annidano le minacce 10/10 nei tuoi 8 orizzonti aziendali senza che un solo byte esca dal tuo Mac o PC.

🎁 BLOCCA 1 ANNO+ DI LICENZA GRATUITA DA GENNAIO 2027
Quali ambiti metteresti subito in "Pausa" e quali accenderesti? Scrivicelo su https://www.c-t-d.group/news.html insieme alla tua email per la newsletter!

#ConnectTheDOTS #SerialKillerApp #SWOT #ControlloDiGestione #CFO #Imprenditori #Gennaio2027"""
}
json.dump(data, open(db_file, "w"), ensure_ascii=False, indent=2)
