import Netstat, subprocess, folium
from urllib.request import urlopen

def extraerInformacionDeCMD():
    subprocess.run("Netstat -noap TCP > netstat.txt", shell=True)
    archivo = listado = list()

    with open("netstat.txt", "r") as netstat: archivo = netstat.readlines()
    netstat.close()
    archivo = archivo[4: len(archivo) - 1]

    for linea in archivo:
        linea = linea.split()
        destino = linea[2].split(":")[0]
        agregar = True

        if destino == '0.0.0.0' or destino == '127.0.0.1': agregar = False
        else:
            for netstat in listado:
                if netstat.destino == destino:
                    agregar = False
                    break

        if agregar:
            local = linea[1]
            estado = linea[3]
            pid = linea[4]
            listado.append(Netstat.Netstat(local, destino, estado, pid))

    listado.append(Netstat.Netstat('', 'destino', 'estado', 'pid'))
    listado.append(Netstat.Netstat('', '192.168.1.5', 'estado', 'pid'))
    return listado

def extraerInformacionDePagina(lista):
    posicionesAEliminar = list()

    for i in range(len(lista)):
        try:
            nt = lista[i]
            url = "https://ipinfo.io/" + nt.destino
            pagina = urlopen(url)
            html = pagina.read().decode("utf-8")[2:-2].split(",\n")
            listado = list()
            diccionario = dict()

            for elemento in html: listado.append(elemento.split(":"))
            for elemento in listado: diccionario[elemento[0].lstrip()] = elemento[1]

            nt.geolocation.country = diccionario['"country"'].lstrip()[1:-1]
            nt.geolocation.region = diccionario['"region"'].lstrip()[1:-1]
            nt.geolocation.city = diccionario['"city"'].lstrip()[1:-1]
            nt.geolocation.organization = diccionario['"org"'].lstrip()[1:-1]

            ubicacion = diccionario['"loc"'].lstrip()[1:-1].split(",")
            nt.geolocation.latitude = ubicacion[0]
            nt.geolocation.longitude = ubicacion[1]

            print(diccionario)
            lista[i] = nt
        except:
            posicionesAEliminar.append(i - len(posicionesAEliminar))
            continue

    for pos in posicionesAEliminar: lista.pop(pos)
    return lista

def crearMapa(lista):
    centrarLat = centrarLong = 0

    if len(lista) > 0:
        centrarLat = sum([float(netstat.geolocation.latitude) for netstat in lista]) / len(lista)
        centrarLong = sum([float(netstat.geolocation.longitude) for netstat in lista]) / len(lista)

    mapa = folium.Map(location=[centrarLat, centrarLong], zoom_start=4)
    for netstat in lista:
        lat = netstat.geolocation.latitude
        long = netstat.geolocation.longitude
        pais = netstat.geolocation.country
        reg = netstat.geolocation.region
        ciudad = netstat.geolocation.city
        organizacion = netstat.geolocation.organization

        popup_html = f"""
            <b>{organizacion}</b><br>
            <ul>
                <li>País: {pais}</li>
                <li>Región: {reg}</li>
                <li>Ciudad: {ciudad}</li>import Geolocation
        """

        folium.Marker(
            location=[lat, long],
            popup=folium.Popup(popup_html, max_width=3000),
            tooltip=organizacion
        ).add_to(mapa)

    mapa.save("mapa_mundial.html");
    print("Mapa creado exitosamente.");

    subprocess.run("mapa_mundial.html", shell=True)

def main():
    listado = extraerInformacionDeCMD()
    listado = extraerInformacionDePagina(listado)
    crearMapa(listado)

if __name__ == '__main__':
    main()
