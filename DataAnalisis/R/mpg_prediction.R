library(neuralnet)
library(corrplot)

# Load the data
dataset <- datasets::mtcars

target <- dataset$mpg

correlation <- cor(dataset)

corrplot(correlation, method = "number")

# Filtrar variables con correlación alta con mpg (por ejemplo, > |0.5|)
correlation_mpg <- correlation["mpg", ]
selected_vars <- names(correlation_mpg[abs(correlation_mpg) > 0.5])
selected_vars <- selected_vars[selected_vars != "mpg"]  # Excluir mpg

# Crear un nuevo conjunto de datos solo con las variables seleccionadas
dataset_selected <- dataset[, c("mpg", selected_vars)]


# Split the data
set.seed(123)

split <- sample(2, nrow(dataset_selected), replace = TRUE, prob = c(0.7, 0.3))
train <- dataset_selected[split == 1, ]
test <- dataset_selected[split == 2, ]

# Estandarización de los datos de entrenamiento
mean_train <- apply(train[, -1], 2, mean)
sd_train <- apply(train[, -1], 2, sd)


#Aplicar estandarización al conjunto de entrenamiento y prueba
train_scaled <- as.data.frame(scale(train[, -1], center = mean_train, scale = sd_train))
train_scaled$mpg <- train$mpg  # Mantener la variable objetivo sin escalar

test_scaled <- as.data.frame(scale(test[, -1], center = mean_train, scale = sd_train))
test_scaled$mpg <- test$mpg

# Función para calcular el MSE en el conjunto de prueba
mse <- function(predictions, actual) {
  mean((predictions - actual)^2)
}

# Probar diferentes configuraciones de capas ocultas y encontrar el mejor modelo
hidden_layers <- list(c(5), c(5, 3), c(6, 4), c(7, 5))
best_mse <- Inf
best_model <- NULL
best_config <- NULL

set.seed(123)

for (hidden in hidden_layers) {
  model <- neuralnet(
    formula = mpg ~ .,
    data = train_scaled,
    hidden = hidden,
    linear.output = TRUE
  )
  
  # Hacer predicciones y calcular el MSE
  predictions <- compute(model, test_scaled[, -1])$net.result
  current_mse <- mse(predictions, test_scaled$mpg)
  
  # Guardar el modelo si es el mejor hasta ahora
  if (current_mse < best_mse) {
    best_mse <- current_mse
    best_model <- model
    best_config <- hidden
  }
}

#plot model

plot(best_model)

cat("Mejor configuración de capas ocultas:", best_config, "\n")
cat("MSE del mejor modelo:", best_mse, "\n")


# Hacer predicciones en el conjunto de prueba usando el mejor modelo
predictions <- compute(best_model, test_scaled[, -1])$net.result

# Comparación de las predicciones y los valores reales
comparison <- cbind(predictions, test_scaled$mpg)
colnames(comparison) <- c("Prediction", "Real")
comparison <- as.data.frame(comparison)

# Calcular y mostrar el error absoluto medio (MAE)
mae <- mean(abs(comparison$Prediction - comparison$Real))
cat("Error Absoluto Medio (MAE):", mae, "\n")

print(comparison)

