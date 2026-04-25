"""
visualizer.py
-------------
Módulo responsável pela geração e salvamento dos gráficos da análise exploratória.
Todos os gráficos são salvos na pasta /images no formato PNG de alta resolução.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np

# Paleta de cores consistente para todas as ações
COLORS = {
    "WEGE3.SA": "#1f77b4",   # Azul
    "PETR4.SA": "#d62728",   # Vermelho
    "VALE3.SA": "#2ca02c",   # Verde
}

# Nomes amigáveis para legendas
LABELS = {
    "WEGE3.SA": "WEGE3",
    "PETR4.SA": "PETR4",
    "VALE3.SA": "VALE3",
}

# Estilo global dos gráficos
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update({
    "figure.dpi": 150,
    "font.family": "DejaVu Sans",
    "axes.titlesize": 14,
    "axes.labelsize": 11,
    "legend.fontsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})


def _save_figure(fig: plt.Figure, filename: str, images_path: str = "images/") -> None:
    """Salva a figura no caminho especificado e fecha a figura para liberar memória."""
    os.makedirs(images_path, exist_ok=True)
    full_path = os.path.join(images_path, filename)
    fig.savefig(full_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✔ Gráfico salvo: '{full_path}'")


def plot_price_evolution(
    processed_data: dict[str, pd.DataFrame], images_path: str = "images/"
) -> None:
    """
    Gera um gráfico de linha individual para cada ação mostrando:
        - Preço de fechamento ajustado
        - Médias móveis de 20 e 50 dias

    Um arquivo PNG é gerado por ação.
    """
    for ticker, df in processed_data.items():
        label = LABELS.get(ticker, ticker)
        color = COLORS.get(ticker, "#333333")

        fig, ax = plt.subplots(figsize=(12, 5))

        ax.plot(df.index, df["Close"], label="Fechamento", color=color, linewidth=1.5, alpha=0.9)
        ax.plot(df.index, df["MA_20"], label="Média Móvel 20d", color="orange",
                linewidth=1.2, linestyle="--", alpha=0.85)
        ax.plot(df.index, df["MA_50"], label="Média Móvel 50d", color="purple",
                linewidth=1.2, linestyle="--", alpha=0.85)

        ax.set_title(f"{label} — Evolução do Preço e Médias Móveis", fontweight="bold")
        ax.set_xlabel("Data")
        ax.set_ylabel("Preço (R$)")
        ax.legend()
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b/%Y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.xticks(rotation=30)

        _save_figure(fig, f"preco_{label}.png", images_path)


def plot_price_comparison(
    processed_data: dict[str, pd.DataFrame], images_path: str = "images/"
) -> None:
    """
    Compara a evolução de preço normalizada de todas as ações em um único gráfico.
    Normalização: base 100 no primeiro pregão da série para facilitar a comparação.
    """
    fig, ax = plt.subplots(figsize=(13, 6))

    for ticker, df in processed_data.items():
        label = LABELS.get(ticker, ticker)
        color = COLORS.get(ticker, None)

        # Normaliza o preço: base 100 no início da série
        first_price = df["Close"].dropna().iloc[0]
        normalized_price = (df["Close"] / first_price) * 100

        ax.plot(df.index, normalized_price, label=label, color=color, linewidth=1.8)

    ax.axhline(y=100, color="gray", linewidth=0.8, linestyle=":", alpha=0.7)
    ax.set_title("Comparação de Desempenho (Base 100)", fontweight="bold")
    ax.set_xlabel("Data")
    ax.set_ylabel("Desempenho Relativo (Base 100)")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b/%Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=30)

    _save_figure(fig, "comparacao_desempenho.png", images_path)


def plot_cumulative_return(
    processed_data: dict[str, pd.DataFrame], images_path: str = "images/"
) -> None:
    """
    Plota o retorno acumulado (%) de cada ação ao longo do período analisado.
    """
    fig, ax = plt.subplots(figsize=(13, 6))

    for ticker, df in processed_data.items():
        label = LABELS.get(ticker, ticker)
        color = COLORS.get(ticker, None)
        ax.plot(df.index, df["Cumulative_Return"], label=label, color=color, linewidth=1.8)

    ax.axhline(y=0, color="gray", linewidth=0.8, linestyle=":", alpha=0.7)
    ax.set_title("Retorno Acumulado no Período (%)", fontweight="bold")
    ax.set_xlabel("Data")
    ax.set_ylabel("Retorno Acumulado (%)")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b/%Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=30)

    _save_figure(fig, "retorno_acumulado.png", images_path)


def plot_return_histograms(
    processed_data: dict[str, pd.DataFrame], images_path: str = "images/"
) -> None:
    """
    Gera histogramas de distribuição dos retornos diários para cada ação,
    com a curva KDE (densidade de kernel) sobreposta.
    """
    n_tickers = len(processed_data)
    fig, axes = plt.subplots(1, n_tickers, figsize=(6 * n_tickers, 5), sharey=False)

    if n_tickers == 1:
        axes = [axes]

    for ax, (ticker, df) in zip(axes, processed_data.items()):
        label = LABELS.get(ticker, ticker)
        color = COLORS.get(ticker, "#555555")
        returns = df["Daily_Return"].dropna()

        sns.histplot(returns, bins=60, kde=True, ax=ax, color=color, alpha=0.6, edgecolor="white")
        ax.axvline(returns.mean(), color="black", linestyle="--", linewidth=1.2,
                   label=f"Média: {returns.mean():.2f}%")
        ax.set_title(f"{label} — Distribuição dos Retornos Diários", fontweight="bold")
        ax.set_xlabel("Retorno Diário (%)")
        ax.set_ylabel("Frequência")
        ax.legend()

    fig.tight_layout(pad=3.0)
    _save_figure(fig, "histogramas_retornos.png", images_path)


def plot_volatility(
    processed_data: dict[str, pd.DataFrame], images_path: str = "images/"
) -> None:
    """
    Plota a volatilidade anualizada rolling (janela de 21 dias) ao longo do tempo.
    """
    fig, ax = plt.subplots(figsize=(13, 5))

    for ticker, df in processed_data.items():
        label = LABELS.get(ticker, ticker)
        color = COLORS.get(ticker, None)
        ax.plot(df.index, df["Volatility_Annualized"], label=label, color=color,
                linewidth=1.5, alpha=0.85)

    ax.set_title("Volatilidade Anualizada Rolling (Janela 21 dias)", fontweight="bold")
    ax.set_xlabel("Data")
    ax.set_ylabel("Volatilidade Anualizada (%)")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b/%Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=30)

    _save_figure(fig, "volatilidade.png", images_path)


def plot_correlation_heatmap(
    processed_data: dict[str, pd.DataFrame], images_path: str = "images/"
) -> None:
    """
    Gera um heatmap de correlação dos retornos diários entre todas as ações analisadas.
    """
    # Monta um DataFrame com os retornos diários de cada ação
    returns_df = pd.DataFrame({
        LABELS.get(ticker, ticker): df["Daily_Return"]
        for ticker, df in processed_data.items()
    })

    correlation_matrix = returns_df.corr()

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt=".3f",
        cmap="RdYlGn",
        vmin=-1,
        vmax=1,
        center=0,
        square=True,
        ax=ax,
        linewidths=0.5,
        annot_kws={"size": 12},
    )
    ax.set_title("Correlação dos Retornos Diários", fontweight="bold")

    _save_figure(fig, "correlacao_retornos.png", images_path)


def plot_boxplot_returns(
    processed_data: dict[str, pd.DataFrame], images_path: str = "images/"
) -> None:
    """
    Gera um boxplot comparativo dos retornos diários de todas as ações.
    Permite identificar outliers e a dispersão dos retornos.
    """
    returns_df = pd.DataFrame({
        LABELS.get(ticker, ticker): processed_data[ticker]["Daily_Return"]
        for ticker in processed_data
    })

    fig, ax = plt.subplots(figsize=(9, 6))
    returns_df.boxplot(
        ax=ax,
        patch_artist=True,
        boxprops=dict(facecolor="lightblue", color="steelblue"),
        medianprops=dict(color="firebrick", linewidth=2),
        flierprops=dict(marker="o", markersize=3, alpha=0.4, color="gray"),
    )

    ax.axhline(y=0, color="gray", linewidth=0.8, linestyle=":", alpha=0.7)
    ax.set_title("Boxplot dos Retornos Diários por Ação", fontweight="bold")
    ax.set_xlabel("Ativo")
    ax.set_ylabel("Retorno Diário (%)")

    _save_figure(fig, "boxplot_retornos.png", images_path)


def generate_all_charts(
    processed_data: dict[str, pd.DataFrame], images_path: str = "images/"
) -> None:
    """
    Executa a geração de todos os gráficos em sequência.

    Gráficos gerados:
        1. Evolução de preço individual com médias móveis (1 por ação)
        2. Comparação de desempenho normalizado
        3. Retorno acumulado no período
        4. Histogramas de retornos diários
        5. Volatilidade anualizada rolling
        6. Heatmap de correlação
        7. Boxplot comparativo dos retornos

    Parâmetros:
        processed_data : Dicionário {ticker: DataFrame processado}
        images_path    : Pasta onde os PNGs serão salvos
    """
    print("\n[Visualizações] Gerando gráficos...")

    plot_price_evolution(processed_data, images_path)
    plot_price_comparison(processed_data, images_path)
    plot_cumulative_return(processed_data, images_path)
    plot_return_histograms(processed_data, images_path)
    plot_volatility(processed_data, images_path)
    plot_correlation_heatmap(processed_data, images_path)
    plot_boxplot_returns(processed_data, images_path)

    print(f"\n  ✔ Todos os gráficos foram salvos em '{images_path}'")
