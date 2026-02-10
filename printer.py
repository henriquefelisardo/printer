from flask import Flask, request, jsonify
import win32api
import win32print
import os
import tempfile

app = Flask(__name__)

@app.route('/', methods=['POST'])
def print_file():
    data = request.json
    
    # Exemplo: Espera receber um JSON {'texto': 'Olá Mundo'}
    conteudo = data.get('texto', '')
    
    if not conteudo:
        return jsonify({"erro": "Nenhum conteúdo fornecido"}), 400

    try:
        # 1. Cria um arquivo temporário para imprimir
        filename = tempfile.mktemp(".txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(conteudo)

        # 2. Envia para a impressora padrão do Windows
        # O comando 'print' usa o aplicativo padrão associado ao arquivo (ex: Bloco de Notas)
        win32api.ShellExecute(
            0,
            "print",
            filename,
            # Se a impressora não for a padrão, use: '/d:"Nome_da_Impressora"'
            None, 
            ".",
            0
        )

        return jsonify({"status": "Enviado para impressão", "arquivo": filename}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    # Roda na porta 5000
    app.run(port=3500)