#!/usr/bin/env python3
"""
analytics.py — CLI principal do vagas-analytics.

Author: Guilherme Crepaldi

Uso:
    python analytics.py                      # análise completa no terminal
    python analytics.py --report             # gera relatório markdown+HTML
    python analytics.py --graficos           # gera todos os gráficos
    python analytics.py --export-html        # exporta relatório em HTML
    python analytics.py --all                # faz tudo

Flags combináveis: --report --graficos --export-html
"""

import argparse
import sys
from datetime import datetime

import config
from helpers.loader import carregar_vagas
from analyzers.mercado import analisar_mercado
from analyzers.skills import analisar_skills
from analyzers.salarios import analisar_salarios
from analyzers.empresas import analisar_empresas


def _print_header(texto: str):
    """Imprime um header bonitinho no terminal."""
    largura = 72
    print()
    print("=" * largura)
    print(f"  {texto}")
    print("=" * largura)


def _print_dict_como_tabela(dados: dict, cabecalho: tuple[str, str]):
    """Imprime dict como tabela simples no terminal."""
    chave_nome, valor_nome = cabecalho
    print(f"  {chave_nome:<30} {valor_nome}")
    print(f"  {'-'*30} {'-'*10}")
    for k, v in dados.items():
        print(f"  {str(k)[:30]:<30} {v}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="📊 vagas-analytics — Análise do mercado Python no Brasil",
    )
    parser.add_argument("--report", action="store_true",
                        help="Gera relatório markdown + HTML em output/")
    parser.add_argument("--graficos", action="store_true",
                        help="Gera gráficos PNG em output/")
    parser.add_argument("--export-html", action="store_true",
                        help="Exporta relatório em HTML (junto com --report)")
    parser.add_argument("--all", action="store_true",
                        help="Executa análise completa com relatório e gráficos")
    parser.add_argument("--data", type=str, default=None,
                        help="Caminho para CSV/JSON customizado")
    args = parser.parse_args()

    start = datetime.now()

    # ── Carrega dados ──────────────────────────────────────────────
    _print_header("📂 Carregando dados...")
    try:
        vagas = carregar_vagas()
    except FileNotFoundError as e:
        print(f"  [ERRO] {e}")
        sys.exit(1)

    print(f"  ✅ {len(vagas)} vagas carregadas.")
    print(f"  ⏱️  {datetime.now() - start}")

    # ── Análises ───────────────────────────────────────────────────
    _print_header("📈 Analisando mercado...")
    mercado = analisar_mercado(vagas)

    _print_header("🛠️  Analisando skills...")
    skills = analisar_skills(vagas)

    _print_header("💰 Analisando salários...")
    salarios = analisar_salarios(vagas)

    _print_header("🏢 Analisando empresas...")
    empresas = analisar_empresas(vagas)

    # ── Print resumo no terminal ───────────────────────────────────
    _print_header("📊 RESUMO DO MERCADO")
    print(f"  Total de vagas analisadas: {mercado['total_vagas_analisadas']}")
    print(f"  Empresas diferentes:       {empresas['total_empresas']}")
    print(f"  Skills detectadas:         {len(skills['skills_counts'])}")
    if salarios["salario_medio_geral"]:
        print(f"  Salário médio geral:       R$ {salarios['salario_medio_geral']:,.0f}")
        print(f"  Salário mediano geral:     R$ {salarios['salario_mediano_geral']:,.0f}")
    print()

    print("  Top 10 Skills mais pedidas:")
    for i, (skill, count) in enumerate(skills["top_skills"].items()):
        if i >= 10:
            break
        pct = skills["skills_porcentagem"].get(skill, 0)
        print(f"    {i+1:2d}. {skill:<20} {count:>4} vagas ({pct}%)")

    print()
    print("  Top 5 empresas contratantes:")
    for i, (emp, count) in enumerate(empresas["top_empresas"].items()):
        if i >= 5:
            break
        print(f"    {i+1:2d}. {emp:<25} {count} vagas")

    print()
    print("  Tipos de contratação:")
    for tipo, count in sorted(mercado["tipos_contratacao"].items(),
                               key=lambda x: -x[1]):
        print(f"    {tipo:<25} {count} vagas")

    if salarios["media_por_senioridade"]:
        print()
        print("  Salário médio por senioridade:")
        for nivel, dados in salarios["media_por_senioridade"].items():
            print(f"    {nivel:<25} R$ {dados['media']:>8,.0f}  ({dados['quantidade']} vagas)")

    # ── Geração de gráficos ────────────────────────────────────────
    graficos_gerados: list[tuple[str, Path]] = []
    if args.graficos or args.all:
        from visualizers import graficos as gfx

        _print_header("🖼️  Gerando gráficos...")

        # Barras: Top 15 skills
        if skills["top_skills"]:
            top15 = dict(list(skills["top_skills"].items())[:15])
            path = gfx.grafico_barras_horizontal(
                top15, "Skills Mais Pedidas — Python Brasil",
                "top_skills.png", xlabel="Menções")
            graficos_gerados.append(("Top 15 Skills", path))
            print(f"  [ok] top_skills.png")

        # Barras: Top 10 empresas
        if empresas["top_empresas"]:
            top10 = dict(list(empresas["top_empresas"].items())[:10])
            path = gfx.grafico_barras_horizontal(
                top10, "Top 10 Empresas Contratantes — Python Brasil",
                "top_empresas.png",
                cor=config.COR_SECUNDARIA, xlabel="Vagas")
            graficos_gerados.append(("Top 10 Empresas", path))
            print(f"  [ok] top_empresas.png")

        # Pizza: tipos de contratação
        if mercado["tipos_contratacao"]:
            path = gfx.grafico_pizza(
                mercado["tipos_contratacao"],
                "Tipos de Contratação",
                "tipos_contratacao.png")
            graficos_gerados.append(("Tipos de Contratação", path))
            print(f"  [ok] tipos_contratacao.png")

        # Pizza: faixas salariais
        if salarios["faixas_salariais"]:
            path = gfx.grafico_pizza(
                salarios["faixas_salariais"],
                "Distribuição Salarial — Faixas",
                "faixas_salariais.png")
            graficos_gerados.append(("Faixas Salariais", path))
            print(f"  [ok] faixas_salariais.png")

        # Dispersão: salários
        if salarios["salarios_validos"]:
            path = gfx.grafico_dispersao_salarios(
                salarios["salarios_validos"],
                "Distribuição de Salários por Vaga",
                "salarios_dispersao.png")
            graficos_gerados.append(("Dispersão Salários", path))
            print(f"  [ok] salarios_dispersao.png")

        # Barras agrupadas: média e mediana por senioridade
        if salarios["media_por_senioridade"]:
            path = gfx.grafico_barras_agrupadas(
                salarios["media_por_senioridade"],
                "Salário Médio e Mediano por Senioridade",
                "salarios_senioridade.png",
                ylabel="Salário (R$)")
            graficos_gerados.append(("Salários por Senioridade", path))
            print(f"  [ok] salarios_senioridade.png")

        # Wordcloud de skills
        if skills["skills_counts"]:
            from visualizers.wordcloud import gerar_wordcloud
            path = gerar_wordcloud(
                skills["skills_counts"],
                "wordcloud_skills.png",
                title="Skills em Vagas Python — Brasil",
            )
            if path:
                graficos_gerados.append(("Wordcloud Skills", path))
                print(f"  [ok] wordcloud_skills.png")
            else:
                print(f"  [-] wordcloud_skills.png pulado (biblioteca não disponível)")

        # Pizza: senioridades
        if mercado["senioridades"]:
            path = gfx.grafico_pizza(
                mercado["senioridades"],
                "Distribuição por Senioridade",
                "senioridades.png")
            graficos_gerados.append(("Senioridades", path))
            print(f"  [ok] senioridades.png")

    # ── Relatório ──────────────────────────────────────────────────
    if args.report or args.export_html or args.all:
        from helpers.reporter import gerar_relatorio

        _print_header("📝 Gerando relatório...")
        gerar_relatorio(
            mercado=mercado,
            skills=skills,
            salarios=salarios,
            empresas=empresas,
            graficos_gerados=graficos_gerados,
            export_html=(args.export_html or args.all),
        )

    # ── Final ──────────────────────────────────────────────────────
    elapsed = datetime.now() - start
    _print_header(f"✅ Concluído em {elapsed.total_seconds():.1f}s")
    print(f"  📁 Resultados em: {config.OUTPUT_DIR.resolve()}")
    print()


if __name__ == "__main__":
    main()
