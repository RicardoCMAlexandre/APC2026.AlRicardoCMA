import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#VARIAVEL ----------
ARQUIVO_MORADORES = "moradores.csv"
VALORES_SENTINELA = [99999, 88888, 77777]

df_original = None
df_moradores = None
df_filtrado = None
canvas_grafico = None

# FUNCAO CONVERTER PONTO VIRGULA -----
def converter_para_numero(serie):
    return pd.to_numeric(
        serie.astype(str).str.replace(",", ".", regex=False),
        errors="coerce"
    )

# FUNCAO ABRI ARQUIVO PDAD/ TRANSFORMA NUMEROS ---
def carregar_dados():
    df = pd.read_csv(ARQUIVO_MORADORES, sep=None, engine="python")

    # PROBLEMA - PRIMEIRA COLUNA DO XLSX
    df.columns = df.columns.str.replace("\ufeff", "", regex=False)

    colunas_numericas = [
        "localidade",
        "idade_calculada",
        "E03",
        "escolaridade",
        "I04",
        "I13",
        "renda_ind"
    ]

    for coluna in colunas_numericas:
        if coluna in df.columns:
            df[coluna] = converter_para_numero(df[coluna])

    return df

# FUNCAO REBUT DAS INFORMAÇÕES -----
# revisar, esta retirando muita gente, tirando dados, fazer no final -----
def limpar_dados(df):
    
    df_limpo = df.copy()

    colunas_usadas = [
        "localidade",
        "idade_calculada",
        "E03",
        "escolaridade",
        "I04",
        "I13"
    ]

    for coluna in colunas_usadas:
        if coluna in df_limpo.columns:
            df_limpo = df_limpo[~df_limpo[coluna].isin(VALORES_SENTINELA)]

    df_limpo = df_limpo.dropna(subset=colunas_usadas)

    df_limpo = df_limpo[df_limpo["I04"] == 1]

    return df_limpo

# FUNCAO TROCA NOME / FAZ ROTULO
def criar_rotulos(df):
    df_rotulado = df.copy()

    mapa_genero = {
        1: "Masculino",
        2: "Feminino"
    }

    mapa_ocupacao = {
        1: "Empregado no setor público",
        2: "Militar / bombeiro / policial militar",
        3: "Empregado no setor privado",
        4: "Empregado doméstico",
        5: "Estágio remunerado",
        6: "Aprendiz",
        7: "Conta própria ou autônomo",
        8: "Empregador",
        9: "Serviço militar obrigatório",
        10: "Trabalhador não remunerado"
    }

    mapa_escolaridade = {
        1: "Sem instrução",
        2: "Fundamental incompleto",
        3: "Fundamental completo",
        4: "Médio incompleto",
        5: "Médio completo",
        6: "Superior incompleto",
        7: "Superior completo",
        8: "Sem classificação"
    }

    mapa_localidade = {
        5301: "Plano Piloto",
        5302: "Gama",
        5303: "Taguatinga",
        5304: "Brazlândia",
        5305: "Sobradinho",
        5306: "Planaltina",
        5307: "Paranoá",
        5308: "Núcleo Bandeirante",
        5309: "Ceilândia",
        5310: "Guará",
        5311: "Cruzeiro",
        5312: "Samambaia",
        5313: "Santa Maria",
        5314: "São Sebastião",
        5315: "Recanto das Emas",
        5316: "Lago Sul",
        5317: "Riacho Fundo",
        5318: "Lago Norte",
        5319: "Candangolândia",
        5320: "Águas Claras",
        5321: "Riacho Fundo II",
        5322: "Sudoeste e Octogonal",
        5323: "Varjão",
        5324: "Park Way",
        5325: "SCIA",
        5326: "Sobradinho II",
        5327: "Jardim Botânico",
        5328: "Itapoã",
        5329: "SIA",
        5330: "Vicente Pires",
        5331: "Fercal",
        5332: "Sol Nascente / Pôr do Sol",
        5333: "Arniqueira",
        5334: "Arapoanga",
        5335: "Água Quente",
        5336: "Área Rural",
        5241: "Águas Lindas de Goiás",
        5242: "Alexânia",
        5243: "Cidade Ocidental",
        5244: "Cristalina",
        5245: "Cocalzinho de Goiás",
        5246: "Formosa",
        5247: "Luziânia",
        5248: "Novo Gama",
        5249: "Padre Bernardo",
        5250: "Planaltina de Goiás",
        5251: "Santo Antônio do Descoberto",
        5252: "Valparaíso de Goiás"
    }

    df_rotulado["genero_nome"] = df_rotulado["E03"].map(mapa_genero)
    df_rotulado["ocupacao_nome"] = df_rotulado["I13"].map(mapa_ocupacao)
    df_rotulado["escolaridade_nome"] = df_rotulado["escolaridade"].map(mapa_escolaridade)
    df_rotulado["localidade_nome"] = df_rotulado["localidade"].map(mapa_localidade)

    df_rotulado["genero_nome"] = df_rotulado["genero_nome"].fillna("Não identificado")
    df_rotulado["ocupacao_nome"] = df_rotulado["ocupacao_nome"].fillna("Não identificado")
    df_rotulado["escolaridade_nome"] = df_rotulado["escolaridade_nome"].fillna("Não identificado")
    df_rotulado["localidade_nome"] = df_rotulado["localidade_nome"].fillna("Não identificado")

    return df_rotulado

