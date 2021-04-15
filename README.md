# Diversity
![Screenshot](Diversity.jpg)

Este es nuestro Curiosity particular, llamado Diversity, el cual está siendo desarrollado en la Academia DiverBOT.

El proyecto empezó en Octubre de 2019, donde a partir del diseño de https://bricolabs.cc/wiki/proyectos/curiosity_btl , el cual se modificó con los alumnos del taller de robótica de AMARAC (Denia). El proyecto quedó interrumpido por la COVID19.

En Octubre de 2020 se retomó, con los alumnos Jairo, Josep, Daniel, Fran, Arnau, Pepe y Yeray. Actualmente están desarrollando los programas de las distintos controladores.

2021-03-31 Ya han conseguido hacer el servidor de imagenes de la camara del robot, así como el cliente para poder visualizarlas en el PC. Se ha programado en Python, utilizando OpenCV2 para la captura de imagenes, threading para la optimización de procesos, y pickle para la serialización de los frames. 

2021-04-14 Teniendo en cuenta los fallos de seguridad de pickle, se ha modificado la transferencia de imagenes. Ahora se realiza con numpy
