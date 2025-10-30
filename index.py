import struct


def salvar_mlang(nome, codigo: str):
    assinatura = b"MLNG"
    versao = b"\x01"
    dados = codigo.encode("utf-8")
    tamanho = struct.pack("<I", len(dados))  # 4 bytes (little endian)

    with open(nome, "wb") as f:
        f.write(assinatura)
        f.write(versao)
        f.write(tamanho)
        f.write(dados)
    print(f"Arquivo {nome} criado com sucesso!")


def ler_mlang(nome):
    with open(nome, "rb") as f:
        assinatura = f.read(4)
        if assinatura != b"MLNG":
            raise ValueError("Arquivo inválido")
        versao = f.read(1)
        tamanho = struct.unpack("<I", f.read(4))[0]
        codigo = f.read(tamanho).decode("utf-8")
        return codigo


# Exemplo
codigo_fonte = """
let x = 10
print x + 5
"""

salvar_mlang("exemplo.mlang", codigo_fonte)
print("Lido de volta:")
print(ler_mlang("exemplo.mlang"))
