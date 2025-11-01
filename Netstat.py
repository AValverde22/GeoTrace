import Geolocation

class Netstat:
    def __init__(self, local, destino, estado, PID):
        self._local = local
        self._destino = destino
        self._estado = estado
        self._PID = PID
        self._geolocation = Geolocation.Geolocation()

    @property
    def local(self): return self._local

    @property
    def destino(self): return self._destino

    @property
    def estado(self): return self._estado

    @property
    def PID(self): return self._PID

    @property
    def geolocation(self): return self._geolocation
