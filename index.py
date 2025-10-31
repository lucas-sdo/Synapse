import struct

# ---------- Sistema de arquivo ----------
# Synapse


def salvar_Syn(nome, codigo: str):
    assinatura = b"syn"
    dados = codigo.encode("utf-8")
    # tamanho = struct.pack("<I", len(dados))

    with open(nome, "wb") as binario:
        binario.write(assinatura)
        # binario.write(tamanho)
        binario.write(dados)
    print(f"Arquivo {nome} criado com sucesso!")


def ler_Syn(nome):
    with open(nome, "rb") as binario:
        assinatura = binario.read(3)
        if assinatura != b"syn":
            raise ValueError("Arquivo inválido")

        codigo = binario.read().decode("utf-8")
        return codigo

# def ler_Syn(nome):
# with open(nome, "rb") as binario:
#     assinatura = binario.read(3)
#     if assinatura != b"syn":
#         raise ValueError("Arquivo inválido")
#     tamanho = struct.unpack("<I", binario.read(4))[0]
#     codigo = binario.read(tamanho).decode("utf-8")
#     return codigo


# ---------- Interpretador ----------
def interpretar(codigo):
    variaveis = {}
    linhas = [linha.strip()
              for linha in codigo.strip().split("\n") if linha.strip()]

    for linha in linhas:
        # Definição de variável (atualmente pode ser integer ou string)
        if linha.startswith("var"):
            partes = linha.split("/")
            tipo = partes[1]
            nome = partes[2]
            valor = partes[3]

            if tipo == "str":
                valor = valor

            elif tipo == "int":
                valor = int(valor)

            else:
                raise ValueError(f"Tipo '{tipo}' não reconhecido")

            variaveis[nome] = valor

        # Definição de retornos (funciona semelhantemente ao print())
        elif linha.startswith("return/"):
            expressao = linha.replace("return/", "").strip()

            if expressao in variaveis:
                print(variaveis[expressao])

            else:
                palavras = expressao.split()
                for i, palavra in enumerate(palavras):
                    if palavra in variaveis:
                        palavras[i] = str(variaveis[palavra])
                expressao_final = ' '.join(palavras)

                try:
                    resultado = eval(expressao_final)
                    print(resultado)

                except Exception:
                    print(expressao_final)


# ---------- Caso seja preciso escrever o código syn aqui: ----------
# codigo_fonte = """
# var/int/x/100
# var/int/y/90

# var/str/txt/Eu sou uma string!

# return/x + y
# return/txt
# """

# salvar_Syn("exemplo.syn", codigo_fonte)
# print("Lido de volta:")
conteudo = ler_Syn("exemplo.syn")
# print(conteudo)
interpretar(conteudo)