# PROBLEMA DE TIRAR RENDA ---
def obter_renda_valida(df):
    renda_valida = df[
        ~df["renda_ind"].isin(VALORES_SENTINELA)
    ]["renda_ind"].dropna()

    return renda_valida

# FUNCAO DO FILTRO ----------
def atualizar_filtro():
    global df_filtrado

  # 3 topicos (+ 3)
    localidade_escolhida = combo_localidade.get()
    ocupacao_escolhida = combo_ocupacao.get()
    sexo_escolhido = combo_sexo.get()

    df_filtrado = df_moradores.copy()

    if localidade_escolhida != "Todas":
        df_filtrado = df_filtrado[
            df_filtrado["localidade_nome"] == localidade_escolhida
        ]

    if ocupacao_escolhida != "Todas":
        df_filtrado = df_filtrado[
            df_filtrado["ocupacao_nome"] == ocupacao_escolhida
        ]

    if sexo_escolhido != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["genero_nome"] == sexo_escolhido
        ]

    atualizar_estatisticas()
    atualizar_tabela()
    gerar_grafico()

# FUNCAO DE ATUALIZACAO DAS ESTATITISCAS
def atualizar_estatisticas():
    total = len(df_filtrado)

    if total == 0:
        label_estatisticas.config(
            text="Nenhum registro encontrado para os filtros selecionados."
        )
        return

    renda_valida = obter_renda_valida(df_filtrado)

    if len(renda_valida) > 0:
        renda_media = renda_valida.mean()
        renda_mediana = renda_valida.median()
    else:
        renda_media = 0
        renda_mediana = 0

    idade_media = df_filtrado["idade_calculada"].mean()

    genero_principal = df_filtrado["genero_nome"].mode()
    ocupacao_principal = df_filtrado["ocupacao_nome"].mode()

    if len(genero_principal) > 0:
        genero_principal = genero_principal.iloc[0]
    else:
        genero_principal = "Não identificado"

    if len(ocupacao_principal) > 0:
        ocupacao_principal = ocupacao_principal.iloc[0]
    else:
        ocupacao_principal = "Não identificado"

    texto = (
        f"Registros no recorte: {total}\n"
        f"Renda média individual: R$ {renda_media:.2f}\n"
        f"Renda mediana individual: R$ {renda_mediana:.2f}\n"
        f"Idade média: {idade_media:.1f} anos\n"
        f"Gênero mais frequente: {genero_principal}\n"
        f"Ocupação mais frequente: {ocupacao_principal}"
    )

    label_estatisticas.config(text=texto)

