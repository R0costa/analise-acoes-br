"""
data_collector.py
-----------------
Módulo responsável pela coleta de dados históricos de ações brasileiras
utilizando a biblioteca yfinance.
"""

import os
import yfinance as yf
import pandas as pd
from datetime import datetime


# Mapeamento de tickers para nomes amigáveis
TICKER_NAMES = {
    "WEGE3.SA": "WEG S.A.",
    "PETR4.SA": "Petrobras PN",
    "VALE3.SA": "Vale S.A.",
}


def download_stock_data(
    tickers: list[str],
    start_date: str,
    end_date: str,
    save_path: str = "data/",
) -> dict[str, pd.DataFrame]:
    """
    Baixa dados históricos de ações via yfinance e salva em CSV.

    Parâmetros:
        tickers     : Lista de tickers no formato Yahoo Finance (ex: ["WEGE3.SA"])
        start_date  : Data de início no formato "YYYY-MM-DD"
        end_date    : Data de fim no formato "YYYY-MM-DD"
        save_path   : Caminho da pasta onde os CSVs serão salvos

    Retorno:
        Dicionário {ticker: DataFrame} com os dados baixados
    """
    os.makedirs(save_path, exist_ok=True)
    stock_data = {}

    for ticker in tickers:
        print(f"  → Baixando dados de {ticker} ({TICKER_NAMES.get(ticker, ticker)})...")

        try:
            raw_df = yf.download(ticker, start=start_date, end=end_date, progress=False)

            if raw_df.empty:
                print(f"    ⚠ Nenhum dado encontrado para {ticker}. Pulando.")
                continue

            # Flatten MultiIndex columns if present (yfinance >= 0.2 may return them)
            if isinstance(raw_df.columns, pd.MultiIndex):
                raw_df.columns = raw_df.columns.get_level_values(0)

            # Garante que o índice de datas seja do tipo datetime
            raw_df.index = pd.to_datetime(raw_df.index)
            raw_df.index.name = "Date"

            # Salva CSV com o nome do ticker (sem ".SA" para limpeza do nome do arquivo)
            file_name = ticker.replace(".SA", "") + ".csv"
            file_path = os.path.join(save_path, file_name)
            raw_df.to_csv(file_path)

            stock_data[ticker] = raw_df
            print(f"    ✔ {len(raw_df)} registros salvos em '{file_path}'")

        except Exception as e:
            print(f"    ✗ Erro ao baixar {ticker}: {e}")

    return stock_data


def load_stock_data(tickers: list[str], data_path: str = "data/") -> dict[str, pd.DataFrame]:
    """
    Carrega dados de ações a partir de arquivos CSV previamente salvos.

    Parâmetros:
        tickers   : Lista de tickers no formato Yahoo Finance (ex: ["WEGE3.SA"])
        data_path : Caminho da pasta onde os CSVs estão armazenados

    Retorno:
        Dicionário {ticker: DataFrame} com os dados carregados
    """
    stock_data = {}

    for ticker in tickers:
        file_name = ticker.replace(".SA", "") + ".csv"
        file_path = os.path.join(data_path, file_name)

        if not os.path.exists(file_path):
            print(f"  ⚠ Arquivo não encontrado: {file_path}")
            continue

        df = pd.read_csv(file_path, index_col="Date", parse_dates=True)
        stock_data[ticker] = df
        print(f"  ✔ Dados de {ticker} carregados ({len(df)} registros)")

    return stock_data
