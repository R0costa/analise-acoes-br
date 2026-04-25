"""
main.py
-------
Script principal do projeto "Análise Exploratória do Mercado de Ações Brasileiro".

Executa o pipeline completo:
    1. Coleta de dados históricos via yfinance
    2. Tratamento e enriquecimento dos dados
    3. Geração de estatísticas descritivas
    4. Geração e salvamento de gráficos

Uso:
    python main.py
"""

import sys
import os
from datetime import datetime

# Garante que o Python encontre o pacote 'src' independentemente de onde o script é chamado
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_collector import download_stock_data, load_stock_data
from src.data_processor import process_all_stocks, get_descriptive_stats
from src.visualizer import generate_all_charts


# ──────────────────────────────────────────────
# CONFIGURAÇÕES DO PROJETO
# ──────────────────────────────────────────────

# Ativos listados na B3 para análise
TICKERS = ["WEGE3.SA", "PETR4.SA", "VALE3.SA"]

# Período de análise (aproximadamente 3 anos)
START_DATE = "2021-01-01"
END_DATE = datetime.today().strftime("%Y-%m-%d")

# Pastas de saída
DATA_PATH = "data/"
IMAGES_PATH = "images/"

# Se True, baixa os dados novamente mesmo que já existam na pasta /data
FORCE_DOWNLOAD = False


# ──────────────────────────────────────────────
# FUNÇÕES AUXILIARES
# ──────────────────────────────────────────────

def check_existing_data(tickers: list[str], data_path: str) -> bool:
    """Verifica se os arquivos CSV de todos os tickers já existem localmente."""
    for ticker in tickers:
        file_name = ticker.replace(".SA", "") + ".csv"
        if not os.path.exists(os.path.join(data_path, file_name)):
            return False
    return True


def print_section(title: str) -> None:
    """Formata e imprime um separador de seção no terminal."""
    width = 60
    print(f"\n{'=' * width}")
    print(f"  {title}")
    print(f"{'=' * width}")


# ──────────────────────────────────────────────
# PIPELINE PRINCIPAL
# ──────────────────────────────────────────────

def main():
    start_time = datetime.now()

    print("\n" + "=" * 60)
    print("  ANÁLISE EXPLORATÓRIA — MERCADO DE AÇÕES BRASILEIRO")
    print(f"  Ativos: {', '.join(t.replace('.SA', '') for t in TICKERS)}")
    print(f"  Período: {START_DATE} → {END_DATE}")
    print("=" * 60)

    # ── ETAPA 1: Coleta de dados ──────────────────────────────
    print_section("ETAPA 1 — Coleta de Dados")

    data_exists = check_existing_data(TICKERS, DATA_PATH)

    if data_exists and not FORCE_DOWNLOAD:
        print("  ℹ Arquivos CSV encontrados. Carregando dados locais...")
        stock_data = load_stock_data(TICKERS, DATA_PATH)
    else:
        if FORCE_DOWNLOAD:
            print("  ℹ FORCE_DOWNLOAD=True. Baixando dados novamente...")
        else:
            print("  ℹ Arquivos CSV não encontrados. Iniciando download...")
        stock_data = download_stock_data(TICKERS, START_DATE, END_DATE, DATA_PATH)

    if not stock_data:
        print("\n  ✗ Nenhum dado disponível. Encerrando execução.")
        sys.exit(1)

    # ── ETAPA 2: Tratamento e processamento ──────────────────
    print_section("ETAPA 2 — Tratamento e Processamento dos Dados")
    processed_data = process_all_stocks(stock_data)

    # ── ETAPA 3: Estatísticas descritivas ────────────────────
    print_section("ETAPA 3 — Estatísticas Descritivas")
    stats_df = get_descriptive_stats(processed_data)
    print("\n" + stats_df.to_string())

    # Salva as estatísticas em CSV para referência
    stats_path = os.path.join(DATA_PATH, "estatisticas_descritivas.csv")
    stats_df.to_csv(stats_path)
    print(f"\n  ✔ Estatísticas salvas em '{stats_path}'")

    # ── ETAPA 4: Geração de gráficos ─────────────────────────
    print_section("ETAPA 4 — Geração de Gráficos")
    generate_all_charts(processed_data, IMAGES_PATH)

    # ── RESUMO FINAL ─────────────────────────────────────────
    elapsed = (datetime.now() - start_time).seconds
    print_section("ANÁLISE CONCLUÍDA")
    print(f"  ⏱ Tempo total: {elapsed}s")
    print(f"  📁 Dados:     '{DATA_PATH}'")
    print(f"  🖼  Gráficos:  '{IMAGES_PATH}'")
    print("\n  Obrigado por usar este projeto!\n")


if __name__ == "__main__":
    main()
