![](./images/logos_feder.png)

| Documento | [Métricas FAIR](README.md) - Manual de usuario               |
| --------- | ------------------------------------------------------------ |
| Fecha     | 25/05/2020                                                   |
| Proyecto  | [ASIO](https://www.um.es/web/hercules/proyectos/asio) (Arquitectura Semántica e Infraestructura Ontológica) en el marco de la iniciativa [Hércules](https://www.um.es/web/hercules/) para la Semántica de Datos de Investigación de Universidades que forma parte de [CRUE-TIC](http://www.crue.org/SitePages/ProyectoHercules.aspx) |
| Módulo    | Infraestructura Ontológica                                   |
| Tipo      | Manual de usuario                                            |

# Métricas FAIR - Manual de usuario

El presente documento describe en detalle el proceso de desarrollo del software despliegue de entorno, generación e inserción de datos en el entorno y la creación resultados gráficos del análisis de métricas FAIR.

El script main.py es el punto de entrada principal de la aplicación, que invoca a los módulos necesarios para:

- **Desplegar el entorno (Sandbox)**: Es posible indicar que se despliegue mediante una invocación al Script main.py por medio del parámetro -s 

  - **Factoría de URIs:** Este componente software que genera los identificadores para los recursos, y añade un nivel de indirección que permite gestionar la persistencia (cambio de el contenido de un recurso, manteniendo su identificador publico, después de que el recurso haya cambiado), por lo que es relevante en todos aquellas métricas donde de una forma u otra, se evalúa la persistencia de los recursos y/o sus identificadores.
  - **MariaDB:** Es la capa de persistencia usada por la factoría de URIs y por lo tanto es una dependencia de esta.
  - **Trellis:** Es el servidor LDP que soporta el acceso a los recursos, soportando negociación de contenido tanto en formato como en versión, generando a su vez metadatos, orientados a la auditoria de datos, y versionado de recursos(Memento). Es de vital importancia para la evaluación de métricas FAIR ya que tanto los recursos y metadatos que serán evaluados, lo serán en el formato gestionado por Trellis.
  - **Fuseki + TDB:** Fuseki actúa como EndPoint SPAPQL 1.1, y TDB es el Triple Store que soporta el almacenamiento. Aunque no será evaluado directamente, es el motor de almacenamiento y acceso a datos usado por Trellis, por lo que es un fuerte dependencia de este.

- **Generación de datos:** Es posible indicar que se generen los datos mediante una invocación al Script main.py por medio del parámetro -d .El fichero **instances_generator_metadata.json** disponible en la ruta /data, actúa como semilla para generar los  datos que serán insertados en el entorno. Podemos ver la estructura (en formato json) bajo estas líneas

  ```
  [
    {
      "class": "university",
      "language": "en-EN",
      "instances": 3,
      "properties" : [
        "name", "description"
      ],
      "child": [
        {
          "parentProperty": "has-groups",
          "childProperty": "has-university",
          "class": "group",
          "language": "en-EN",
          "instances": 3,
          "properties" : [
            "name", "description"
          ],
          "child": [
            {
              "parentProperty": "has-researchers",
              "childProperty": "has-group",
              "class": "researcher",
              "language": "en-EN",
              "instances": 5,
              "properties" : [
                "name","surname","address"
              ]
            }
          ]
        }
      ]
    }
  ]
  ```

  Los atributos mas relevantes son:

  - class: Nombre de la clase que se generara.
  - Properties: Lista de propiedades que se asociaran a la clase
  - instances: Número de instancias que se crearan para esa clase
  - childs: Lista de clases hijas, que se crearan. Estas clases hijas tienen los mismos atributos que se han descrito.
  - parentProperty: Nombre de la propiedad de el padre que contendrá una lista de los identificadores del padre
  - childPorperty: Nombre de la propiedad que tendrá el hijo, que apuntara a el identificador de la clase padre

  Esto generara tripletas del tipo:

  ~~~
  @prefix as:    <https://www.w3.org/ns/activitystreams#> .
  @prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
  @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
  @prefix ldp:   <http://www.w3.org/ns/ldp#> .
  @prefix skos:  <http://www.w3.org/2004/02/skos/core#> .
  @prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
  @prefix acl:   <http://www.w3.org/ns/auth/acl#> .
  @prefix vcard: <http://www.w3.org/2006/vcard/ns#> .
  @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
  @prefix dc:    <http://purl.org/dc/terms/> .
  
  <http://localhost:8080/researcher/3b4efe41-31f8-44d7-9929-94a2b16bc8dc>
          rdf:type  rdfs:Resource ;
          dc:title  "Instance 3 of class researcher" ;
          <http://hercules.org/um/en-EN/res/name>  "name_3" ;
          <http://hercules.org/um/en-EN/res/has-canonical-uri>  "http://hercules.org/um/en-EN/res/researcher/1675729b-5cb6-3a1f-8efc-ca1f88c75076" ;
          <http://hercules.org/um/en-EN/res/surname>  "surname_3" ;
          <http://hercules.org/um/en-EN/res/address>  "address_3" ;
          <http://hercules.org/um/en-EN/res/has-group>  "2" ;
          rdf:type  ldp:RDFSource .
  
  ~~~

- **Evaluación de métricas:** Siempre se reevaluaran las métricas al invocar el script main.py. Esto generara un fichero con los resultados en la ruta data, llamado  **FAIR_evaluation_out.csv** con lso resultados obtenidos.

* **Generación de visualización:** Es posible indicar que se cree la visualización mediante una invocación al Script main.py por medio del parámetro -v . Esto invocará el script `fairviz.py` se encarga de procesar el fichero CSV (generado en el punto anterior) que contiene los resultados de la evaluación de los indicadores FAIR para generar una gráfica de barras de niveles FAIR por área, así como gráficas radar de progreso por cada indicador, agrupadas por áreas.

Para más información, consultar el documento de [Análisis de métodos FAIR](https://github.com/HerculesCRUE/ib-asio-docs-/blob/master/entregables_hito_1/05-An%C3%A1lisis_de_m%C3%A9todos_FAIR/ASIO_Izertis_AnalisisDeMetodosFAIR.md), donde se especifica la propuesta de metodología de evaluación FAIR, las referencias y el listado de indicadores, siguiendo las indicaciones del grupo de trabajo [FAIR Data Maturity Model](https://www.rd-alliance.org/groups/fair-data-maturity-model-wg) de la [RDA](https://www.rd-alliance.org/).

## Formato de fichero de resultado de evaluación

El formato del fichero de entrada requiere 6 columnas obligatorias:
* **FACET**: el tipo de faceta entre *FINDABLE*, *ACCESSIBLE*, *INTEROPERABLE* y *REUSABLE*
* **PRINCIPLE**: identificador de métrica FAIR asociada
* **INDICATOR_ID**: identificador del indicador según la RDA
* **PRIORITY**: prioridad del indicador entre *Essential*, *Important* y *Useful*
* **METRIC**: indica el nivel de implementación del indicador. Es un entero entre 0 y 4
* **SCORE**: indica si el indicador está totalmente implementado (METRIC = 4) o no (METRIC < 4)

La salida que produce el script consta de cuatro ficheros *HTML* con los gráficos, que son almacenados
en la carpeta *plots*.

## Ejecución

Para generar los resultados de la evaluación de métricas FAIR es necesario ejecutar el siguiente comando:

```bash
python main.py -s -d -v
```

El documento [manual_despliegue](./manual_despliegue.md#Ejecución de generación de métricas FAIR) contiene información detallada sobre el proceso de ejecución.