# FUNCAO GERAR GRAFICO ----------
# DIMINIUR TAMANHO??
# REVER
# ATUALIZADO (+3 GRAFICOS)
def gerar_grafico():
    global canvas_grafico

    if canvas_grafico is not None:
        canvas_grafico.get_tk_widget().destroy()

    tipo_grafico = combo_grafico.get()

    figura, eixo = plt.subplots(figsize=(8, 4))

    if tipo_grafico == "Distribuição por sexo":
        if len(df_filtrado) == 0:
            eixo.text(
                0.5,
                0.5,
                "Nenhum dado encontrado para os filtros selecionados.",
                ha="center",
                va="center"
            )
            eixo.set_axis_off()
        else:
            contagem_genero = df_filtrado["genero_nome"].value_counts()

            eixo.bar(contagem_genero.index, contagem_genero.values)
            eixo.set_title("Distribuição da população ocupada por sexo")
            eixo.set_xlabel("Sexo")
            eixo.set_ylabel("Quantidade de pessoas")

    elif tipo_grafico == "Renda média por escolaridade":
        dados_renda = df_filtrado[
            ~df_filtrado["renda_ind"].isin(VALORES_SENTINELA)
        ].dropna(subset=["renda_ind"])

        if len(dados_renda) == 0:
            eixo.text(
                0.5,
                0.5,
                "Nenhum dado de renda válido encontrado para os filtros selecionados.",
                ha="center",
                va="center"
            )
            eixo.set_axis_off()
        else:
            renda_por_escolaridade = (
                dados_renda
                .groupby("escolaridade_nome")["renda_ind"]
                .mean()
                .sort_values()
            )

            eixo.barh(renda_por_escolaridade.index, renda_por_escolaridade.values)
            eixo.set_title("Renda média individual por escolaridade")
            eixo.set_xlabel("Renda média individual em R$")
            eixo.set_ylabel("Escolaridade")

    elif tipo_grafico == "Comparação entre duas RAs":
        ra1 = combo_ra1.get()
        ra2 = combo_ra2.get()

        if ra1 == ra2:
            eixo.text(
                0.5,
                0.5,
                "Selecione duas RAs diferentes para comparar.",
                ha="center",
                va="center"
            )
            eixo.set_axis_off()
        else:
            dados_comparacao = df_moradores.copy()

            if combo_ocupacao.get() != "Todas":
                dados_comparacao = dados_comparacao[
                    dados_comparacao["ocupacao_nome"] == combo_ocupacao.get()
                ]

            if combo_sexo.get() != "Todos":
                dados_comparacao = dados_comparacao[
                    dados_comparacao["genero_nome"] == combo_sexo.get()
                ]

            dados_comparacao = dados_comparacao[
                dados_comparacao["localidade_nome"].isin([ra1, ra2])
            ]

            if len(dados_comparacao) == 0:
                eixo.text(
                    0.5,
                    0.5,
                    "Nenhum dado encontrado para comparar as RAs selecionadas.",
                    ha="center",
                    va="center"
                )
                eixo.set_axis_off()
            else:
                contagem_ras = (
                    dados_comparacao["localidade_nome"]
                    .value_counts()
                    .reindex([ra1, ra2], fill_value=0)
                )

                eixo.bar(contagem_ras.index, contagem_ras.values)
                eixo.set_title(f"Comparação entre {ra1} e {ra2}")
                eixo.set_xlabel("Região Administrativa")
                eixo.set_ylabel("Quantidade de pessoas ocupadas")
                eixo.tick_params(axis="x", rotation=0)

    figura.tight_layout()

    canvas_grafico = FigureCanvasTkAgg(figura, master=frame_grafico)
    canvas_grafico.draw()
    canvas_grafico.get_tk_widget().grid(row=0, column=0, sticky="nsew")


def atualizar_tabela():
    for item in tabela.get_children():
        tabela.delete(item)

    colunas_exibidas = [
        "localidade_nome",
        "genero_nome",
        "idade_calculada",
        "escolaridade_nome",
        "ocupacao_nome",
        "renda_ind"
    ]

    amostra = df_filtrado[colunas_exibidas].head(50)

    for _, linha in amostra.iterrows():
        renda = linha["renda_ind"]

        if pd.isna(renda) or renda in VALORES_SENTINELA:
            renda_texto = "Sem renda válida"
        else:
            renda_texto = f"R$ {renda:.2f}"

        tabela.insert(
            "",
            "end",
            values=(
                linha["localidade_nome"],
                linha["genero_nome"],
                int(linha["idade_calculada"]),
                linha["escolaridade_nome"],
                linha["ocupacao_nome"],
                renda_texto
            )
        )

#FUNCAO PARA EXPORTAR ARQUIVO CVS
def exportar_dados():
    if df_filtrado is None or len(df_filtrado) == 0:
        messagebox.showwarning("Exportação", "Não há dados para exportar.")
        return

    caminho = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Arquivo CSV", "*.csv")],
        title="Salvar dados filtrados"
    )

    if caminho:
        df_filtrado.to_csv(caminho, index=False, encoding="utf-8-sig")
        messagebox.showinfo("Exportação concluída", "Arquivo CSV exportado com sucesso!")

