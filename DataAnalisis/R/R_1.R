library(neuralnet)
library(corrplot)
library(ggplot2)

data <- USArrests

# reemplazar nombres 

colnames(data) <- c("Asesinatos", "Asaltos", "P_urbana", "Violaciones")

################################## Funciones ########################################################

# Normalización
Normalizar <- function(x) {
  return((x - min(x)) / (max(x) - min(x)))
}

# Ploteo de 2 Variables.

Graficar <- function(data, var1, var2) {
  ggplot(data, aes_string(x = var1, y = var2)) + geom_point() + geom_smooth(method = "lm")
}

# Neuralnet 5,3,1 

nnet <- function(data, formula) {
  Salida <- neuralnet(
    formula,
    data = data,
    hidden = c(5, 3),
    linear.output = TRUE
  )
  return(Salida)
}


data_scaled <- as.data.frame(lapply(data, Normalizar))

################################## Exploración#######################################################
str(data)
summary(data)

cor(data_scaled)
corrplot(cor(data_scaled), method = "number")

pairs(data_scaled)

USArrests$Urban_Group <- ifelse(USArrests$UrbanPop > median(USArrests$UrbanPop), "Urban", "Rural")



Graficar(data_scaled, "Asesinatos", "Asaltos")

################################## neuralnet ########################################################
# Train /test
set.seed(123)

indices <- sample(1:nrow(data_scaled), 0.7 * nrow(data_scaled))
train <- data_scaled[indices, ]
test <- data_scaled[-indices, ]

# Entrenamiento de la Red
pred_asesinatos <- nnet(train, as.formula("Asesinatos ~ Asaltos + Violaciones"))
pred_violaciones <- nnet(train, as.formula("Violaciones ~ Asaltos + P_urbana + Asesinatos"))
pred_pop <- nnet(train, as.formula("P_urbana ~ Asesinatos + Asaltos + Violaciones"))

# Testeo

test_asesinatos <- predict(pred_asesinatos, test)
test_violaciones <- predict(pred_violaciones, test)
test_pop <- predict(pred_pop, test)

# Error
mse_m1 <- mean((test$Asesinatos - test_asesinatos)^2)
mse_m2 <- mean((test$Violaciones - test_violaciones)^2)
mse_m3 <- mean((test$P_urbana - test_pop)^2)
print(paste("Los MSE son: ", mse_m1, mse_m2, mse_m3))

# predict
asesinatos_pred<- predict(pred_asesinatos, data_scaled)
violaciones_pred<- predict(pred_violaciones, data_scaled)
pop_pred<- predict(pred_pop, data_scaled)

# Graficos

Graficar(data_scaled, "Asesinatos", "asesinatos_pred")
Graficar(data_scaled, "Violaciones", "violaciones_pred")
Graficar(data_scaled, "P_urbana", "pop_pred")


################################## Clustering ########################################################

# Usar el método del codo para encontrar el número óptimo de clústeres
wss <- (nrow(data_scaled) - 1) * sum(apply(data_scaled, 2, var))
for (i in 2:15) wss[i] <- sum(kmeans(data_scaled, centers = i)$withinss)

# Graficar el codo
plot(1:15, wss, type = "b", main = "Método del Codo", xlab = "Número de Clústeres", ylab = "Suma de Errores Cuadráticos dentro del Clúster")

# Kmeans

kmeans_result <- kmeans(data_scaled, centers = 10, nstart = 25)

kmeans_result$cluster
kmeans_result$centers

# Graficar los clústeres

plot(data_scaled[c("Asesinatos", "Asaltos")], col = kmeans_result$cluster)
points(kmeans_result$centers[, c("Asesinatos", "Asaltos")], col = 1:4, pch = 8, cex = 2)

plot(data_scaled[c("Asesinatos", "Violaciones")], col = kmeans_result$cluster)
points(kmeans_result$centers[, c("Asesinatos", "Violaciones")], col = 1:4, pch = 8, cex = 2)

plot(data_scaled[c("Asesinatos", "P_urbana")], col = kmeans_result$cluster)
points(kmeans_result$centers[, c("Asesinatos", "P_urbana")], col = 1:4, pch = 8, cex = 2)

# Agregar las etiquetas de clúster al dataset original
data_scaled$Cluster <- as.factor(kmeans_result$cluster)

# Visualización de los clústeres en un gráfico de dispersión
library(ggplot2)
ggplot(data_scaled, aes(x = Asesinatos, y = Asaltos, color = Cluster)) +
  geom_point(size = 3) +
  theme_minimal() +
  labs(title = "Clustering de Estados por Criminalidad", x = "Tasa de Homicidios (Murder)", y = "Tasa de Asaltos (Assault)")

dist_matrix <- dist(scale(USArrests[, -5]))
hc <- hclust(dist_matrix, method = "ward.D2")
plot(hc)

