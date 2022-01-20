"""
config.py — Configurações centrais do projeto vagas-analytics.

Author: Guilherme Crepaldi
"""

from pathlib import Path

# ── Caminhos ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"           # CSV/JSON do vagas-tech-scraper
SAMPLES_DIR = BASE_DIR / "samples"     # dados de exemplo simulados
OUTPUT_DIR = BASE_DIR / "output"       # gráficos e relatórios gerados
OUTPUT_DIR.mkdir(exist_ok=True)

# Nome dos arquivos esperados do scraper (nesta ordem de prioridade)
DATA_FILES = ["vagas.csv", "vagas.json"]

# Fallback para demonstração
SAMPLE_FILE = SAMPLES_DIR / "vagas_sample.csv"

# ── Paleta de cores (tema escuro clean) ──────────────────────────────
COR_PRIMARIA = "#00BFA5"       # teal
COR_SECUNDARIA = "#FF6F00"     # laranja escuro
COR_TERCEARIA = "#448AFF"      # azul claro
COR_FUNDO = "#1E1E1E"          # fundo escuro
COR_TEXTO = "#E0E0E0"          # texto claro
COR_DESTAQUE = "#FFD740"       # amarelo para highlights

# Cores para categorias (skills, empresas, etc.)
CORES_CATEGORIAS = [
    "#00BFA5", "#FF6F00", "#448AFF", "#FFD740",
    "#E040FB", "#FF5252", "#69F0AE", "#40C4FF",
    "#FFD740", "#FF6E40", "#B388FF", "#00E5FF",
]

# ── Configurações de gráficos ─────────────────────────────────────────
GRAFICO_LARGURA = 14
GRAFICO_ALTURA = 8
GRAFICO_DPI = 120
GRAFICO_FONTE_TAM = 11

# ── Faixas salariais nominais (para classificação) ────────────────────
FAIXAS_SALARIAIS = {
    "até 2k": (0, 2000),
    "2k-4k": (2000, 4000),
    "4k-7k": (4000, 7000),
    "7k-12k": (7000, 12000),
    "acima de 12k": (12000, 999999),
}
