# 📈 Análise Exploratória do Mercado de Ações Brasileiro

> Projeto de Ciência de Dados com análise histórica de ativos da B3 (WEG, Petrobras e Vale), utilizando Python, yfinance, Pandas e Matplotlib.

[!\[Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)
[!\[Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas)](https://pandas.pydata.org/)
[!\[yfinance](https://img.shields.io/badge/yfinance-0.2%2B-green)](https://pypi.org/project/yfinance/)
[!\[Matplotlib](https://img.shields.io/badge/Matplotlib-3.8%2B-orange)](https://matplotlib.org/)
[!\[License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

\---

## 📋 Sumário

* [Sobre o Projeto](#-sobre-o-projeto)
* [Objetivos](#-objetivos)
* [Tecnologias Utilizadas](#-tecnologias-utilizadas)
* [Estrutura do Repositório](#-estrutura-do-repositório)
* [Como Executar](#-como-executar)
* [Visualizações Geradas](#-visualizações-geradas)
* [Insights Obtidos](#-insights-obtidos)
* [Melhorias Futuras](#-melhorias-futuras)
* [Autor](#-autor)

\---

## 🧠 Sobre o Projeto

Este projeto realiza uma **Análise Exploratória de Dados (EDA)** sobre três grandes ativos listados na B3 (Bolsa de Valores do Brasil):

|Ticker|Empresa|Setor|
|-|-|-|
|WEGE3|WEG S.A.|Bens de Capital|
|PETR4|Petrobras PN|Petróleo e Gás|
|VALE3|Vale S.A.|Mineração|

A análise cobre um período de aproximadamente **3 anos** e explora preços históricos, retornos, volatilidade e correlações entre os ativos — fornecendo uma base sólida para interpretações financeiras e tomada de decisão.

\---

## 🎯 Objetivos

* **Coletar** dados históricos reais de ações diretamente do Yahoo Finance
* **Tratar** os dados: limpeza de nulos, ordenação temporal e consistência
* **Calcular** métricas financeiras: retorno diário, médias móveis, volatilidade e retorno acumulado
* **Visualizar** padrões e tendências por meio de gráficos informativos e profissionais
* **Extrair insights** sobre o desempenho comparativo dos ativos

\---

## 🛠 Tecnologias Utilizadas

|Biblioteca|Versão Mínima|Finalidade|
|-|-|-|
|`yfinance`|0.2.40|Coleta de dados históricos via Yahoo Finance|
|`pandas`|2.0.0|Manipulação e análise de dados tabulares|
|`numpy`|1.26.0|Cálculos numéricos (volatilidade, etc.)|
|`matplotlib`|3.8.0|Geração de gráficos estáticos|
|`seaborn`|0.13.0|Gráficos estatísticos (heatmap, histograma)|
|`jupyter`|1.0.0|Exploração interativa via notebook|

\---

## 📁 Estrutura do Repositório

```
analise-acoes-br/
│
├── data/                         # CSVs com dados históricos e estatísticas
│   ├── WEGE3.csv
│   ├── PETR4.csv
│   ├── VALE3.csv
│   └── estatisticas\_descritivas.csv
│
├── images/                       # Gráficos gerados automaticamente
│   ├── preco\_WEGE3.png
│   ├── preco\_PETR4.png
│   ├── preco\_VALE3.png
│   ├── comparacao\_desempenho.png
│   ├── retorno\_acumulado.png
│   ├── histogramas\_retornos.png
│   ├── volatilidade.png
│   ├── correlacao\_retornos.png
│   └── boxplot\_retornos.png
│
├── notebooks/
│   └── analise\_exploratoria.ipynb   # Notebook com análise interativa completa
│
├── src/
│   ├── \_\_init\_\_.py
│   ├── data\_collector.py            # Coleta e carregamento de dados (yfinance)
│   ├── data\_processor.py            # Limpeza, métricas e transformações
│   └── visualizer.py                # Geração e salvamento de gráficos
│
├── main.py                          # Pipeline principal (executa tudo)
├── requirements.txt                 # Dependências do projeto
├── .gitignore
└── README.md
```

\---

## 🚀 Como Executar

### Pré-requisitos

* Python 3.11 ou superior
* pip (gerenciador de pacotes)

### 1\. Clone o repositório

```bash
git clone https://github.com/R0costa/analise-acoes-br.git
cd analise-acoes-br
```

### 2\. Crie e ative um ambiente virtual (recomendado)

```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\\Scripts\\activate
```

### 3\. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4\. Execute o pipeline completo

```bash
python main.py
```

O script irá:

1. Baixar os dados históricos (ou carregar CSVs já existentes)
2. Processar e calcular as métricas
3. Imprimir as estatísticas descritivas no terminal
4. Salvar todos os gráficos em `/images`

### 5\. (Opcional) Explorar via Jupyter Notebook

```bash
jupyter notebook notebooks/analise\_exploratoria.ipynb
```

\---

## 📊 Visualizações Geradas

### Evolução do Preço com Médias Móveis

> Preço de fechamento ajustado e médias móveis de 20 e 50 dias para cada ativo.

!\[Preço WEGE3](images/preco\_WEGE3.png)
!\[Preço PETR4](images/preco\_PETR4.png)
!\[Preço VALE3](images/preco\_VALE3.png)

\---

### Comparação de Desempenho (Base 100)

> Todos os ativos normalizados para a mesma base inicial, permitindo comparação direta de rentabilidade relativa.

!\[Comparação](images/comparacao\_desempenho.png)

\---

### Retorno Acumulado no Período

> Variação percentual acumulada desde o início da série histórica.

!\[Retorno Acumulado](images/retorno\_acumulado.png)

\---

### Distribuição dos Retornos Diários

> Histogramas com curva KDE para análise da distribuição estatística dos retornos.

!\[Histogramas](images/histogramas\_retornos.png)

\---

### Volatilidade Anualizada Rolling

> Volatilidade calculada com janela de 21 dias e anualizada (×√252).

!\[Volatilidade](images/volatilidade.png)

\---

### Correlação entre os Ativos

> Heatmap de correlação de Pearson dos retornos diários.

!\[Correlação](images/correlacao\_retornos.png)

\---

### Boxplot dos Retornos

> Comparativo da dispersão e presença de outliers nos retornos diários.

!\[Boxplot](images/boxplot\_retornos.png)

\---

## 💡 Insights Obtidos

> Os insights abaixo são baseados na análise do período \*\*2021–2024\*\*. Os valores exatos dependem da execução com dados reais.

### 1\. Desempenho Relativo

* **WEGE3** historicamente apresenta crescimento mais consistente e menor volatilidade, refletindo a solidez de uma empresa exportadora de bens de capital.
* **PETR4** e **VALE3** mostram maior sensibilidade a fatores externos: preço do petróleo, câmbio e cotações de minério de ferro.

### 2\. Volatilidade

* Os três ativos apresentam volatilidade anualizada acima de 20%, característica de mercados emergentes e papéis cíclicos.
* Picos de volatilidade coincidem com eventos macroeconômicos relevantes (eleições, variações do dólar, crises de commodities).

### 3\. Correlação

* **PETR4 e VALE3** tendem a ter correlação moderada a alta, pois ambas são empresas exportadoras de commodities influenciadas pelo câmbio e cenário global.
* **WEGE3** apresenta correlação menor com as outras duas, sugerindo que pode atuar como elemento de diversificação em uma carteira.

### 4\. Distribuição dos Retornos

* Os retornos diários seguem aproximadamente uma distribuição normal, porém com **caudas pesadas** (leptocúrtica), indicando que eventos extremos (crashes ou ralis) são mais frequentes do que uma distribuição gaussiana pura sugeriria.

### 5\. Médias Móveis

* Cruzamentos da MA\_20 com a MA\_50 (golden/death cross) podem ser identificados visualmente nos gráficos de preço, servindo como sinais de tendência de curto e médio prazo.

\---

## 🚀 Melhorias Futuras

|#|Melhoria|Descrição|
|-|-|-|
|1|**Dashboard Interativo**|Desenvolver interface web com **Streamlit** ou **Plotly Dash** permitindo ao usuário selecionar ativos, período e métricas dinamicamente|
|2|**Modelo Preditivo**|Implementar modelos de séries temporais (**LSTM**, **Prophet** ou **ARIMA**) para previsão de preços e retornos futuros|
|3|**API REST**|Criar uma **API com FastAPI** que sirva os dados processados em tempo real, viabilizando integração com outros sistemas e dashboards|
|4|**Análise de Portfólio**|Adicionar módulo de **Teoria Moderna de Portfólio** (Markowitz) para calcular a fronteira eficiente e a alocação ótima entre os ativos|
|5|**Alertas Automáticos**|Implementar sistema de **notificações** (e-mail ou Telegram) quando determinadas condições de mercado forem identificadas (ex: cruzamento de médias)|

\---

## 👤 Autor

**R0costa**   
[LinkedIn](https://linkedin.com/in/kauanaraujo7) · [GitHub](https://github.com/R0costa) · [E-mail](barroskauan15@gmail.com)

\---

## 📄 Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

\---

> ⭐ Se este projeto foi útil para você, considere deixar uma estrela no repositório!

