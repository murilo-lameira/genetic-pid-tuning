import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import random
import os

# ==========================================
# 1. Carregamento e Limpeza de Dados
# ==========================================
arquivo_csv = "../data/db_thermal_freezer.csv" 

if not os.path.exists(arquivo_csv):
    print(f"⚠️ Arquivo {arquivo_csv} não encontrado.")
    print("Certifique-se de que o CSV está na mesma pasta que este script ou altere o caminho na variável 'arquivo_csv'.")
    exit()

df = pd.read_csv(arquivo_csv)
colunas = ['temp_fria', 'temp_ambiente', 'carga_termica', 'peltier_pwm', 'fan_pwm', 'temp_fria_prox']
df = df.dropna(subset=colunas)

X = df[['temp_fria', 'temp_ambiente', 'carga_termica', 'peltier_pwm', 'fan_pwm']]
y = df['temp_fria_prox']

# ==========================================
# 2. Treinamento do Gêmeo Digital (Regressão)
# ==========================================
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)

gemeo_digital = LinearRegression()
gemeo_digital.fit(X_treino, y_treino)

previsoes = gemeo_digital.predict(X_teste)
erro_medio = mean_absolute_error(y_teste, previsoes)
precisao_r2 = r2_score(y_teste, previsoes)

print(f"✅ Gêmeo Digital Validado!")
print(f"Margem de Erro: {erro_medio:.3f} °C")
print(f"Precisão (Score R²): {precisao_r2 * 100:.1f}%\n")

# ==========================================
# 3. Função de Fitness (Simulação PID)
# ==========================================
def avaliar_pid(pid, modelo, setpoint=10.0, temp_inicial=25.0, temp_amb=25.0, carga=1.0, tempo_simulacao=120):
    Kp, Ki, Kd = pid
    temp_atual = temp_inicial
    erro_anterior = 0
    integral = 0
    itae = 0 
    
    for t in range(tempo_simulacao):
        erro = temp_atual - setpoint
        integral += erro
        derivada = erro - erro_anterior
        
        sinal_controle = (Kp * erro) + (Ki * integral) + (Kd * derivada)
        pwm = max(0, min(100, sinal_controle))
        fan_pwm = 100.0
        
        estado_atual = pd.DataFrame(
            [[temp_atual, temp_amb, carga, pwm, fan_pwm]], 
            columns=['temp_fria', 'temp_ambiente', 'carga_termica', 'peltier_pwm', 'fan_pwm']
        )
        
        temp_prox = modelo.predict(estado_atual)[0]
        itae += t * abs(erro)
        
        temp_atual = temp_prox
        erro_anterior = erro
        
    return 1.0 / (itae + 1e-6)

# ==========================================
# 4. Motor do Algoritmo Genético
# ==========================================
tamanho_populacao = 50
geracoes = 120
taxa_mutacao = 0.1

populacao = np.random.uniform(0, 10, (tamanho_populacao, 3))
print("Iniciando a Evolução Genética...\n")

melhor_pid = None

for geracao in range(geracoes):
    notas = [avaliar_pid(individuo, gemeo_digital) for individuo in populacao]
    
    melhor_indice = np.argmax(notas)
    melhor_pid = populacao[melhor_indice]
    
    if geracao % 5 == 0 or geracao == geracoes - 1:
        print(f"Geração {geracao:02d} | Melhor Nota: {notas[melhor_indice]:.5f} | PID: Kp={melhor_pid[0]:.2f}, Ki={melhor_pid[1]:.2f}, Kd={melhor_pid[2]:.2f}")
        
    nova_populacao = [melhor_pid] # Elitismo
    
    while len(nova_populacao) < tamanho_populacao:
        # Seleção por Torneio
        comp1 = random.sample(range(tamanho_populacao), 3)
        vencedor_1 = populacao[max(comp1, key=lambda i: notas[i])]
        
        comp2 = random.sample(range(tamanho_populacao), 3)
        vencedor_2 = populacao[max(comp2, key=lambda i: notas[i])]
        
        # Cruzamento
        filho = (vencedor_1 + vencedor_2) / 2.0
        
        # Mutação
        if random.random() < taxa_mutacao:
            indice_mutacao = random.randint(0, 2)
            filho[indice_mutacao] += random.uniform(-1, 1)
            filho[indice_mutacao] = max(0, filho[indice_mutacao])
            
        nova_populacao.append(filho)
        
    populacao = np.array(nova_populacao)

print("EVOLUÇÃO CONCLUÍDA!")
print(f"Parâmetros Finais Ideais: Kp={melhor_pid[0]:.2f}, Ki={melhor_pid[1]:.2f}, Kd={melhor_pid[2]:.2f}")

# ==========================================
# 5. Dashboard de Resultados para o Portfólio
# ==========================================
temp_atual = 25.0
setpoint = 10.0
historico_temp = []
historico_pwm = []
erro_anterior = 0
integral = 0

Kp, Ki, Kd = melhor_pid

for t in range(120):
    erro = temp_atual - setpoint
    integral += erro
    derivada = erro - erro_anterior
    
    sinal_controle = (Kp * erro) + (Ki * integral) + (Kd * derivada)
    pwm = max(0, min(100, sinal_controle))
    
    estado_atual = pd.DataFrame(
        [[temp_atual, 25.0, 1.0, pwm, 100.0]], 
        columns=['temp_fria', 'temp_ambiente', 'carga_termica', 'peltier_pwm', 'fan_pwm']
    )
    
    temp_atual = gemeo_digital.predict(estado_atual)[0]
    erro_anterior = erro
    
    historico_temp.append(temp_atual)
    historico_pwm.append(pwm)

plt.figure(figsize=(12, 5))

# Gráfico 1: A Curva de Temperatura
plt.subplot(1, 2, 1)
plt.plot(historico_temp, label='Temperatura Real', color='#0078D7', linewidth=2)
plt.axhline(y=setpoint, color='#E81123', linestyle='--', label='Setpoint (10°C)')
plt.title('Resposta ao Degrau (Sintonia Genética)')
plt.ylabel('Temperatura (°C)')
plt.xlabel('Passos da Simulação')
plt.legend()
plt.grid(True)

# Gráfico 2: O Esforço de Controle
plt.subplot(1, 2, 2)
plt.plot(historico_pwm, label='Potência da Peltier (PWM)', color='#FF8C00', linewidth=2)
plt.title('Ação de Controle do PID')
plt.ylabel('PWM (%)')
plt.xlabel('Passos da Simulação')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('../assets/grafico_tuning.png', dpi=300, bbox_inches='tight')
plt.show()