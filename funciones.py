from logging import warning
import requests
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np


#autentificacion API BCRA
AUTHORIZATION = 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTA5MDAxNzIsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJtYXVyaWNpb3YuaW5ub3ZhQGdtYWlsLmNvbSJ9.b7HcUulJUTey3IJO337EXGX-62ip9xt5qN4OVAWkGJGVk48wLG7uKEYdl-aokCDemfnCn0vdfSaNOEQQeHCLTw'


#Funcion consulta api
def consulta_api(url):
    headers = {'Authorization': AUTHORIZATION, 'content-type': 'application/json'}
    r= requests.get(url= url, headers= headers)
    if(r.status_code == 200):
        return r
    else:
        print('Error:', r.status_code)


# Funcion Generadora de Graficos - Movimiento del Dolar y Eventos
def graficos_eventos(df_usd, df_eventos):
    from matplotlib.dates import DateFormatter, MonthLocator
    x1 = df_usd.Fecha.values
    
    y_usd_of = df_usd.USD_of.values
    y_usd_blue = df_usd.USD_blue.values

    x2 = df_eventos[df_eventos['Fecha'] >= x1.min()].Fecha.values
    y_evento = df_eventos[df_eventos['Fecha'] >= x1.min()].Tipo_Evento.values

    fig = plt.figure(figsize= (20,12))
    ax = plt.axes()

    # Anotaciones
    y_text = 0
    for d, r in zip(x2, y_evento):
        ax.annotate(r, xy=(d, 5), xytext=(-3, y_text),
                textcoords="offset points", ha="right")
        y_text += 10

    
    ax.xaxis.set_major_locator(MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(DateFormatter("%b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    plt.plot(x1, y_usd_of, color='tomato', label= 'USD Oficial')  # estilo de línea  
    plt.plot(x1, y_usd_blue, color='blue', label= 'USD Blue')  # estilo de línea     

    plt.vlines(x2, label= 'Eventos', color= 'orange', ymin= 0, ymax=380)
    ax.set(xlabel= 'Fechas', ylabel= 'Valor Peso (Arg) / USD', title = 'Historico USD y Eventos Politicos-Economicos')
    ax.legend()

    # Rejilla
    ax.grid(color='lightgray', linestyle='dashed')

    return plt.show()


# Funcion de Grafico para Regesion Lineal Dolar Oficial
def grafico_reg_lineal_oficial(df, titulo = 'Regresion (USD Oficial)'):
    from sklearn.linear_model import LinearRegression
    from matplotlib.dates import DateFormatter, MonthLocator

    modelo_usd_of = LinearRegression(fit_intercept= True)
    
    # Convertimos fechas en ordinal para poder trabajar
    df['Fecha_or']=df['Fecha'].map(dt.datetime.toordinal)

    x1 = df.Fecha.values.reshape(-1, 1)
    x1_or =df.Fecha_or.values.reshape(-1, 1)
    y_oficial = df.USD_of.values.reshape(-1,1)
    
    modelo_usd_of.fit(x1_or, y_oficial)
    y_of_pred = modelo_usd_of.predict(x1_or)
    
    #Grafico
    fig = plt.figure()
    ax = plt.axes()

    ax.xaxis.set_major_locator(MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(DateFormatter("%b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    plt.plot(x1, y_oficial, label = 'Movimiento Dolar')
    plt.plot(x1, y_of_pred, label = 'Regresion Lineal')

    ax.set(title= titulo, xlabel = 'Fecha', ylabel = 'Pesos (Arg) / USD')
    ax.legend()
    ax.grid(color= 'lightgray')
        
    return plt.show()


# Funcion de Grafico de Regesion Lineal Dolar Blue
def grafico_reg_lineal_blue(df, titulo = 'Regresion (USD Blue)'):
    from sklearn.linear_model import LinearRegression
    from matplotlib.dates import DateFormatter, MonthLocator

    modelo_usd_blue = LinearRegression(fit_intercept= True)
    
    # Convertimos fechas en ordinal para poder trabajar
    df['Fecha_or']=df['Fecha'].map(dt.datetime.toordinal)

    x1 = df.Fecha.values.reshape(-1, 1)
    x1_or =df.Fecha_or.values.reshape(-1, 1)
    y_blue = df.USD_blue.values.reshape(-1,1)
    
    modelo_usd_blue.fit(x1_or, y_blue)
    y_blue_pred = modelo_usd_blue.predict(x1_or)
    
    #Grafico
    fig = plt.figure()
    ax = plt.axes()

    ax.xaxis.set_major_locator(MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(DateFormatter("%b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    plt.plot(x1, y_blue, label = 'Movimiento Dolar')
    plt.plot(x1, y_blue_pred, label = 'Regresion Lineal')

    ax.set(title= titulo, xlabel = 'Fecha', ylabel = 'Pesos (Arg) / USD')
    ax.legend()
    ax.grid(color= 'lightgray')
        
    return plt.show()


# Funcion para obtener los valores de prediccion de ambos Dolares
def pred_regresion(df, cant_dias):
    import datetime as dt
    from sklearn.linear_model import LinearRegression
    modelo_usd_of = LinearRegression(fit_intercept= True)
    modelo_usd_blue = LinearRegression(fit_intercept= True)

    fecha_hoy = dt.datetime.today()
    fecha = fecha_hoy + dt.timedelta(days= cant_dias)


    # Creo las fechas a predecir
    X_fecha = np.array(fecha.toordinal()).reshape(-1,1)

    # Convertimos fechas en ordinal para poder trabajar
    df['Fecha_or']=df['Fecha'].map(dt.datetime.toordinal)

    x1_or =df.Fecha_or.values.reshape(-1, 1)
    y_oficial = df.USD_of.values.reshape(-1,1)
    y_blue = df.USD_blue.values.reshape(-1,1)

    modelo_usd_of.fit(x1_or, y_oficial)
    modelo_usd_blue.fit(x1_or, y_blue)

    y_of_pred = round(float(modelo_usd_of.predict(X_fecha)), 2)
    y_blue_pred = round(float(modelo_usd_blue.predict(X_fecha)),2)

    return y_of_pred, y_blue_pred   