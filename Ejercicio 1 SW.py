from flask import Flask
from flask_restx import Api, Resource, reqparse
import numpy as np


'''
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
app = Flask(__name__)
def count_ways(n):
    # Para calcular el número de formas de llegar a la distancia d, podemos usar dos métodos:
    # Mediante un bucle
    # Usando la fórmula de Fibonacci (ideal para este problema, menor potencia de cómputo)
    PHI = (1 + 5 ** 0.5) / 2
    PSI = (1 - 5 ** 0.5) / 2
    # Fórmula de Fibonacci
    dp_0 = 0
    dp_1 = 1
    dp_2 = 2
    dp_n = (PHI ** (n+1) - PSI ** (n+1)) / (5 ** 0.5)
    return int(dp_n)

api = Api(app, 
          version='1.0', 
          title='Patrones de Propagación API',
          description='Calcula el número de patrones para alcanzar una distancia dada en una dimensión.',
          doc='/swagger')  # <- Aquí configuramos que la documentación esté en /swagger

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)