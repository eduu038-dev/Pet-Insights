# 🐕 Pet Insights
### O Sistema de Análise de Vendas para Pet Shops
## 📝 Sobre o Projeto:
- Este projeto consiste em um dashboard interativo desenvolvido com Streamlit, que permite:\
**➡️Analisar a quantidade de vendas e faturamento;\
➡️Visualizar os produtos mais e menos vendidos;\
➡️Filtrar por categoria, ano e mês;\
➡️Exibir gráficos de tendências de vendas e faturamento (via Plotly);\
➡️Realizar uma previsão de vendas e faturamento para os próximos 6 meses, utilizando Scikit-Learn.**
- Esta ferramenta busca analisar e prever a demanda de produtos, de forma a permitir um melhor controle dos estoques (previnindo possíveis faltas ou excessos),
- Além disso, ela também busca exibir alguns insights importantes para o negócio, como itens mais vendidos, menos vendidos, faturamento, etc.

 <br>
 
## 🖥️ Tecnologias 
- As tecnologias e ferramentas utilizadas nesse projeto são:\
➡️**Linguagem de Programação:** *Python*\
➡️**Framework:** *Streamlit*\
➡️**Bibliotecas de Ciência de Dados/AI:** *Scikt-Learn (machine learning), Plotly (criação e visualização de gráficos), Pandas e NumPy (manipulação e análise de dados)*\
➡️**Controle de Versão:** *GitHub*

 <br>
 
## ⬇️ Instalação 
- É possível executar a ferramenta pelo **navegador web** (através do link https://petinsights.streamlit.app/), ou localmente.
- Caso seja localmente, siga os passos a seguir para instalar e utilizar a ferramenta: 
  
 I. **Clone o repositório** 
```
git clone https://github.com/eduu038-dev/Pet-Insights
cd Pet-Insights
```
  II. **Instale as dependências**
 ```
pip install -r requirements.txt
```
  III. **Execute o Streamlit**
```
streamlit run main.py
```
  IV. **O app Streamlit iniciará no navegador, geralmente em:**
  ```
http://localhost:8501
```
 <br>

## ✅ Como utilizar a ferramenta

### 1️⃣ Importando os Dados
- O primeiro passo é realizar a importação da base de dados necessária para a análise. Neste caso, os formatos aceitos são **XLSX (Excel)** e **CSV**.
<img src="RDIMG/uplarq.png" width="600">

**⚠️ Atenção:** *para que a ferramenta funcione, a base de dados deve estar organizada da seguinte maneira:*
  ```
Data_Venda,Produto,Quantidade,Preco_Unitario,Categoria,Valor_Total

1.Data_Venda: a data da venda do produto (2025-01-01)
2.Produto: o nome do produto (Ração Premium)
3.Quantidade: a quantidade vendida (25)
4.Preco_Unitario: o preço unitário do produto (150.99) 
5.Categoria: a categoria que o produto pertence (Alimentação)
6.Valor_Total: o valor total das vendas (3774.75)
```
 <br>

### 2️⃣ Resumo Geral e Filtros
- Nesta seção, é possível visualizar algumas informações básicas, como as **Vendas Totais** e o **Faturamento Total**, além dos **Itens Mais Vendidos**, **Itens Menos Vendidos** e **Faturamento por Produto.**
- É possível filtrar as informações por **Categoria, Mês** e **Ano**.
<img src="RDIMG/resgeral.png" width="600">

<br>
  
### 3️⃣ Previsão Futura
- Nesta seção, é possível visualizar a previsão da **Quandidade de Vendas** e **Faturamento** para os próximos 6 meses.
- É possível observar através de **Gráficos** e **Tabela**
<img src="RDIMG/resprev.png" width="600">
