import os
import sys
import pyttsx3
from datetime import date,timedelta
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl



engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 180)

tareasatiempo = ctrl.Antecedent(np.arange(0, 100, 1), 'tareasatiempo')
calidad = ctrl.Antecedent(np.arange(0,100,1), 'calidad')
command = ctrl.Consequent(np.arange(0,100,1), 'command')

tareasatiempo.automf(3)
calidad.automf(3)

command['deficiente'] = fuzz.trimf(command.universe,[0,0,49])
command['promedio'] = fuzz.trimf(command.universe,[25,50,75])
command['Excelente'] = fuzz.trimf(command.universe,[51,100,100])

r1 = ctrl.Rule(tareasatiempo['poor'] & calidad['poor'], command['deficiente'])
r2 = ctrl.Rule(tareasatiempo['poor'] & calidad['average'], command['deficiente'])
r3 = ctrl.Rule(tareasatiempo['poor'] & calidad['good'], command['promedio'])

r4 = ctrl.Rule(tareasatiempo['average'] & calidad['poor'], command['deficiente'])
r5 = ctrl.Rule(tareasatiempo['average'] & calidad['average'], command['deficiente'])
r6 = ctrl.Rule(tareasatiempo['average'] & calidad['good'], command['promedio'])

r7 = ctrl.Rule(tareasatiempo['good'] & calidad['poor'], command['deficiente'])
r8 = ctrl.Rule(tareasatiempo['good'] & calidad['average'], command['promedio'])
r9 = ctrl.Rule(tareasatiempo['good'] & calidad['good'], command['Excelente'])

command_ctrl = ctrl.ControlSystem(rules=[r1,r2,r3,r4,r5,r6,r7,r8,r9])
command_results = ctrl.ControlSystemSimulation(command_ctrl)

peticiones = {
    "enviarA" : ["enviar"],
    "mastiempo" : ["mas tiempo", "no he logrado", "aplazar", "tiempo", "plazo"],
    "problemas" : ["problemas", "un problema"],
    "salir":["salir"]
  }
peticionesjef = {
  "ActsEnviadas": ["enviadas"],
  "SoldePlazo": ["solicitudes", "ampliacion", "plazo"],
  "problemas": ["problemas", "inconvenientes"],
  "nuevtarea": ["asignar", "nueva tarea"],
  "desempeno": ["desempeño", "buen empleado"],
  "salir":["salir"]
}

class empleado:
  def __init__ (self, eid, id_jefe, nombre, desctarea, link1, disponibilidad, plazo, diaspedidos, pro, res, tareasenviadasatiempo, totaldetareas, calidad):
    self.eid = eid
    self.id_jefe = id_jefe
    self.nombre = nombre
    self.desctarea = desctarea
    self.link1 = link1
    self.disponibilidad = disponibilidad
    self.plazo = plazo
    self.diaspedidos = diaspedidos
    self.pro = pro
    self.res = res
    self.tareasenviadasatiempo = tareasenviadasatiempo
    self.totaldetareas = totaldetareas
    self.calidad = calidad
A= empleado( 1, 1, "Carlos","Realizar un informe del inventario","", 1, date(2019,5,25), 0, "", "", 5, 10,60)
B= empleado(2,1, "Luciana","","", 0, (0,0,0), 0, "", "",9,10, 92)
C= empleado(3,1, "Ernesto","Realizar un informe de los ultimos ingresos","", 1, (2019,5,30), 0, "", "", 8,12, 80)

D= empleado(4,2,"Susana","", "",0, (0,0,0), 0, "", "", 10,10,40)
E= empleado(5,2, "Lorenzo","Elaborar un software para el cliente TigerMarket","", 1, (2019,6,10), 0, "", "", 10, 11, 96)

empleados = [A,B,C,D,E]
class jefe:
  def __init__ (self, idj, nombre,petdeplazos, repproblemas):
    self.idj = idj
    self.nombre = nombre
    self.petdeplazos = petdeplazos
    self.repproblemas = repproblemas

Y= jefe(1,"Luis", "", "")
Z= jefe(2,"Sergio", "", "")

jefes = [Y, Z]

#PARA EMPLEADOS

def despedida():
  print("\nQue bueno haberte ayudado. Adios")
  engine.say('Que bueno haberte ayudado. Adios')
  engine.runAndWait()
  main()
