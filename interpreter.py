import math
import datetime
import json
# ---------- Sistema de arquivo ----------
# Synapse


def salvar_Syn(nome, codigo: str):
    assinatura = b"/syn/"
    dados = codigo.encode("utf-8")
    # tamanho = struct.pack("<I", len(dados))

    with open(nome, "wb") as binario:
        binario.write(assinatura)
        # binario.write(tamanho)
        binario.write(dados)
    print(f"Arquivo {nome} criado com sucesso!")


def ler_Syn(nome):
    with open(nome, "rb") as binario:
        assinatura = binario.read(5)
        if assinatura != b"/syn/":
            raise TypeError(get_error("file_errors", "invalid_file"))

        codigo = binario.read().decode("utf-8")
        return codigo


with open(r'extras\errors.json', 'r', encoding='utf-8') as f:
    errors_data = json.load(f)


def get_error(category, error_name, **kwargs):
    try:
        if category in errors_data and error_name in errors_data[category]:
            error_info = errors_data[category][error_name]
            message = error_info["message"]

            if "{" in message and "}" in message:
                try:
                    message = message.format(**kwargs)
                except KeyError as e:
                    message = error_info["message"]

            return f"{error_info['code']}: {message}"
        return f"SYN000: Error '{error_name}' not found in category '{category}'"
    except Exception as e:
        return f"SYN000: Error formatting message: {str(e)}"


conteudo = ler_Syn("exemplo.syn")

# ---------- Interpretador ---------- #
variaveis = {}
funcoes = {}
sets = {}


def encontrar_chave_fechamento(texto, inicio_busca):
    nivel_aninhamento = 0
    for posicao in range(inicio_busca, len(texto)):
        if texto[posicao] == "{":
            nivel_aninhamento += 1
        elif texto[posicao] == "}":
            nivel_aninhamento -= 1
            if nivel_aninhamento == 0:
                return posicao
    return -1


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


def processar_valor_set(valor_str, tipo):
    valor_str = valor_str.strip()

    if tipo == "str":
        if (valor_str.startswith('"') and valor_str.endswith('"')) or \
                (valor_str.startswith("'") and valor_str.endswith("'")):
            return valor_str[1:-1]
        return valor_str

    elif tipo == "svar":
        # Para svar, substituir variáveis no valor
        valor_processado = valor_str
        for var_name, var_value in variaveis.items():
            if isinstance(var_value, tuple):
                valor_real = var_value[0]
            else:
                valor_real = var_value
            # Substituir o nome da variável pelo seu valor
            valor_processado = valor_processado.replace(
                var_name, str(valor_real))

        # Remover aspas se existirem
        if (valor_processado.startswith('"') and valor_processado.endswith('"')) or \
           (valor_processado.startswith("'") and valor_processado.endswith("'")):
            return valor_processado[1:-1]
        return valor_processado

    elif tipo == "int":
        # Para int, primeiro substituir variáveis e depois converter
        for var_name, var_value in variaveis.items():
            if isinstance(var_value, tuple):
                valor_real = var_value[0]
            else:
                valor_real = var_value
            valor_str = valor_str.replace(var_name, str(valor_real))
        return int(valor_str)

    elif tipo == "float":
        # Para float, primeiro substituir variáveis e depois converter
        for var_name, var_value in variaveis.items():
            if isinstance(var_value, tuple):
                valor_real = var_value[0]
            else:
                valor_real = var_value
            valor_str = valor_str.replace(var_name, str(valor_real))
        return float(valor_str)

    elif tipo == "bool":
        if valor_str == "True":
            return True
        elif valor_str == "False":
            return False
        else:
            raise TypeError(get_error("variable_errors", "boolean_value"))
    else:
        raise TypeError(get_error("syntax_errors", "invalid_type", tipo=tipo))


