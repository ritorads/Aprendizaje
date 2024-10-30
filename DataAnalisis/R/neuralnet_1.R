# Cargar librerias 
library(neuralnet)
library(NeuralNetTools)
library(corrplot)

# cargar dataset iris

data("iris")
head(iris)

# preparar los datos binarios
iris_bin <- iris[iris$Species %in% c("setosa", "versicolor"),]

# convertir la variable Species a binaria
iris_bin$Species <- ifelse(iris_bin$Species == "setosa",0,1)

# normalizar los datos
iris_bin[,1:4] <- scale(iris_bin[,1:4])

#creamos la red 
set.seed(123)

nn <- neuralnet(
  formula = Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width,
  data = iris_bin,
  hidden = c(5,2,2), # 5 neuronas en la capa de entrada, 2 en la capa oculta y 2 en la capa de salida
  linear.output = FALSE, # la salida no es lineal, False para problemas de clasificacion
)

plot(nn)


# hacer predicciones
pred <- compute(nn, iris_bin[,1:4])$net.result

# convertir probabilidades a clases binarias
pred_bin <- ifelse(pred > 0.5, 1, 0)

# calcular la precisión
precision <- mean(pred_bin == iris_bin$Species)

cat("La precisión es: ", precision * 100, "%\n")
