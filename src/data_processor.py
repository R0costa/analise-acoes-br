"""
data_processor.py
-----------------
Módulo responsável pelo tratamento e limpeza dos dados de ações,
além do cálculo de métricas financeiras fundamentais.
"""

import pandas as pd
import numpy as np


def clean_stock_data(df: pd.DataFrame, ticker: str = "") -> pd.DataFrame:
    """
    Realiza a limpeza e padronização de um DataFrame de ações.

    Etapas:
        1. Remove linhas com todos os valores nulos
        2. Preenche NaNs isolados (forward fill, depois backward fill)
        3. Ordena o índice cronologicamente
        4. Remove duplicatas de datas

    Parâmetros:
        df     : DataFrame com dados brutos da ação
        ticker : Nome do ticker (apenas para logs)

    Retorno:
        DataFrame limpo e ordenado
    """
    initial_rows = len(df)

    # Remove linhas completamente vazias
    df = df.dropna(how="all")

    # Preenche valores ausentes isolados com o valor anterior (forward fill)
    # e com o próximo valor caso seja o primeiro registro (backward fill)
    df = df.ffill().bfill()

    # Garante ordenação cronológica
    df = df.sort_index()

    # Remove datas duplicadas mantendo o último registro
    df = df[~df.index.duplicated(keep="last")]

    removed_rows = initial_rows - len(df)
    if removed_rows > 0:
        print(f"  ℹ {ticker}: {removed_rows} linha(s) removida(s) durante a limpeza.")

    return df


def calculate_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula o retorno diário percentual com base no preço de fechamento ajustado.

    Fórmula: retorno_t = (Close_t / Close_{t-1} - 1) * 100

    Parâmetros:
        df : DataFrame com coluna 'Close'

    Retorno:
        DataFrame com coluna adicional 'Daily_Return'
    """
    df = df.copy()
    df["Daily_Return"] = df["Close"].pct_change() * 100
    return df


def calculate_moving_averages(
    df: pd.DataFrame, windows: list[int] = [20, 50]
) -> pd.DataFrame:
    """
    Calcula médias móveis simples (SMA) para as janelas especificadas.

    Parâmetros:
        df      : DataFrame com coluna 'Close'
        windows : Lista de janelas (em dias úteis) para cálculo

    Retorno:
        DataFrame com colunas adicionais 'MA_{janela}'
    """
    df = df.copy()
    for window in windows:
        column_name = f"MA_{window}"
        df[column_name] = df["Close"].rolling(window=window).mean()
    return df


def calculate_volatility(df: pd.DataFrame, window: int = 21) -> pd.DataFrame:
    """
    Calcula a volatilidade anualizada dos retornos diários.

    Fórmula: volatilidade = desvio_padrão_rolling * sqrt(252)
    (252 = número aproximado de pregões por ano na B3)

    Parâmetros:
        df     : DataFrame com coluna 'Daily_Return'
        window : Janela em dias úteis para o cálculo rolling (padrão: 21 ≈ 1 mês)

    Retorno:
        DataFrame com coluna adicional 'Volatility_Annualized'
    """
    df = df.copy()
    trading_days_per_year = 252
    df["Volatility_Annualized"] = (
        df["Daily_Return"].rolling(window=window).std() * np.sqrt(trading_days_per_year)
    )
    return df


def calculate_cumulative_return(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula o retorno acumulado em relação ao primeiro pregão da série.

    Fórmula: retorno_acumulado_t = (Close_t / Close_0 - 1) * 100

    Parâmetros:
        df : DataFrame com coluna 'Close'

    Retorno:
        DataFrame com coluna adicional 'Cumulative_Return'
    """
    df = df.copy()
    first_valid_close = df["Close"].dropna().iloc[0]
    df["Cumulative_Return"] = (df["Close"] / first_valid_close - 1) * 100
    return df


def process_all_stocks(
    stock_data: dict[str, pd.DataFrame],
) -> dict[str, pd.DataFrame]:
    """
    Aplica todo o pipeline de processamento em cada ação do dicionário.

    Pipeline:
        1. Limpeza dos dados brutos
        2. Cálculo de retorno diário
        3. Cálculo de médias móveis (MA_20 e MA_50)
        4. Cálculo de volatilidade anualizada
        5. Cálculo de retorno acumulado

    Parâmetros:
        stock_data : Dicionário {ticker: DataFrame bruto}

    Retorno:
        Dicionário {ticker: DataFrame processado}
    """
    processed_data = {}

    for ticker, df in stock_data.items():
        print(f"  → Processando {ticker}...")

        df_clean = clean_stock_data(df, ticker)
        df_returns = calculate_daily_returns(df_clean)
        df_ma = calculate_moving_averages(df_returns, windows=[20, 50])
        df_vol = calculate_volatility(df_ma)
        df_final = calculate_cumulative_return(df_vol)

        processed_data[ticker] = df_final
        print(f"    ✔ {ticker}: processamento concluído ({len(df_final)} registros)")

    return processed_data


def get_descriptive_stats(
    processed_data: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Compila estatísticas descritivas de todas as ações em uma tabela consolidada.

    Métricas incluídas:
        - Retorno médio diário (%)
        - Desvio padrão dos retornos (%)
        - Retorno mínimo e máximo diário (%)
        - Retorno acumulado total no período (%)
        - Volatilidade média anualizada (%)

    Parâmetros:
        processed_data : Dicionário {ticker: DataFrame processado}

    Retorno:
        DataFrame com estatísticas consolidadas por ação
    """
    stats_list = []

    for ticker, df in processed_data.items():
        returns = df["Daily_Return"].dropna()
        stats = {
            "Ativo": ticker.replace(".SA", ""),
            "Retorno Médio Diário (%)": round(returns.mean(), 4),
            "Desvio Padrão (%)": round(returns.std(), 4),
            "Retorno Mínimo (%)": round(returns.min(), 4),
            "Retorno Máximo (%)": round(returns.max(), 4),
            "Retorno Acumulado (%)": round(df["Cumulative_Return"].dropna().iloc[-1], 2),
            "Volatilidade Média Anualizada (%)": round(
                df["Volatility_Annualized"].dropna().mean(), 2
            ),
        }
        stats_list.append(stats)

    return pd.DataFrame(stats_list).set_index("Ativo")
