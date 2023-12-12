"""
visualizers/wordcloud.py — Nuvem de palavras das skills mais pedidas.

Author: Guilherme Crepaldi

Gera uma wordcloud estilizada salva em output/.
"""

from pathlib import Path
from typing import Optional
from collections import Counter

import config

# Tenta importar wordcloud; falha graciosa se não estiver instalado
try:
    from wordcloud import WordCloud
    HAS_WORDCLOUD = True
except ImportError:
    HAS_WORDCLOUD = False


def gerar_wordcloud(
    skills_counts: Counter,
    nome_arquivo: str = "wordcloud_skills.png",
    title: Optional[str] = None,
) -> Optional[Path]:
    """
    Gera uma nuvem de palavras a partir da contagem de skills.

    Args:
        skills_counts: Counter com {'skill': frequencia}
        nome_arquivo: nome do PNG em output/
        title: título opcional (inserido via matplotlib)

    Returns:
        Path para o arquivo gerado, ou None se wordcloud não estiver
        disponível.
    """
    if not HAS_WORDCLOUD:
        print("[AVISO] wordcloud não instalado. Pulando nuvem de palavras.")
        print("         Instale com: pip install wordcloud")
        return None

    wc = WordCloud(
        width=1600,
        height=900,
        background_color=config.COR_FUNDO,
        colormap="viridis",
        max_words=80,
        prefer_horizontal=0.7,
        relative_scaling=0.5,
        random_state=42,
        collocations=False,
    ).generate_from_frequencies(skills_counts)

    # Salva direto
    caminho = config.OUTPUT_DIR / nome_arquivo
    wc.to_file(str(caminho))

    # Se tiver matplotlib e título, sobrepõe legenda
    if title:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots(figsize=(16, 9),
                                    facecolor=config.COR_FUNDO)
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            ax.set_title(title, fontsize=18, fontweight="bold",
                         color=config.COR_TEXTO, pad=20)
            fig.savefig(caminho, dpi=120, bbox_inches="tight",
                        facecolor=config.COR_FUNDO)
            plt.close(fig)
        except ImportError:
            pass  # já salvou direto, de boa

    return caminho
