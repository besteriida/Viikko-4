"""
Ohjelma joka tulostaa tiedostosta luettujen varausten alkiot ja niiden tietotyypit

varausId | nimi | sähköposti | puhelin | varauksenPvm | varauksenKlo | varauksenKesto | hinta | varausVahvistettu | varattuTila | varausLuotu
------------------------------------------------------------------------
201 | Muumi Muumilaakso | muumi@valkoinenlaakso.org | 0509876543 | 2025-11-12 | 09:00 | 2 | 18.50 | True | Metsätila 1 | 2025-08-12 14:33:20
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
202 | Niiskuneiti Muumilaakso | niisku@muumiglam.fi | 0451122334 | 2025-12-01 | 11:30 | 1 | 12.00 | False | Kukkahuone | 2025-09-03 09:12:48
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
203 | Pikku Myy Myrsky | myy@pikkuraivo.net | 0415566778 | 2025-10-22 | 15:45 | 3 | 27.90 | True | Punainen Huone | 2025-07-29 18:05:11
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
204 | Nipsu Rahapulainen | nipsu@rahahuolet.me | 0442233445 | 2025-09-18 | 13:00 | 4 | 39.95 | False | Varastotila N | 2025-08-01 10:59:02
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
205 | Hemuli Kasvikerääjä | hemuli@kasvikeraily.club | 0463344556 | 2025-11-05 | 08:15 | 2 | 19.95 | True | Kasvitutkimuslabra | 2025-10-09 16:41:55
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
"""
from datetime import datetime
from unicodedata import name

def muunna_varaustiedot(varaus: list) -> list:
    # Tähän tulee siis varaus oletustietotyypeillä (str)
    # Varauksessa on 11 saraketta -> Lista -> Alkiot 0-10
    # Muuta tietotyypit haluamallasi tavalla -> Seuraavassa esimerkki ensimmäisestä alkioista
    muutettuvaraus = []
    muutettuvaraus.append(int(varaus[0].lstrip('\ufeff')))
    muutettuvaraus.append(str(varaus[1]))
    muutettuvaraus.append(str(varaus[2]))
    muutettuvaraus.append(str(varaus[3]))
    muutettuvaraus.append(datetime.strptime(varaus[4], "%Y-%m-%d").date())
    muutettuvaraus.append(datetime.strptime(varaus[5], "%H:%M").time())
    muutettuvaraus.append(int(varaus[6]))
    muutettuvaraus.append(float(varaus[7]))
    muutettuvaraus.append(varaus[8].strip() == "True")
    muutettuvaraus.append(str(varaus[9]))
    muutettuvaraus.append(datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S"))
    return muutettuvaraus


def hae_varaukset(varaustiedosto: str) -> list:
    # HUOM! Tälle funktioille ei tarvitse tehdä mitään!
    # Jos muutat, kommentoi miksi muutit
    varaukset = []
    varaukset.append(["varausId", "nimi", "sähköposti", "puhelin", "varauksenPvm", "varauksenKlo", "varauksenKesto", "hinta", "varausVahvistettu", "varattuTila", "varausLuotu"])
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset

def main():
    # HUOM! seuraaville riveille ei tarvitse tehdä mitään osassa A!
    # Osa B vaatii muutoksia -> Esim. tulostuksien (print-funktio) muuttamisen.
    # Kutsutaan funkioita hae_varaukset, joka palauttaa kaikki varaukset oikeilla tietotyypeillä
    varaukset = hae_varaukset("varaukset.txt")
       
    print("📅 Vahvistetut varaukset")
    print("------------------------------------------------------------------------")
    for vahvaraus in varaukset[1:]:
        
        if vahvaraus[8]:  # Vain vahvistetut varaukset
            nimi = vahvaraus[1]
            tila = vahvaraus[9]
            pvm = vahvaraus[4].strftime("%d.%m.%Y")
            klo = vahvaraus[5].strftime("%H.%M")
            print(f"- {nimi}, {tila}, {pvm}, {klo}")

    print("\n 🕰️ Pitkät varaukset (yli 3 h)")
    print("------------------------------------------------------------------------")

    for pitkavaraus in varaukset[1:]:
        if pitkavaraus[6] > 3:  # Vain yli 3 h
            nimi = pitkavaraus[1]
            pvm = pitkavaraus[4].strftime("%d.%m.%Y")
            klo = pitkavaraus[5].strftime("%H.%M")
            kesto = pitkavaraus[6]
            tila = pitkavaraus[9]
            print(f"- {nimi}, {pvm}, {klo}, {kesto} h, {tila}")
    
    print("\n💸 Maxetut varaukset")
    print("------------------------------------------------------------------------")

    for varaus in varaukset[1:]:
        nimi = varaus[1]
        if varaus[8] == True:
            print(f"- {nimi} -> Vahvistettu")    
        else:
            print(f"- {nimi} -> Ei vahvistettu")

    print("\n🤝 Vahvistetut varaukset")
    print("------------------------------------------------------------------------")
    
    vahvistettu_lkm = 0
    eivahvistettu_lkm = 0
    for varaus in varaukset[1:]:
        if varaus[8] == True:
            vahvistettu_lkm += 1
        else:
            eivahvistettu_lkm += 1

    print(f"Vahvistettuja varauksia: {vahvistettu_lkm}")
    print(f"Ei vahvistettuja varauksia: {eivahvistettu_lkm}")

    print("\n🤑 Massii tulos yhteensä")
    print("------------------------------------------------------------------------")

    kokonaistulo = sum(varaus[7] for varaus in varaukset[1:] if varaus[8])
    muutettu_kokonaistulo = f"{kokonaistulo:.2f}".replace(".", ",")
    print(f"Vahvistettujen varausten kokonaistulot: {muutettu_kokonaistulo} €")


    print("\n🤑 Raha äijä")
    print("------------------------------------------------------------------------")
    kallein_varaus = max(varaukset[1:], key=lambda v: v[7])
    nimi = kallein_varaus[1]
    tila = kallein_varaus[9]
    print(f"-Nimi:{nimi}, Tila: {tila}, Kallein varaus: ({kallein_varaus[7]:.2f} €)")


    print("\n🌄 Varausten määrä päivämäärittäin")
    print("------------------------------------------------------------------------")

    varaukset_paivittain = {}
    for varaus in varaukset[1:]:
        paiva = varaus[4]
        if paiva not in varaukset_paivittain:
            varaukset_paivittain[paiva] = 0
        varaukset_paivittain[paiva] += 1

    for paiva, lkm in sorted(varaukset_paivittain.items()):
        print(f"-Varausten määrä päivämäärittäin {paiva.strftime('%d.%m.%Y')}: {lkm} kpl")   



if __name__ == "__main__":
    main()