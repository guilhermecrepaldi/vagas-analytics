"""
analyzers/salarios.py — Análise de faixas salariais das vagas Python.

Author: Guilherme Crepaldi

Trata valores como 'A combinar', 'Nao informado' e ranges como
'3k-5k' convertendo para a média do intervalo.
"""

import re
from collections import defaultdict
from statistics import mean, median
from typing import Any, Optional

import config


# salario.py: trata ranges tipo 3k-5k e converte pra media
def parse_salario(valor: str) -> Optional[float]:
    """
    Tenta extrair um valor numérico (em R$) de uma string de salário.

    Suporta:
      - "R$ 5.000,00" -> 5000.0
      - "5k" -> 5000.0
      - "3k-5k" -> 4000.0 (média do range)
      - "R$ 3.000 a R$ 5.000" -> 4000.0
      - None / "" / "A combinar" / "Nao informado" -> None
    """
    if not valor or not isinstance(valor, str):
        return None

    valor = valor.strip()
    if not valor or valor.lower() in ("a combinar", "não informado", "nao informado", "-"):
        return None

    # Normaliza: remove espaços extras, troca "a" por "-"
    normalizado = valor.lower().replace(" ", "")
    normalizado = re.sub(r"a(?=\d)", "-", normalizado)

    # Tenta extrair range (ex: 3k-5k ou 3000-5000)
    range_match = re.search(
        r"(?:r\$\s*)?(\d+[\.,]?\d*)\s*k?\s*[-–aà]\s*(?:r\$\s*)?(\d+[\.,]?\d*)\s*k?",
        normalizado,
    )
    if range_match:
        v1 = _parse_valor_simples(range_match.group(1))
        v2 = _parse_valor_simples(range_match.group(2))
        if v1 and v2:
            return round((v1 + v2) / 2, 2)

    # Valor único (ex: 5k, R$ 5000, 5000.00)
    valor_simples = _parse_valor_simples(valor)
    if valor_simples:
        return valor_simples

    return None


def _parse_valor_simples(texto: str) -> Optional[float]:
    """Converte '5k' -> 5000, '5.000,00' -> 5000, '5000' -> 5000."""
    # Remove símbolos de moeda e espaços
    texto = texto.replace("r$", "").replace(" ", "").replace(".", "").replace(",", ".")

    # Suporta sufixo k
    k_match = re.match(r"(\d+(?:\.\d+)?)\s*k$", texto, re.IGNORECASE)
    if k_match:
        return float(k_match.group(1)) * 1000

    try:
        return float(texto)
    except ValueError:
        return None


def _classificar_faixa(valor: float) -> str:
    """Classifica um valor salarial em faixas nominais."""
    for nome, (min_, max_) in config.FAIXAS_SALARIAIS.items():
        if min_ <= valor < max_:
            return nome
    return "acima de 12k"


def analisar_salarios(vagas: list[dict[str, Any]]) -> dict:
    """
    Retorna estatísticas salariais detalhadas.

    Inclui média por senioridade, média por cidade, distribuição
    por faixas, e total de vagas com salário informado.
    """
    salarios_por_senioridade = defaultdict(list)
    salarios_por_cidade = defaultdict(list)
    faixas_salariais: defaultdict = defaultdict(int)
    salarios_validos = []
    total_com_salario = 0
    total_sem_salario = 0

    for vaga in vagas:
        campo_salario = (
            vaga.get("salario")
            or vaga.get("salario_range")
            or vaga.get("remuneracao")
            or ""
        )
        salario = parse_salario(campo_salario)

        if salario is not None:
            total_com_salario += 1
            salarios_validos.append(salario)

            senioridade = vaga.get("senioridade") or vaga.get("nivel") or "Nao informado"
            salarios_por_senioridade[senioridade].append(salario)

            cidade = vaga.get("cidade") or vaga.get("local") or "Nao informado"
            salarios_por_cidade[cidade].append(salario)

            faixa = _classificar_faixa(salario)
            faixas_salariais[faixa] += 1
        else:
            total_sem_salario += 1

    # Calcula médias por senioridade
    media_por_senioridade = {}
    for nivel, valores in salarios_por_senioridade.items():
        if valores:
            media_por_senioridade[nivel] = {
                "media": round(mean(valores), 2),
                "mediana": round(median(valores), 2),
                "min": round(min(valores), 2),
                "max": round(max(valores), 2),
                "quantidade": len(valores),
            }

    # Top 10 cidades com mais dados salariais
    media_por_cidade = {}
    for cidade, valores in salarios_por_cidade.items():
        if len(valores) >= 2:  # Só inclui se tiver pelo menos 2 dados
            media_por_cidade[cidade] = {
                "media": round(mean(valores), 2),
                "mediana": round(median(valores), 2),
                "quantidade": len(valores),
            }

    # Ordena cidades por média (decrescente)
    media_por_cidade = dict(
        sorted(media_por_cidade.items(), key=lambda x: -x[1]["media"])
    )

    return {
        "salarios_validos": salarios_validos,
        "salario_medio_geral": round(mean(salarios_validos), 2) if salarios_validos else 0,
        "salario_mediano_geral": round(median(salarios_validos), 2) if salarios_validos else 0,
        "total_com_salario": total_com_salario,
        "total_sem_salario": total_sem_salario,
        "faixas_salariais": dict(sorted(faixas_salariais.items())),
        "media_por_senioridade": media_por_senioridade,
        "media_por_cidade": media_por_cidade,
    }
