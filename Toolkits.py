def priceStringtoFload(price:str)->float:
    prices= price.replace("ab", "").replace(".", "").replace(",", ".").replace("€","").replace("inkl Versand","").replace(".\n\n","").replace("siehe Shop","").replace("Zzgl Versandkosten","").strip()
    return float(prices)