def problemas(emp):
  engine.say('\nCuenta en breves lineas cual es tu problema:\n ')
  engine.runAndWait()
  problema = input(str("Cuenta en breves lineas cual es tu problema: \n"))
  print("\nHe enviado este mensaje a tu jefe.")
  engine.say('He enviado este mensaje a tu jefe.')
  engine.runAndWait()
  emp.pro = problema
  despedida()
def mastiempo(emp):
  engine.say('¿Cuantos dias quieres aplazar tu entrega?')
  engine.runAndWait()
  tiemp = int(input("\n¿Cuantos dias quieres aplazar tu entrega?"))
  while (tiemp<0 or tiemp>150):
    if(tiemp<0):
      engine.say('jajaja los dias no pueden ser negativos. Ingrese cuantos dias quiere aplazar su entrega: ')
      tiemp = int(input("\njajaja los dias no pueden ser negativos. Ingrese cuantos dias quiere aplazar su entrega: "))
    if (tiemp>150):
      engine.say('Limite alcanzado. No puedes aplazar la actividad tantos dias. Ingrese la cantidad de dias que desea aplazar la actividad:')
      tiemp = int(input("\nLimite alcanzado. No puedes aplazar la actividad tantos dias. Ingrese la cantidad de dias que desea aplazar la actividad:"))
  emp.diaspedidos = tiemp
  engine.say('He enviado una solicitud de plazo de'+str(emp.diaspedidos)+' dias a tu jefe.')
  print("He enviado una solicitud de plazo  de", tiemp, "dias a tu jefe.")
  engine.runAndWait()

  despedida()
def enviarA(emp):
  conlink = "https://drive.google.com/"
  engine.say('Por favor ingrese el link de su actividad. Recuerde que debe ser un archivo en google drive.')
  engine.runAndWait()
  link = input(str("Por favor ingrese el link de su actividad. Recuerde que debe ser un archivo en google drive. Inglese link: "))
  link.capitalize()
  while (link.find(conlink)<0):
    engine.say('Recuerda que el link a enviar debe ser un documento en google drive!')
    engine.runAndWait()
    link = input(str("Recuerda que el link a enviar debe ser un documento en google drive! Ingrese link:"))
  engine.say('Lo he añadido a la carpeta de entrega de tu jefe')
  print("\nLo he añadido a la carpeta de entrega de tu jefe")
  engine.runAndWait()
  emp.link1 = link
  emp.disponibilidad = 0
  emp.plazo = (0,0,0)
  emp.desctarea = ""
  despedida()
def agregar2 (clave, agr, emp):
  print("\nLo tendre en cuenta para la proxima vez!")
  engine.say('Lo tendre en cuenta para la proxima vez!')
  engine.runAndWait()
  agre = agr.split()
  for x in agre:
    if (len(x)<=2 or x=="los" or x=="las" or x=="unos" or x=="unas" or x == "necesito" or x == "quiero" or x == "actividad"):
      a = agre.index(x)
      agre.pop(a)
  
  for c, v in peticiones.items():
    if (c == clave):
      for x in agre:
        v.append(x)
  deteccion(clave, emp)       
def deteccion(c1, emp):
  if(c1 == "enviarA"):
    enviarA(emp)
  if (c1 == "mastiempo"):
    mastiempo(emp)
  if (c1 == "problemas"):
    problemas(emp)
  if(c1 == "salir"):
    engine.say('Ha sido un gusto! Hasta pronto')
    print("Ha sido un gusto. Hasta pronto!")
    engine.runAndWait()
    main()
def agregar (arg, peticion, emp):
  arg.capitalize()
  for c, v in peticiones.items():
    for va in v:
      if(arg.find(va)>=0):
        if (c == "enviarA"):
          agregar2("enviarA",peticion, emp)
          break
        if (c == "mastiempo"):
          agregar2("mastiempo",peticion, emp)
          break
        if (c == "problemas"):
          agregar2("problemas",peticion, emp)
          break
        if(c == "salir"):
          agregar2("salir",peticion, emp)
          break 
def soons (son, clave, peticion, emp):
  if(son == "si" or son == "SI" or son == "sI"):
    deteccion(clave, emp)
  else:
    nocomp(peticion, emp) 
def nocomp(peticion, emp):
  engine.say('No he logrado comprender tu peticion. ¿quieres enviar una tarea, pedir mayor plazo o presentas problemas con tu actividad?')  
  agr = input(str("\nNo he logrado comprender tu peticion. ¿quieres enviar una tarea, pedir mayor plazo o presentas problemas con tu actividad?\n"))
  engine.runAndWait()
  agregar(agr, peticion, emp)
