library("dplyr")
library("ggplot2")

#Definición del dataset del caso
data <- read.csv("weight_change_dataset.csv")

#Exploración de los datos 

# Estadísticas descriptivas
str(data)
summary(data)

# Contar valores NA por columna
colSums(is.na(data))

# Número de filas duplicadas
sum(duplicated(data))

# Limpieza de los datos


# Opción 1: Eliminar filas con cualquier NA
data_clean <- na.omit(data)

# Opción 2: Imputar valores faltantes con la mediana (para variables numéricas)
#data_clean <- data %>%
#  mutate(across(where(is.numeric), ~ ifelse(is.na(.), median(., na.rm = TRUE), .)))

# Eliminar filas duplicadas
data_clean <- data_clean %>% distinct()

# Convertir variables categóricas a factores
data_clean <- data_clean %>%
  mutate

# Convertir variables categóricas a factores
data <- data %>% mutate(across(where(is.character), as.factor))


# Transformación de 'sleep_quality' a valores numéricos
data$Sleep.Quality <- ifelse(data$Sleep.Quality == "Poor", 0,
                             ifelse(data$Sleep.Quality == "Fair", 1,
                                    ifelse(data$Sleep.Quality == "Good", 2, 3)))

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

# filtrar algunos campos en un nuevo dataframe

data_filtered <- data[, 
  c("ID del Participante", "Edad", "Género", "Calidad del Sueño", "Nivel de Estrés", "Cambio de Peso (libras)", "Peso Final (libras)")]
colnames(data_filtered) <- c("ID", "Edad", "Genero", "CalidadSueno", "NivelEstres", "CambioPeso", "PesoFinal")

edad <- data_filtered$Edad
genero <- data_filtered$Genero
calidad_sueno <- data_filtered$CalidadSueno
nivel_estres <- data_filtered$NivelEstres
cambio_peso <- data_filtered$CambioPeso

# Estres por edad
boxplot(nivel_estres ~ edad, data = data_filtered, xlab = "Edad", ylab = "Nivel de Estres", main = "Estres por Edad")

# Calidad de sueño por edad
# box
boxplot(calidad_sueno ~ edad, data = data_filtered, xlab = "Edad", ylab = "Calidad de Sueño", main = "Calidad de Sueño por Edad")

# Distribución del cambio de peso
ggplot(data_filtered, aes(x = cambio_peso)) + 
  geom_histogram(binwidth = 1, fill = "skyblue", color = "black") +
  theme_minimal() +
  labs(title = "Distribución del Cambio de Peso", x = "Cambio de Peso (kg)", y = "Frecuencia")

# Boxplot de género vs cambio de peso
ggplot(data_filtered, aes(x = genero, y = cambio_peso, fill = genero)) + 
  geom_boxplot() +
  theme_minimal() +
  labs(title = "Cambio de Peso por Género", x = "Género", y = "Cambio de Peso (kg)") +
  theme(legend.position = "none")

# Correlación entre variables numéricas
library(GGally)
ggcorr(data_clean %>% select(where(is.numeric)), label = TRUE)



