# Distribuidor de grupos: Sacramentos UC
---
## Requisitos
* Python
* Gurobi

---
## Archivos y formatos
Para generar los grupos el programa requiere de tres archivos .tsv, los que deben tener los campos *nombre, apellido, sexo, horarios disponibles*. En este excel(https://drive.google.com/file/d/1VXz2IgYSwCKxqSeecjwfW0LS7uaTCUbA/view?usp=sharing) pueden encontrar un ejemplo de un formato tipo.

---
## Ejecutar el programa

### Modificar datos de posicion
En *standarize.py* se tienen que cambiar las lineas de los datos:
* _file: Ruta al archivo .tsv
* _gender: Columna en la que se encuentra el sexo de la persona (se parte contando desde 0)
* _name: Columna en la que esta el nombre, se espera que el apellido este a su derecha (se parte contando desde 0)
* _schedule: Columna en la que comienza el calendario de disponibilidad (se parte contando desde 0)

Tomando el archivo de los catequistas como ejemplo, sus lineas debieran ser:
``` python
catechists_file = '1_sem_2021/catequistas.tsv'
catechists_gender = 2
catechists_name = 0
catechists_schedule = 6
```
### Ejecucion
Debe ejecutar el codigo *gurobi_model.py* para generar los grupos

---
---
# Modelo

## Datos
* c: Campus --> [0, 4]
* f: Catequista mujer --> [lista mujeres]
* h: Catequista hombre --> [lista hombres]
* m: Modulo --> [0, 34]
* o: Confirmando --> [lista confirmandos]
* t: Asesor --> [lista asesores]
* $$
* d<sup>p</sup><sub>c, m</sub>: 1 si la persona *p* esta disponible en el campus *c* en el modulo *m*, 0 en otro caso



## Variables
* P^{h, f}_(c, m)

## FO
\sum
