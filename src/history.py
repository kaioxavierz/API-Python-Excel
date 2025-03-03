import pandas as pd
from datetime import datetime
#dados = pd.DataFrame(columns=["id", "marca", "tipo", "quantidade", "custo_producao", "preco"])
#dados.to_excel('./database/estoque.xlsx', index=False, engine='openpyxl')

historyPath = f"./database/migrations/history.txt"

def save_history(method, id, previous=''):
    if not isinstance(previous, str):
     previous_data = previous.to_json(orient="records")

     with open(historyPath, 'a') as history:
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history.write("\nmethod: " + method + " ItemId: " + str(id) + " previous: " + previous_data + " Data: " + str(data))
        history.close()
        return
    
    with open(historyPath, 'a') as history:
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history.write("\nmethod: " + method + " ItemId: " + str(id) + " Data: " + str(data))
        history.close()
        return

def showHistory():
    df = pd.read_csv(historyPath, sep=", ", engine="python")
    json_data = df.to_json(orient="records", indent=4)
    return json_data


