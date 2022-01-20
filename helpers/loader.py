"""
utils/loader.py — Carrega dados do CSV/JSON output do vagas-tech-scraper.

Author: Guilherme Crepaldi

Tenta carregar o CSV real primeiro. Se não achar, carrega o sample
com um warning amigável.
"""

import csv
import json
import warnings
from pathlib import Path
from typing import Any

import config


def carregar_vagas() -> list[dict[str, Any]]:
    """
    Retorna uma lista de dicionários com os dados das vagas.

    Prioridade:
      1. CSV produzido pelo vagas-tech-scraper (data/vagas.csv)
      2. JSON produzido pelo scraper (data/vagas.json)
      3. CSV de exemplo (samples/vagas_sample.csv) com warning
    """
    for data_file in config.DATA_FILES:
        caminho = config.DATA_DIR / data_file
        if caminho.exists():
            if data_file.endswith(".csv"):
                return _ler_csv(caminho)
            return _ler_json(caminho)

    # Fallback: dados de exemplo
    warnings.warn(
        f"Dados reais não encontrados em {config.DATA_DIR}. "
        f"Carregando amostra de demonstração: {config.SAMPLE_FILE}"
    )
    if config.SAMPLE_FILE.exists():
        return _ler_csv(config.SAMPLE_FILE)

    raise FileNotFoundError(
        f"Nenhum dado encontrado. Coloque um CSV/JSON em {config.DATA_DIR} "
        f"ou certifique-se de que {config.SAMPLE_FILE} existe."
    )


def _ler_csv(caminho: Path) -> list[dict[str, Any]]:
    """Lê um CSV e retorna lista de dicionários."""
    with open(caminho, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [linha for linha in reader]


def _ler_json(caminho: Path) -> list[dict[str, Any]]:
    """Lê um JSON (lista de objetos) e retorna lista de dicionários."""
    with open(caminho, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "vagas" in data:
        return data["vagas"]
    raise ValueError(f"Formato JSON não reconhecido em {caminho}")
