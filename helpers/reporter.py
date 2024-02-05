"""
utils/reporter.py — Gera relatório markdown e HTML com os resultados
da análise, incluindo tabelas formatadas e referências aos gráficos.

Author: Guilherme Crepaldi
"""

from datetime import datetime
from pathlib import Path
from typing import Any

import config

# ── Template HTML ─────────────────────────────────────────────────────
_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  body {{
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    max-width: 960px; margin: 2rem auto; padding: 0 1rem;
    background: {bg}; color: {text};
    line-height: 1.6;
  }}
  h1 {{ color: {primary}; border-bottom: 2px solid {primary}; padding-bottom: 0.3rem; }}
  h2 {{ color: {secondary}; margin-top: 2rem; }}
  h3 {{ color: {tertiary}; }}
  table {{
    width: 100%; border-collapse: collapse; margin: 1rem 0;
    background: {card_bg}; border-radius: 8px; overflow: hidden;
  }}
  th, td {{ padding: 0.6rem 1rem; text-align: left; border-bottom: 1px solid {border}; }}
  th {{ background: {header_bg}; color: {primary}; font-weight: 600; }}
  tr:hover {{ background: {hover_bg}; }}
  img {{ max-width: 100%; border-radius: 8px; margin: 1rem 0; box-shadow: 0 2px 12px rgba(0,0,0,0.3); }}
  .stats-grid {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem; margin: 1.5rem 0;
  }}
  .stat-card {{
    background: {card_bg}; border-radius: 8px; padding: 1.2rem;
    text-align: center; border: 1px solid {border};
  }}
  .stat-value {{ font-size: 1.8rem; font-weight: 700; color: {primary}; }}
  .stat-label {{ font-size: 0.85rem; color: {muted}; margin-top: 0.3rem; }}
  .footer {{ margin-top: 3rem; text-align: center; font-size: 0.85rem; color: {muted}; }}
</style>
</head>
<body>
{content}
<div class="footer">
  <p>Gerado em {date} pelo <strong>vagas-analytics</strong></p>
