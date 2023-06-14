Human Counter

Descripción.
Implementación del algoritmo YOLO v3 para la detección y conteo de personas. Forma parte del proyecto final del de Diplomatura Universitaria en Data Science dicatada por mundos E. El Objeto del proyecto es utilizar el algoritmo YOLO para realizar un conteo del trafico de personas frente diferentes locales comerciales. El conteo de personas frente a cada local comercial queda registrado en una única tabla. Los datos obtenidos forman un dataset para ser analizados en una segunda etapa con el objetivo de proporcionar metricas objetivas para la toma de decisiones basada en datos en areas tales como 
1)Información precisa sobre el tráfico de personas
2)Valuación de Alquileres basada en datos
3)Optimización del espacio
4) etc.

Configuración previa al uso.
Dentro de la carpeta "utils" se enciuentra el fichero config.py. En el se puede configurar:
a) URL de la cámara de vigilancia (input_url)
b) El intervalo de tiempo en el que se realizara una captura del video para realizar el conteo. El valor es expresado en segundos (interval).
c)Valor de Confianza. Este valor configura el umbral de confianza para considerar valida una detección. Toma valores entre 0 y 1. Se recomienda valores en torno a 0.5, ya que valores mas altos omitiria del conteo a un numero significativo de deteciones (confidence_val)
d)Url de la base de datos remota
e)Identificador del local. Este se encuentra registrado previamente en la base de datos dentro de la tabla "locations"

Es requisito descargar el archivo yolov3.weights de la siguiente url:https://pjreddie.com/darknet/yolo/. listado de dentro de versiones YOLOv3-416 y hacer click en el enlace weights perteneciente a la fila del mismo. 

Ejecución y opciones de flags
Dentro del directorio se ejecuta el comando "python persons_counter.py" 
sin flags se ejecuta sin imprimir en la terminal, salvo en el caso que se de un error con la conexión a la URL de destino.
adicionalment se puede ejecutar el script con los siguientes flags:
-v o --verbose: Se imprimira en pantalla los resultados del conteo para cada cuadro, la fecha y hora del conteo y el tiempo que tomo el proceso de analisis del cuadro. Ejemplo de uso  "python persons_counter.py -v" o "python persons_counter.py --verbose".
-d o --video: Con este flag se mostrará en pantalla el feed de video de la camara en una ventana y la captura del cuadro analizado. Hasta que no se obtenga una deteccion el cuadro de captura no se mostrará y se actualizara cuando ocurra una nueva detección. Ejemplo de uso  "python persons_counter.py -d" o "python persons_counter.py --video".
-s o --save: Al utilizarse esta opción se habilita a que los cuadros capturados se almacenen dentro del directorio "imgs". Las imagenes se mantendran grabadadas durante y luego de la ejecución del programa. Si se inicia posteriormente el programa sin el flag de save las imagenes serán borradas, por lo que se recomienda mover las imagenes de interés a otro directorio. Ejemplo de uso  "python persons_counter.py -s" o "python persons_counter.py --save".
Los flags pueden usarse de manera individual o en conjunto. Ejemplo de uso  "python persons_counter.py -v -d -s"

Para salir de la ejecución presionar ctrl+C, o la letra q cuando se ejecute mostrando las ventanas de video.




