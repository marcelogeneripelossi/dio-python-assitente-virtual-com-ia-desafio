# ==========================================================
# Contexto global
# ==========================================================

perfis = None
produtos = None
transacoes = None
historico = None
palavras_chave = None
chave_sugestoes = None

# ==========================================================
# Constantes
# ==========================================================

mapa_risco_perfil = {
    "baixo": "conservador",
    "medio": "moderado",
    "alto": "arrojado"
}

negacoes = {
    "dispensar",
    "dispenso",
    "forma alguma",
    "evitar",
    "jamais",
    "nada",
    "nao",
    "nem",
    "nem pensar",
    "nem quero",
    "nem sequer",
    "nunca"}

perfil_sinonimos = {
    "arriscado": "arrojado",
    "arriscar": "arrojado",
    "acoes": "arrojado",
    "acao": "arrojado",
    "bolsa": "arrojado",

    "seguro": "conservador",
    "seguranca": "conservador",

    "equilibrado": "moderado"
}

perfil_tipos = [
        "conservador",
        "conservadora",
        "conservadores",
        "conservadoras",
        "moderado",
        "moderada",
        "moderados",
        "moderadas",
        "arrojado",
        "arrojada",
        "arrojados",
        "arrojadas"
    ]
