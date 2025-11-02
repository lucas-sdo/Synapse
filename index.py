
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

# ---------- Interpretador ---------- #


def interpretar(codigo):
    variaveis = {}
    funcoes = {}
    linhas = [linha.strip()
              for linha in codigo.strip().split("\n") if linha.strip()]

    def dividir_argumentos(conteudo):
        partes = []
        atual = ""
        nivel = 0
        for char in conteudo:
            if char == "(":
                nivel += 1
            elif char == ")":
                nivel -= 1
            if char == "," and nivel == 0:
                partes.append(atual.strip())
                atual = ""
            else:
                atual += char
        if atual:
            partes.append(atual.strip())
        return partes

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
                raise NameError(f"Error: Type '{tipo}' not reconized")

            variaveis[nome] = (valor, tipo)

        elif linha.startswith("return/"):
            partes_totais = linha.split("/", 2)
            if len(partes_totais) < 3:
                raise SyntaxError(
                    "Return inválido: falta conteúdo após os tipos")

            tipos = [t.strip() for t in partes_totais[1].split(",")]
            conteudo = partes_totais[2].strip()

            elementos = dividir_argumentos(conteudo)

            if len(tipos) != len(elementos):
                raise ValueError(
                    f"Return expects {len(tipos)} parts, found {len(elementos)}"
                )

            resultado_final = ""

            for tipo, elemento in zip(tipos, elementos):
                if elemento.startswith("(") and elemento.endswith(")"):
                    elemento = elemento[1:-1].strip()

                if tipo == "str":
                    if (elemento.startswith('"') and elemento.endswith('"')) or (
                        elemento.startswith("'") and elemento.endswith("'")
                    ):
                        valor = elemento[1:-1]
                    else:
                        valor = elemento
                elif tipo == "svar":
                    # CORREÇÃO: Verifica se a variável está armazenada como tupla ou como valor simples
                    for var_name, var_value in variaveis.items():
                        # Se é uma tupla (valor, tipo), pega apenas o valor
                        if isinstance(var_value, tuple):
                            valor_real = var_value[0]
                        else:
                            valor_real = var_value
                        elemento = elemento.replace(var_name, str(valor_real))

                    if (elemento.startswith('"') and elemento.endswith('"')) or (
                        elemento.startswith("'") and elemento.endswith("'")
                    ):
                        valor = elemento[1:-1]
                    else:
                        valor = elemento
                elif tipo == "int":
                    for var_name, var_value in variaveis.items():
                        if isinstance(var_value, tuple):
                            valor_real = var_value[0]
                        else:
                            valor_real = var_value
                        elemento = elemento.replace(var_name, str(valor_real))
                    valor = int(eval(elemento))
                elif tipo == "float":
                    for var_name, var_value in variaveis.items():
                        if isinstance(var_value, tuple):
                            valor_real = var_value[0]
                        else:
                            valor_real = var_value
                        elemento = elemento.replace(var_name, str(valor_real))
                    valor = float(eval(elemento))
                elif tipo == "bool":
                    for var_name, var_value in variaveis.items():
                        if isinstance(var_value, tuple):
                            valor_real = var_value[0]
                        else:
                            valor_real = var_value
                        elemento = elemento.replace(var_name, str(valor_real))
                    valor = bool(eval(elemento))
                else:
                    raise NameError(f"Unknown return type '{tipo}'")

                resultado_final += str(valor)

            print(resultado_final)

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
                    if param_real in variaveis:
                        valor_real = str(variaveis[param_real])
                        codigo_modificado = codigo_modificado.replace(
                            param_formal, valor_real)
                    else:
                        codigo_modificado = codigo_modificado.replace(
                            param_formal, param_real)

                interpretar(codigo_modificado)

            else:
                raise KeyError(
                    f'Function "{nome_func}" not found/does not exists')

        elif linha.startswith("input/"):
            partes = linha.split("/")
            tipo = partes[1]
            nome = partes[2]
            txt = partes[3]
            if tipo == 'int':
                novo_input = int(input(txt))
            elif tipo == 'float':
                novo_input = float(input(txt))
            elif tipo == 'str':
                novo_input = input(txt)
            else:
                raise SyntaxError(f"Error: Unreconized type {tipo}")
            # CORREÇÃO: Armazena como tupla (valor, tipo) para consistência
            variaveis[nome] = (novo_input, tipo)

        else:
            raise SyntaxError(f"Error: Unreconized element {linha.split()[0]}")

        i = 0
        i += 1


interpretar(conteudo)
