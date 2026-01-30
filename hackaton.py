import pandas as pd
import spacy
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import SpacyNlpEngine

# 1. Configuração do Reconhecimento para o Contexto Brasileiro
def setup_brazilian_analyzer():
    # Carrega o modelo spaCy em português
    nlp = spacy.load("pt_core_news_lg")

    # Configura o Presidio para usar o spaCy em português
    nlp_engine = SpacyNlpEngine(models=[{"lang_code": "pt", "model_name": "pt_core_news_lg"}])
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, default_score_threshold=0.4)

    # Recognizer para CPF
    cpf_pattern = Pattern(name="cpf_pattern", regex=r"\d{3}\.?\d{3}\.?\d{3}-?\d{2}", score=0.8)
    cpf_recognizer = PatternRecognizer(
        supported_entity="CPF",
        patterns=[cpf_pattern],
        context=["cpf", "cadastro", "pessoa física"],
        supported_language="pt"
    )

    # Recognizer para RG
    rg_pattern = Pattern(name="rg_pattern", regex=r"\d{1,2}\.?\d{3}\.?\d{3}-?[\dX]", score=0.8)
    rg_recognizer = PatternRecognizer(
        supported_entity="RG",
        patterns=[rg_pattern],
        context=["rg", "identidade", "carteira"],
        supported_language="pt"
    )

    # Adiciona os novos reconhecedores ao engine
    analyzer.registry.add_recognizer(cpf_recognizer)
    analyzer.registry.add_recognizer(rg_recognizer)

    return analyzer

# 2. Processamento do Arquivo Excel
def processar_pedidos(input_file, output_file):
    df = pd.read_excel(input_file) # Lê o arquivo excel
    analyzer = setup_brazilian_analyzer()
    
    contem_pii = []

    for index, row in df.iterrows():
        texto_pedido = str(row['Texto Mascarado']) # Avalia os textos separadamente
        
        results = analyzer.analyze(
            text=texto_pedido,
            language='pt',
            entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "CPF", "RG"]
        )
        
        # Modelo detectou PII?
        detectado = len(results) > 0
        contem_pii.append("SIM - Contém Dados Pessoais" if detectado else "NÃO")


    # Adiciona coluna com resultado
    df['IDENTIFICADOR_PII'] = contem_pii
    df.to_excel(output_file, index=False)
    print(f"Análise concluída. Resultado salvo em: {output_file}")

# Execução
if __name__ == "__main__":
    processar_pedidos('AMOSTRA_e-SIC.xlsx', 'AMOSTRA_e-SIC_SINALIZADA.xlsx')

