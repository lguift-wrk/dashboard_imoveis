from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    df = pd.read_excel('imoveis.xlsx')

    # Limpeza e padronização
    df = df.fillna('')
    for col in ['UF', 'Cidade', 'Bairro', 'Quartos', 'Vagas', 'Tipo Imóvel', 'Faixa Preço', 'Faixa Desconto']:
        df[col] = df[col].astype(str).str.strip().str.upper()

    df['Preço'] = pd.to_numeric(df['Preço'], errors='coerce')
    df['Valor de avaliação'] = pd.to_numeric(df['Valor de avaliação'], errors='coerce')
    df['Desconto ok'] = pd.to_numeric(df['Desconto ok'], errors='coerce')

    df['Preço'] = df['Preço'].apply(lambda x: f"{int(x):,}".replace(",", ".") if pd.notnull(x) else "")
    df['Valor de avaliação'] = df['Valor de avaliação'].apply(lambda x: f"{int(x):,}".replace(",", ".") if pd.notnull(x) else "")
    df['Desconto ok'] = df['Desconto ok'].apply(lambda x: f"{int(round(x))}%" if pd.notnull(x) else "")

    imoveis = df.to_dict(orient='records')
    return render_template('index.html', imoveis=imoveis)

if __name__ == '__main__':
    app.run(debug=True)