def peti(peticion, emp):
  peticion.capitalize()
  for c,v in peticiones.items():
    for va in v:
      if(peticion.find(va)>=0):
        if (c == "enviarA"):
          engine.say('¿Necesitas enviar tu actividad asignada?')
          engine.runAndWait()
          son = input(str("\n¿Necesitas enviar tu actividad asignada?"))
          soons(son, c, peticion, emp)
          break
        if (c == "mastiempo"):
          engine.say('¿Necesitas mas tiempo para realizar tu actividad asignada?')
          engine.runAndWait()
          son = input(str("\n¿Necesitas mas tiempo para realizar tu actividad asignada?"))
          soons(son, c, peticion, emp)
          break
        if (c == "problemas"):
          engine.say('¿Presentas problemas con tu actividad asignada?')
          engine.runAndWait()
          son = input(str("\n¿Presentas problemas con tu actividad asignada?"))
          soons(son, c, peticion, emp)
          break
        if (c == "salir"):
          engine.say('\n¿Desea salir?')
          engine.runAndWait()
          son = input(str("\n¿Desea salir?"))
          soons(son, c, peticion, emp) 
  nocomp(peticion, emp)
def saludo(sal, nom):
    saludos = ["Hola", "Jucagi", "hola", "jucagi"]
    preguntas = ["¿como estas?", "¿que tal?"]
    sal.capitalize()
    for x in saludos:
        if(sal.find(x)>=0):
            print("\nHola", nom)
            engine.say('Hola'+nom)
            engine.runAndWait()
            break
    for x in preguntas:
        if(sal.find(x)>=0):
            print('\nEstoy muy bien, ¡gracias!')
            engine.say('Estoy muy bien, ¡gracias!')
            engine.runAndWait()
            break
def info(emp):
  if(emp.disponibilidad==1):
    fecha = emp.plazo
    print("\nseñor(a)", emp.nombre, "usted tiene 1 tarea asignada para la fecha: ", fecha, "\nDescripcion de la tarea: ", emp.desctarea, "\n","Dias solicitados: ",emp.diaspedidos)
    if(len(emp.res)>0):
        print("Solucion al problema: ", emp.res)
        emp.res = ""
    engine.say('señor(a)' + emp.nombre + 'usted tiene 1 tarea asignada para la fecha en pantalla')
    engine.say('¿en que puedo ayudarte?')
    engine.runAndWait()
  else:
    print("\nNo tiene tareas asignadas, vuelva mas tarde.")
    engine.say('No tiene tareas asignadas, vuelva mas tarde.')
    engine.runAndWait()
    despedida()
#PARA JEFES


def desempeniof(x):
  for e in empleados:
    if (e.id_jefe == x.idj):
       porcentajeres = (e.tareasenviadasatiempo*100)/e.totaldetareas
       porcentajecal = e.calidad
       command_results.input['tareasatiempo'] = porcentajeres
       command_results.input['calidad'] = porcentajecal
       command_results.compute()
       command.view(sim=command_results)
       
       print("\nEl desempeño de", e.nombre, "es de un", command_results.output['command'],"%")
       if(command_results.output['command']<40):
           print("Es un empleado deficiente\n")
       elif(command_results.output['command']<75):
           print("Es un empleado promedio\n")
       else:
           print("Es un empleado excelente\n")
        
  saludo3(x)
def error():
  print("\nPor favor, digite los datos correctamente.")
  engine.say('Por favor, digite los datos correctamente.')
  engine.runAndWait()
def nuevatarea(x):
  for e in empleados:
    if (e.disponibilidad == 0):
      engine.say('le asignare la tarea a'+e.nombre+'que esta disponible. Acontinuacion por favor digite la fecha')
      engine.runAndWait()
      print("\nLe asignare la tarea a", e.nombre, "que esta disponible")
      print("A continuacion por favor digite la fecha")
      dia = int(input("Dia:"))
      while (dia<0 and dia>31):
        error()
        dia = int(input("\nDia:"))
      mes = int(input("Mes:"))
      while(mes>12 or mes<0):
        error()
        mes = int(input("\nMes:"))
      anio= int(input("Año:"))
      while (anio>2020 or anio<2019):
        error()
        anio = int(input("\nAnio: "))
      e.plazo = date(anio, mes, dia)
      engine.say('Haga una breve descripcion de la tarea')
      engine.runAndWait()
      desc = input(str("\nDescripcion de la tarea:"))
      e.desctarea = desc
      e.disponibilidad = 1
      print("\nTarea asignada")
      engine.say('la tarea ha sido asignada')
      engine.runAndWait()
      saludo3(x)
      break
  print("\nLo siento, ", x.nombre, "no hay ningun empleado disponible...")
  engine.say('Lo siento'+x.nombre+'no hay ningun empleado disponible')
  engine.runAndWait()
  saludo3(x)
