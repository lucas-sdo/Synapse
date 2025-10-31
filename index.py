import struct

# ---------- Sistema de arquivo ----------


def salvar_simple_script(nome, codigo: str):
    assinatura = b"SP"
    versao = b"\x01"
    dados = codigo.encode("utf-8")
    tamanho = struct.pack("<I", len(dados))

    with open(nome, "wb") as binario:
        binario.write(assinatura)
        binario.write(versao)
        binario.write(tamanho)
        binario.write(dados)
    print(f"Arquivo {nome} criado com sucesso!")


def ler_simple_script(nome):
    with open(nome, "rb") as binario:
        assinatura = binario.read(2)
        if assinatura != b"SP":
            raise ValueError("Arquivo inválido")
        versao = binario.read(1)
        tamanho = struct.unpack("<I", binario.read(4))[0]
        codigo = binario.read(tamanho).decode("utf-8")
        return codigo


# ---------- Interpretador ----------
def interpretar(codigo):
    variaveis = {}
    linhas = [linha.strip()
              for linha in codigo.strip().split("\n") if linha.strip()]

    for linha in linhas:
        # Definição de variável
        if linha.startswith("var"):
            partes = linha.split("/")
            tipo = partes[1]
            nome = partes[2]
            valor = partes[3]

            # Remove aspas de strings
            if tipo == "str":
                print(nome, valor)

            elif tipo == "int":
                valor = int(valor)

            else:
                raise ValueError(f"Tipo '{tipo}' não reconhecido")

            variaveis[nome] = valor

        # Comando de retorno (print)
        elif linha.startswith("return/"):
            expressao = linha.replace("return/", "").strip()

            # Substitui nomes de variáveis pelos valores
            for nome, valor in variaveis.items():
                expressao = expressao.replace(nome, str(valor))
            try:
                resultado = eval(expressao)
            except Exception:
                resultado = expressao
            print(resultado)


# ---------- Exemplo de uso ----------
codigo_fonte = """
var/int/x/100
var/int/y/90

var/str/txt/Eu sou uma string!

return/x + y
return/txt
"""

salvar_simple_script("exemplo.sp", codigo_fonte)
print("Lido de volta:")
conteudo = ler_simple_script("exemplo.sp")
print(conteudo)
print("\nSaída da execução:")
interpretar(conteudo)
