class Geolocation:
    def __init__(self):
        self._country = None
        self._region = None
        self._city = None
        self._organization = None
        self._latitude = None
        self._longitude = None

    @property
    def country(self): return self._country
    @country.setter
    def country(self, pais): self._country = pais

    @property
    def region(self): return self._region
    @region.setter
    def region(self, new_region): self._region = new_region

    @property
    def city(self): return self._city
    @city.setter
    def city(self, ciudad): self._city = ciudad

    @property
    def organization(self): return self._organization
    @organization.setter
    def organization(self, organizacion): self._organization = organizacion

    @property
    def latitude(self): return self._latitude
    @latitude.setter
    def latitude(self, latitud): self._latitude = latitud

    @property
    def longitude(self): return self._longitude
    @longitude.setter
    def longitude(self, longitud): self._longitude = longitud