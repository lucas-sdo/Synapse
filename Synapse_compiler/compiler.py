from llvmlite import ir, binding
import traceback


class CompiladorSyn:
    def __init__(self):
        self.module = ir.Module("synapse_module")
        self.module.triple = binding.get_default_triple()
        self.builder = None
        self.variaveis = {}

        printf_ty = ir.FunctionType(
            ir.IntType(32),
            [ir.PointerType(ir.IntType(8))],
            var_arg=True
        )
        self.printf = ir.Function(self.module, printf_ty, name="printf")

        msg = "%d\n\0"
        array_ty = ir.ArrayType(ir.IntType(8), len(msg))
        self.format_str = ir.GlobalVariable(self.module, array_ty, name="fmt")
        self.format_str.global_constant = True
        self.format_str.initializer = ir.Constant(
            array_ty, bytearray(msg, "utf8"))

    def obter_valor(self, token):
        """Obtém valor de uma variável ou constante"""
        token = token.strip()

        if token.isdigit():
            return ir.Constant(ir.IntType(64), int(token))

        if token in self.variaveis:
            return self.builder.load(self.variaveis[token], name=f"{token}_val")

        if any(op in token for op in ['+', '-', '*', '/']):
            return self.processar_expressao(token)
        else:
            raise ValueError(f"Valor desconhecido: {token}")

    def processar_expressao(self, expressao):
        """Processa expressões matemáticas como x+20, y*2, etc."""
        expressao = expressao.strip()

        if expressao.isdigit():
            return ir.Constant(ir.IntType(64), int(expressao))

        if expressao in self.variaveis:
            return self.builder.load(self.variaveis[expressao], name=f"{expressao}_val")

        operadores = ['+', '-', '*', '/']

        for op in operadores:
            if op in expressao:
                partes = expressao.split(op, 1)
                if len(partes) == 2:
                    left = partes[0].strip()
                    right = partes[1].strip()

                    left_val = self.obter_valor(left)
                    right_val = self.obter_valor(right)

                    if op == '+':
                        return self.builder.add(left_val, right_val, name="soma")
                    elif op == '-':
                        return self.builder.sub(left_val, right_val, name="subtracao")
                    elif op == '*':
                        return self.builder.mul(left_val, right_val, name="multiplicacao")
                    elif op == '/':
                        return self.builder.sdiv(left_val, right_val, name="divisao")

        return self.obter_valor(expressao)

    def compilar_para_llvm(self, codigo_syn):
        """Converte código Syn para LLVM IR"""
        linhas = [linha.strip()
                  for linha in codigo_syn.splitlines() if linha.strip()]

        func_type = ir.FunctionType(ir.IntType(32), [])
        main_func = ir.Function(self.module, func_type, name="main")

        entry_block = main_func.append_basic_block("entry")
        self.builder = ir.IRBuilder(entry_block)

        for linha in linhas:
            self.processar_linha(linha)

        self.builder.ret(ir.Constant(ir.IntType(32), 0))

        return self.module

    def processar_linha(self, linha):
        """Processa uma linha do código Syn"""
        partes = linha.split("/")
        comando = partes[0]

        if comando == "var":
            self.compilar_variavel(partes)
        elif comando == "return":
            self.compilar_print(partes)

    def compilar_variavel(self, partes):
        """Compila declaração de variável: var/tipo/nome/valor"""
        if len(partes) < 4:
            raise ValueError(f"Declaração de variável incompleta: {partes}")

        tipo = partes[1]
        nome = partes[2]
        valor = partes[3]

        if tipo == "int":
            ptr = self.builder.alloca(ir.IntType(64), name=nome)
            valor_llvm = self.processar_expressao(valor)
            self.builder.store(valor_llvm, ptr)
            self.variaveis[nome] = ptr
        else:
            raise TypeError('For now the only accepted type is int.')

    def compilar_print(self, partes):
        """Compila comando return (que agora funciona como print): return/tipo/valor"""
        if len(partes) < 3:
            raise ValueError(f"Comando return incompleto: {partes}")

        tipo = partes[1]
        valor = partes[2]

        if tipo == 'int':
            valor_llvm = self.obter_valor(valor)
            fmt_ptr = self.builder.bitcast(
                self.format_str,
                ir.PointerType(ir.IntType(8))
            )

            self.builder.call(self.printf, [fmt_ptr, valor_llvm])
        else:
            raise TypeError("Unreconized type for now")

    def salvar_ir(self, arquivo="program.ll"):
        with open(arquivo, "w") as f:
            f.write(str(self.module))

    def executar_jit(self):
        """Executa o código diretamente usando JIT do llvmlite"""
        try:
            binding.initialize_native_target()
            binding.initialize_native_asmprinter()

            ir_code = str(self.module)
            # print("=== LLVM IR ===")
            # print(ir_code)
            # print("===============")

            mod = binding.parse_assembly(ir_code)
            mod.verify()

            target = binding.Target.from_default_triple()
            target_machine = target.create_target_machine()

            backing_mod = binding.parse_assembly("")
            engine = binding.create_mcjit_compiler(backing_mod, target_machine)

            engine.add_module(mod)
            engine.finalize_object()

            func_ptr = engine.get_function_address("main")

            from ctypes import CFUNCTYPE, c_int32
            functype = CFUNCTYPE(c_int32)
            main_func = functype(func_ptr)

            resultado = main_func()
            return resultado

        except Exception as e:
            print(f"Erro na execução JIT: {e}")
            traceback.print_exc()
            return None


compilador = CompiladorSyn()
codigo_syn = """
    var/int/x/10
    var/int/y/x + 100
    return/int/x
    return/int/y
    return/int/50
    var/int/z/y+200
    return/int/z
"""

try:
    modulo_ir = compilador.compilar_para_llvm(codigo_syn)
    compilador.salvar_ir("program.ll")

    resultado = compilador.executar_jit()
    # print(f"Retorno da função main: {resultado}")

except Exception as e:
    print(f"Erro durante a compilação: {e}")
    traceback.print_exc()
