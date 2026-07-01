# ===================================
# Métodos do Motor
# ===================================

def obter_gastos_maior_categoria(perfil):

        saidas = transacoes[
            (transacoes["id_cliente"] == perfil["id"])
            &
            (transacoes["tipo"] == "saida")
        ]

        if not saidas.empty:

            resumo = (
                saidas
                .groupby("categoria")["valor"]
                .sum()
            )

            categoria = resumo.idxmax()

            valor = resumo.max()

            return (
                f"Sua maior despesa está na categoria "
                f"'{categoria}', totalizando "
                f"R$ {formatar_moeda(valor)}."
            )

def obter_gastos(perfil):
        saidas = transacoes[
            (transacoes["id_cliente"] == perfil["id"])
            &
            (transacoes["tipo"] == "saida")
        ]

        total = saidas["valor"].sum()

        return(
            f"Suas despesas totalizam "
            f"R$ {formatar_moeda(total)}."
        )

def obter_historico(perfil):
    hist = historico[
        historico["id_cliente"] == perfil["id"]
    ]

    if hist.empty:
        return "Você não possui atendimentos registrados."

    hist = hist.sort_values("data", ascending=False)    #.head(5)

    linhas = []

    for _, atendimento in hist.iterrows():

        linhas.append(
            f"- {atendimento['data']} | "
            f"{atendimento['tema']} | "
            f"{atendimento['canal']}"
        )

    return (
        "Seu histórico de atendimento:\n"
        + "\n".join(linhas)
    )

def obter_metas(perfil):
    metas = perfil.get("metas", [])

    if not metas:
        return ("Você não possui metas cadastradas.")

    if metas:
        texto_metas = []

        for meta in metas:
            texto_metas.append(
                f"- {meta['meta']} "
                f"(R$ {formatar_moeda(meta['valor_necessario'])} "
                f"até {meta['prazo']})"
            )

        return (
            "Suas metas atuais são:\n"
            + "\n".join(texto_metas)
        )

def obter_transacoes(perfil):
        trans = transacoes[
            transacoes["id_cliente"] == perfil["id"]
        ]

        if not trans.empty:

            ultimas = (
                trans
                .sort_values("data", ascending=False)
                .head(3)
            )

            linhas = []

            for _, t in ultimas.iterrows():

                linhas.append(
                    f"- {t['data']} | "
                    f"{t['descricao']} | "
                    f"R$ {formatar_moeda(t['valor'])}"
                )

            return (
                "Suas últimas transações foram:\n"
                + "\n".join(linhas)
            )


def obter_ultimo_atendimento(perfil):
    hist = historico[
        historico["id_cliente"] == perfil["id"]
    ]

    if hist.empty:
        return "Você não possui atendimentos registrados."

    ultimo = (
        hist
        .sort_values("data")
        .iloc[-1]
    )

    return (
        f"Seu último atendimento foi em "
        f"{ultimo['data']} via {ultimo['canal']}.\n"
        f"Tema: {ultimo['tema']}.\n"
        f"Resumo: {ultimo['resumo']}."
    )
