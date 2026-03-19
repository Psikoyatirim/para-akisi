import warnings
warnings.filterwarnings("ignore")

import yfinance as yf
import pandas as pd
import requests
import time
import os
from datetime import datetime

# ================= TELEGRAM =================
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8035211094:AAEqHt4ZosBJsuT1FxdCcTR9p9uJ1O073zY')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '-1002715468798')

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=15)
        if r.status_code == 200:
            print("📤 Telegram gönderildi", flush=True)
        else:
            print(f"⚠️ Telegram hatası: {r.status_code}", flush=True)
    except Exception as e:
        print(f"⚠️ Telegram hatası: {e}", flush=True)

def send_parcali(baslik, liste, parca_basina=40):
    if not liste:
        return
    for i in range(0, len(liste), parca_basina):
        parca = liste[i:i + parca_basina]
        toplam = (len(liste) + parca_basina - 1) // parca_basina
        no = (i // parca_basina) + 1
        ek = f" ({no}/{toplam})" if toplam > 1 else ""
        msg = f"{baslik}{ek}\n" + "  ".join(parca)
        send_telegram(msg)
        time.sleep(0.5)

# ================= SEMBOLLER =================
SYMBOLS = [
    "A1CAP.IS", "ACSEL.IS", "ADEL.IS", "ADESE.IS", "ADGYO.IS",
    "AEFES.IS", "AFYON.IS", "AGESA.IS", "AGHOL.IS", "AGROT.IS",
    "AGYO.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS", "AKENR.IS",
    "AKFGY.IS", "AKFIS.IS", "AKFYE.IS", "AKGRT.IS", "AKMGY.IS",
    "AKSA.IS", "AKSEN.IS", "AKSGY.IS", "AKSUE.IS", "AKYHO.IS",
    "ALARK.IS", "ALBRK.IS", "ALCAR.IS", "ALCTL.IS", "ALFAS.IS",
    "ALGYO.IS", "ALKA.IS", "ALKIM.IS", "ALKLC.IS", "ALTNY.IS",
    "ALVES.IS", "ANELE.IS", "ANGEN.IS", "ANHYT.IS", "ANSGR.IS",
    "ARCLK.IS", "ARDYZ.IS", "ARENA.IS", "ARSAN.IS", "ARTMS.IS",
    "ARZUM.IS", "ASELS.IS", "ASGYO.IS", "ASTOR.IS", "ASUZU.IS",
    "ATAGY.IS", "ATAKP.IS", "ATATP.IS", "ATEKS.IS", "ATLAS.IS",
    "AVGYO.IS", "AVHOL.IS", "AVOD.IS", "AVTUR.IS", "AYDEM.IS",
    "AYES.IS", "AYGAZ.IS", "AZTEK.IS", "BAGFS.IS", "BAKAB.IS",
    "BALAT.IS", "BALSU.IS", "BANVT.IS", "BASCM.IS", "BAYRK.IS",
    "BEGYO.IS", "BERA.IS", "BESLR.IS", "BEYAZ.IS", "BFREN.IS",
    "BIMAS.IS", "BIGTK.IS", "BIOEN.IS", "BIZIM.IS", "BJKAS.IS",
    "BLCYT.IS", "BMSTL.IS", "BNTAS.IS", "BORLS.IS", "BORSK.IS",
    "BOSSA.IS", "BRISA.IS", "BRKO.IS", "BRKSN.IS", "BRSAN.IS",
    "BRYAT.IS", "BSOKE.IS", "BTCIM.IS", "BUCIM.IS", "BURCE.IS",
    "BURVA.IS", "BVSAN.IS", "CANTE.IS", "CASA.IS", "CCOLA.IS",
    "CELHA.IS", "CEMAS.IS", "CEMTS.IS", "CIMSA.IS", "CLEBI.IS",
    "CMENT.IS", "COSMO.IS", "CRDFA.IS", "CRFSA.IS", "CUSAN.IS",
    "CWENE.IS", "DAGI.IS", "DARDL.IS", "DENGE.IS", "DERIM.IS",
    "DESA.IS", "DESPC.IS", "DEVA.IS", "DGGYO.IS", "DITAS.IS",
    "DMRGD.IS", "DMSAS.IS", "DOAS.IS", "DOCO.IS", "DOFER.IS",
    "DOGUB.IS", "DOHOL.IS", "DOKTA.IS", "DUNYH.IS", "DYOBY.IS",
    "DZGYO.IS", "EBEBK.IS", "ECILC.IS", "ECZYT.IS", "EDIP.IS",
    "EGEEN.IS", "EGEGY.IS", "EGEPO.IS", "EGGUB.IS", "EGSER.IS",
    "EKGYO.IS", "EKIZ.IS", "EKOS.IS", "EKSUN.IS", "EMKEL.IS",
    "EMNIS.IS", "ENERY.IS", "ENJSA.IS", "ENKAI.IS", "ENTRA.IS",
    "EPLAS.IS", "ERBOS.IS", "EREGL.IS", "ERSU.IS", "ESCOM.IS",
    "ESEN.IS", "ETILR.IS", "EUHOL.IS", "EUPWR.IS", "EUREN.IS",
    "EUYO.IS", "EYGYO.IS", "FENER.IS", "FONET.IS", "FORMT.IS",
    "FORTE.IS", "FRIGO.IS", "FROTO.IS", "GARAN.IS", "GEDIK.IS",
    "GEDZA.IS", "GENIL.IS", "GENTS.IS", "GEREL.IS", "GESAN.IS",
    "GIPTA.IS", "GLBMD.IS", "GLCVY.IS", "GLRMK.IS", "GLYHO.IS",
    "GMTAS.IS", "GOLTS.IS", "GOODY.IS", "GOZDE.IS", "GRSEL.IS",
    "GSDDE.IS", "GSDHO.IS", "GSRAY.IS", "GUBRF.IS", "GWIND.IS",
    "HALKB.IS", "HATEK.IS", "HATSN.IS", "HEDEF.IS", "HEKTS.IS",
    "HLGYO.IS", "HOROZ.IS", "HRKET.IS", "HUBVC.IS", "HUNER.IS",
    "HURGZ.IS", "ICBCT.IS", "IDGYO.IS", "IHLAS.IS", "IHLGM.IS",
    "IMASM.IS", "INDES.IS", "INFO.IS", "INTEK.IS", "INVEO.IS",
    "INVES.IS", "ISCTR.IS", "ISDMR.IS", "ISFIN.IS", "ISGSY.IS",
    "ISKUR.IS", "ISMEN.IS", "IZENR.IS", "IZMDC.IS", "JANTS.IS",
    "KAPLM.IS", "KAREL.IS", "KARSN.IS", "KARTN.IS", "KATMR.IS",
    "KAYSE.IS", "KBORU.IS", "KCHOL.IS", "KENT.IS", "KERVN.IS",
    "KGYO.IS", "KIMMR.IS", "KLGYO.IS", "KLKIM.IS", "KLMSN.IS",
    "KLNMA.IS", "KLRHO.IS", "KLSER.IS", "KLSYN.IS", "KLYPV.IS",
    "KMPUR.IS", "KNFRT.IS", "KOCMT.IS", "KONKA.IS", "KONTR.IS",
    "KONYA.IS", "KOPOL.IS", "KORDS.IS", "KOTON.IS", "KRDMA.IS",
    "KRDMB.IS", "KRDMD.IS", "KRONT.IS", "KRSTL.IS", "KRTEK.IS",
    "KRVGD.IS", "KSTUR.IS", "KTSKR.IS", "KUTPO.IS", "KUYAS.IS",
    "LIDER.IS", "LIDFA.IS", "LINK.IS", "LOGO.IS", "LUKSK.IS",
    "MAALT.IS", "MAGEN.IS", "MAKIM.IS", "MANAS.IS", "MARBL.IS",
    "MARKA.IS", "MARMR.IS", "MARTI.IS", "MAVI.IS", "MEDTR.IS",
    "MEGAP.IS", "MEGMT.IS", "MEPET.IS", "MERCN.IS", "MERIT.IS",
    "MERKO.IS", "METRO.IS", "MGROS.IS", "MNDRS.IS", "MOBTL.IS",
    "MOGAN.IS", "MPARK.IS", "MRSHL.IS", "MSGYO.IS", "MTRKS.IS",
    "MTRYO.IS", "NATEN.IS", "NETAS.IS", "NIBAS.IS", "NTGAZ.IS",
    "NTHOL.IS", "NUGYO.IS", "NUHCM.IS", "OBASE.IS", "ODAS.IS",
    "ORGE.IS", "ORMA.IS", "OSTIM.IS", "OTKAR.IS", "OTTO.IS",
    "OYAKC.IS", "OYLUM.IS", "OZGYO.IS", "OZRDN.IS", "OZSUB.IS",
    "PAGYO.IS", "PARSN.IS", "PATEK.IS", "PEKGY.IS", "PENTA.IS",
    "PETKM.IS", "PETUN.IS", "PGSUS.IS", "PKART.IS", "PKENT.IS",
    "PNSUT.IS", "POLHO.IS", "PRDGS.IS", "PRKAB.IS", "PRKME.IS",
    "PSGYO.IS", "QNBFK.IS", "QNBTR.IS", "RAYSG.IS", "RGYAS.IS",
    "RODRG.IS", "RUBNS.IS", "RYSAS.IS", "SAHOL.IS", "SANEL.IS",
    "SANFM.IS", "SANKO.IS", "SARKY.IS", "SASA.IS", "SAYAS.IS",
    "SEGMN.IS", "SEGYO.IS", "SEKUR.IS", "SELEC.IS", "SELVA.IS",
    "SILVR.IS", "SISE.IS", "SKBNK.IS", "SKTAS.IS", "SMART.IS",
    "SNGYO.IS", "SNPAM.IS", "SOKM.IS", "SONME.IS", "SUMAS.IS",
    "SUNTK.IS", "SUWEN.IS", "TATGD.IS", "TAVHL.IS", "TBORG.IS",
    "TCELL.IS", "TDGYO.IS", "TEKTU.IS", "TGSAS.IS", "THYAO.IS",
    "TKFEN.IS", "TKNSA.IS", "TLMAN.IS", "TMSN.IS", "TOASO.IS",
    "TRGYO.IS", "TRHOL.IS", "TRILC.IS", "TRMET.IS", "TRALT.IS",
    "TSKB.IS", "TTKOM.IS", "TTRAK.IS", "TUKAS.IS", "TUPRS.IS",
    "TURSG.IS", "ULKER.IS", "ULUSE.IS", "ULUUN.IS", "UNLU.IS",
    "USAK.IS", "VAKBN.IS", "VAKKO.IS", "VANGD.IS", "VBTYZ.IS",
    "VERTU.IS", "VESBE.IS", "VESTL.IS", "VKGYO.IS", "VKING.IS",
    "VSNMD.IS", "YATAS.IS", "YAYLA.IS", "YBTAS.IS", "YESIL.IS",
    "YGGYO.IS", "YIGIT.IS", "YKBNK.IS", "YONGA.IS", "YUNSA.IS",
    "YYAPI.IS", "ZEDUR.IS", "ZOREN.IS", "ZRGYO.IS"
]

# ================= VERİ ÇEK =================
def get_data(symbol):
    try:
        df = yf.download(symbol, interval="1d", period="60d",
                         auto_adjust=False, progress=False, timeout=30)
        if df is None or df.empty or len(df) < 10:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        return df
    except Exception:
        return None

# ================= PARA AKIŞI =================
def money_flow(df):
    try:
        df = df[["Open", "Close", "Volume"]].dropna()
        if len(df) < 2:
            return None, None
        mf = (df["Close"] - df["Open"]) * df["Volume"]
        return mf > 0, mf < 0
    except Exception:
        return None, None

# ================= TARAMA =================
def scan_market(scan_number=1):
    giris = []
    cikis = []
    toplam = len(SYMBOLS)

    print(f"\n{'='*50}", flush=True)
    print(f"🔍 TARAMA #{scan_number} — {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}", flush=True)
    print(f"{'='*50}", flush=True)

    for i, symbol in enumerate(SYMBOLS, 1):
        if i % 50 == 1:
            print(f"📈 [{i}/{toplam}] İşleniyor...", flush=True)

        df = get_data(symbol)
        if df is None:
            continue

        ad = symbol.replace('.IS', '')

        try:
            g, c = money_flow(df)
            if g is not None and len(g) > 0:
                if bool(g.iloc[-1]):
                    giris.append(ad)
                elif bool(c.iloc[-1]):
                    cikis.append(ad)
        except Exception:
            continue

        time.sleep(0.1)

    print(f"✅ Tamamlandı! 🟢 Giriş: {len(giris)} | 🔴 Çıkış: {len(cikis)}", flush=True)

    zaman = datetime.now().strftime('%d.%m.%Y %H:%M')

    # ===== ÖZET =====
    send_telegram(
        f"💰 Para Akışı — #{scan_number}\n"
        f"🕒 {zaman}\n\n"
        f"🟢 Para Girişi: {len(giris)}\n"
        f"🔴 Para Çıkışı: {len(cikis)}"
    )
    time.sleep(0.5)

    if giris:
        send_parcali("📅 🟢 PARA GİRİŞİ", sorted(giris))

    if cikis:
        send_parcali("📅 🔴 PARA ÇIKIŞI", sorted(cikis))

    if not giris and not cikis:
        send_telegram(f"ℹ️ Tarama #{scan_number} — Sinyal bulunamadı.\n🕒 {zaman}")


# ================= OTOMATİK DÖNGÜ =================
if __name__ == "__main__":
    print("🚀 Para Akışı Otomatik Tarayıcı Başladı", flush=True)

    send_telegram(
        f"🤖 Para Akışı Bot Aktif\n"
        f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
        f"🔄 Her 2 saatte bir tarama yapılacak\n"
        f"📅 Günlük (1D) sinyaller"
    )

    scan_count = 0
    while True:
        scan_count += 1
        scan_market(scan_number=scan_count)
        print(f"\n⏳ 2 saat bekleniyor...", flush=True)
        time.sleep(7200)
