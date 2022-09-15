"""
analyzers/mercado.py — Análise geral do mercado de vagas Python no Brasil.

Author: Guilherme Crepaldi

Gera estatísticas sobre total de vagas por fonte, por mês,
distribuição por cidade, etc.
"""

from collections import Counter, defaultdict
from datetime import datetime
from typing import Any

import config


def analisar_mercado(vagas: list[dict[str, Any]]) -> dict:
    """
    Retorna um dicionário com métricas gerais do mercado:
      - total_vagas
      - vagas_por_fonte
      - vagas_por_mes
      - vagas_por_cidade (top 15)
      - tipos_contratacao
      - senioridades
    """
    stats = {
        "total_vagas_analisadas": len(vagas),
        "vagas_por_fonte": Counter(),
        "vagas_por_mes": Counter(),
        "vagas_por_cidade": Counter(),
        "tipos_contratacao": Counter(),
        "senioridades": Counter(),
    }

    for vaga in vagas:
        # Fonte / site de origem
        fonte = vaga.get("fonte") or vaga.get("site") or "Nao informado"
        stats["vagas_por_fonte"][fonte] += 1

        # Data / mês
        data_str = vaga.get("data_publicacao") or vaga.get("data") or ""
        if data_str:
            try:
                # Tenta vários formatos comuns
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S"):
                    try:
                        dt = datetime.strptime(data_str[:10], fmt)
                        stats["vagas_por_mes"][dt.strftime("%Y-%m")] += 1
                        break
                    except ValueError:
                        continue
            except Exception:
                pass

        # Cidade
        cidade = vaga.get("cidade") or vaga.get("local") or "Nao informado"
        stats["vagas_por_cidade"][cidade] += 1

        # Tipo de contratação
        tipo = vaga.get("tipo_contratacao") or vaga.get("tipo") or "Nao informado"
        stats["tipos_contratacao"][tipo] += 1

        # Senioridade
        nivel = vaga.get("senioridade") or vaga.get("nivel") or "Nao informado"
        stats["senioridades"][nivel] += 1

    # Ordena e limita cidades
    stats["vagas_por_cidade"] = dict(
        stats["vagas_por_cidade"].most_common(15)
    )
    stats["vagas_por_fonte"] = dict(stats["vagas_por_fonte"])
    stats["vagas_por_mes"] = dict(sorted(stats["vagas_por_mes"].items()))
    stats["tipos_contratacao"] = dict(stats["tipos_contratacao"])
    stats["senioridades"] = dict(stats["senioridades"])

    return stats
