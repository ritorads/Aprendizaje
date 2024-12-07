library(neuralnet)
library(NeuralNetTools)
library(corrplot)

# Load the data csv
data <- read.csv("weight_change_dataset.csv")

target <- data$Final.Weight..lbs.

# Transformar a variables numéricas (0, 1, 2) Gender, Physical.Activity.Level, Sleep.Quality

# Transformación de 'gender' de "M" a 0 y "F" a 1
data$Gender <- ifelse(data$Gender == "M", 0, 1)

# Transformación de 'physical_activity_level' a valores numéricos
data$Physical.Activity.Level <- ifelse(data$Physical.Activity.Level == "Sedentary", 0, 
                                       ifelse(data$Physical.Activity.Level == "Lightly Active", 1,
                                              ifelse(data$Physical.Activity.Level == "Moderately Active", 2, 3)))

# Transformación de 'sleep_quality' a valores numéricos
data$Sleep.Quality <- ifelse(data$Sleep.Quality == "Poor", 0,
                             ifelse(data$Sleep.Quality == "Fair", 1,
                                    ifelse(data$Sleep.Quality == "Good", 2, 3)))

# Verifica los primeros datos transformados para asegurarte de que están correctos
head(data)

# Busquemos las correlaciones

# 1. Cargar la matriz de correlación ya calculada
correlation <- cor(data)

# 2. Extraer las correlaciones con respecto al target
target_correlations <- correlation[, "Final.Weight..lbs."]

# 3. Ordenar las correlaciones por valor absoluto de mayor a menor
target_correlations <- sort(abs(target_correlations), decreasing = TRUE)

# 4. Excluir la correlación del target consigo mismo (que siempre será 1)
target_correlations <- target_correlations[names(target_correlations) != "Final.Weight..lbs."]

# 5. Mostrar las variables con las mejores correlaciones
print(target_correlations)

# 6. Visualizar la matriz de correlación
corrplot(correlation, method = "number")

# Separa Train y test
set.seed(123)
train_indices <- sample(1:nrow(data), 0.6 * nrow(data))
train_data <- data[train_indices, ]
test_data <- data[-train_indices, ]

# Guardar medias y desviaciones estándar antes de la estandarización
mean_train <- apply(train_data, 2, mean)
sd_train <- apply(train_data, 2, sd)

# estandarizar los datos 
train_data_scaled <- scale(train_data, center = mean_train, scale = sd_train)
test_data_scaled <- scale(test_data, center = mean_train, scale = sd_train)

# dataframe
train_data_scaled <- as.data.frame(train_data_scaled)
test_data_scaled <- as.data.frame(test_data_scaled)

# Definir la fórmula
formula <- as.formula("Final.Weight..lbs. ~ .")

# Crear la red neuronal
nn <- neuralnet(formula, data = train_data_scaled, hidden = c(5, 3), linear.output = TRUE)

# Predecir los valores de test
predictions_scaled <- predict(nn, test_data_scaled)

# Revertir la estandarización de las predicciones
predictions <- predictions_scaled * sd_train["Final.Weight..lbs."] + mean_train["Final.Weight..lbs."]

# Calcular el MSE en la escala original
mse <- function(predictions, actual) {
  mean((predictions - actual)^2)
}

mse_value <- mse(predictions, test_data$Final.Weight..lbs.)
cat("MSE:", mse_value, "\n")

# Visualizar la red neuronal
plotnet(nn)

# Comparación de las predicciones y los valores reales en escala original
comparison_original <- cbind(predictions, test_data$Final.Weight..lbs.)
colnames(comparison_original) <- c("Predicted", "Actual")

comparison_original <- as.data.frame(comparison_original)

print(comparison_original)

# Calcular y mostrar el error absoluto medio (MAE) en la escala original
mae <- mean(abs(comparison_original[, "Predicted"] - comparison_original[, "Actual"]))
cat("Error Absoluto Medio (MAE):", mae, "\n")

# accuracy 

precision <- mean(1 - abs(comparison_original[, "Predicted"] - comparison_original[, "Actual"]) / comparison_original[, "Actual"])
cat("Precisión:", precision, "\n")


colnames(data) <- c(
  "ID del Participante",
  "Edad",
  "Género",
  "Peso Actual (libras)",
  "Tasa Metabólica Basal (Calorías)",
  "Calorías Consumidas Diariamente",
  "Superávit/Déficit Calórico Diario",
  "Cambio de Peso (libras)",
  "Duración (semanas)",
  "Nivel de Actividad Física",
  "Calidad del Sueño",
  "Nivel de Estrés",
  "Peso Final (libras)"
)