def processar_valor_set(valor_str, tipo):
    valor_str = valor_str.strip()

    if tipo == "str":
        if (valor_str.startswith('"') and valor_str.endswith('"')) or \
                (valor_str.startswith("'") and valor_str.endswith("'")):
            return valor_str[1:-1]
        return valor_str

    elif tipo == "svar":
        # Para svar, substituir variáveis no valor
        valor_processado = valor_str
        for var_name, var_value in variaveis.items():
            if isinstance(var_value, tuple):
                valor_real = var_value[0]
            else:
                valor_real = var_value
            # Substituir o nome da variável pelo seu valor
            valor_processado = valor_processado.replace(
                var_name, str(valor_real))

        # Remover aspas se existirem
        if (valor_processado.startswith('"') and valor_processado.endswith('"')) or \
           (valor_processado.startswith("'") and valor_processado.endswith("'")):
            return valor_processado[1:-1]
        return valor_processado

    elif tipo == "int":
        # Para int, primeiro substituir variáveis e depois converter
        for var_name, var_value in variaveis.items():
            if isinstance(var_value, tuple):
                valor_real = var_value[0]
            else:
                valor_real = var_value
            valor_str = valor_str.replace(var_name, str(valor_real))
        return int(valor_str)

    elif tipo == "float":
        # Para float, primeiro substituir variáveis e depois converter
        for var_name, var_value in variaveis.items():
            if isinstance(var_value, tuple):
                valor_real = var_value[0]
            else:
                valor_real = var_value
            valor_str = valor_str.replace(var_name, str(valor_real))
        return float(valor_str)

    elif tipo == "bool":
        if valor_str == "True":
            return True
        elif valor_str == "False":
            return False
        else:
            raise TypeError(get_error("variable_errors", "boolean_value"))
    else:
        raise TypeError(get_error("syntax_errors", "invalid_type", tipo=tipo))


def obter_set(nome):
    if nome not in sets:
        raise NameError(get_error("system_errors",
                        "set_not_found", set_name=nome))
    return sets[nome]


