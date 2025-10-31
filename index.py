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


conteudo = ler_Syn("exemplo.syn")
# def ler_Syn(nome):
# with open(nome, "rb") as binario:
#     assinatura = binario.read(3)
#     if assinatura != b"syn":
#         raise ValueError("Arquivo inválido")
#     tamanho = struct.unpack("<I", binario.read(4))[0]
#     codigo = binario.read(tamanho).decode("utf-8")
#     return codigo


# ---------- Interpretador ---------- #
def interpretar(codigo):
    variaveis = {}
    funcoes = {}
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
                if (primeiro_tipo in [int, float] and tipo in [int, float]):
                    continue
                elif tipo != primeiro_tipo:
                    return False, f"Error: operating diferent types of data {operandos[0][0]}({primeiro_tipo.__name__}) and {operando}({tipo.__name__})"
        return True, None

    for linha in linhas:
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

        elif linha.startswith("return/"):
            expressao = linha.split("/", 1)[1].strip()

            if expressao in variaveis:
                print(variaveis[expressao])
            else:
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
                    print(f"Erro ao calcular: {e}")

        elif linha.startswith("/"):
            continue

        elif linha.startswith("func/"):
            inicio_parenteses = linha.find('(')
            fim_parenteses = linha.find(')')

            if inicio_parenteses == -1 or fim_parenteses == -1:
                raise SyntaxError(
                    "Function definition must have code inside parentheses")

            cabecalho = linha[:inicio_parenteses].strip()
            codigo_func = linha[inicio_parenteses + 1:fim_parenteses].strip()

            partes = cabecalho.split("/")
            if len(partes) < 4:
                raise SyntaxError("Invalid function definition format")

            nome_func = partes[1]
            parametros = partes[2].split(",") if partes[2] else []

            funcoes[nome_func] = (parametros, codigo_func)

        elif linha.startswith("call/"):
            partes = linha.split("/")
            nome_func = partes[1]
            parametros_reais = partes[2].split(",") if len(partes) > 2 else []

            if nome_func in funcoes:
                parametros_formais, codigo_func = funcoes[nome_func]

                if len(parametros_reais) != len(parametros_formais):
                    raise ValueError(
                        f"Error: Function '{nome_func}' expects {len(parametros_formais)} parameters, but {len(parametros_reais)} were provided")

                codigo_modificado = codigo_func

                for param_formal, param_real in zip(parametros_formais, parametros_reais):
                    codigo_modificado = codigo_modificado.replace(
                        param_formal, param_real)

                interpretar(codigo_modificado)

            else:
                raise KeyError(
                    f'Function "{nome_func}" not found/does not exists')

        else:
            raise SyntaxError(f"Error: Unreconized element {linha.split()[0]}")
        i = 0
        i += 1


interpretar(conteudo)
