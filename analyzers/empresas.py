"""
analyzers/empresas.py — Análise das empresas que mais contratam Python no Brasil.

Author: Guilherme Crepaldi

Identifica top contratantes, setores de atuação (quando disponível)
e distribuição geográfica das empresas.
"""

from collections import Counter, defaultdict
from typing import Any


# Palavras-chave para inferir setor a partir do nome/descrição da empresa
_SETORES_CHAVES = {
    "banco": "Fintech / Bancário",
    "bradesco": "Fintech / Bancário",
    "itau": "Fintech / Bancário",
    "nubank": "Fintech / Bancário",
    "picpay": "Fintech / Bancário",
    "pagseguro": "Fintech / Bancário",
    "mercadopago": "Fintech / Bancário",
    "saude": "Saúde",
    "saúde": "Saúde",
    "hospital": "Saúde",
    "educacao": "Educação",
    "educação": "Educação",
    "escola": "Educação",
    "ecommerce": "E-commerce",
    "e-commerce": "E-commerce",
    "magalu": "E-commerce",
    "shopee": "E-commerce",
    "americanas": "E-commerce",
    "tech": "Tecnologia",
    "software": "Tecnologia",
    "tecnologia": "Tecnologia",
    "consultoria": "Consultoria",
    "consulting": "Consultoria",
    "startup": "Startup",
    "agro": "Agronegócio",
    "agronegocio": "Agronegócio",
    "logistica": "Logística",
    "logística": "Logística",
    "transporte": "Logística",
    "midia": "Mídia / Comunicação",
    "mídia": "Mídia / Comunicação",
    "comunicacao": "Mídia / Comunicação",
    "comunicação": "Mídia / Comunicação",
    "seguros": "Seguros",
    "seguradora": "Seguros",
    "energia": "Energia",
    "telecom": "Telecomunicações",
    "vivo": "Telecomunicações",
    "tim": "Telecomunicações",
    "claro": "Telecomunicações",
}


def _inferir_setor(empresa: str) -> str:
    """Tenta adivinhar o setor baseado no nome da empresa."""
    nome = empresa.lower()
    for palavra, setor in _SETORES_CHAVES.items():
        if palavra in nome:
            return setor
    return "Outros / Não classificado"


def analisar_empresas(vagas: list[dict[str, Any]]) -> dict:
    """
    Retorna estatísticas das empresas contratantes.

    Inclui top 20 empresas, distribuição por setor, e
    cidades com mais oportunidades por empresa.
    """
    empresas_counter: Counter = Counter()
    setores_counter: Counter = Counter()
    empresas_por_cidade: defaultdict = defaultdict(Counter)

    for vaga in vagas:
        empresa = vaga.get("empresa") or vaga.get("companhia") or "Nao informado"
        empresas_counter[empresa] += 1

        setor = _inferir_setor(empresa)
        setores_counter[setor] += 1

        cidade = vaga.get("cidade") or vaga.get("local") or "Nao informado"
        empresas_por_cidade[empresa][cidade] += 1

    top_empresas = dict(empresas_counter.most_common(20))
    setores = dict(setores_counter.most_common())

    # Empresas com vagas em múltiplas cidades
    empresas_multicidade = {
        emp: dict(cidades.most_common(5))
        for emp, cidades in empresas_por_cidade.items()
        if len(cidades) > 1
    }

    return {
        "top_empresas": top_empresas,
        "total_empresas": len(empresas_counter),
        "setores": setores,
        "empresas_multicidade": empresas_multicidade,
    }
