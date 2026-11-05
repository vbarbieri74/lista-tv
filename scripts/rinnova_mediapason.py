"""Rinnova i link con token dei canali Mediapason nella lista M3U.

Per ogni canale apre la pagina embed ufficiale di telelombardia.video,
legge il nuovo indirizzo .m3u8 (con token valido ~2 giorni) e lo
sostituisce nella lista. Esce con codice 1 se un canale non si trova.
"""
import re
import sys
import urllib.request

LISTA = "italia-ordinata.m3u"
EMBED = "https://telelombardia.video/video/embed?wv_id="
CANALI = {
    "Telelombardia": "RqhUo7mywPtkUqZ1z7ajlsiSmpejQtlcki5iAz3xs4xD7XtgisCo6VnH8be1-m7HrmTtFpmdxh3FWgnoAjwAbg",
    "Antenna 3 Lombardia": "RqhUo7mywPtkUqZ1z7ajllXbW21NWTl7OCLyPFyMX6rkqFrStKECO-3M_JMmc40mDGQU3cJ6o4uhPMIwwQPPRA",
    "Top Calcio 24": "RqhUo7mywPtkUqZ1z7ajlvUrX1AzopotJ0LHzPFTL06Shiyk0gNv8KVrB1LP9v4AfQyAwdNzcRGAjewOK1yO4A",
    "MilaNow": "RqhUo7mywPtkUqZ1z7ajllR7yIh96SCYf07t4WMWhF56Fv9tqLF41a0MEFiKwOm1KVHVC-gdy5rPCHTRWSfxNQ",
}
M3U8 = re.compile(r"https?://[^\"'\s<>\\]+/hls/([0-9A-F]+)/index\.m3u8\?hdnts=[^\"'\s<>\\]+")


def nuovo_link(wv_id):
    req = urllib.request.Request(EMBED + wv_id, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    m = M3U8.search(html)
    return (m.group(1), m.group(0)) if m else (None, None)


def main():
    testo = open(LISTA, encoding="utf-8").read()
    errori = 0
    for nome, wv_id in CANALI.items():
        try:
            chiave, url = nuovo_link(wv_id)
        except Exception as e:  # rete o pagina non disponibile
            chiave, url = None, None
            print(f"{nome}: errore {e}")
        if not url:
            print(f"{nome}: link non trovato")
            errori += 1
            continue
        vecchio = re.compile(r"https?://[^\s]+/hls/" + chiave + r"/index\.m3u8\?hdnts=[^\s]+")
        testo, n = vecchio.subn(url, testo)
        print(f"{nome}: aggiornato ({n})" if n else f"{nome}: voce non presente nella lista")
        errori += 0 if n else 1
    open(LISTA, "w", encoding="utf-8").write(testo)
    sys.exit(1 if errori else 0)


if __name__ == "__main__":
    main()
