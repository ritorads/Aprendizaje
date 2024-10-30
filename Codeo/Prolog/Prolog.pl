/*constantes*/
ana.
juan.
pedro.
carlos.
carmen.

/*predicados*/

/*esHombre*/
esHombre(juan).
esHombre(pedro).
esHombre(carlos).

/*esMujer*/
esMujer(ana).
esMujer(carmen).

/*Relaciones*/
adulto(juan,carmen).

/*Reglas*/
masculino(X):- esHombre(X).
femenino(X):- esMujer(X).
esAdulto(X):- adulto(X).