def actsenviadas(x):
  for a in empleados:
    if (a.id_jefe == x.idj):
      print(a.nombre, ":",a.link1, "\n")
  saludo3(x)
def SoldePlazo(x):
  for a in empleados:
    if (a.id_jefe == x.idj):
      if(a.diaspedidos>0):
        engine.say(a.nombre+' solicita una extencion de '+ str(a.diaspedidos)+' dias')
        engine.say('¿Autoriza aplazar la fecha de entrega?')
        engine.runAndWait()
        print(a.nombre, "solicita una extencion de ", a.diaspedidos, "dias")
        print("¿Autoriza aplazar la fecha de entrega ", a.diaspedidos, "dias?")
        acept = input()
        if (acept == "si"or acept=="SI"):
          fecha = a.plazo
          dias = timedelta(days=a.diaspedidos)
          fechamasdias= fecha+dias
          a.plazo = fechamasdias
          a.diaspedidos = 0
        else:
          engine.say('No se ha aceptado su solicitud de ampliacion del plazo')
          print("No se ha aceptado su solicitud de ampliacion del plazo")
          engine.runAndWait()
          a.diaspedidos = "No se ha aceptado su solicitud de ampliacion del plazo"
          a.diaspedidos = 0
  saludo3(x)
def problemasjefe(x):
  for a in empleados: 
    if (a.id_jefe == x.idj):
      if (len(a.pro)>1):
        print("\nEl empleado", a.nombre, "describio el siguiente inconveniente: \n")
        engine.say('El empleado'+a.nombre+'describio el siguiente inconveniente: ')
        print(a.pro)
        print("\nIngrese su respuesta: ")
        engine.say('Ingrese su respuesta')
        respuestajefe= input()
        a.res = respuestajefe
        a.pro = ""
        print("\nSu respuesta ha sido enviada!")
        engine.say('su respuesta ha sido enviada')
        engine.runAndWait()
  print("\nNo tiene mas solicitudes")
  engine.say('no tiene mas solicitudes')
  engine.runAndWait()
  saludo3(x) 
def deteccionjefe(clave, x):
  if(clave == "ActsEnviadas"):
    actsenviadas(x)
  if(clave == "SoldePlazo"):
    SoldePlazo(x)
  if (clave == "problemas"):
    problemasjefe(x)
  if(clave == "nuevtarea"):
    nuevatarea(x)
  if (clave == "desempeno"):
    desempeniof(x)
  if(clave == "salir"):
    engine.say('Ha sido un gusto. Hasta pronto')
    print("Ha sido un gusto. Hasta pronto")
    engine.runAndWait()
    main()
def agregarjefes2(clave, agr, a):
  print("\nLo tendre en cuenta para un futuro!")
  engine.say('Lo tendre en cuenta para un futuro!')
  agre = agr.split()
  for x in agre:
    if (len(x)<=2 or x=="los" or x=="las" or x=="unos" or x=="unas" or x == "necesito" or x == "quiero" or x == "actividad"):
      a = agre.index(x)
      agre.pop(a)
  for c,v in peticionesjef.items():
    if (c == clave):
      for x in agre:
        v.append(x)
  engine.runAndWait()
  deteccionjefe(clave, a)
def agregarjefe(agr, peticion, x):
  agr.capitalize()
  for c,v in peticionesjef.items():
    for va in v:
      if (agr.find(va)>=0):
        if (c == "ActsEnviadas"):
          agregarjefes2("ActsEnviadas", peticion, x)
          break
        if (c == "SoldePlazo"):
          agregarjefes2("SoldePlazo", peticion, x)
          break
        if (c == "problemas"):
          agregarjefes2("problemas", peticion, x)
          break
        if (c == "nuevtarea"):
          agregarjefes2("nuevtarea", peticion, x)
        if (c == "desempeno"):
          agregarjefes2("desempeno", peticion, x)
        if(c == "salir"):
          agregarjefes2("salir", peticion, x)
def despedidajefe():
  engine.say('Supongo que eso es todo! hasta pronto')
  print("\nSupongo que eso es todo! hasta pronto")
  engine.runAndWait()
  main()
