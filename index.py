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

        elif linha.startswith("func/"):
            partes = linha.split("/")

            nome = partes[1]
            parametros = partes[2]
            conteudo = partes[3]

            print(nome, parametros, conteudo)

        elif linha.startswith("call/"):
            nome_func = linha[2]
            if nome_func not in funcoes:
                raise NameError(f"Error: Function {nome_func} doesn't exists")

        else:
            raise SyntaxError(f"Error: Unreconized element {linha.split()[0]}")


def executar_linha(linhas_func):
    variaveis = {}
    funcoes = {}
    linhas = [linha.strip()
              for linha in linhas_func.strip().split("\n") if linha.strip()]

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

        elif linha.startswith("func/"):
            i += 1
            partes = linha.split("/")

            partes = linha.split("/")
            nome_func = partes[1]
            parametros_str = partes[2]
            corpo_func = partes[3]

            parametros = [p.strip() for p in parametros_str.split(",")]
            linhas_corpo = [corpo_func]

            funcoes[nome_func] = {
                'parametros': parametros,
                'corpo': linhas_corpo
            }

        elif linha.startswith("call/"):
            partes = linha.split("/")
            nome_func = partes[1]
            argumentos_str = partes[2]
            argumentos = [a.strip() for a in argumentos_str.split(",")]

            if not parametros:
                raise SyntaxError(
                    f'Error: Method "call/" must include a parameter, even if it is "null"')
            if nome_func not in funcoes:
                raise NameError(f"Error: Function {nome_func} doesn't exists")

        else:
            raise SyntaxError(f"Error: Unreconized element {linha.split()[0]}")


conteudo = ler_Syn("exemplo.syn")
interpretar(conteudo)
