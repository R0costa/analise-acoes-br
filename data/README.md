Esta pasta armazena os arquivos CSV com os dados históricos baixados via yfinance.

Arquivos gerados após a execução do projeto:
- WEGE3.csv                      → Dados históricos da WEG S.A.
- PETR4.csv                      → Dados históricos da Petrobras PN
- VALE3.csv                      → Dados históricos da Vale S.A.
- estatisticas_descritivas.csv   → Tabela consolidada de métricas por ativo

Os arquivos CSV não são versionados por padrão (ver .gitignore).
Execute `python main.py` para gerá-los automaticamente.
