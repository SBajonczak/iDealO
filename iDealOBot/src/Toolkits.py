def priceStringtoFload(price:str)->float:
    prices= price.replace("ab", "").replace(".", "").replace(",", ".").replace("€","").replace("inkl Versand","").replace(".\n\n","").replace("siehe Shop","").replace("Zzgl Versandkosten","").strip()
    if (prices==""):
        return 0.0
    return float(prices)