import funciones
import pandas as pd
import datetime as dt




dic_url = {
            'url_usd' : 'https://api.estadisticasbcra.com/usd',
            'url_usd_of' : 'https://api.estadisticasbcra.com/usd_of',
          }

# Creo Dataframe
print('Carga de datos')
df_usd = pd.DataFrame(funciones.consulta_api(dic_url['url_usd']).json())
print('Falta menos')
df_usd_of = pd.DataFrame(funciones.consulta_api(dic_url['url_usd_of']).json())
print('Carga finalizada\n')
# Renombro Columnas
df_usd.rename({'d': 'Fecha', 'v': 'USD_blue'}, axis= 1, inplace= True)
df_usd_of.rename({'d': 'Fecha', 'v': 'USD_of'}, axis= 1, inplace= True)

# Convierto fechas a tipo datetime
df_usd['Fecha'] = pd.to_datetime(df_usd['Fecha'])
df_usd_of['Fecha'] = pd.to_datetime(df_usd_of['Fecha'])

# Junto los tipos de Dolares en un solo Dataframe
df_usd_total = pd.merge(df_usd_of, df_usd, on= 'Fecha', how= 'left')

df_usd_total.dropna(inplace= True)

fecha_hoy = dt.date.today()
fecha_años = fecha_hoy - dt.timedelta(days=365)

# Reduzco el tamaño del dataframe
df_usd_total = df_usd_total[df_usd_total['Fecha'] >= str(fecha_años)]
print('*************        Comenzemos           *************\n')
dias = 0

while(True):
    print('Ingrese 0 (cero) para Salir')
    while(True):
        try:
            dias = int(input('Ingresar la cantidad de dias: '))
        except:
            print('\nValor incorrecto, ingrese un numero mayor a 0 (cero)!!\n')
        else:
            break
    if dias == 0: break
    of, blue = funciones.pred_regresion(df_usd_total, dias)

    print(f'\nLa prediccion a {dias} días nos dice que el valor del dolar Oficial podria ser de ${of}')
    print(f'La prediccion a {dias} días nos dice que el valor del dolar Blue podria ser de ${blue}\n')

print('\n***     ¡¡¡Gracias por usar la Calculadora!!!     ***')