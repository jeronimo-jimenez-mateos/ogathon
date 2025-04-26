import numpy as np
from itertools import permutations
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, reqparse, fields
from decimal import Decimal, getcontext # Para mejorar la precisión de los cálculos


'''
Ejercicio 1:
Para llegar a la distancia d, podemos hacerlo de la siguiente manera:
1. Dando un paso de 1 desde la distancia d-1
2. Dando un paso de 2 desde la distancia d-2

A su vez, para llegar a la distancia d-1, podemos hacerlo de la siguiente manera:
1. Dando un paso de 1 desde la distancia d-2
2. Dando un paso de 2 desde la distancia d-3

Si lo traemos al origen:
1. Solo hay una forma de llegar a la distancia 1 (dando un paso de 1 desde la distancia 0)
2. Hay dos formas de llegar a la distancia 2 (dando un paso de 1 desde la distancia 1 o dando un paso de 2 desde la distancia 0)
'''
def count_ways(n):
    getcontext().prec = 100  
    # Para calcular el número de formas de llegar a la distancia d, podemos usar dos métodos:
    # Mediante un bucle
    # Usando la fórmula de Fibonacci (ideal para este problema, menor potencia de cómputo)
    sqrt5 = Decimal(5).sqrt()
    PHI = (1 + 5 ** 0.5) / 2
    PSI = (1 - 5 ** 0.5) / 2
    # Fórmula de Fibonacci
    PHI = (Decimal(1) + sqrt5) / Decimal(2)
    PSI = (Decimal(1) - sqrt5) / Decimal(2)

    dp_n = (PHI ** (n + 1) - PSI ** (n + 1)) / sqrt5
    dp_n = dp_n.to_integral_value(rounding='ROUND_HALF_EVEN')  # redondeo seguro
    return str(dp_n)
    
'''
Ejercicio 2:
Definimos las funciones necesarias para resolver el problema:
'''

def suma_cuadrados_digitos(n):
    """Devuelve la suma de los cuadrados de los dígitos de un número."""
    return sum(int(digit) ** 2 for digit in str(n))

def secuencia_llega_a_89(n):
    """Devuelve True si la secuencia generada por n llega a 89."""
    seen = set()
    while n != 1 and n != 89:
        if n in seen:
            return False  
        seen.add(n)
        n = suma_cuadrados_digitos(n)
    return n == 89

def contar_numeros_hasta_maximo(max_num):
    """Cuenta cuántos números menores o iguales a max_num generan una secuencia que llega a 89."""
    contador = 0
    for i in range(1, max_num + 1):
        if secuencia_llega_a_89(i):
            contador += 1
    return contador
'''
Ejercicio 3:
En este caso, solo hay una función:
'''

def calcular_movimientos_optimizado(residuos):
    """
    Calcula el número mínimo de movimientos necesarios para ordenar los residuos,
    probando todas las permutaciones posibles de asignación de contenedores.
    
    Args:
        residuos: Lista o array 2D donde residuos[i][j] representa la cantidad
                 del tipo de residuo j en el contenedor i
                 Ejemplo: [[1, 3, 2], [2, 1, 3], [3, 2, 1]]
    
    Returns:
        Una tupla con (mínimo de movimientos, mejor permutación de contenedores)
    """
    residuos = np.array(residuos)
    num_contenedores = residuos.shape[0]
    
    # Generamos todas las permutaciones posibles de asignación de contenedores
    todas_permutaciones = list(permutations(range(num_contenedores)))
    
    mejor_movimientos = float('inf')
    mejor_permutacion = None
    
    # Probamos cada permutación
    for permutacion in todas_permutaciones:
        movimientos_actual = calcular_movimientos_para_permutacion(residuos, permutacion)
        
        if movimientos_actual < mejor_movimientos:
            mejor_movimientos = movimientos_actual
            mejor_permutacion = permutacion
    
    return mejor_movimientos, mejor_permutacion

def calcular_movimientos_para_permutacion(residuos, permutacion):
    """
    Calcula los movimientos necesarios para una permutación específica.
    
    Args:
        residuos: Array numpy de residuos
        permutacion: Tupla que indica la asignación de cada tipo de residuo a un contenedor
    
    Returns:
        El número de movimientos necesarios
    """
    residuos_copia = residuos.copy()
    movimientos = 0
    
    # Para cada tipo de residuo (Vidrio, Cartón, Plástico)
    for tipo in range(len(permutacion)):
        contenedor_asignado = permutacion[tipo]
        
        # Comprobamos los residuos mal ubicados
        for contenedor in range(residuos_copia.shape[0]):
            # Si el residuo está en un contenedor que no es el asignado para ese tipo
            if contenedor != contenedor_asignado:
                residuos_a_mover = residuos_copia[contenedor, tipo]
                residuos_copia[contenedor, tipo] = 0
                movimientos += residuos_a_mover
                residuos_copia[contenedor_asignado, tipo] += residuos_a_mover
    
    return int(movimientos)



app = Flask(__name__)
api = Api(app, 
          version='1.0', 
          title='Patrones de Propagación API',
          description='Calcula el número de patrones para alcanzar una distancia dada en una dimensión.',
          doc='/swagger') 

ns = api.namespace('challenges', description='Operaciones de retos')

parser = reqparse.RequestParser()
parser.add_argument('n', type=int, required=True, help='Distancia para calcular el número de patrones')

@ns.route('/solution-1')
class Solution1(Resource):
    @api.doc(params={'n': 'Distancia a calcular'})
    def get(self):
        args = parser.parse_args()
        n = args.get('n')

        if n is None:
            api.abort(400, "El parámetro 'n' es requerido.")
        if n < 0:
            api.abort(400, "La distancia debe ser un número positivo.")
        
        patrones = count_ways(n)
        return str(patrones)
    
@ns.route('/solution-2')
class Solution2(Resource):
    @api.doc(params={'n': 'Número máximo para calcular cuántos números llegan a 89'})
    def get(self):
        args = parser.parse_args()
        n = args.get('n')

        if n is None:
            api.abort(400, "El parámetro 'n' es requerido.")
        if n < 1:
            api.abort(400, "El número debe ser un entero positivo.")
        
        count = contar_numeros_hasta_maximo(n)
        return count

residuo_model = fields.List(fields.Integer, description="Contenedor [x, y, cantidad]")
residuos_model = api.schema_model('Residuos', {
    'type': 'array',
    'items': {
        'type': 'array',
        'items': {
            'type': 'integer'
        }
    },
    'description': 'Lista de residuos como arrays de enteros'
})

@ns.route('/solution-3')
class Solution3(Resource):
    @api.expect(residuos_model)  # Esto genera automáticamente el campo en Swagger
    def post(self):
        residuos = request.get_json()
        if residuos is None:
            api.abort(400, "Faltan los datos de residuos.")

        movimientos = calcular_movimientos_optimizado(residuos)
        return int(movimientos)
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)