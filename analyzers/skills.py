"""
analyzers/skills.py — Identifica as skills mais pedidas nas vagas Python.

Author: Guilherme Crepaldi

Extrai skills dos textos das vagas usando um conjunto de palavras-chave
conhecidas do ecossistema Python. # isso ainda ta cru, preciso melhorar o parser de texto
"""

import re
from collections import Counter
from typing import Any

# Conjunto de skills conhecidas do mercado Python brasileiro
# TODO: carregar de um arquivo externo ou YAML no futuro
SKILLS_CONHECIDAS = {
    # Frameworks / Libs Python
    "django", "flask", "fastapi", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "sqlalchemy", "celery", "pytest",
    "requests", "beautifulsoup", "scrapy", "selenium", "airflow",
    "pyspark", "plotly", "dash", "streamlit", "bot framework",
    # Banco de dados
    "postgresql", "postgres", "mysql", "mongodb", "redis",
    "sqlite", "sql server", "oracle", "elasticsearch", "dynamodb",
    # Cloud / DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "k8s",
    "terraform", "ansible", "ci/cd", "jenkins", "gitlab ci",
    "github actions", "linux",
    # Ferramentas e conceitos
    "git", "github", "gitlab", "rest", "rest api", "graphql",
    "api", "microservicos", "microservices", "rabbitmq", "kafka",
    "api rest", "api restful",
    # Testes
    "tdd", "testes", "unit test", "integration test",
    # Outras linguagens (comuns em vagas Python)
    "javascript", "typescript", "react", "html", "css",
    "node.js", "vue.js", "angular",
    # Metodologias
    "scrum", "kanban", "agile", "devops",
}

# Compila regex para busca case-insensitive de palavras compostas
_SKILLS_PATTERNS = {
    skill: re.compile(r"\b" + re.escape(skill) + r"\b", re.IGNORECASE)
    for skill in sorted(SKILLS_CONHECIDAS, key=lambda s: -len(s))
}


def extrair_skills(vaga: dict[str, Any]) -> list[str]:
    """
    Extrai skills mencionadas no título, descrição e requisitos da vaga.
    Retorna uma lista com as skills encontradas (pode conter duplicatas
    se a mesma skill aparece em múltiplos campos).
    """
    texto = " ".join([
        vaga.get("titulo", ""),
        vaga.get("descricao", ""),
        vaga.get("requisitos", ""),
        vaga.get("skills", ""),
        vaga.get("stack", ""),
    ]).lower()

    encontradas = []
    for skill, pattern in _SKILLS_PATTERNS.items():
        if pattern.search(texto):
            encontradas.append(skill)

    return encontradas


def analisar_skills(vagas: list[dict[str, Any]]) -> dict:
    """
    Retorna estatísticas das skills encontradas nas vagas.
    """
    skills_counts: Counter = Counter()
    vagas_com_skill: Counter = Counter()

    for vaga in vagas:
        skills = extrair_skills(vaga)
        skills_unicas = set(skills)
        for skill in skills:
            skills_counts[skill] += 1
        for skill in skills_unicas:
            vagas_com_skill[skill] += 1

    total = len(vagas)
    # Skills mais mencionadas (contagem bruta)
    top_skills = dict(skills_counts.most_common(30))

    # Percentual de vagas que pedem cada skill
    pct_skills = {
        skill: round((count / total) * 100, 1)
        for skill, count in vagas_com_skill.most_common(30)
    }

    return {
        "skills_counts": skills_counts,
        "top_skills": top_skills,
        "skills_porcentagem": pct_skills,
        "total_vagas_analisadas": total,
    }
