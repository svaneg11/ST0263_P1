# ST0263_P1
Proyecto1 Topicos Especiales en Telematica

1. Ubicarse en la carpeta ST0263_P1

```cd ST0263_P1```

2. Instalar los archivos de requirements.txt

```pip install -r requirements.txt```

# Como testear el nodo de BD (Single server)

1. Correr con python el archivo  ST0263_P1/node/main_server.py -p ##, siendo ## un número de puerto 
    por el cual se desee correr el servidor

2. Correr el programa ST0263_P1/main_client.py -h host -p puerto, donde el host se puede dejar en blanco y tomará 
    como predeterminado el localhost o el 127.0.0.1 y el número de puerto se debe indicar el indicado por el servidor

3. Hacer las pruebas que quiera usando los métodos get, set o delete.

# Como testear en modo cluster la BD

1. Correr con python el archivo  ST0263_P1/node/main_server.py -p ##, siendo ## un número de puerto 
    por el cual se desee correr el servidor. Se hace esto para cada nodo

2. Correr con python el archivo  ST0263_P1/node/main_server.py -c ## 'nombre'. Siendo ## el número de puerto que se desee,
    en este puerto estará el servidor de frontend, y 'nombre' un nombre cualquiera que se le debe dar al cluster. Este nombre
    es fundamental para recuperar los datos, ya que con este nombre se almacenan los nodos participes en el sistema de base de 
    datos distribuida.

3. Correr el programa ST0263_P1/main_client.py -h host -p puerto, donde el host se puede dejar en blanco y tomará 
    como predeterminado el localhost o el 127.0.0.1 y el número de puerto se debe indicar el indicado por el servidor. En este caso se especifica el puerto del servidor front-end, los comandos son similares al modo single-node.

## Comando para el main_client.py

- get key -> obtiene el valor especificado por key
- set key value -> almacena value con la clave key
- delete key -> elimina la clave key
- out -> sale del programa cliente

Nota: para ver todos los redireccionamientos de la base de datos redistribuida se puede ver la terminal del servidor front end
    , en este momento solo los envía al último nodo por un problema de hotspots al usar la función hash() de python.

## Documentacion de endpoints con OpenAPI
Mientras el servidor corre abrir el navegador y acceder a
```host:port/docs```