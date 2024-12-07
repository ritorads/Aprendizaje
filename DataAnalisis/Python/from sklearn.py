import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import tensorflow as tf

# Simular el dataset USArrests
np.random.seed(123)
USArrests = pd.DataFrame({
    "Assault": np.random.randint(50, 300, 50),
    "UrbanPop": np.random.randint(30, 90, 50),
    "Rape": np.random.uniform(10, 50, 50),
    "Murder": np.random.uniform(2, 15, 50)
})

# Escalado de datos
scaler = MinMaxScaler()
X_M1 = USArrests[["Assault", "UrbanPop", "Rape"]]
y_M1 = USArrests["Murder"]
X_M1_scaled = scaler.fit_transform(X_M1)

# Dividir datos en entrenamiento y prueba para M1
X_train_M1, X_test_M1, y_train_M1, y_test_M1 = train_test_split(X_M1_scaled, y_M1, test_size=0.2, random_state=42)

# Crear y entrenar el modelo ANN para M1
model_M1 = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(X_train_M1.shape[1],)),
    tf.keras.layers.Dense(5, activation='relu'),
    tf.keras.layers.Dense(1)
])
model_M1.compile(optimizer='adam', loss='mse', metrics=['mae'])
model_M1.fit(X_train_M1, y_train_M1, epochs=100, verbose=0)

# Generar predicciones Y1 para alimentar M2
USArrests["Y1"] = model_M1.predict(X_M1_scaled).flatten()

# Preparar datos para el modelo M2
second_df = pd.DataFrame({
    "Y1": USArrests["Y1"],
    "Género": np.random.choice(["Masculino", "Femenino", "No-binario"], 50),
    "Penal": np.random.choice(["Santiago 1", "Colina 1", "Rancagua"], 50),
    "Número_de_veces": np.random.randint(0, 11, 50),
    "Arma": np.random.choice(["Cuchillo", "Pistola", "Granada"], 50)
})

# Codificar variables categóricas
le_genero = LabelEncoder()
second_df["Género_encoded"] = le_genero.fit_transform(second_df["Género"])
second_df["Penal_encoded"] = LabelEncoder().fit_transform(second_df["Penal"])
second_df["Arma_encoded"] = LabelEncoder().fit_transform(second_df["Arma"])

X_M2 = second_df[["Y1", "Género_encoded", "Penal_encoded", "Número_de_veces", "Arma_encoded"]]
y_M2 = np.random.uniform(0, 1, len(X_M2))  # Peligrosidad simulada
X_M2_scaled = scaler.fit_transform(X_M2)

# Dividir datos en entrenamiento y prueba para M2
X_train_M2, X_test_M2, y_train_M2, y_test_M2 = train_test_split(X_M2_scaled, y_M2, test_size=0.2, random_state=42)

# Crear y entrenar el modelo ANN para M2
model_M2 = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(X_train_M2.shape[1],)),
    tf.keras.layers.Dense(5, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model_M2.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model_M2.fit(X_train_M2, y_train_M2, epochs=100, verbose=0)

# Generar predicciones Y2 para alimentar M3
second_df["Y2"] = model_M2.predict(X_M2_scaled).flatten()

# Preparar datos para el modelo M3
third_df = pd.DataFrame({
    "Y2": second_df["Y2"],
    "Comuna": np.random.choice(["La Reina", "Santiago", "La Cisterna"], 50),
    "Nivel": np.random.choice(["Alto", "Bajo"], 50),
    "Reincidente": np.random.choice([0, 1], 50)
})

# Codificar variables categóricas
third_df["Comuna_encoded"] = LabelEncoder().fit_transform(third_df["Comuna"])
third_df["Nivel_encoded"] = LabelEncoder().fit_transform(third_df["Nivel"])
X_M3 = third_df[["Y2", "Comuna_encoded", "Nivel_encoded", "Reincidente"]]
y_M3 = np.random.choice([0, 1], 50)  # Barrio inseguro simulado
X_M3_scaled = scaler.fit_transform(X_M3)

# Dividir datos en entrenamiento y prueba para M3
X_train_M3, X_test_M3, y_train_M3, y_test_M3 = train_test_split(X_M3_scaled, y_M3, test_size=0.2, random_state=42)

# Crear y entrenar el modelo ANN para M3
model_M3 = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(X_train_M3.shape[1],)),
    tf.keras.layers.Dense(5, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model_M3.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model_M3.fit(X_train_M3, y_train_M3, epochs=100, verbose=0)

# Evaluar el modelo final (M3)
loss, accuracy = model_M3.evaluate(X_test_M3, y_test_M3, verbose=0)
print(f"Model M3 Loss: {loss}, Accuracy: {accuracy}")
