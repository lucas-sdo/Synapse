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

    def verificar_tipos_operacao(expressao, variaveis):
        palavras = expressao.split()
        operandos = []

        for palavra in palavras:
            if palavra in ['+', '-', '*', '/', '%']:
                continue
            elif palavra in variaveis:
                operandos.append((palavra, type(variaveis[palavra])))
            else:
                try:
                    int(palavra)
                    operandos.append((palavra, int))
                except ValueError:
                    try:
                        float(palavra)
                        operandos.append((palavra, float))
                    except ValueError:
                        operandos.append((palavra, str))

        if len(operandos) > 1:
            primeiro_tipo = operandos[0][1]
            for operando, tipo in operandos[1:]:
                if tipo != primeiro_tipo:
                    return False, f"Error: operating diferent types of data {operandos[0][0]}({primeiro_tipo.__name__}) e {operando}({tipo.__name__})"
                continue
            return True, None

    for linha in linhas:
        # Definição de variável
        if linha.startswith("var"):
            partes = linha.split("/")
            tipo = partes[1]
            nome = partes[2]
            valor = partes[3]

            if tipo == "bool":
                if valor not in ["True", "False"]:
                    raise ValueError(
                        f'Error: Variables type boolean must be "True" or "False"')
                else:
                    valor = True if valor == "True" else False

            elif tipo == "str":
                valor = valor

            elif tipo == "int":
                valor = int(valor)

            elif tipo == "float":
                valor = float(valor)

            else:
                raise ValueError(f"Error: Type '{tipo}' not reconized")

            variaveis[nome] = valor

        # Definição de retornos
        elif linha.startswith("return/"):
            expressao = linha.replace("return/", "").strip()

            if expressao in variaveis:
                print(variaveis[expressao])

            else:
                # Verificar tipos antes de executar
                valido, erro = verificar_tipos_operacao(expressao, variaveis)
                if not valido:
                    raise ValueError(erro)

                palavras = expressao.split()
                for i, palavra in enumerate(palavras):
                    if palavra in variaveis:
                        palavras[i] = str(variaveis[palavra])
                expressao_final = ' '.join(palavras)

                try:
                    resultado = eval(expressao_final)
                    print(resultado)
                except Exception as e:
                    print(expressao_final)


conteudo = ler_Syn("exemplo.syn")
interpretar(conteudo)
