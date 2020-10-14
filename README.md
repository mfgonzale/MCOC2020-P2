# MCOC2020-P2

# Informe Diseño del Reticulado

![imagen](/Ret1.png)

* Rediseño de 5 barras.
  
  *Se seleccionaron 5 barras del reticulado. La barra 0-3 en la cual su R cambió a 3cm y su t a 1,7 cm, la barra 5-3 con R igual    a 3,3cm y t igual a 3,3cm, la barra 1-4 con R igual a 3,3cm y t igual a 3,3 cm, la barra 6-4 con R igual a 3,3cm y t igual a    5,7cm y la barra 0-5 con R igual a 3,3cm y t igual a 3,3cm. 

  *Barra Nodo 0,3
  
  ![imagen](/03.jpg)
  
  *Barra Nodo 5,3
  
  ![imagen](/53.jpg)
  
  *Barra Nodo 1,4
  
  ![imagen](/14.jpg)
 
  *Barra Nodo 6,4
 
  ![imagen](/64.jpg)

  *Barra Nodo 0,5
  
  ![imagen](/05.jpg)
  
* Funcion Rediseño de cada barra.
  
  *Al principio descarta el rediseño si es que el factor de utilización es igual a 1 y el diseño original cumple con los            requisitos mínimos.
   Luego de identificar si la fuerza es en tracción o compresión, calcula el área requerida para cumplir con la fluencia de la      barra, obteniendo de esta el radio mínimo de la barra con el espesor igual al radio mínimo.
   Lo fundamental de la función es que toma el Rmin y recorre un arreglo de 501 elementos que son desde el Rmin al Rmin + 500      mm.
   Para cada R dentro de este arreglo, se calcula un tmin. Para cada valor valor posible de t>tmin y t<R, se calcula el área, se    comprueba si es que cumple con la función "chequear_diseño" (la cual se adaptó para admitir valores variables) y en caso de      encontrar un área menor a algún caso anterior, se guarda el nuevo valor como Amin, guardando el R y t respectivo a esa área.
   En caso de no cumplir con ningún caso, la función no efectúa cambios en los R y t originales.

* Factores de utilizacion nuevos.
  
  Los nuevos factores de utilizacion son 1 en las primeras cuatro barras y en la última barra es 0,81

* Fuerzas sobre las barras
  
  *Fuerzas en caso 1.4 D 

![imagen](/fuerzas14d.png)
 
  *Fuerzas en caso 1.2 D + 1.6L

![imagen](/fuerzas12d16l.png)

* Deformada para cada combinacion de carga.
 
 * deformada para 1.4D
 
 ![img](/deformada14d.png)
 
 * deformada para 1.2D + 1.6L
 
 ![img](/deformada12d16l.png)

* Desplazamiento vertical maximo antes de los cambios.

![img](/desplazamientonodos.jpg)

Se observan los datos respectivos al eje Z , el mayor seria claramente 1 y 6 e cargas muertas y nodo 3 en cargas vivas. 

* Comentarios sobre nueva distribucion FU
  * Existen 2 opciones en el caso de que la FU aumena esto significaria que el diseño original no cumple. SI el FU disminuye el rediseño sera la mejor opcion
