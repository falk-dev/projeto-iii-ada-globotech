from analise.sistema import SistemaAnaliseEngajamento

sistema_analise_engajamento = SistemaAnaliseEngajamento()
arquivo = "interacoes_globo.csv"
sistema_analise_engajamento.processar_interacoes_csv(arquivo)
