# 🏛️ Visão Geral do Gêmeo Digital (Digital Twin)

Modelagem preditiva orientada a dados a partir da telemetria física do projeto [[02 - Projetos/Thermal-Freezer-IoT/MAIN|Thermal Freezer IoT]].

---

## 🎯 Por que um Gêmeo Digital?

Na engenharia de controle, sistemas térmicos possuem elevado atraso de transporte e inércia. Sintonizar os parâmetros Kp, Ki e Kd empiricamente em bancada consome muito tempo e estressa os componentes físicos.

O Gêmeo Digital substitui a sintonia manual:
1. Treinamento de modelo preditivo usando regressão linear múltipla (`scikit-learn`) sobre a telemetria IoT real ($PWM$ aplicado vs. $T_{\text{real}}$).
2. Simulação em tempo acelerado: centenas de combinações de controle testadas em segundos em ambiente virtual.

---

## 📊 Precisão e Aderência do Modelo

- **Coeficiente de Determinação ($R^2$):** **99.7%**
- **Margem de Erro Média:** **0.38°C**
- O modelo reproduz fielmente as dinâmicas de rampa, ganho estático e atraso de transporte observados na pastilha Peltier real.

---

[[02 - Projetos/Genetic-PID-Tuning/MAIN|Hub Genetic PID Tuning]] | [[01 - Algoritmo Genético & Otimização Evolutiva|Algoritmo Genético & Otimização Evolutiva]] | [[00 - Índice Principal]]

