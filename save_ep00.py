import os, json
from PIL import Image, ImageDraw, ImageFont

repo = "/Users/ingconsani/Development/c-t-d.group"
assets, caroselli = f"{repo}/assets", f"{repo}/assets/caroselli"
desktop = "/Users/ingconsani/Desktop/CtD_LinkedIn_Caroselli_PDF"
os.makedirs(caroselli, exist_ok=True); os.makedirs(desktop, exist_ok=True)

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
center_txt(d, 62, 1100, "ANATOMIA DI UNA SERIAL KILLER APP • INNESCO #00", fnt(28), (255,255,255), 34)
d.ellipse([440, 175, 760, 455], fill=(255,255,255), outline=dk, width=8)
center_txt(d, 275, 290, "ZERO CLOUD", fnt(38), cr, 46)
center_txt(d, 325, 290, "100% OFFLINE", fnt(34), dk, 42)
y = center_txt(d, 505, 1020, "NON E' UN'APP. E' LA PRIMA 'APP-NON-APP' (CON AI 100% OFFLINE).", fnt(52), dk, 64)
d.line([(250, y+20), (950, y+20)], fill=cr, width=5)
center_txt(d, y+42, 1000, "24 Funzioni Brevettate • Zero Cloud • Per Persone e Aziende.", fnt(34), cr, 44)
d.rectangle([24, 1035, 1176, 1176], fill=dk)
center_txt(d, 1060, 1100, "DOMANI ORE 08:15 IL TRAILER COMPLETO QUI SU LINKEDIN", fnt(26), (245,197,24), 32)
center_txt(d, 1108, 1100, "Anteprima immediata (+ 1 Anno Gratis): www.c-t-d.group/news.html", fnt(25), (255,255,255), 32)
for folder in [assets, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_00.png")
for folder in [caroselli, desktop]: im.save(f"{folder}/Ancora_LinkedIn_Puntata_00.pdf", "PDF", resolution=150.0)

db_file = f"{repo}/regia_posts.json"
data = json.load(open(db_file)) if os.path.exists(db_file) else {}
data["00"] = {
  "ep_title": "IL TRAILER: Come raccontare la prima 'App-non-App'?",
  "ta": "Connect the DOTS #00-A: La Prima App-non-App (Offline)",
  "ba": """24 funzioni brevettate.
Intelligenza Artificiale estesa, ma 100% offline.
Zero cloud. Zero canoni server.

Non è un'app. È la prima "App-non-App" (per Persone, Professionisti e Aziende).
Spiegarla in un post normale era impossibile: per questo parte la serie "Anatomia di una Serial Killer App".

Domani mattina alle 08:15 esce il Trailer completo qui su LinkedIn.
Chi vuole vederlo subito in anteprima (e bloccare 1 Anno+ gratis da Gennaio 2027) lo trova già aperto qui:
👉 https://www.c-t-d.group/news.html#news-ep-00

#ConnectTheDOTS #SerialKillerApp #AppNonApp""",
  "tb": "Connect the DOTS #00: Anatomia di una Serial Killer App",
  "bb": """Come si presenta al mercato la prima "App-non-App" che non è mai esistita prima?
Quando abbiamo provato a spiegare Connect the DOTS (in uscita a Gennaio 2027) con un post tradizionale, ci siamo accorti che era impossibile.
Ecco perché parte "Anatomia di una Serial Killer App" (sfoglia le 2 slide del Trailer qui sotto 👇).

Quando qualche mese fa la Ferrari ha svelato la sua prima vettura elettrica, la Luce, chi si è fermato alle prime foto statiche cercava i vecchi schemi del motore termico. Chi invece si è seduto al volante ha scoperto dieci auto diverse in una sola piattaforma.

Con Connect the DOTS (CtD) ci siamo trovati davanti allo stesso dilemma comunicativo:

🔹 Uso esteso dell'Intelligenza Artificiale, ma 100% OFFLINE sul tuo Mac, PC o smartphone, unendo l'AI al sapere umano degli esperti di dominio (SME) dentro il tuo Profilo aggiornato a costo server zero.
🔹 24 componenti brevettati riuniti in 3 Sistemi integrati (3 Systems in 1 Platform): Diagnosi Strategica (formula S = C + P + T + R e SWOT istantanea in RAM), Secondo Cervello esecutivo (Palestra pratica di 21 Giorni con risultati certificati) e Sviluppo Relazionale in modalità Pull (senza chiamate a freddo).
🔹 Progettata contemporaneamente sia per le Persone e i Talenti (mondo P) sia per Professionisti, Consulenti, Imprenditori, PMI e Network aziendali (mondo B), facendoli dialogare attraverso una lingua comune ("Esperanto") di circa 1.000 ambiti operativi (DOT).
🔹 Nativamente conforme a EU AI Act e GDPR, con Scudo di Anonimizzazione AI automatico sulle domande libere, inquadramento del Regime Fiscale iniziale e registro crittografico locale.

Come raccontare tutto questo senza scrivere un manuale di 200 pagine?

Con questa serie aperta di puntate:
1️⃣ Ogni episodio ti siede al volante di 1 singola funzione che "elimina" una vecchia illusione del digitale o della consulenza (chatbot generici, SWOT dimenticate nei PDF, finti guru, networking a freddo).
2️⃣ Ogni uscita ha 1 Slide che vale 1.000 parole + il vantaggio concreto per Persona, Professionista e Imprenditore/PMI.
3️⃣ Nella Slide 2 trovi la Timeline progressiva col Check Verde e su https://www.c-t-d.group/news.html#news-ep-00 leggi le puntate come News.

🎯 COSA SCOPRIRAI IN OGNI PUNTATA PER IL TUO PROFILO:
👤 Persona o Talento: Coach privato offline, Tasto Pausa ('0') contro il sovraccarico e Palestra di 21 giorni.
🎓 Professionista o Consulente: affiancamento di 21 giorni coi migliori clienti e visibilità basata sui risultati reali certificati.
🏢 Imprenditore, PMI o Rete: SWOT predittiva in RAM oltre il solo fatturato, ricerca riservata di partner al 2° grado e scambio di crediti B2B.

🎁 IL TUO FEEDBACK VALE 1 ANNO+ DI LICENZA GRATUITA DA GENNAIO 2027
Vai su https://www.c-t-d.group/news.html#news-ep-00 : lasciando un feedback sulle funzioni (anche usando l'opzione "Altro" per specificare la tua realtà) e la tua email per la newsletter, ti assicuri l'uso gratuito per un anno o più nel Programma Early Adopter di Gennaio 2027!

Quale "falsa promessa" del digitale o della consulenza vorresti veder eliminata per prima? 👇

#ConnectTheDOTS #SerialKillerApp #AppNonApp #3SystemsInOnePlatform #EdgeAI #AIAct #GDPR #Gennaio2027"""
}
json.dump(data, open(db_file, "w"), ensure_ascii=False, indent=2)

def col(hdr, col_b, img, pdf, tid, tval, bid, bval):
    return f"""<div style="background:#0e0e14;border:2px solid {col_b};border-radius:12px;padding:16px;">
    <div style="background:{col_b};color:#000;padding:7px 12px;border-radius:6px;font-weight:800;margin-bottom:12px;">{hdr}</div>
    <div style="display:grid;grid-template-columns:145px 1fr;gap:12px;margin-bottom:12px;align-items:center;">
      <img src="assets/{img}" style="width:100%;border-radius:6px;border:1px solid {col_b};">
      <div><code style="color:#f5c518;font-size:0.8rem;">{pdf}</code>
        <a href="assets/caroselli/{pdf}" download="{pdf}" style="display:block;margin-top:8px;padding:8px;background:#1e293b;color:#38bdf8;border:1px solid #38bdf8;border-radius:6px;text-align:center;text-decoration:none;font-weight:800;font-size:0.82rem;">📥 Scarica / Salva {pdf}</a>
        <a href="https://www.linkedin.com/sharing/compose" target="_blank" style="display:block;margin-top:6px;padding:8px;background:#0a66c2;color:#fff;border-radius:6px;text-align:center;text-decoration:none;font-weight:800;font-size:0.82rem;">🚀 Apri Finestra Post LinkedIn</a>
      </div>
    </div>
    <div style="margin-bottom:10px;"><span id="c-{tid}" style="font-size:0.78rem;color:#3cd070;font-weight:800;">🟢 {len(tval)}/58 caratteri (OK)</span>
      <div style="display:flex;gap:6px;margin-top:4px;"><input id="i-{tid}" value="{tval}" maxlength="58" oninput="cnt('{tid}',58)" style="flex:1;padding:8px;background:#16161f;color:#fff;border:1px solid #444;border-radius:6px;font-weight:700;">
      <button onclick="cp('{tid}',this,58)" style="background:#f5c518;color:#000;border:none;padding:8px 12px;border-radius:6px;font-weight:800;cursor:pointer;">📋 1. Copia Titolo PDF</button></div>
    </div>
    <div><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
      <span id="c-{bid}" style="font-size:0.78rem;color:#3cd070;font-weight:800;">🟢 {len(bval)}/3000 car. (Margine: +{3000-len(bval)})</span>
      <button onclick="cp('{bid}',this,3000)" style="background:#38bdf8;color:#000;border:none;padding:8px 12px;border-radius:6px;font-weight:800;cursor:pointer;">📋 2. Copia Testo Post (Cmd+V su LinkedIn)</button></div>
      <textarea id="i-{bid}" rows="14" oninput="cnt('{bid}',3000)" style="width:100%;padding:10px;background:#16161f;color:#fff;border:1px solid #444;border-radius:6px;box-sizing:border-box;font-family:inherit;line-height:1.45;">{bval}</textarea>
    </div></div>"""

cards = ""
for k in sorted(data.keys()):
    ep = data[k]
    c1 = col(f"🎯 STREAM 1 (08:15) — ANCORA LAPIDARIA #{k}-A", "#f5c518", f"Ancora_LinkedIn_Puntata_{k}.png", f"Ancora_LinkedIn_Puntata_{k}.pdf", f"ta-{k}", ep["ta"], f"ba-{k}", ep["ba"])
    c2 = col(f"📘 STREAM 2 (08:15) — STUDIO MASTER #{k}-B", "#38bdf8", f"news_ep_{k}.png", f"Carosello_LinkedIn_Puntata_{k}.pdf", f"tb-{k}", ep["tb"], f"bb-{k}", ep["bb"])
    cards += f'<div id="ep-{k}" style="background:#141419;border:1px solid #333;border-radius:14px;padding:20px;margin-bottom:28px;"><h2 style="margin:0 0 14px 0;color:#fff;">Puntata #{k} — {ep["ep_title"]}</h2><div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;">{c1}{c2}</div></div>'

open(f"{repo}/regia_linkedin.html", "w", encoding="utf-8").write(f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Regia LinkedIn CtD</title></head>
<body style="background:#0a0a0d;color:#fff;font-family:-apple-system,sans-serif;margin:0;padding:20px;">
<h2 style="color:#f5c518;text-align:center;margin-top:0;">🎬 CABINA DI REGIA LINKEDIN — COPPIE VALIDATE DC&QA</h2>
<div style="max-width:1360px;margin:0 auto;">{cards}</div>
<script>
function cnt(id,lim){{var l=document.getElementById('i-'+id).value.length,d=lim-l,c=document.getElementById('c-'+id);c.innerText=(d>=0?'🟢 '+l+'/'+lim+' (Margine: +'+d+')':'🔴 SFORAMENTO '+d);c.style.color=d>=0?'#3cd070':'#ef4444';}}
function cp(id,btn,lim){{var v=document.getElementById('i-'+id).value;if(v.length>lim){{alert('Supera il limite di '+(v.length-lim)+' caratteri!');return;}}navigator.clipboard.writeText(v).then(function(){{var o=btn.innerText;btn.innerText='✅ COPIATO! Premi Cmd+V';setTimeout(function(){{btn.innerText=o;}},2500);}});}}
</script></body></html>""")
print("OK: Coppia #00 salvata e pronta!")