def interpretar(codigo):
    linhas = [linha.rstrip() for linha in codigo.splitlines()]

    i = 0
    while i < len(linhas):
        linha = linhas[i].strip()
        if not linha:
            i += 1
            continue

        elif linha.startswith("var/"):
            partes = linha.split("/")
            tipo = partes[1]
            nome = partes[2]
            valor = partes[3]

            if nome in ["i", "j", "index"] and "counter" in valor:
                raise SyntaxWarning(
                    get_error("variable_errors", "loop_variable_reassignment", variable=nome))
            if nome in variaveis:
                tipo_existente = variaveis[nome][1]
                if tipo_existente in ["int", "float"] and any(op in valor for op in ["+", "-", "*", "/", "**"]):
                    expressao_avaliar = valor
                    for var_name, var_value in variaveis.items():
                        if isinstance(var_value, tuple):
                            valor_real = var_value[0]
                        else:
                            valor_real = var_value
                        expressao_avaliar = expressao_avaliar.replace(
                            var_name, str(valor_real))

                    try:
                        valor = eval(expressao_avaliar)
                    except:
                        raise ValueError(
                            get_error("syntax_errors", "invalid_expression", expression=valor))
                else:
                    if tipo_existente == "bool":
                        if valor not in ["True", "False"]:
                            raise TypeError(
                                get_error("variable_errors", "boolean_value"))
                        else:
                            valor = True if valor == "True" else False
                    elif tipo_existente == "str":
                        valor = valor
                    elif tipo_existente == "int":
                        valor = int(valor)
                    elif tipo_existente == "float":
                        valor = float(valor)

                variaveis[nome] = (valor, tipo_existente)

            else:
                if tipo == "bool":
                    if valor not in ["True", "False"]:
                        raise TypeError(
                            get_error("variable_errors", "boolean_value"))
                    else:
                        valor = True if valor == "True" else False
                elif tipo == "str":
                    valor = valor
                elif tipo == "int":
                    valor = int(valor)
                elif tipo == "float":
                    valor = float(valor)
                else:
                    raise TypeError(get_error("syntax_errors",
                                    "invalid_type", tipo=tipo))

                variaveis[nome] = (valor, tipo)

            i += 1

        elif linha.startswith("set/"):
            partes = linha.split("/")
            if len(partes) < 4:
                raise SyntaxError(get_error("function_errors", "parameter_mismatch",
                                            function="set", expected="at least 3", provided=len(partes)-1))

            nome = partes[1]
            tipos = partes[2]
            valores = partes[3]

            if not (valores.startswith("{") and valores.endswith("}")):
                raise SyntaxError(
                    get_error("syntax_errors", "missing_block"))

            valores = valores[1:-1].strip()

            tipos_lista = [t.strip() for t in tipos.split(",")]
            valores_lista = dividir_argumentos(valores)

            if len(tipos_lista) != len(valores_lista):
                raise SyntaxError(get_error("return_errors", "type_count_mismatch",
                                            expected=len(tipos_lista), types=tipos_lista,
                                            found=len(valores_lista), values=valores_lista))

            valores_processados = []
            for tipo, valor_str in zip(tipos_lista, valores_lista):
                try:
                    valor_processado = processar_valor_set(valor_str, tipo)
                    valores_processados.append(valor_processado)
                except Exception as e:
                    raise ValueError(
                        get_error("math_errors", "invalid_math_value", value=valor_str))

            sets[nome] = {
                "tipos": tipos_lista,
                "valores": valores_processados
            }

            print(f"Set '{nome}' criado com sucesso: {valores_processados}")
            i += 1

        elif linha.startswith("add/"):
            partes = linha.split("/")
            if len(partes) < 4:
                raise SyntaxError(get_error("function_errors", "parameter_mismatch",
                                            function="add", expected="at least 3", provided=len(partes)-1))

            nome_set = partes[1]
            tipo = partes[2]
            valor_str = partes[3]

            # Processar o valor baseado no tipo
            try:
                valor_processado = processar_valor_set(valor_str, tipo)
            except Exception as e:
                raise ValueError(
                    get_error("math_errors", "invalid_math_value", value=valor_str))

            # Adicionar ao set
            if nome_set in sets:
                sets[nome]["tipos"].append(tipo)
                sets[nome]["valores"].append(valor_processado)
                print(
                    f"Elemento '{valor_processado}' adicionado ao set '{nome_set}'")
            else:
                # Se o set não existe, criar um novo
                sets[nome_set] = {
                    "tipos": [tipo],
                    "valores": [valor_processado]
                }
                print(
                    f"Set '{nome_set}' criado com elemento: {valor_processado}")

            i += 1

        elif linha.startswith("remove/"):
            partes = linha.split("/")
            if len(partes) < 3:
                raise SyntaxError(get_error("function_errors", "parameter_mismatch",
                                            function="remove", expected="at least 2", provided=len(partes)-1))

            nome_set = partes[1]
            indice_str = partes[2]

            try:
                if indice_str in variaveis:
                    indice = variaveis[indice_str][0]
                else:
                    indice = int(indice_str)
            except ValueError:
                raise ValueError(
                    get_error("math_errors", "invalid_math_value", value=indice_str))

            set_data = obter_set(nome_set)

            if indice < 0 or indice >= len(set_data["valores"]):
                raise IndexError(get_error("system_errors", "index_out_of_range",
                                           index=indice, max_index=len(set_data["valores"])-1))

            valor_removido = set_data["valores"].pop(indice)
            tipo_removido = set_data["tipos"].pop(indice)

            print(
                f"Elemento '{valor_removido}' removido do set '{nome_set}' na posição {indice}")
            i += 1

        elif linha.startswith("get/"):
            partes = linha.split("/")
            if len(partes) < 4:
                raise SyntaxError(get_error("function_errors", "parameter_mismatch",
                                            function="get", expected="at least 3", provided=len(partes)-1))

            nome_set = partes[1]
            indice_str = partes[2]
            nome_variavel = partes[3]

            try:
                if indice_str in variaveis:
                    indice = variaveis[indice_str][0]
                else:
                    indice = int(indice_str)
            except ValueError:
                raise ValueError(
                    get_error("math_errors", "invalid_math_value", value=indice_str))

            set_data = obter_set(nome_set)

            if indice < 0 or indice >= len(set_data["valores"]):
                raise IndexError(get_error("system_errors", "index_out_of_range",
                                           index=indice, max_index=len(set_data["valores"])-1))

            valor = set_data["valores"][indice]
            tipo = set_data["tipos"][indice]

            variaveis[nome_variavel] = (valor, tipo)
            print(
                f"Valor '{valor}' do set '{nome_set}'[{indice}] armazenado em '{nome_variavel}'")
            i += 1

        elif linha.startswith("size/"):
            partes = linha.split("/")
            if len(partes) < 3:
                raise SyntaxError(get_error("function_errors", "parameter_mismatch",
                                            function="size", expected="at least 2", provided=len(partes)-1))

            nome_set = partes[1]
            nome_variavel = partes[2]

            set_data = obter_set(nome_set)
            tamanho = len(set_data["valores"])

            variaveis[nome_variavel] = (tamanho, "int")
            print(
                f"Tamanho do set '{nome_set}': {tamanho} (armazenado em '{nome_variavel}')")
            i += 1

        elif linha.startswith("if/"):
            rest_text = "\n".join(linhas[i:])

            idx_open = rest_text.find("{")
            if idx_open == -1:
                raise SyntaxError(
                    get_error("syntax_errors", "missing_block_start"))

            cond_text = rest_text[3:idx_open].strip()

            cond_text = cond_text.rstrip('/').strip()

            end1 = encontrar_chave_fechamento(rest_text, idx_open)
            if end1 == -1:
                raise SyntaxError(
                    get_error("syntax_errors", "block_not_closed"))

            block1 = rest_text[idx_open + 1:end1].strip()

            idx_open2 = rest_text.find("{", end1 + 1)
            block2 = None
            end2 = None
            if idx_open2 != -1:
                end2 = encontrar_chave_fechamento(rest_text, idx_open2)
                if end2 == -1:
                    raise SyntaxError(
                        get_error("syntax_errors", "block_not_closed"))
                block2 = rest_text[idx_open2 + 1:end2].strip()

            consumed_pos = end2 if end2 is not None else end1
            lines_consumed = rest_text[:consumed_pos + 1].count("\n") + 1
            i += lines_consumed

            cond_eval = cond_text

            try:
                if cond_eval.startswith("if/"):
                    cond_eval = cond_eval[3:].strip()

                for var_name, var_value in variaveis.items():
                    if isinstance(var_value, tuple):
                        valor_real = var_value[0]
                    else:
                        valor_real = var_value
                    cond_eval = cond_eval.replace(var_name, str(valor_real))

                cond_result = eval(cond_eval)
            except Exception as e:
                raise ValueError(get_error(
                    "loop_errors", "invalid_condition", condition=cond_text, details=str(e)))

            if cond_result:
                if block1:
                    interpretar(block1)
            else:
                if block2:
                    interpretar(block2)
            continue

        elif linha.startswith("return/"):
            partes_totais = linha.split("/", 2)
            if len(partes_totais) < 3:
                raise SyntaxError(
                    get_error("return_errors", "missing_content"))

            tipos = [t.strip() for t in partes_totais[1].split(",")]
            conteudo = partes_totais[2].strip()

            elementos = dividir_argumentos(conteudo)

            if len(tipos) != len(elementos):
                raise SyntaxError(get_error("return_errors", "type_count_mismatch",
                                  expected=len(tipos), types=tipos, found=len(elementos), values=elementos))

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
                    for var_name, var_value in variaveis.items():
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
                    valor = int(eval(elemento.strip('/')))

                elif tipo == "float":
                    for var_name, var_value in variaveis.items():
                        if isinstance(var_value, tuple):
                            valor_real = var_value[0]
                        else:
                            valor_real = var_value
                        elemento = elemento.replace(var_name, str(valor_real))
                    valor = float(eval(elemento.strip('/')))

                elif tipo == "set":
                    nome_set = partes_totais[2]
                    set_data = obter_set(nome_set)

                    for j, (tipo, valor) in enumerate(zip(set_data["tipos"], set_data["valores"])):
                        print(f"[{j}] {tipo}: {valor}")
                    continue

                elif tipo == "bool":
                    for var_name, var_value in variaveis.items():
                        if isinstance(var_value, tuple):
                            valor_real = var_value[0]
                        else:
                            valor_real = var_value
                        elemento = elemento.replace(var_name, str(valor_real))
                    valor = bool(eval(elemento))
                else:
                    raise TypeError(get_error("syntax_errors",
                                    "invalid_type", tipo=tipo))

                resultado_final += str(valor)
                if tipo != "set":
                    print(resultado_final)
            i += 1

        elif linha.startswith("//"):
            i += 1
            continue

        elif linha.startswith("func/"):
            header_part = linhas[i]

            if "{" in header_part:
                idx = header_part.find("{")
                header = header_part[:idx].strip()
                rest = header_part[idx+1:]
                block_lines = [rest]
                brace_count = 1

            else:
                header = header_part.strip()
                block_lines = []
                brace_count = 0

            j = i + 1

            while j < len(linhas) and brace_count > 0:
                linej = linhas[j]
                brace_count += linej.count("{")
                brace_count -= linej.count("}")
                block_lines.append(linej)
                j += 1

            if brace_count > 0:
                while j < len(linhas) and brace_count > 0:
                    linej = linhas[j]
                    brace_count += linej.count("{")
                    brace_count -= linej.count("}")
                    block_lines.append(linej)
                    j += 1

            if brace_count != 0:
                raise SyntaxError(
                    get_error("syntax_errors", "block_not_closed"))

            codigo_func_raw = "\n".join(block_lines)

            if "}" in codigo_func_raw:
                codigo_func = codigo_func_raw.rsplit("}", 1)[0].strip()
            else:
                codigo_func = codigo_func_raw.strip()

            partes = header.split("/")
            if len(partes) < 2:
                raise SyntaxError(
                    get_error("function_errors", "invalid_definition"))

            nome_func = partes[1]
            parametros = partes[2].split(",") if len(
                partes) > 2 and partes[2] else []

            funcoes[nome_func] = (parametros, codigo_func)
            i = j
            continue

        elif linha.startswith("call/"):
            partes = linha.split("/")
            nome_func = partes[1]
            parametros_reais = partes[2].split(",") if len(partes) > 2 else []

            if nome_func in funcoes:
                parametros_formais, codigo_func = funcoes[nome_func]

                if len(parametros_reais) != len(parametros_formais):
                    raise SyntaxError(get_error("function_errors", "parameter_mismatch",
                                                function=nome_func, expected=len(parametros_formais), provided=len(parametros_reais)))

                codigo_modificado = codigo_func

                for param_formal, param_real in zip(parametros_formais, parametros_reais):
                    if param_real in variaveis:
                        entry = variaveis[param_real]
                        if isinstance(entry, tuple) and len(entry) == 2:
                            valor_real, tipo_entry = entry
                        else:
                            valor_real = entry
                            tipo_entry = None

                        if tipo_entry == "str":
                            replacement = f'"{valor_real}"'
                        else:
                            replacement = str(valor_real)
                        codigo_modificado = codigo_modificado.replace(
                            param_formal, replacement)
                    else:
                        codigo_modificado = codigo_modificado.replace(
                            param_formal, param_real)

                interpretar(codigo_modificado)

            else:
                raise NameError(get_error("function_errors",
                                "function_not_found", function=nome_func))
            i += 1

        elif linha.startswith("input/"):
            partes = linha.split("/")
            tipo = partes[1]
            nome = partes[2]
            txt = partes[3]
            if tipo == 'int':
                try:
                    novo_input = int(input(txt))
                except ValueError:
                    raise ValueError(
                        get_error("input_errors", "conversion_failed", target_type="integer"))
            elif tipo == 'float':
                try:
                    novo_input = float(input(txt))
                except ValueError:
                    raise ValueError(
                        get_error("input_errors", "conversion_failed", target_type="float"))
            elif tipo == 'str':
                novo_input = input(txt)
            else:
                raise TypeError(get_error("syntax_errors",
                                "invalid_type", tipo=tipo))
            variaveis[nome] = (novo_input, tipo)
            i += 1

        elif linha.startswith("loop/"):
            max_iteracoes = 1024
            iteracao_atual = 0
            partes = linha.split("/", 2)
            condicao_texto = partes[1]

            restante_codigo = "\n".join(linhas[i:])

            posicao_abre_chaves = restante_codigo.find("{")
            if posicao_abre_chaves == -1:
                raise SyntaxError(
                    get_error("syntax_errors", "missing_block_start"))

            posicao_fecha_chaves = encontrar_chave_fechamento(
                restante_codigo, posicao_abre_chaves)

            if posicao_fecha_chaves == -1:
                raise SyntaxError(
                    get_error("syntax_errors", "block_not_closed"))

            conteudo_bloco = restante_codigo[posicao_abre_chaves +
                                             1:posicao_fecha_chaves].strip()

            codigo_consumido = restante_codigo[:posicao_fecha_chaves+1]
            linhas_consumidas = codigo_consumido.count("\n")
            i += linhas_consumidas + 1

            while iteracao_atual < max_iteracoes:
                iteracao_atual += 1

                condicao_atual = condicao_texto
                for nome_variavel, valor_variavel in variaveis.items():
                    if isinstance(valor_variavel, tuple):
                        valor_real = valor_variavel[0]
                    else:
                        valor_real = valor_variavel
                    condicao_atual = condicao_atual.replace(
                        nome_variavel, str(valor_real))

                try:
                    resultado_condicao = eval(condicao_atual)
                except Exception as erro:
                    raise ValueError(get_error(
                        "loop_errors", "invalid_condition", condition=condicao_texto, details=str(erro)))

                if not resultado_condicao:
                    break

                interpretar(conteudo_bloco)
            else:
                raise OverflowError(get_error(
                    "loop_errors", "max_iterations_exceeded", max_iterations=max_iteracoes))

        elif linha.startswith("const/"):
            partes = linha.split("/")
            valor = partes[1]

            if valor == "pi":
                variaveis["pi"] = (math.pi, "float")
            elif valor == "e":
                variaveis["e"] = (math.e, "float")
            elif valor == "tau":
                variaveis["tau"] = (math.tau, "float")
            else:
                raise NameError(get_error("system_errors",
                                "constant_not_found", constant=valor))
            i += 1

        elif linha.startswith("date/"):
            partes = linha.split("/")
            especificacao = partes[1]
            data = datetime.datetime.now()

            if not especificacao:
                print(data.strftime("%c"))
            elif especificacao == "week_day":
                print(data.strftime("%w"))
            elif especificacao == "week_s":
                print(data.strftime("%a"))
            elif especificacao == "week_b":
                print(data.strftime("%A"))

            elif especificacao == "month_day":
                print(data.strftime("%d"))
            elif especificacao == "month_s":
                print(data.strftime("%b"))
            elif especificacao == "month_b":
                print(data.strftime("%B"))

            elif especificacao == "year_day":
                print(data.strftime("%j"))
            elif especificacao == "year_s":
                print(data.strftime("%y"))
            elif especificacao == "year_b":
                print(data.strftime("%Y"))

            elif especificacao == "date":
                print(data.strftime("%x"))
            elif especificacao == "time":
                print(data.strftime("%X"))
            elif especificacao == "am_pm":
                print(data.strftime("%p"))
            else:
                print(data.strftime("%c"))
            i += 1

        elif linha.startswith("math/"):
            partes = linha.split("/")
            if len(partes) < 4:
                raise SyntaxError(get_error("function_errors", "parameter_mismatch",
                                            function="math", expected="at least 3", provided=len(partes)-1))

            operacao = partes[1]
            nome = partes[2]
            valores_str = partes[3]
            valores = [v.strip() for v in valores_str.split(",")]

            valores_processados = []
            for valor in valores:
                for var_name, var_value in variaveis.items():
                    if isinstance(var_value, tuple):
                        valor_real = var_value[0]
                    else:
                        valor_real = var_value
                    valor = valor.replace(var_name, str(valor_real))

                try:
                    valor_num = eval(valor)
                    valores_processados.append(valor_num)
                except:
                    raise ValueError(
                        get_error("math_errors", "invalid_math_value", value=valor))

            # Operações que precisam de 1 valor
            if operacao in ["sqrt", "cbrt", "fac", "round", "floor", "ceil"]:
                if len(valores_processados) != 1:
                    raise SyntaxError(get_error("math_errors", "parameter_count",
                                                operation=operacao, required=1, provided=len(valores_processados)))

                if operacao == "sqrt":
                    resultado = math.sqrt(valores_processados[0])
                elif operacao == "cbrt":
                    # math.cbrt não existe no Python padrão
                    resultado = valores_processados[0] ** (1/3)
                elif operacao == "fac":
                    resultado = math.factorial(int(valores_processados[0]))
                elif operacao == "round":
                    resultado = round(valores_processados[0])
                elif operacao == "floor":
                    resultado = math.floor(valores_processados[0])
                elif operacao == "ceil":
                    resultado = math.ceil(valores_processados[0])

            # Operações que precisam de 2 valores
            elif operacao in ["expo", "gcd"]:
                if len(valores_processados) != 2:
                    raise SyntaxError(get_error("math_errors", "parameter_count",
                                                operation=operacao, required=2, provided=len(valores_processados)))

                if operacao == "expo":
                    resultado = valores_processados[0] ** valores_processados[1]
                elif operacao == "gcd":
                    resultado = math.gcd(
                        int(valores_processados[0]), int(valores_processados[1]))

            # Operações que podem ter 1 ou 2 valores
            elif operacao == "log":
                if len(valores_processados) == 1:
                    resultado = math.log(valores_processados[0])
                elif len(valores_processados) == 2:
                    resultado = math.log(
                        valores_processados[0], valores_processados[1])
                else:
                    raise SyntaxError(get_error("math_errors", "parameter_count",
                                                operation=operacao, required="1 or 2", provided=len(valores_processados)))

            else:
                raise SyntaxError(
                    get_error("math_errors", "invalid_operation", operation=operacao))

            variaveis[nome] = (resultado, "float")
            i += 1

        elif linha.startswith("/syn/"):
            i += 1
            continue

        elif linha.startswith("config/"):
            partes = linha.split("/")
            tipo = partes[1]
            if tipo == "documentation":
                with open('documentation_original.txt', 'r') as arquivo:
                    conteudo = arquivo.read()
                    with open('documentation_syn.txt', 'w') as arquivo:
                        return arquivo.write(conteudo)
            elif tipo == "error":
                return print('error')
            elif tipo == "config":
                return print('There is no config for now!')
            else:
                raise SyntaxError(
                    'Error: Method config needs a valid configuration name')

        else:
            element = linha.split()[0] if linha.split() else linha
            raise SyntaxError(
                get_error("system_errors", "unrecognized_element", element=element))


interpretar(conteudo)
