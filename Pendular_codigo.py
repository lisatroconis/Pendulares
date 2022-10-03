# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 14:38:56 2022

@author: Lisa
"""
import os
import pandas as pd

# Selección de directorio
os.chdir("C:/Users/Lisa/Documents/Bases de Python/Salud")

#extraigo la base de datos 
tran = pd.read_excel("C:/Users/Lisa/Documents/Bases de Python/Salud/Pendular.xlsx", sheet_name= 'Hoja1')

#reviso las columnas que contiene el dataset
tran.columns

#Genero un subconjunto de la base de datos con las columnas que requiero
tran_s= tran[['hhid','start','I1_req_salud_atencion_med', 'I1_req_salud_vacunaci', 'I1_req_salud_salud_oral', 'I1_req_salud_implemen',
              'I1_req_salud_atencion','I1_req_salud_anticonc', 'I12_enferm_hipertens','I12_enferm_diabetes','I12_enferm_vih','I12_enferm_renales',
              'I12_enferm_cancer','I12_enferm_cardiovascular','I14_enferm_transm_saludment','I14_enferm_transm_tuberc',
              'I14_enferm_transm_sifilis', 'I14_enferm_transm_dengue', 'I14_enferm_transm_leishma','I14_enferm_transm_asma',
              'I14_enferm_transm_epoc','I14_enferm_transm_varicela','I15_neces_salud_sex_anticoncep','I15_neces_salud_sex_preserva',
              'I15_neces_salud_sex_atenci_gest','I15_neces_salud_sex_ginecolo','I15_neces_salud_sex_aborto','I15_neces_salud_sex_controles',
              'I16_s_sintomas_miedo','I16_s_sintomas_rabia','I16_s_sintomas_incertidumbre','I16_s_sintomas_no_sueno',
              'I16_s_sintomas_ansiedad','I16_s_sintomas_depres','I16_s_sintomas_autodano']]

#Estas variables no estan correspondidas en la base de datos.
#'I12_enferm_epoc','I12_enferm_leishmaniasis','I12_enferm_dengue','I12_enferm_sifilis','I12_enferm_tuberculosis','I12_enferm_saludmental'

#agrupo por grupo y sumo los resultados, ya que existe mas de una respuesta por grupo. 
group_sum = tran_s.groupby(by="hhid", dropna=False).sum()

#Cuento numero de grupos (#numero de filas)
n_groups = len(group_sum.axes[0])
 
#Quito la columna grupo como index y la convierto en columna 
group_sum= group_sum.reset_index()

#Reviso que sea un dataframe
type(group_sum)

#Todos los valores mayores o iguales a 1 convertirlos en 1 
group_sum.set_index('hhid',inplace=True)
group_sum[group_sum >= 1] = 1

#Total porcentaje por columna
group_sum.loc['Porcen',:]= ((group_sum.sum(axis=0))/n_groups)

#Total conteo por columna
group_sum.loc['Total',:] = group_sum.iloc[0:(n_groups-1) ,:].sum(axis = 0)

#Selecciono las tablas para generar los graficos
graficos_porc = group_sum.iloc[n_groups:(n_groups + 1),:]
graficos_abs = group_sum.iloc[(n_groups + 1):(n_groups + 2),:]

#Genero un nuevo subconjunto de datos 
edad = tran[['hhid', 'mem_A5_edad']]

#generar nuevas columnas para agregar 1 si cumple con la condicion.

# method 1
#edad['0 a 5'] = np.where(edad[(edad['mem_A5_edad']>0) and (edad['mem_A5_edad']<=5)], '1', '0')

#Seleccionar en que categoria pertenece cada edad
rating = []
for row in edad['mem_A5_edad']:
    if row <= 5 : rating.append('0 a 5')
    elif (row >= 6 and row <=11) : rating.append('6 a 11')
    elif (row >= 12 and row <=17) : rating.append('12 a 17')
    elif (row >= 18 and row <=28) :   rating.append('18 a 28')
    elif (row >= 29 and row <=59) :   rating.append('29 a 59')
    elif  row >= 60 :   rating.append('mayor 60')
    
    else: rating.append('Not_Rated')

#generar la nueva columna con las categorias
edad['rating'] = rating

#generar las variables dicotomicas para cda categoria
dummies = pd.get_dummies(edad['rating'])

#Concatenar las nuevas columnas con el dataframe original 
edad = pd.concat([edad, dummies], axis=1)

#crear nuevo dataset removiendo columnas
edad.drop(edad.columns[[1,2]], axis=1, inplace=True)

edad.columns
edad = edad[['hhid', '0 a 5', '6 a 11', '12 a 17', '18 a 28', '29 a 59', 'mayor 60']]

#agrupo por grupo y sumo los resultados, ya que existe mas de una respuesta por grupo. 
edad_sum = edad.groupby(by="hhid", dropna=False).sum()

#Cuento numero de grupos (#numero de filas)
n_edad = len(edad_sum.axes[0])
 
#Quito la columna grupo como index y la convierto en columna 
edad_sum  = edad_sum.reset_index()

#Reviso que sea un dataframe
type(edad_sum)

#Todos los valores mayores o iguales a 1 convertirlos en 1 
edad_sum.set_index('hhid',inplace=True)
edad_sum[edad_sum >= 1] = 1

#Total porcentaje por columna
edad_sum.loc['Porcen',:]= ((edad_sum.sum(axis=0))/n_edad)

#Total conteo por columna
edad_sum.loc['Total',:] = edad_sum.iloc[0:(n_edad-1) ,:].sum(axis = 0)

#Selecciono las tablas para generar los graficos
graficos_porce = edad_sum.iloc[n_edad:(n_edad + 1),:]


Writer= pd.ExcelWriter("C:/Users/Lisa/Documents/Bases de Python/Bases Actualizables/tabla_salud_pendular.xlsx")

tran.to_excel(Writer, sheet_name='basecruda.xlsx')
group_sum.to_excel(Writer, sheet_name='Tablas.xlsx')
graficos_porc.to_excel(Writer, sheet_name='graficos_porc.xlsx')
graficos_abs.to_excel(Writer, sheet_name='graficos_abs.xlsx')
edad_sum.to_excel(Writer, sheet_name='edad sum.xlsx')
graficos_porce.to_excel(Writer, sheet_name='graficos_porc_edad.xlsx')

Writer.save()


