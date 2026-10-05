"""Filigrana uguale per tutti + PDF cifrato (AES-256) con divieto di stampa, copia e modifica.
Si apre senza password; la password del proprietario (serve solo a togliere i blocchi) la tiene Fabrizio
e non va scritta nel repository.
uso: python3 proteggi.py <input.pdf> <output.pdf> <password_proprietario>"""
import sys, math, pymupdf
src, dst, owner = sys.argv[1], sys.argv[2], sys.argv[3]
TXT = 'Fabrizio Fiorucci · vietata la duplicazione'
doc = pymupdf.open(src)
font = pymupdf.Font('helv')
for page in doc:
    W, H = page.rect.width, page.rect.height
    size = W / 40
    tw = font.text_length(TXT, fontsize=size)
    ang = math.degrees(math.atan2(H, W))          # lungo la diagonale
    # una sola riga lungo la diagonale, molto leggera
    for off in (0,):
        cx, cy = W / 2 + off, H / 2
        shape = page.new_shape()
        p0 = pymupdf.Point(cx, cy)
        shape.insert_text(pymupdf.Point(cx - tw / 2, cy + size / 3), TXT, fontsize=size, fontname='helv',
                          color=(0.5, 0.55, 0.6), fill_opacity=0.045, morph=(p0, pymupdf.Matrix(-ang)))
        shape.commit(overlay=True)
    # avviso fisso in basso a destra, più leggibile
    note = 'La proprietà intellettuale di questo documento è di Fabrizio Fiorucci, ne sono proibite la divulgazione e la duplicazione'
    page.insert_text((W - font.text_length(note, fontsize=W/120) - W*0.02, H - H*0.015), note,
                     fontsize=W / 120, fontname='helv', color=(0.37, 0.43, 0.51), fill_opacity=0.8)
doc.set_metadata({**doc.metadata, 'author': 'Fabrizio Fiorucci', 'title': doc.metadata.get('title') or src.rsplit('/',1)[-1][:-4],
                  'subject': 'La proprietà intellettuale di questo documento è di Fabrizio Fiorucci, ne sono proibite la divulgazione e la duplicazione', 'keywords': '© Fabrizio Fiorucci, tutti i diritti riservati'})
perm = pymupdf.PDF_PERM_ACCESSIBILITY   # solo lettura per gli screen reader: niente stampa, copia, modifica, annotazioni
doc.save(dst, encryption=pymupdf.PDF_ENCRYPT_AES_256, owner_pw=owner, user_pw='', permissions=perm, garbage=3, deflate=True)
print('ok', dst)