</div>
</body>
</html>"""


def _tabela_md(cabecalhos: list[str], linhas: list[list], title: str = "") -> str:
    """Monta tabela markdown."""
    md = f"\n### {title}\n\n" if title else "\n"
    md += "| " + " | ".join(cabecalhos) + " |\n"
    md += "| " + " | ".join("---" for _ in cabecalhos) + " |\n"
    for linha in linhas:
        md += "| " + " | ".join(str(c) for c in linha) + " |\n"
    return md


def _tabela_html(cabecalhos: list[str], linhas: list[list]) -> str:
    """Monta tabela HTML."""
    html = "<table><thead><tr>"
    for h in cabecalhos:
        html += f"<th>{h}</th>"
    html += "</tr></thead><tbody>"
    for linha in linhas:
        html += "<tr>"
        for cel in linha:
            html += f"<td>{cel}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html


def _fmt(valor: Any) -> str:
    """Formata valor bonitinho pra tabela."""
    if isinstance(valor, float):
        if valor >= 1000:
            return f"R$ {valor:,.0f}".replace(",", ".")
        return f"R$ {valor:,.2f}"
    return str(valor)


def gerar_relatorio(
    mercado: dict,
    skills: dict,
    salarios: dict,
    empresas: dict,
    graficos_gerados: list[tuple[str, Path]],
    export_html: bool = True,
) -> str:
    """
    Gera relatório markdown (e HTML opcional) com todos os resultados.
    Retorna o markdown como string.
    """
    now = datetime.now().strftime("%d/%m/%Y às %H:%M")

    # ── Cabeçalho ──────────────────────────────────────────────────
    md = f"# 📊 Relatório de Análise — Mercado Python Brasil\n\n"
    md += f"**Gerado em:** {now}  \n"
    md += f"**Total de vagas analisadas:** {mercado['total_vagas_analisadas']}\n\n"
    md += "---\n\n"

    # ── Cards de resumo (markdown compacto) ────────────────────────
    md += "## 📈 Resumo\n\n"
    md += f"- **Total de vagas:** {mercado['total_vagas_analisadas']}\n"
    if salarios["salario_medio_geral"]:
        md += f"- **Salário médio:** R$ {salarios['salario_medio_geral']:,.0f}\n"
        md += f"- **Salário mediano:** R$ {salarios['salario_mediano_geral']:,.0f}\n"
    md += f"- **Empresas diferentes:** {empresas['total_empresas']}\n"
    md += f"- **Skills diferentes detectadas:** {len(skills['skills_counts'])}\n\n"

    # ── Vagas por fonte ────────────────────────────────────────────
    md += "## 🗂️ Vagas por Fonte\n\n"
    if mercado["vagas_por_fonte"]:
        linhas = [[f, str(n)] for f, n in mercado["vagas_por_fonte"].items()]
        md += _tabela_md(["Fonte", "Vagas"], linhas)
        md += "\n"
    else:
        md += "_Sem dados de fonte._\n\n"

    # ── Contratação ────────────────────────────────────────────────
    md += "## 💼 Tipos de Contratação\n\n"
    if mercado["tipos_contratacao"]:
        linhas = [[t, str(n)] for t, n in mercado["tipos_contratacao"].items()]
        md += _tabela_md(["Tipo", "Vagas"], linhas)
        md += "\n"
    else:
        md += "_Sem dados de contratação._\n\n"

    # ── Senioridades ───────────────────────────────────────────────
    md += "## 🎯 Senioridades\n\n"
    if mercado["senioridades"]:
        linhas = [[s, str(n)] for s, n in mercado["senioridades"].items()]
        md += _tabela_md(["Senioridade", "Vagas"], linhas)
        md += "\n"

    # ── Top Skills ─────────────────────────────────────────────────
    md += "## 🛠️ Skills Mais Pedidas\n\n"
    if skills["top_skills"]:
        linhas = [
            [s, str(n), f"{skills['skills_porcentagem'].get(s, 0)}%"]
            for s, n in list(skills["top_skills"].items())[:20]
        ]
        md += _tabela_md(["Skill", "Menções", "% Vagas"], linhas)
        md += "\n"

    # ── Salários ───────────────────────────────────────────────────
    md += "## 💰 Análise Salarial\n\n"
    md += f"- **Vagas com salário informado:** {salarios['total_com_salario']}\n"
    md += f"- **Vagas sem salário:** {salarios['total_sem_salario']}\n"
    if salarios["salario_medio_geral"]:
        md += f"- **Salário médio geral:** R$ {salarios['salario_medio_geral']:,.0f}\n"
        md += f"- **Salário mediano geral:** R$ {salarios['salario_mediano_geral']:,.0f}\n\n"

    if salarios["faixas_salariais"]:
        md += "### Faixas Salariais\n\n"
        linhas = [[f, str(n)] for f, n in salarios["faixas_salariais"].items()]
        md += _tabela_md(["Faixa", "Vagas"], linhas)
        md += "\n"

    if salarios["media_por_senioridade"]:
        md += "### Média Salarial por Senioridade\n\n"
        linhas = [
            [n, _fmt(d["media"]), _fmt(d["mediana"]), _fmt(d["min"]),
             _fmt(d["max"]), str(d["quantidade"])]
            for n, d in salarios["media_por_senioridade"].items()
        ]
        md += _tabela_md(
            ["Senioridade", "Média", "Mediana", "Mínimo", "Máximo", "Vagas"],
            linhas,
        )
        md += "\n"

    if salarios["media_por_cidade"]:
        md += "### Salário Médio por Cidade\n\n"
        linhas = [
            [c, _fmt(d["media"]), _fmt(d["mediana"]), str(d["quantidade"])]
            for c, d in list(salarios["media_por_cidade"].items())[:15]
        ]
        md += _tabela_md(["Cidade", "Média", "Mediana", "Vagas"], linhas)
        md += "\n"

    # ── Empresas ───────────────────────────────────────────────────
    md += "## 🏢 Top Empresas Contratantes\n\n"
    if empresas["top_empresas"]:
        linhas = [[e, str(n)] for e, n in empresas["top_empresas"].items()]
        md += _tabela_md(["Empresa", "Vagas"], linhas)
        md += "\n"

    if empresas["setores"]:
        md += "### Setores de Atuação\n\n"
        linhas = [[s, str(n)] for s, n in empresas["setores"].items()]
        md += _tabela_md(["Setor", "Vagas"], linhas)
        md += "\n"

    # ── Gráficos ───────────────────────────────────────────────────
    md += "## 📸 Gráficos Gerados\n\n"
    if graficos_gerados:
        for nome, path in graficos_gerados:
            rel = path.relative_to(config.BASE_DIR) if path else nome
            md += f"![{nome}]({rel.as_posix()})\n\n"
    else:
        md += "_Nenhum gráfico gerado._\n\n"

    md += "---\n"
    md += f"*Relatório automático gerado pelo **vagas-analytics** em {now}.*\n"

    # ── Exporta HTML ────────────────────────────────────────────────
    if export_html:
        html_content = _gerar_html(
            md, mercado, skills, salarios, empresas, graficos_gerados, now
        )
        html_path = config.OUTPUT_DIR / "relatorio.html"
        html_path.write_text(html_content, encoding="utf-8")
        print(f"  [ok] Relatório HTML salvo: {html_path}")

    # Salva markdown
    md_path = config.OUTPUT_DIR / "relatorio.md"
    md_path.write_text(md, encoding="utf-8")
    print(f"  [ok] Relatório markdown salvo: {md_path}")

    return md


def _gerar_html(
    md: str,
    mercado: dict,
    skills: dict,
    salarios: dict,
    empresas: dict,
    graficos_gerados: list[tuple[str, Path]],
    date_str: str,
) -> str:
    """Constrói o HTML a partir dos dados estruturados."""
    # Cards
    cards = f"""
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">{mercado['total_vagas_analisadas']}</div>
        <div class="stat-label">Vagas Analisadas</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{empresas['total_empresas']}</div>
        <div class="stat-label">Empresas</div>
      </div>
    """

    if salarios["salario_medio_geral"]:
        cards += f"""
      <div class="stat-card">
        <div class="stat-value">R$ {salarios['salario_medio_geral']:,.0f}</div>
        <div class="stat-label">Salário Médio</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{len(skills['skills_counts'])}</div>
        <div class="stat-label">Skills Detectadas</div>
      </div>
        """

    cards += "</div>"

    # Tabelas
    content = f"<h1>📊 Mercado Python Brasil</h1>"
    content += f"<p><strong>Gerado em:</strong> {date_str}</p>"
    content += cards

    # Vagas por fonte
    if mercado["vagas_por_fonte"]:
        content += "<h2>🗂️ Vagas por Fonte</h2>"
        linhas = [[f, str(n)] for f, n in mercado["vagas_por_fonte"].items()]
        content += _tabela_html(["Fonte", "Vagas"], linhas)

    # Tipos de contratação
    if mercado["tipos_contratacao"]:
        content += "<h2>💼 Tipos de Contratação</h2>"
        linhas = [[t, str(n)] for t, n in mercado["tipos_contratacao"].items()]
        content += _tabela_html(["Tipo", "Vagas"], linhas)

    # Skills top 20
    if skills["top_skills"]:
        content += "<h2>🛠️ Top 20 Skills</h2>"
        linhas = [
            [s, str(n), f"{skills['skills_porcentagem'].get(s, 0)}%"]
            for s, n in list(skills["top_skills"].items())[:20]
        ]
        content += _tabela_html(["Skill", "Menções", "% Vagas"], linhas)

    # Salário por senioridade
    if salarios["media_por_senioridade"]:
        content += "<h2>💰 Salário por Senioridade</h2>"
        linhas = [
            [n, _fmt(d["media"]), _fmt(d["mediana"]), str(d["quantidade"])]
            for n, d in salarios["media_por_senioridade"].items()
        ]
        content += _tabela_html(["Senioridade", "Média", "Mediana", "Vagas"], linhas)

    # Top empresas
    if empresas["top_empresas"]:
        content += "<h2>🏢 Top 10 Empresas</h2>"
        linhas = [[e, str(n)] for e, n in list(empresas["top_empresas"].items())[:10]]
        content += _tabela_html(["Empresa", "Vagas"], linhas)

    # Gráficos
    if graficos_gerados:
        content += "<h2>📸 Gráficos</h2>"
        for nome, path in graficos_gerados:
            rel = path.relative_to(config.BASE_DIR).as_posix()
            content += f'<img src="../{rel}" alt="{nome}"><br>'

    return _HTML_TEMPLATE.format(
        title="Relatório — Mercado Python Brasil",
        content=content,
        date=date_str,
        bg=config.COR_FUNDO,
        text=config.COR_TEXTO,
        primary=config.COR_PRIMARIA,
        secondary=config.COR_SECUNDARIA,
        tertiary=config.COR_TERCEARIA,
        card_bg="#252526",
        header_bg="#1A1A1A",
        border="#333333",
        hover_bg="#2D2D2D",
        muted="#888888",
    )
