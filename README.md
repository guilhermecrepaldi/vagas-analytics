# vagas-analytics

📊 **Python job market analysis tool for Brazil.** Extracts trends, salary ranges, in-demand skills, and top hiring companies from job posting data collected by [vagas-tech-scraper](https://github.com/your-org/vagas-tech-scraper).

## Features

- **Market Overview** — total listings per source, per month, per city
- **Skills Analysis** — most demanded technologies, tag cloud generation
- **Salary Analysis** — average/median by seniority and city, range classification, handles "A combinar" / ranges like `3k-5k`
- **Company Analysis** — top hirers, industry classification
- **Visual Reports** — matplotlib charts (bar, pie, scatter) with dark theme
- **Exportable Reports** — Markdown and HTML output with embedded charts
- **CLI flags** — granular control over what to generate

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run full analysis (uses sample data if real data isn't present)
python analytics.py --all

# 3. Or run individual steps
python analytics.py                    # terminal summary only
python analytics.py --report           # markdown report
python analytics.py --graficos         # charts only
python analytics.py --export-html      # HTML report
```

## Project Structure

```
vagas-analytics/
├── analytics.py             # CLI entry point
├── config.py                # paths, colors, settings
├── analyzers/
│   ├── mercado.py           # overall market analysis
│   ├── skills.py            # skill extraction & counting
│   ├── salarios.py          # salary parsing & aggregation
│   └── empresas.py          # company & industry analysis
├── visualizers/
│   ├── graficos.py          # matplotlib charts (dark theme)
│   └── wordcloud.py         # word cloud generation
├── utils/
│   ├── loader.py            # CSV/JSON data loader
│   └── reporter.py          # markdown & HTML report builder
├── samples/
│   └── vagas_sample.csv     # 20 fictional job listings for demo
├── output/                  # generated charts & reports
├── requirements.txt
├── .gitignore
└── README.md
```

## Data Format

The tool expects CSV files with the following columns (flexible naming — multiple aliases are tried internally):

| Column              | Aliases                    | Description                          |
|---------------------|----------------------------|--------------------------------------|
| `titulo`            | —                          | Job title                            |
| `empresa`           | `companhia`                | Company name                         |
| `cidade`            | `local`                    | City / location                      |
| `remoto`            | —                          | Remote policy (sim/nao/hibrido)      |
| `salario`           | `salario_range`, `remuneracao` | Salary string (e.g. "R$ 5k-8k")  |
| `tipo_contratacao`  | `tipo`                     | CLT / PJ / Estágio                   |
| `senioridade`       | `nivel`                    | Seniority level                      |
| `data_publicacao`   | `data`                     | Publication date                     |
| `fonte`             | `site`                     | Source platform (LinkedIn, Gupy...)  |
| `descricao`         | `requisitos`, `skills`, `stack` | Job description text          |

Place your real data in `data/vagas.csv` (or `data/vagas.json`). If absent, the tool falls back to the sample file with a warning.

## Sample Data

The `samples/` folder contains 20 realistic fictional job listings from well-known Brazilian tech companies (Nubank, Itaú, Magalu, EBANX, QuintoAndar, Stone, etc.) covering multiple seniority levels, contract types, and salary ranges. Use it for demos or while waiting for real scraper output.

## Requirements

- Python 3.10+
- matplotlib
- numpy
- wordcloud (optional, for tag cloud)

## Output

Everything lands in `output/`:
- `top_skills.png` — horizontal bar chart
- `top_empresas.png` — top hiring companies
- `tipos_contratacao.png` — contract type distribution
- `faixas_salariais.png` — salary bracket pie chart
- `salarios_dispersao.png` — salary scatter plot
- `salarios_senioridade.png` — grouped bar chart (mean × median)
- `senioridades.png` — seniority distribution (pie)
- `wordcloud_skills.png` — tag cloud (if wordcloud installed)
- `relatorio.md` — full markdown report
- `relatorio.html` — HTML report with styling

## License

MIT

## Author

👤 **Guilherme Crepaldi**