def nocompjefe(peticionjefe, x):
  engine.say('No he logrado comprender tu peticion. ')
  engine.runAndWait()
  agr = input(str("\nNo he logrado comprender tu peticion. ¿quieres ver las actividades enviadas, ver las solicitudes de ampliacion de plazos, ver los problemas que tienen tus empleados, asignar alguna tarea o ver el desempenio de sus empleados? \n"))
  agregarjefe(agr, peticionjefe, x)
def soons2(son2, clave, peticion, x):
  if(son2 == "si" or son2 == "SI" or son2 == "sI"):
    deteccionjefe(clave, x)
  else:
    nocompjefe(peticion, x)
def saludo3(x):
  engine.say('¿Desea que lo ayude en algo mas?')
  engine.runAndWait()
  print("\n¿Desea que lo ayude en algo mas?")
  res = input()
  if (res == "si" or res == "SI"):
    saludo2(x)
  else:
    despedidajefe()
def saludo2(x):
  peticionjefe = input()
  peticionjefe.capitalize()
  for c,v in peticionesjef.items():
    for va in v:
      if (peticionjefe.find(va)>=0):
        if(c == "ActsEnviadas"):
          engine.say('¿Desea ver las actividades enviadas de sus empleados?')
          engine.runAndWait()
          son2 = input(str("\n¿Desea ver las actividades enviadas de sus empleados?"))
          soons2( son2, c, peticionesjef, x)
          break
        if(c == "SoldePlazo"):
          engine.say('¿Desea ver las solicitudes de ampliacion de plazos de sus empleados?')
          engine.runAndWait()
          son2 = input(str("\n¿Desea ver las solicitudes de ampliacion de plazos de sus empleados?"))
          soons2( son2, c, peticionesjef, x)
          break
        if(c == "problemas"):
          engine.say('¿Desea ver los inconvenientes que tienen sus empleados?')
          engine.runAndWait()
          son2 = input(str("\n¿Desea ver los inconvenientes que tienen sus empleados?"))
          soons2( son2, c, peticionesjef, x)
          break
        if (c == "nuevtarea"):
          engine.say('¿Desea asignar una nueva tarea?')
          engine.runAndWait()
          son2 = input(str("\n¿Desea asignar una nueva tarea?"))
          soons2(son2, c, peticionesjef, x)
          break
        if (c == "desempeno"):
          engine.say('¿Desea ver el desempenio de sus empleados?')
          engine.runAndWait()
          son2 = input(str("\n¿Desea ver el desempenio de sus empleados?"))
          soons2(son2, c, peticionesjef, x)
          break
        if (c == "salir"):
          engine.say('¿Esta seguro que desea salir?')
          engine.runAndWait()
          son2 = input(str("\n¿Esta seguro que desea salir?"))
          soons2(son2, c, peticionesjef, x)
          break
  nocompjefe(peticionjefe, x)
def saludo1jefe(x):
  engine.say('Puedo ayudarlo en estas acciones')
  print("Jefe", x.nombre, "Puedo ayudarlo en:\nVer actividades enviadas de sus empleados\nVer solicitudes de ampliacion de plazos\nVer problemas de los empleados\nAsignar nueva tarea\nVer desempenio de sus empleados\n¿En que puedo ayudarlo?")
  engine.runAndWait()
  saludo2(x)
#MAIN
def main():
  print("-------------------------------------------------------------------")
  print("                     HOLA, ME LLAMO JUCAGI                          ")
  print("--------------------------------------------------------------------")
  eoj = input()
  if (eoj == "902/"):
    idemp = int(input(""))
    for x in empleados:
      if(x.eid == idemp):
        name = x.nombre
        salu = input()
        saludo(salu, name)
        info(x)
        peticion=input()
        peti(peticion, x)
    print("No se reconoce la informacion")
    engine.say('No se reconoce la informacion')
    engine.runAndWait()
    main()
  elif (eoj == '442/'):
    idjef = int(input(""))
    for j in jefes:
      if (j.idj == idjef):
        name = j.nombre
        salu = input()
        saludo(salu, name)
        saludo1jefe(j)
        saludo2(j)
    print("No se reconoce la informacion")
    engine.say('No se reconoce la informacion')
    engine.runAndWait()
    main()   
  else:
    print("No es trabajador de la empresa.")
    engine.say('No es trabajador de la empresa.')
    engine.runAndWait()
    main()
  
if __name__ == "__main__":
    main()