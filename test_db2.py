import psycopg
def test(pwd):
    try:
        conn = psycopg.connect(f"postgresql://postgres:{pwd}@junction.proxy.rlwy.net:36866/railway")
        print("Success:", pwd)
        return True
    except Exception as e:
        pass
    return False

test("mLFmAfxqD1bjuVMnciowAxrdYVSxQQdF")
test("mLFmAfxgD1bjuVMnciowAxrdYVSxQQdF")
test("mLFmAfxqD1bJuVMnciowAxrdYVSxQQdF")
test("mLFmAfxgD1bJuVMnciowAxrdYVSxQQdF")
test("mLFmAfxqDlbjuVMnciowAxrdYVSxQQdF")
