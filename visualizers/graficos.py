"""
visualizers/graficos.py — Geração de gráficos com matplotlib.

Author: Guilherme Crepaldi

Tema escuro clean. Salva PNGs em output/.
# esse grafico de pizza ta horrivel, mas pro MVP serve
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from pathlib import Path
from typing import Optional

import config


# ── Tema escuro ───────────────────────────────────────────────────────
plt.style.use("dark_background")
plt.rcParams.update({
    "figure.facecolor": config.COR_FUNDO,
    "axes.facecolor": "#252526",
    "axes.edgecolor": "#555555",
    "axes.labelcolor": config.COR_TEXTO,
    "axes.titlecolor": config.COR_TEXTO,
    "text.color": config.COR_TEXTO,
    "xtick.color": config.COR_TEXTO,
    "ytick.color": config.COR_TEXTO,
    "grid.color": "#333333",
    "grid.alpha": 0.4,
    "font.size": config.GRAFICO_FONTE_TAM,
    "figure.dpi": config.GRAFICO_DPI,
})


def _salvar(fig: plt.Figure, nome: str) -> Path:
    """Salva a figura em output/ e retorna o caminho."""
    caminho = config.OUTPUT_DIR / nome
    fig.savefig(caminho, dpi=config.GRAFICO_DPI, bbox_inches="tight",
                facecolor=config.COR_FUNDO)
    plt.close(fig)
    return caminho


def _fmt_reais(x: float, _) -> str:
    """Formatador para eixos com valores em R$."""
    if x >= 1000:
        return f"R$ {x/1000:.0f}k"
    return f"R$ {x:.0f}"


# ── Gráficos ──────────────────────────────────────────────────────────

def grafico_barras_horizontal(
    dados: dict,
    titulo: str,
    nome_arquivo: str,
    cor: str = config.COR_PRIMARIA,
    xlabel: str = "",
) -> Path:
    """Gráfico de barras horizontal (ex: top skills, top empresas)."""
    labels = list(dados.keys())
    valores = list(dados.values())

    fig, ax = plt.subplots(figsize=(config.GRAFICO_LARGURA, config.GRAFICO_ALTURA))
    bars = ax.barh(range(len(labels)), valores, color=cor, edgecolor="none")

    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_title(titulo, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel(xlabel, fontsize=11)

    # Rótulos nas barras
    for i, (bar, val) in enumerate(zip(bars, valores)):
        ax.text(
            bar.get_width() + max(valores) * 0.01,
            bar.get_y() + bar.get_height() / 2,
            str(val),
            va="center", fontsize=9, color=config.COR_TEXTO,
        )

    fig.tight_layout()
    return _salvar(fig, nome_arquivo)


def grafico_pizza(
    dados: dict,
    titulo: str,
    nome_arquivo: str,
) -> Path:
    """
    Gráfico de pizza para distribuições (contratação, faixas salariais, etc.).
    # esse grafico de pizza ta horrivel, mas pro MVP serve
    """
    labels = list(dados.keys())
    valores = list(dados.values())
    cores = config.CORES_CATEGORIAS[: len(labels)]

    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(
        valores,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=cores,
        textprops={"color": config.COR_TEXTO, "fontsize": 10},
        pctdistance=0.75,
        wedgeprops={"edgecolor": config.COR_FUNDO, "linewidth": 1},
    )
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontsize(9)

    ax.set_title(titulo, fontsize=14, fontweight="bold", pad=15)
    fig.tight_layout()
    return _salvar(fig, nome_arquivo)


def grafico_dispersao_salarios(
    salarios: list[float],
    titulo: str,
    nome_arquivo: str,
    labels: Optional[list[str]] = None,
) -> Path:
    """
    Gráfico de dispersão mostrando distribuição dos salários.
    Cada ponto é uma vaga.
    """
    fig, ax = plt.subplots(figsize=(config.GRAFICO_LARGURA, 5))

    x = list(range(len(salarios)))
    ax.scatter(x, salarios, alpha=0.5, s=30, color=config.COR_PRIMARIA,
               edgecolors="none")

    # Linha da média
    media = np.mean(salarios)
    ax.axhline(media, color=config.COR_DESTAQUE, linestyle="--", linewidth=1.5,
               label=f"Média: R$ {media:,.0f}")

    ax.set_title(titulo, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Vagas (ordenadas)", fontsize=11)
    ax.set_ylabel("Salário (R$)", fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_reais))
    ax.legend(fontsize=10)

    fig.tight_layout()
    return _salvar(fig, nome_arquivo)


def grafico_barras_agrupadas(
    dados: dict[str, dict],
    titulo: str,
    nome_arquivo: str,
    ylabel: str = "",
) -> Path:
    """
    Gráfico de barras agrupadas para comparar métricas entre categorias
    (ex: média salarial por senioridade).
    """
    categorias = list(dados.keys())
    metrica = [dados[c].get("media", 0) for c in categorias]
    mediana = [dados[c].get("mediana", 0) for c in categorias]

    x = np.arange(len(categorias))
    width = 0.35

    fig, ax = plt.subplots(figsize=(config.GRAFICO_LARGURA, 6))
    bars1 = ax.bar(x - width / 2, metrica, width, label="Média",
                   color=config.COR_PRIMARIA)
    bars2 = ax.bar(x + width / 2, mediana, width, label="Mediana",
                   color=config.COR_SECUNDARIA)

    ax.set_xticks(x)
    ax.set_xticklabels(categorias, fontsize=10)
    ax.set_title(titulo, fontsize=14, fontweight="bold", pad=15)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_reais))
    ax.legend(fontsize=10)

    fig.tight_layout()
    return _salvar(fig, nome_arquivo)
