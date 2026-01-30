# hackaton
O projeto desenvolve a aplicação de um identificador de informações sensíveis em consultas públicas

Este projeto foi desenvolvido para o 1º Hackathon em Controle Social: Desafio Participa DF, na categoria Acesso à Informação.  
O objetivo é identificar automaticamente pedidos de acesso à informação que contenham dados pessoais (nome, CPF, RG, telefone, e-mail), garantindo que sejam corretamente classificados como não públicos, conforme a LGPD e o edital.

Objetivo
- Ler pedidos de acesso à informação em planilhas Excel.
- Detectar automaticamente dados pessoais usando Presidio Analyzer e spaCy em português.
- Reconhecer entidades específicas: CPF, RG, nome de pessoa, telefone, e-mail.
- Gerar uma nova planilha com a coluna IDENTIFICADOR_PII indicando se o pedido contém dados pessoais.
- Calcular métricas de desempenho (Precisão, Recall e F1-Score) com base em gabarito fornecido.

Pré-requisitos
- Python 3.11+
- pip (gerenciador de pacotes)

Dependências
Instale todas as bibliotecas com:
```bash
pip install -r requirements.txt