#FUNCAO PARA EXPORTAR TXT
def exportar_estatisticas():
    """Exporta as estatísticas do filtro atual para TXT."""
    if df_filtrado is None or len(df_filtrado) == 0:
        messagebox.showwarning("Exportação", "Não há estatísticas para exportar.")
        return

    caminho = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Arquivo TXT", "*.txt")],
        title="Salvar estatísticas"
    )

    if caminho:
        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write("Sistema PDAD 2024 - Trabalho e Ocupação no DF\n")
            arquivo.write("=" * 55)
            arquivo.write("\n\n")
            arquivo.write(label_estatisticas.cget("text"))
            arquivo.write("\n\n")
            arquivo.write(f"Filtro de localidade: {combo_localidade.get()}\n")
            arquivo.write(f"Filtro de ocupação: {combo_ocupacao.get()}\n")
            arquivo.write(f"Filtro de sexo: {combo_sexo.get()}\n")
            arquivo.write(f"Tipo de gráfico: {combo_grafico.get()}\n")
            arquivo.write(f"RA 1 comparação: {combo_ra1.get()}\n")
            arquivo.write(f"RA 2 comparação: {combo_ra2.get()}\n")

        messagebox.showinfo("Exportação concluída", "Arquivo TXT exportado com sucesso!")

#FUNCAO REBUT DOS FILTROS
def limpar_filtros():
    combo_localidade.set("Todas")
    combo_ocupacao.set("Todas")
    combo_sexo.set("Todos")
    combo_grafico.set("Distribuição por sexo")

    valores_ra = list(combo_ra1["values"])

    if len(valores_ra) > 0:
        combo_ra1.set(valores_ra[0])

    if len(valores_ra) > 1:
        combo_ra2.set(valores_ra[1])
    elif len(valores_ra) > 0:
        combo_ra2.set(valores_ra[0])

    atualizar_filtro()
  
# -----------------
# PROGRAMA PRICIPAL
# -----------------

try:
    df_original = carregar_dados()
    df_moradores = limpar_dados(df_original)
    df_moradores = criar_rotulos(df_moradores)
    df_filtrado = df_moradores.copy()

except Exception as erro:
    janela_erro = tk.Tk()
    janela_erro.withdraw()
    messagebox.showerror(
        "Erro ao carregar dados",
        f"Ocorreu um erro ao carregar o arquivo moradores.csv:\n\n{erro}"
    )
    raise


janela = tk.Tk()
janela.title("PDAD 2024 - Trabalho e Ocupação")
janela.geometry("1050x720")

titulo = tk.Label(
    janela,
    text="Sistema PDAD 2024 - Trabalho e Ocupação no DF",
    font=("Arial", 17, "bold")
)
titulo.pack(pady=10)

descricao = tk.Label(
    janela,
    text=(
        "Este sistema permite explorar dados da população ocupada do Distrito Federal "
        "a partir da PDAD 2024. O usuário pode filtrar por localidade, ocupação e sexo, "
        "visualizar estatísticas de renda e idade, comparar duas RAs no mesmo gráfico "
        "e exportar os resultados. "
        "Feito por Ricardo Carvalho Muniz Alexandre."
    ),
    wraplength=950,
    justify="center"
)
descricao.pack(pady=5)

label_registros = tk.Label(
    janela,
    text=(
        f"{len(df_original)} moradores carregados no arquivo original · "
        f"{len(df_moradores)} moradores ocupados após limpeza dos valores sentinela"
    ),
    font=("Arial", 10, "bold")
)
label_registros.pack(pady=5)

abas = ttk.Notebook(janela)
abas.pack(fill="both", expand=True, padx=10, pady=10)

aba_analise = ttk.Frame(abas)
aba_tabela = ttk.Frame(abas)

abas.add(aba_analise, text="Análise e gráficos")
abas.add(aba_tabela, text="Tabela e exportação")

frame_filtros = tk.LabelFrame(aba_analise, text="Filtros")
frame_filtros.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

tk.Label(frame_filtros, text="Localidade / RA:").grid(
    row=0, column=0, padx=5, pady=5, sticky="w"
)

localidades = sorted(df_moradores["localidade_nome"].dropna().unique().tolist())
localidades.insert(0, "Todas")

combo_localidade = ttk.Combobox(
    frame_filtros,
    values=localidades,
    state="readonly",
    width=35
)
combo_localidade.set("Todas")
combo_localidade.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_filtros, text="Ocupação:").grid(
    row=1, column=0, padx=5, pady=5, sticky="w"
)

ocupacoes = sorted(df_moradores["ocupacao_nome"].dropna().unique().tolist())
ocupacoes.insert(0, "Todas")

combo_ocupacao = ttk.Combobox(
    frame_filtros,
    values=ocupacoes,
    state="readonly",
    width=35
)
combo_ocupacao.set("Todas")
combo_ocupacao.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_filtros, text="Sexo:").grid(
    row=2, column=0, padx=5, pady=5, sticky="w"
)

