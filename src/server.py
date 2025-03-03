from flask import Flask,request, jsonify
import pandas as pd
import os
from history import save_history, showHistory
# Caminho do arquivo estoque excel
path = f"./database/estoque.xlsx"
#historyPath = f"./database/migrations/history.txt"

app = Flask(__name__)

def load_data():
      if os.path.exists(path):
            return pd.read_excel(path)
      else: 
            return pd.DataFrame(columns=["id", "marca", "tipo", "quantidade", "custo_producao", "preco"])
# func para transformar o DataFrame to excel
def save_data(df):
      df.to_excel(path, index=False)


@app.route('/estoque', methods=['GET'])
def get_estoque():
    df = load_data()
    return jsonify(df.to_dict())

@app.route('/estoque', methods=['POST'])
def create():
    df = load_data()
    data = request.json
    newId = 1 if df.empty else df["id"].max() + 1
    #Get na requisição
    new_item = pd.DataFrame([{
         "id": newId,
        "marca":data.get("marca"),
        "tipo":data.get("tipo"),
        "quantidade":data.get("quantidade"),
        "custo_producao":data.get("custo_producao"),
        "preco":data.get("custo_producao")
    }])

    df = pd.concat([df, new_item], ignore_index=True)
    save_data(df)
    save_history("Create", newId)
    return jsonify({"message": "item adicionado com sucesso!"})
    

@app.route('/estoque/<int:item_id>', methods=['PUT'])
def update(item_id):
    df = load_data()
    if item_id not in df["id"].values:
        return jsonify({"error": "id não encontrado"}), 404
    
    #Item em formato DataFrame antes de ser atualizado
    previous = df[df["id"] == item_id]
    data = request.json

    df.loc[df["id"] == item_id, "marca"] = data.get("marca", df.loc[df["id"] == item_id, "marca"])
    df.loc[df["id"] == item_id, "tipo"] = data.get("tipo", df.loc[df["id"] == item_id, "tipo"])
    df.loc[df["id"] == item_id, "quantidade"] = data.get("quantidade", df.loc[df["id"] == item_id, "quantidade"])
    df.loc[df["id"] == item_id, "custo_producao"] = data.get("custo_producao", df.loc[df["id"] == item_id, "custo_producao"])
    df.loc[df["id"] == item_id, "preco"] = data.get("preco", df.loc[df["id"] == item_id, "preco"])

    save_data(df)
    save_history("Update", item_id, previous)
    return jsonify({"message": "Item atualizado com sucesso!", "id": item_id})
          

@app.route('/estoque/<int:item_id>', methods=['DELETE'])
def delete(item_id):
     df = load_data()

     if item_id not in df["id"].values:
        return jsonify({"error": "id não encontrado"}), 404
     
     previous = df[df["id"] == item_id]
     df = df[df["id"] != item_id]  # Remove a linha pelo ID
     save_data(df)
     save_history("Delete", item_id, previous)
     return jsonify({"message": "Item removido com sucesso!"})


if __name__ == '__main__':
    app.run(debug=True)


