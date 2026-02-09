import pandas as pd
import numpy as np
from fractions import Fraction
import pyodbc
import warnings 

# Settings the warnings to be ignored 
warnings.filterwarnings('ignore') 

connection = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=BDSQROPRODB;'
    'DATABASE=BODESA_DWH;'
    'Trusted_Connection=yes'
)
start_date = '01/01/2024'
end_date = '01/12/2024'
iIdCentro0 = 203
iIdCentro1 = 204

Historico_fecha= start_date + '_' + end_date
Tienda='***'

with open("informacion.sql", "r", encoding="utf-8") as file:
    query = file.read()
    
params = (
    start_date,
    end_date,
    iIdCentro0,
    iIdCentro1
)

df = pd.read_sql(query, connection, params=params)

connection.close()

Excel_resultadosGpoTA = pd.DataFrame()
Excel_resultadosGpoTB = pd.DataFrame()
Excel_resultadosTA = pd.DataFrame()
Excel_resultadosTB = pd.DataFrame()
df=df.sort_values(by='Cuenta')
##df=df.sort_values(by='Cuenta', ascending=False)
cuentas_unicas = df['Cuenta'].drop_duplicates().rename_axis('Eliminar').reset_index()


for c in list(range(len(cuentas_unicas))):
    ccuenta = cuentas_unicas['Cuenta'][c]
    df_parte = df[df.Cuenta == ccuenta]
    históricoCompras = list(df_parte['CodGpoArt'])#.drop_duplicates())
    productos_comprados = len(históricoCompras)

    if productos_comprados > 0:
        us_genero = df_parte.iloc[0, 1]
        us_edad = df_parte.iloc[0, 2]
        us_cappago = df_parte.iloc[0, 6]

        df_registros = pd.DataFrame()
        for i in range(productos_comprados):
            df_cuenta_productos = df[df.CodGpoArt == históricoCompras[i]]
            df_registros = pd.concat([df_registros, df_cuenta_productos], ignore_index=True)

        df_registros = df_registros.sort_values(by=['Cuenta'])
        df_registros = df_registros[df_registros.Cuenta != ccuenta].sort_values(by=['Cuenta'])

        df_registros_b = pd.DataFrame(data=df_registros[['Cuenta', 'Genero', 'Edad', 'CapacidadPago']],
                                      columns=['Cuenta', 'Genero', 'Edad', 'CapacidadPago']).reset_index(drop=True)

        # Filter by gender, age range, and payment capacity range
        df_registros_b2 = df_registros_b[(df_registros_b['Genero'] == us_genero) &
                                         (df_registros_b['Edad'] >= us_edad - 4) &
                                         (df_registros_b['Edad'] <= us_edad + 4) &
                                         (df_registros_b['CapacidadPago'] >= us_cappago - 200) &
                                         (df_registros_b['CapacidadPago'] <= us_cappago + 200)]

        cuentasABuscar = df_registros_b2.Cuenta.unique()
        productosSeleccionador = df[df['Cuenta'].isin(cuentasABuscar)]
        productosSeleccionador2 = productosSeleccionador[productosSeleccionador['CodGpoArt'].isin(históricoCompras)]
        productosSeleccionador2_sinduplicados = productosSeleccionador2.drop_duplicates()

        productosSeleccionador3 = productosSeleccionador2_sinduplicados.copy()
        productosSeleccionador3['SoloDepa'] = productosSeleccionador3['CodDepa'].astype(int)

        Depas_TA = [13, 10, 37, 38, 15, 8, 16, 35, 30, 44, 25]
        productosseleccionadosGpo_TA = productosSeleccionador3[productosSeleccionador3['SoloDepa'].isin(Depas_TA)]
        productosseleccionadosGpo_TB = productosSeleccionador3[~productosSeleccionador3['SoloDepa'].isin(Depas_TA)]

        Gpo_TA = pd.DataFrame(productosseleccionadosGpo_TA['CodGpoArt'].value_counts(ascending=False))
        Gpo_TA = Gpo_TA.rename_axis('CodGpoArt').reset_index()
        total_count = Gpo_TA['count'].sum()
        

        TA=productosseleccionadosGpo_TA['SoloDepa'].value_counts(ascending=False)
        TA = TA.rename_axis('Dep').reset_index()
        total_countDP = TA['count'].sum()

        Gpo_TA['Support'] = Gpo_TA['count'] / total_count
        TA['Support'] = TA['count'] / total_countDP

        total =[]
        for i in Gpo_TA['count']:
            total.append(total_count)
        Gpo_TA['TotEnt'] = total

        total =[]
        for i in TA['count']:
            total.append(total_countDP)
        TA['TotEnt'] = total
 

        Gpo_TB = pd.DataFrame(productosseleccionadosGpo_TB['CodGpoArt'].value_counts(ascending=False))
        Gpo_TB = Gpo_TB.rename_axis('CodGpoArt').reset_index()
        total_countB = Gpo_TB['count'].sum()

        TB=productosseleccionadosGpo_TB['SoloDepa'].value_counts(ascending=False)
        TB = TB.rename_axis('Dep').reset_index()
        total_countBDP = TB['count'].sum()

        Gpo_TB['Support'] = Gpo_TB['count'] / total_countB
        TB['Support'] = TB['count'] / total_countBDP

        total =[]
        for i in Gpo_TB['count']:
            total.append(total_count)
        Gpo_TB['TotEnt'] = total

        total =[]
        for i in TB['count']:
            total.append(total_countDP)
        TB['TotEnt'] = total

        # Get the top two most frequent articles in each group
        most_frequent_TA = productosseleccionadosGpo_TA['CodGpoArt'].value_counts().nlargest(2).index
        most_frequent_TB = productosseleccionadosGpo_TB['CodGpoArt'].value_counts().nlargest(2).index
     
        Gpo_TA = Gpo_TA[['CodGpoArt', 'Support', 'count', 'TotEnt']].head(10).rename_axis('Orden').reset_index()
        Gpo_TB = Gpo_TB[['CodGpoArt', 'Support', 'count', 'TotEnt']].head(10).rename_axis('Orden').reset_index()

        TA = TA[['Dep', 'Support', 'count', 'TotEnt']].head(10).rename_axis('Orden').reset_index()
        TB = TB[['Dep', 'Support', 'count', 'TotEnt']].head(10).rename_axis('Orden').reset_index()

        # Concatenate the results for Gpo_TA, Gpo_TB, TA, and TB with the corresponding columns
        Excel_resultadosGpoTA = pd.concat([Excel_resultadosGpoTA, pd.DataFrame({
            'AnalisisID': Historico_fecha,
            'Cuenta': ccuenta,
            'Negocio': 1,
            'CodGpoArt': Gpo_TA['CodGpoArt'],
            'Orden': Gpo_TA['Orden'],
            'count': Gpo_TA['count'],
            'TotEnt':total_count,
            'Support': Gpo_TA['Support'],
            'EtiquetaDepa': 'Ticket Alto',
            'Region': Tienda
        })], ignore_index=True)

        Excel_resultadosGpoTB = pd.concat([Excel_resultadosGpoTB, pd.DataFrame({
            'AnalisisID': Historico_fecha,
            'Cuenta': ccuenta,
            'Negocio': 1,
            'CodGpoArt': Gpo_TB['CodGpoArt'],
            'Orden': Gpo_TB['Orden'],
            'count': Gpo_TB['count'],
            'TotEnt':total_countB,
            'Support': Gpo_TB['Support'],
            'EtiquetaDepa': 'Ticket Bajo',
            'Region': Tienda
        })], ignore_index=True)


        Excel_resultadosTA = pd.concat([Excel_resultadosTA, pd.DataFrame({
            'AnalisisID': Historico_fecha,
            'Cuenta': ccuenta,
            'Negocio': 1, 
            'CodDepa':TA['Dep'], 
            'Orden':TA['Orden'],
            'count':TA['count'],
            'TotEnt':total_countDP,
            'Support': TA['Support'],
            'EtiquetaDepa':'Ticket Alto', 
            'Region':Tienda 
        })], ignore_index=True)

        Excel_resultadosTB = pd.concat([Excel_resultadosTB, pd.DataFrame({
            'AnalisisID': Historico_fecha,
            'Cuenta': ccuenta,
            'Negocio': 1, 
            'CodDepa':TB['Dep'], 
            'Orden':TB['Orden'],
            'count':TB['count'],
            'TotEnt':total_countBDP,
            'Support': TB['Support'],
            'EtiquetaDepa':'Ticket Bajo', 
            'Region':Tienda 
        })], ignore_index=True)


