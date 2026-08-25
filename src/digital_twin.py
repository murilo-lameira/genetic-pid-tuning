import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Carregamento e Limpeza
df = pd.read_csv("data/db_thermal_freezer.csv")
colunas = ['temp_fria', 'temp_ambiente', 'carga_termica', 'peltier_pwm', 'fan_pwm', 'temp_fria_prox']
df = df.dropna(subset=colunas)

X = df[['temp_fria', 'temp_ambiente', 'carga_termica', 'peltier_pwm', 'fan_pwm']]
y = df['temp_fria_prox']

# 2. Separação: 80% para Estudar (Treino), 20% para Prova (Teste)
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Treinamento
gemeo_digital = LinearRegression()
gemeo_digital.fit(X_treino, y_treino)

# 4. A Prova Final (Validação)
# Pedimos pro modelo adivinhar o futuro naqueles 20% de dados que ele não viu
previsoes = gemeo_digital.predict(X_teste)

erro_medio = mean_absolute_error(y_teste, previsoes)
precisao_r2 = r2_score(y_teste, previsoes)

print(f"✅ Gêmeo Digital Validado!")
print(f"Margem de Erro: {erro_medio:.3f} °C")
print(f"Precisão (Score R²): {precisao_r2 * 100:.1f}%\n")

# 5. Gráfico para o Portfólio (Comparando as 50 primeiras predições)
plt.figure(figsize=(10, 5))
plt.plot(y_teste.values[:50], label='Temperatura Real (Geladeira)', marker='o')
plt.plot(previsoes[:50], label='Previsão do Gêmeo Digital', linestyle='dashed', marker='x')
plt.title("Realidade vs. Simulação (Gêmeo Digital)")
plt.ylabel("Temperatura °C")
plt.xlabel("Tempo (Amostras)")
plt.legend()
plt.grid(True)
plt.show()