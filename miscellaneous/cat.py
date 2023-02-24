# Zehaztutako helbide erlatiboko fitxategi baten eduki osoa pantailan bistaratzeko

def irakurri(fitxategia):
    try:
        file=open(fitxategia)
        for line in file:
            lerroa=line.strip()
            print(lerroa)
        file.close()
    except:
        print('Helbidea gaizki idatzita dago edo fitxategia ez da existitzen')

fitx=str(eval(input('Idatzi fitxategia dagoeneko helbide erlatiboa: ')))
irakurri(fitx)