combo_sexo = ttk.Combobox(
    frame_filtros,
    values=["Todos", "Masculino", "Feminino"],
    state="readonly",
    width=35
)
combo_sexo.set("Todos")
combo_sexo.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_filtros, text="Tipo de gráfico:").grid(
    row=3, column=0, padx=5, pady=5, sticky="w"
)

combo_grafico = ttk.Combobox(
    frame_filtros,
    values=[
        "Distribuição por sexo",
        "Renda média por escolaridade",
        "Comparação entre duas RAs"
    ],
    state="readonly",
    width=35
)
combo_grafico.set("Distribuição por sexo")
combo_grafico.grid(row=3, column=1, padx=5, pady=5)

ras_comparacao = sorted(df_moradores["localidade_nome"].dropna().unique().tolist())

tk.Label(frame_filtros, text="RA 1 comparação:").grid(
    row=4, column=0, padx=5, pady=5, sticky="w"
)

combo_ra1 = ttk.Combobox(
    frame_filtros,
    values=ras_comparacao,
    state="readonly",
    width=35
)

if len(ras_comparacao) > 0:
    combo_ra1.set(ras_comparacao[0])

combo_ra1.grid(row=4, column=1, padx=5, pady=5)

tk.Label(frame_filtros, text="RA 2 comparação:").grid(
    row=5, column=0, padx=5, pady=5, sticky="w"
)

combo_ra2 = ttk.Combobox(
    frame_filtros,
    values=ras_comparacao,
    state="readonly",
    width=35
)

if len(ras_comparacao) > 1:
    combo_ra2.set(ras_comparacao[1])
elif len(ras_comparacao) > 0:
    combo_ra2.set(ras_comparacao[0])

combo_ra2.grid(row=5, column=1, padx=5, pady=5)

botao_filtrar = tk.Button(
    frame_filtros,
    text="Aplicar filtro",
    command=atualizar_filtro,
    width=18
)
botao_filtrar.grid(row=6, column=0, padx=5, pady=10)

botao_limpar = tk.Button(
    frame_filtros,
    text="Limpar filtros",
    command=limpar_filtros,
    width=18
)
botao_limpar.grid(row=6, column=1, padx=5, pady=10)

frame_estatisticas = tk.LabelFrame(aba_analise, text="Estatísticas descritivas")
frame_estatisticas.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

label_estatisticas = tk.Label(
    frame_estatisticas,
    text="",
    justify="left",
    font=("Arial", 11),
    width=55,
    anchor="w"
)
label_estatisticas.grid(row=0, column=0, padx=10, pady=10)

frame_grafico = tk.LabelFrame(aba_analise, text="Gráfico")
frame_grafico.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

aba_analise.grid_rowconfigure(1, weight=1)
aba_analise.grid_columnconfigure(1, weight=1)
frame_grafico.grid_rowconfigure(0, weight=1)
frame_grafico.grid_columnconfigure(0, weight=1)

frame_botoes_exportacao = tk.LabelFrame(aba_tabela, text="Exportação")
frame_botoes_exportacao.pack(fill="x", padx=10, pady=10)

botao_exportar_csv = tk.Button(
    frame_botoes_exportacao,
    text="Exportar dados filtrados em CSV",
    command=exportar_dados,
    width=30
)
botao_exportar_csv.grid(row=0, column=0, padx=10, pady=10)

botao_exportar_txt = tk.Button(
    frame_botoes_exportacao,
    text="Exportar estatísticas em TXT",
    command=exportar_estatisticas,
    width=30
)
botao_exportar_txt.grid(row=0, column=1, padx=10, pady=10)

frame_tabela = tk.LabelFrame(aba_tabela, text="Amostra dos dados filtrados")
frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

colunas_tabela = (
    "Localidade",
    "Gênero",
    "Idade",
    "Escolaridade",
    "Ocupação",
    "Renda"
)

tabela = ttk.Treeview(
    frame_tabela,
    columns=colunas_tabela,
    show="headings",
    height=18
)

for coluna in colunas_tabela:
    tabela.heading(coluna, text=coluna)

tabela.column("Localidade", width=130)
tabela.column("Gênero", width=130)
tabela.column("Idade", width=70)
tabela.column("Escolaridade", width=180)
tabela.column("Ocupação", width=180)
tabela.column("Renda", width=130)

barra_vertical = ttk.Scrollbar(
    frame_tabela,
    orient="vertical",
    command=tabela.yview
)

tabela.configure(yscrollcommand=barra_vertical.set)

tabela.pack(side="left", fill="both", expand=True)
barra_vertical.pack(side="right", fill="y")

atualizar_filtro()

janela.mainloop()
