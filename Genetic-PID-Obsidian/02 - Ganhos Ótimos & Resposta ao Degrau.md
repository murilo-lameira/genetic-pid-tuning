# 🎯 Ganhos Ótimos & Resposta ao Degrau

Resultados da convergência evolutiva, valores ótimos de ganhos e validação em resposta ao degrau virtual.

---

## 🏆 Parâmetros Ótimos Convergidos

Após 100 gerações de otimização, o algoritmo genético convergiu para a seguinte parametrização:

| Ganho | Valor Encontrado | Papel Físico no Sistema Térmico |
| :--- | :--- | :--- |
| **$K_p$ (Proporcional)** | **22.26** | Resposta enérgica imediata para quebrar a inércia da pastilha |
| **$K_i$ (Integral)** | **0.02** | Eliminação do erro de regime estacionário sem causar *windup* |
| **$K_d$ (Derivativo)** | **3.55** | Força de frenagem para evitar *overshoot* ao se aproximar da meta |

---

## 📈 Comportamento Dinâmico (Resposta ao Degrau)

- **Tempo de Subida / Rampa:** Rápido e controlado, utilizando a potência máxima permitida no início.
- **Overshoot / Ultrapassagem:** **0% (Zero)**. O sistema desacelera suavemente ao atingir a temperatura alvo.
- **Erro em Regime Estacionário:** **0.0°C**. Estabilidade contínua com esforço de controle amortecido.

---

[[02 - Projetos/Genetic-PID-Tuning/MAIN|Hub Genetic PID Tuning]] | [[00 - Visão Geral do Gêmeo Digital|Visão Geral do Gêmeo Digital]] | [[00 - Índice Principal]]

