from collections.abc import Collection

class Estacion:

    def __init__(self, nombre, latitud, longitud):

        if not isinstance(nombre, str):

            raise TypeError("El nombre de la estacion debe de ser un objeto de la clase String")
        elif not all(isinstance(variable, float) for variable in [latitud, longitud]):

            raise TypeError("La variables de latitud y longitud deben de ser valores flotantes")

        self.nombre = nombre;

        self.latitud = latitud;

        self.longitud = longitud;


    def __repr__(self):

        return f"{self.nombre}, ({self.latitud},{self.longitud})"

    def __hash__(self):

        return hash((self.nombre, self.latitud, self.longitud))

    def __eq__(self, other):

        if isinstance(other, Estacion):

            return self.nombre == other.nombre

        return False


class EstacionPaso (Estacion):

    def __init__(self, nombre, latitud, longitud, linea):

        super().__init__(nombre, latitud, longitud)

        if not isinstance(linea, str):

            raise ValueError("Se debe de proporcionar un objeto String indicando el nombre de la línea a la que pertenece esta estación.");

        self.linea = linea

        self.estaciones_adyacentes = []


class EstacionCorrespondencia (Estacion):

    def __init__(self, nombre, latitud, longitud, lineas):

        super().__init__(nombre, latitud, longitud)

        if not isinstance(lineas, Collection):

            raise TypeError("Se debe de proporcionar una lista de elementos enteros indicando las líneas a las que pertenece esta estación.")

        elif len(lineas) < 2:

            raise ValueError("La colección pasada como argumento debe de contener por lo menos dos elementos enteros.")

        #lineas = set(lineas)

        lineas = set([nombre_linea.strip() for nombre_linea in lineas])

        if not all(isinstance(item, str) for item in lineas):

            raise TypeError("Los elementos de la colección deben de ser Strings que indiquen el nombre de las líneas a la que pertenece esta estación")

        self.transbordos = dict(zip(lineas, ([] for item in lineas)))

