from flask import Flask, request, jsonify, json, Response
from pymongo import MongoClient
from datetime import datetime, date, time, timedelta

app = Flask(__name__)

#CONECCION MONGO
client = MongoClient()

#CREACIÓN BD "Calculadora"
db = client.calculadora

#CREACIÓN DE COLECCIONES EN LA BASE DE DATOS
log = db.logOperaciones
ram = db.ram

#MOSTRAR ATRIBUTOS GENERALES DEL BOT*******************************************************************************************************************************
@app.route('/api/web-bot/mostrar/atributos', methods=['GET'])
def mostrarAtributos():
    ident=hash("lola")
    creador= 'Hillary Brenes Araya'
    fecha= '17-02-2017'

    result= {'Hola humanos soy TUTI-BOT' : {'Creadora:' : creador, 'Mi identificacion:' : ident, 'Fui creado:' : fecha}}
    js = json.dumps(result)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://ecommerce.com'
    return resp


#MOSTRAR LISTA DE CONOCIMENTOS BOT************************************************************************************************************************************************+
@app.route('/api/web-bot/mostrar/listaConocimientos')
def mostrarlista():
 conocimiento1="Calcula la fecha de parto"
 conocimiento2="Da nombres para niña y niño"
 conocimiento3="Brinda imagen de ropa para niña y niño"

 result= {'Lista de conocimientos de TUTI-BOT' : {'conocimiento #1: ' : conocimiento1, 'conocimiento #2: ' : conocimiento2, 'conocimiento #3: ' : conocimiento3}}
 js = json.dumps(result)
 resp = Response(js, status=200, mimetype='application/json')
 resp.headers['Link'] = 'http://ecommerce.com'
 return resp

#SABER POR DEFECTO: LO QUE SABE A NIVEL DE CODIGO********************************************************************************************************************************
@app.route('/api/web-bot/embarazoSemanas', methods=['POST'])
def nombres():
   semana= request.json['Semanas de embarazo']
   if (semana <= 4):
       meses= "Felicidades, estas iniciando tu embarazo"
   elif (semana >= 5 and semana <=8):
       meses= "primero"
   elif(semana >=9 and semana <= 12):
       meses= "segundo"
   elif(semana >=13 and semana <= 17):
       meses= "Tercer"
   elif (semana >=18 and semana <=21):
       meses= "Cuarto"
   elif(semana >=22 and semana <=25):
       meses= "quinto"
   elif(semana >=26 and semana <=30):
       meses="sexto"
   elif(semana >=31 and semana <=34):
       meses="setimo"
   elif(semana >=35 and semana <=38):
       meses="octavo"
   elif(semana >=39 and semana <=42):
       meses= "noveno"
   elif(semana > 42):
       meses="Las semanas de embarazo son 40"

   resultado= {'Felicidades, mes de embarazo' : meses}

   js = json.dumps(resultado)
   resp = Response(js, status=200, mimetype='application/json')
   resp.headers['Link'] = 'http://ecommerce.com'
   return resp

#APRENDER #1: CALCULO EMBARAZO************************************************************************************************************************************************************
@app.route('/api/web-bot/Aprender', methods=['POST'])
def aprender():
 code = request.json['codigo']
 user=request.json['usuario']
 action = request.json['accion']
 date= datetime.now()

 memoria= {'Codigo:' : code, 'Usuario' : user}
 ram.insert_one(memoria)  #DATOS DE APRENDER INSERTADOS EN LA BASE DE DATOS

 historial = {'Usuario: ': user, 'Fecha: ': date, 'Acción: ': action}
 log.insert_one(historial) #DATOS DE REGISTRO INSERTADOS EN LA BASE DE DATOS

 Result= {"Hola humanos, he aprendido algo nuevo: " : action}

 js = json.dumps(Result)
 resp = Response(js, status=200, mimetype='application/json')
 exec (code)

 return resp
#DESAPRENDER*********************************************************************************************************************************************************++
@app.route('/api/web-bot/desAprender', methods=['POST'])
def desaprenda():
    user = request.json['usuario']
    action = request.json['accion']
    date = datetime.now()
    db.ram.remove({'Usuario': 'Hilla'}) #SE REMUEVE EL ARCHIVO
    historial = {'Usuario: ': user, 'Fecha: ': date, 'Acción: ': action}
    log.insert_one(historial) #DATOS DE REGISTRO INSERTADOS EN LA BASE DE DATOS

    Result = {"Oh no humanos, he desaprendido algo: ": action}
    js = json.dumps(Result)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

#MOSTRAR LOG DE OPERACIONES******************************************************************************************************************************************************
@app.route('/api/web-bot/mostarLog', methods=['GET'])
def mostrarHistorial():
 for buscador in db.logOperaciones.find({}):
  result = print(buscador)

  js = json.dumps(result)
  resp = Response(js, status=200, mimetype='application/json')
  return resp

## Main
if __name__ == '__main__':
    app.run()