# Notas de desenvolvimento — vagas-analytics

**Author:** Guilherme Crepaldi

## Pendências / Melhorias

### Skills (analyzers/skills.py)
- O parser de texto ainda ta cru — usa regex simples de palavra-chave.
- Preciso melhorar: sinonimos (ex: "py" = Python, "tf" = TensorFlow),
  contexto pra evitar falsos positivos, n-grams pra skills compostas
  tipo "machine learning".
- Talvez carregar skills de um YAML externo em vez de set fixo no código.
- Adicionar stemming/lemmatization básico.

### Salários (analyzers/salarios.py)
- Tratar "R$ 3.000,00 a R$ 5.000,00" já funciona.
- Mas "até R$ 6.000" / "a partir de R$ 10.000" ainda não trata
  (usa o valor como single point).
- Adicionar suporte a salário anual vs mensal (ex: "R$ 120k/ano").

### Gráficos (visualizers/graficos.py)
- Pizza ta horrivel ainda — labels se sobrepoem quando tem muitas categorias.
- Arrumar: talvez um donut chart ou agrupar categorias pequenas em "Outros".
- Adicionar mais charts: boxplot pra salários por senioridade, heatmap
  skills × cidade.

### Wordcloud (visualizers/wordcloud.py)
- Dependencia opcional — falha graciosa se não instalado.
- Talvez gerar com Pillow direto como fallback.

### Cobertura de dados
- JSON do scraper ainda tem campos diferentes — normalizar no loader.
- Adicionar schema validation com Pydantic ou dataclasses.

### Performance
- Tá lento com 10k+ vagas? Possivelmente — especialmente o parser de skills
  (O(n * m) onde m = skills conhecidas).
- Otimizar com regex compilado já foi feito, mas talvez vectorizar com
  pandas groupby pra agregações.

## Ideias futuras
- Dashboard interativo com Streamlit (streamlit_app.py)
- Exportar pra PDF via weasyprint
- API de recomendacao: "com suas skills X, voce se encaixa em Y vagas"
- Integração com o scraper via subprocess
- CI/CD: GitHub Actions pra rodar toda semana
- Testes unitarios com pytest
- Dockerfile pra execução isolada
