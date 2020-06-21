![](./images/logos_feder.png)

| Documento | [Métricas FAIR](README.md) - Documentación técnica           |
| --------- | ------------------------------------------------------------ |
| Fecha     | 25/05/2020                                                   |
| Proyecto  | [ASIO](https://www.um.es/web/hercules/proyectos/asio) (Arquitectura Semántica e Infraestructura Ontológica) en el marco de la iniciativa [Hércules](https://www.um.es/web/hercules/) para la Semántica de Datos de Investigación de Universidades que forma parte de [CRUE-TIC](http://www.crue.org/SitePages/ProyectoHercules.aspx) |
| Módulo    | Infraestructura Ontológica                                   |
| Tipo      | Documentación técnica                                        |

# Métricas FAIR - Documentación técnica

El presente documento describe en detalle el proceso de desarrollo del software despliegue de entorno, generación e inserción de datos en el entorno y la creación resultados gráficos del análisis de métricas FAIR.
## Entorno de desarrollo
Ver [manual de despliegue](manual_despliegue.md).
## Librerías empleadas

Para el desarrollo de este módulo software se han empleado 3 librerías Python, en concreto:

```
requests==2.23.0
cryptography==2.9.2
numpy==1.18.4
pandas==1.0.3
more-itertools
rdflib==5.0.0
validators==0.15.0
plotly==4.7.1
```

## Fases del proyecto

El proyecto consta de tres fases

### Evaluación de métricas

Se realizara la evaluación de las métricas FAIR, sobre la arquitectura real usada en el proyecto ASIO, para ello el proyecto permite desplegar las partes relevantes de dicha arquitectura de forma local mediante el despliegue del [Sandbox](#Sandbox)

#### Sandbox

Para generar un nuevo conjunto de métricas es necesario desplegar un entorno que emula las partes relevantes del proyecto ASIO, que influyen en la evaluación de las métricas FAIR. Estas son:

- **Factoría de URIs:** Este componente software que genera los identificadores para los recursos, y añade un nivel de indirección que permite gestionar la persistencia (cambio de el contenido de un recurso, manteniendo su identificador publico, después de que el recurso haya cambiado), por lo que es relevante en todos aquellas métricas donde de una forma u otra, se evalúa la persistencia de los recursos y/o sus identificadores.
- **MariaDB:** Es la capa de persistencia usada por la factoría de URIs y por lo tanto es una dependencia de esta.
- **Trellis:** Es el servidor LDP que soporta el acceso a los recursos, soportando negociación de contenido tanto en formato como en versión, generando a su vez metadatos, orientados a la auditoria de datos, y versionado de recursos(Memento). Es de vital importancia para la evaluación de métricas FAIR ya que tanto los recursos y metadatos que serán evaluados, lo serán en el formato gestionado por Trellis.
- **Fuseki + TDB:** Fuseki actúa como EndPoint SPAPQL 1.1, y TDB es el Triple Store que soporta el almacenamiento. Aunque no será evaluado directamente, es el motor de almacenamiento y acceso a datos usado por Trellis, por lo que es un fuerte dependencia de este.

### Generación de datos

Sobre la arquitectura antes descrita, se generaran conjuntos de datos sintéticos de todos los tipos que estarán presentes en los datos reales, es decir se generan entidades, propiedades e instancias. Sobre dichos conjuntos de datos se realizará la evaluación de métricas FAIR.

### Representación de métricas y resultados finales

Las métricas evaluadas sobre los datos  generaran los KPIs y sus representaciones.

## Pruebas unitarias

Para generar los resultados de la evaluación de pruebas unitarias del software de métricas FAIR es necesario ejecutar el siguiente comando:

```
python unit_test.py
```

### Definición de casos de prueba

```
------------------------------TEST1------------------------------
FINDABLE -> ningún esencial -> 0
ACCESSIBLE -> tiene todos los importantes y útiles, pero ningún esencial -> 0
INTEROPERABLE -> tiene  menos del 50 % de los importantes y todos los útiles -> 1
REUSABLE -> tiene todos los esenciales y todos los útiles, pero menos de la mitad de los importantes -> 1

------------------------------TEST2------------------------------
FINDABLE -> todos los esenciales -> 5
ACCESSIBLE -> tiene todos los esenciales, más de la mitad de los importantes y ningún útil -> 2
INTEROPERABLE -> tiene  todos los importantes y ningún útil -> 3
REUSABLE -> tiene todos los esenciales, todos los importantes y ningún útil -> 3

------------------------------TEST3------------------------------
FINDABLE -> ningún esencial -> 0
ACCESSIBLE -> tiene todos los esenciales, todos los importantes y ningún útil -> 3
INTEROPERABLE -> tiene todos los importantes y más de la mitad de útiles -> 4
REUSABLE -> tiene todos los esenciales, todos los importantes y todos los útiles -> 5

------------------------------TEST4------------------------------
FINDABLE -> todos los esenciales -> 5
ACCESSIBLE -> tiene todos los esenciales, todos los importantes y todos los útiles -> 5
INTEROPERABLE -> tiene todos los importantes y todos los útiles -> 5
REUSABLE -> tiene todos los esenciales, todos los importantes y todos los útiles -> 5
```

### Resultados obtenidos

```bash
Ran 4 tests in 0.427s
OK
```