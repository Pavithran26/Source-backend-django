import psycopg
try:
    conn = psycopg.connect("postgresql://postgres:mLFmAfxqDlBjuVMnciowAxrdYVSxQQdF@junction.proxy.rlwy.net:36866/railway")
    print("Success with qDlBju")
except Exception as e:
    print("Failed qDlBju:", e)

try:
    conn = psycopg.connect("postgresql://postgres:mLFmAfxgDlbjuVMnciowAxrdYVSxQQdF@junction.proxy.rlwy.net:36866/railway")
    print("Success with gDlbju")
except Exception as e:
    print("Failed gDlbju:", e)

try:
    conn = psycopg.connect("postgresql://postgres:mLFmAfxqDlbjuVMnciowAxrdYVSxQQdF@junction.proxy.rlwy.net:36866/railway")
    print("Success with qDlbju")
except Exception as e:
    print("Failed qDlbju:", e)
