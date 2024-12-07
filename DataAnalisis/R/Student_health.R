library(ggplot2)
library(corrplot)
library(neuralnet)

data <- read.csv("TARP.csv")
head(data)

colnames(data) <- c("Humedad del Suelo", "Temperatura", "Humedad del Suelo (Adicional)", "Tiempo",
  "Temperatura del Aire (C)", "Velocidad del Viento (Km/h)", "Humedad del Aire (%)",
  "Ráfagas de Viento (Km/h)", "Presión (KPa)", "pH", "Lluvia", "Nitrógeno (N)",
  "Fósforo (P)", "Potasio (K)", "Estado"
)


# Manejar valores faltantes
data <- na.omit(data)
# Normalización 
Normalizar <- function(x) {
  return((x - min(x)) / (max(x) - min(x)))
}

# Análisis Exploratorio de Datos

data$Estado <- as.factor(ifelse(data$Estado == "ON", 1,
                      ifelse(data$Estado == "OFF", 0, NA)))

str(data)
summary(data)

data_norm <- as.data.frame(lapply(data[, 1:14], Normalizar))

cor(data_norm)
corrplot(cor(data_norm), method = "number")
