from flask import Flask
from flask_restx import Api, Resource, reqparse

'''
Definimos las funciones necesarias para resolver el problema:
'''

def suma_cuadrados_digitos(n):
    """Devuelve la suma de los cuadrados de los dígitos de un número."""
    return sum(int(digit) ** 2 for digit in str(n))

def secuencia_llega_a_89(n):
    """Devuelve True si la secuencia generada por n llega a 89."""
    seen = set()  # Para detectar ciclos
    while n != 1 and n != 89:
        if n in seen:
            return False  # Si encontramos un ciclo sin llegar a 89
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

app = Flask(__name__)

api = Api(app, 
          version='1.0', 
          title='Números que llegan a 89 API',
          description='Calcula cuántos números menores o iguales a un número dado generan una secuencia que llega a 89.',
          doc='/swagger')  # <- Aquí configuramos que la documentación esté en /swagger

ns = api.namespace('challenges', description='Operaciones de retos')
parser = reqparse.RequestParser()
parser.add_argument('n', type=int, required=True, help='Número máximo para calcular cuántos números llegan a 89')

@ns.route('/solution-2')
class Solution1(Resource):
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)