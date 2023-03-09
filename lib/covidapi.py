# / v3 / covid - 19 / countries / {country}
from dataclasses import dataclass
import requests
from requests import Response


@dataclass
class AllResult:
    updated: int
    cases: int
    deaths: int
    deathsPerOneMillion: float
    criticalPerOneMillion: float


@dataclass
class AllCountry:
    updated: int
    country: str
    cases: int
    flag: str
    country_info: dict
    iso2: str
    iso3: str
    deaths: int
    recovered: int
    continent: str

    '''
        En Python existe un módulo llamado dataclass que permite agregar código auto 
        generado a los métodos especiales de la clase con una sola línea de código
        
    '''


# class principal
class CovidAPI:
    def __init__(self):
        self._info_url: str = 'https://disease.sh/v3/covid-19/all'
        self._info_country_url: str = 'https://disease.sh/v3/covid-19/countries/'

    '''
    La anotación -> AllResult es una anotación de tipo de retorno, que indica que la función retornará un objeto de 
    tipo AllResult. La anotación de tipo de retorno es opcional en Python, pero ayuda a documentar el tipo de retorno 
    esperado y facilita la tarea de debugging en algunos casos
    '''

    @property
    def get_info(self) -> AllResult:
        # | dict
        try:
            r: Response = requests.get(self._info_url)
            if r.status_code != 200:
                print('No se ha podido conectar con el servidor')
                return AllResult(updated=0, cases=0, deaths=0, deathsPerOneMillion=0.0, criticalPerOneMillion=0.0)
            data: dict = r.json()
            # flag = data.get("flag")
            return AllResult(updated=data.get("updated"), cases=data.get("cases"), deaths=data.get('deaths'),
                             deathsPerOneMillion=data.get('deathsPerOneMillion'),
                             criticalPerOneMillion=data.get('criticalPerOneMillion'))
        except requests.exceptions.RequestException as e:
            print('No se ha podido conectar con el servidor:', e)
            return AllResult(updated=0, cases=0, deaths=0, deathsPerOneMillion=0.0, criticalPerOneMillion=0.0)

    def get_country_info(self, country: str) -> AllCountry:
        # print(country)
        try:
            r: Response = requests.get(self._info_country_url + country)
            if r.status_code != 200:
                print('No se ha podido conectar con el servidor')
                return AllCountry(updated=0, cases=0, country='',iso2='', flag='', country_info={}, deaths=0,
                                  recovered=0, continent="", iso3=0)
            data: dict = r.json()
            country_info: dict = data.get("countryInfo")
            flag: str = country_info.get("flag")
            iso2: str = country_info.get('iso2')
            iso3: str = country_info.get('iso3')
            # flag = self.get_flag(country) flag=flag, flag='',
            return AllCountry(updated=data.get("updated"), cases=data.get("cases"),country=data.get("country"),
                              flag=flag, iso2=iso2, country_info={}, deaths=data.get("deaths"),
                              recovered=data.get("recovered"), continent=data.get("continent"), iso3=iso3)
        except requests.exceptions.RequestException as e:
            print(f'Error al realizar la solicitud: {e}')
            return AllCountry(updated=0, cases=0, iso2='', flag='', country_info={}, country='', deaths=0,
                              recovered=0, continent="", iso3=iso3)

#
# if __name__ == '__main__':
#     info: CovidAPI = CovidAPI()
#     info_data: AllResult = info.get_info
#     info_country: AllCountry = info.get_country_info('spain')
#     print("Mostramos la info de la url ALL")
#     print(f"El updated es                    : {info_data.updated}")
#     print(f"El cases es                      : {info_data.cases}")
#     print(f"El Nº muertes                    : {info_data.deaths}")
#     print(f"Nº muertos por persona           : {info_data.deathsPerOneMillion}")
#     print(f"Nº estados críticos por persona  : {info_data.criticalPerOneMillion}")
#     print("============================================================================")
#     print(info_data)
#     print("Mostramos la info de la url Country")
#     print(info_country)
