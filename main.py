import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression

st.write("""
# 🐶 Pet Insights 🐱
##### O Sistema de Análise de Vendas para Pet Shops""") # título

st.write("📢 Em caso de dúvidas, consulte o README: https://tinyurl.com/5n8ptzpf")

st.write('\n')
st.write('\n')

###########################################################################################################
# Upload do Arquivo

st.write("\n ### 🗃️ Upload de Dados")
st.write("Para continuarmos, faça o envio dos dados a serem analisados")

uploaded_file = st.file_uploader("Escolha um Arquivo", type=['csv', 'xlsx'])

if uploaded_file is not None:
        
        file_extension = uploaded_file.name.split('.')[-1].lower()

        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Tipo de Arquivo Incorreto. Por Favor, escolha um arquivo CSV ou XSLX.")
            df = pd.DataFrame()

###########################################################################################################
# Modelagem dos Dados do DF

if uploaded_file is not None:
    df.dropna(inplace=True) # Remove linhas com NaN        
    df.dropna(axis=1, inplace=True) # Remove colunas com NaN
    df.drop_duplicates(inplace=True) # Remove duplicatas
    df['Data_Venda'] = pd.to_datetime(df['Data_Venda']) # Altera o tipo da coluna para datetime 

###########################################################################################################
# Exibição Gráficos Simples (Mais Vendidos, Menos Vendidos, Faturamento [Ambos por Categoria e Data]) 

if uploaded_file is not None:

     st.markdown("---")
     st.write("\n ## 📶 Resumo Geral")
     
     # Filtros de Mês/Ano e Categoria
     df["ano"] = df["Data_Venda"].dt.year
     df["mes"] = df["Data_Venda"].dt.month_name()
     ordem_meses = ["January", "February", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"]
     categorias = ["Nenhuma"] + sorted(df["Categoria"].unique().tolist())
     col1, col2, col3 = st.columns(3)
     
     with col1:
          categoria = st.selectbox("Selecione a categoria:", categorias)
     with col2:
          anos_disponiveis = sorted(df["ano"].unique())
          ano = st.selectbox("Selecione o ano:", anos_disponiveis)

     meses_disponiveis = df[df["ano"] == ano]["mes"].dropna().unique().tolist()
     meses_disponiveis = [m for m in ordem_meses if m in meses_disponiveis]
     meses = ["Nenhum"] + meses_disponiveis      
    
     with col3:
          mes = st.selectbox("Selecione o mês:", meses)
     filtro = (df["ano"] == ano)

     if categoria != "Nenhuma":
          filtro &= (df["Categoria"] == categoria)
     if mes != "Nenhum":
          filtro &= (df["mes"] == mes)
     dados_filtrados = df.loc[filtro]

     if dados_filtrados.empty:
          st.warning("Nenhum dado encontrado para os filtros selecionados.")
          st.stop()
     dados_filtrados["faturamento"] = dados_filtrados["Quantidade"] * dados_filtrados["Preco_Unitario"]     
     vendas = (dados_filtrados.groupby("Produto", as_index=False).agg({"Quantidade": "sum", "faturamento": "sum"}).sort_values("Quantidade", ascending=False))

     st.write('\n')

     # Cria o Cartão Métrico do Total de Unidades Vendidas e Faturamento Total (baseado no Power BI)
     total_vendido = int(vendas["Quantidade"].sum())
     total_faturado = float(vendas["faturamento"].sum())
     colA, colB = st.columns(2)
     with colA:     
          st.metric(label="Total de unidades vendidas", value=f"{total_vendido:,}".replace(",", "."))
     with colB:
          st.metric(label="Faturamento total", value=f"R$ {total_faturado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

     st.write('\n')

     # Gráfico Mais Vendidos 
     st.subheader(f"🔥Ranking 5 produtos mais vendidos")
     maisvend= vendas.head(5).sort_values("Quantidade", ascending=True)
     fig_bottom = px.bar(maisvend,x="Produto",y="Quantidade",text="Quantidade",color="Quantidade",color_continuous_scale="Blues")
     fig_bottom.update_traces(textposition="outside")
     st.plotly_chart(fig_bottom, use_container_width=True)

     st.write('\n')

     # Gráfico Menos Vendidos 
     st.subheader(f"📉 Ranking 5 produtos menos vendidos")
     menosvend= vendas.tail(5).sort_values("Quantidade", ascending=False)
     fig_bottom = px.bar(menosvend,x="Produto",y="Quantidade",text="Quantidade",color="Quantidade",color_continuous_scale="Reds")
     fig_bottom.update_traces(textposition="outside")
     st.plotly_chart(fig_bottom, use_container_width=True)

     st.write('\n')

     # Gráfico Faturamento (por Produto)
     st.subheader("💰 Faturamento Total (por produto)")
     top_faturamento = (vendas.sort_values("faturamento", ascending=False).sort_values("faturamento", ascending=True))
     fig3 = px.bar(top_faturamento,x="faturamento",y="Produto",orientation="h",text="faturamento",color="faturamento",color_continuous_scale="Greens",labels={"faturamento": "Faturamento (R$)", "Produto": "Produto"},)
     fig3.update_layout(title= "\n",xaxis_title="Faturamento (R$)",yaxis_title="Produto",title_font_size=18,height=500,)
     fig3.update_traces(texttemplate="R$ %{text:,.2f}", textposition="outside")
     st.plotly_chart(fig3, use_container_width=True)

###########################################################################################################
# Módulo de Previsão

if uploaded_file is not None:
     st.markdown("---")
     st.write(" ## 📶 Previsão de Vendas e Faturamento")
     st.write('\n')

     # Filtro de categoria
     if categoria != "Nenhuma":
          df_pred = df[df["Categoria"] == categoria]
     else:
          df_pred = df

     # Cálculo de faturamento
     df_pred["faturamento"] = df_pred["Quantidade"] * df_pred["Preco_Unitario"]     
     
     # Agrupar por mês (quantidade + faturamento)
     serie_vendas = (df_pred.groupby(pd.Grouper(key="Data_Venda", freq="M")).agg({"Quantidade": "sum", "faturamento": "sum"}).reset_index())
     serie_vendas.rename(columns={"Data_Venda": "ds"}, inplace=True)
     serie_vendas = serie_vendas.sort_values("ds")
     
     if len(serie_vendas) < 6:
          st.warning("Poucos dados históricos para gerar previsão confiável.")
     else:
          serie_vendas["t"] = np.arange(len(serie_vendas)).reshape(-1, 1)
     
          # Modelo preditivo - Quantidade
          X = serie_vendas[["t"]]
          y_qtd = serie_vendas["Quantidade"]
          modelo_qtd = LinearRegression()
          modelo_qtd.fit(X, y_qtd)

          # Modelo preditivo - Faturamento
          y_fat = serie_vendas["faturamento"]
          modelo_fat = LinearRegression()
          modelo_fat.fit(X, y_fat)

          # 6 meses futuros
          t_future = np.arange(len(serie_vendas), len(serie_vendas) + 6).reshape(-1, 1)
          last_date = serie_vendas["ds"].max()
          future_dates = pd.date_range(start=last_date + pd.offsets.MonthBegin(0), periods=6, freq="M")

          # Previsões
          y_qtd_future = modelo_qtd.predict(t_future)
          y_fat_future = modelo_fat.predict(t_future)
          previsoes = pd.DataFrame({"ds": future_dates,"qtd_pred": y_qtd_future,"fat_pred": y_fat_future})

          # Gráfico de Quantidade (Previsão)
          st.subheader("📦 Quantidade")
          fig_qtd = go.Figure()
          fig_qtd.add_trace(go.Scatter(x=serie_vendas["ds"], y=serie_vendas["Quantidade"],mode="lines+markers", name="Histórico", line=dict(color="lightblue")))
          fig_qtd.add_trace(go.Scatter(x=previsoes["ds"], y=previsoes["qtd_pred"],mode="lines+markers", name="Previsão (6 meses)",line=dict(color="orange", dash="dash")))
          fig_qtd.update_layout(title="📈 Quantidade de Vendas previstas nos próximos 6 meses",xaxis_title="Data", yaxis_title="Unidades Vendidas",height=450, legend_title="Legenda")
          st.plotly_chart(fig_qtd, use_container_width=True)

          # Gráfico de Faturamento (Previsão)
          st.subheader("💰Faturamento")
          fig_fat = go.Figure()
          fig_fat.add_trace(go.Scatter(x=serie_vendas["ds"], y=serie_vendas["faturamento"],mode="lines+markers", name="Histórico", line=dict(color="lightgreen")))
          fig_fat.add_trace(go.Scatter(x=previsoes["ds"], y=previsoes["fat_pred"],mode="lines+markers", name="Previsão (6 meses)",line=dict(color="gold", dash="dash")))
          fig_fat.update_layout(title="💵 Faturamento previsto nos próximos 6 meses",xaxis_title="Data", yaxis_title="Faturamento (R$)",height=450, legend_title="Legenda")
          st.plotly_chart(fig_fat, use_container_width=True)

          # Tabela de Previsões (mostra os valores previstos do Faturamento e da Quantidade Vendida em formato de tabela)
          st.subheader("📅 Tabela de Previsões") 
          tabela = previsoes.copy()
          tabela["Mês"] = tabela["ds"].dt.strftime("%B %Y")
          tabela["Quantidade Prevista"] = tabela["qtd_pred"].astype(int)
          tabela["Faturamento Previsto (R$)"] = tabela["fat_pred"].round(2)
          st.dataframe(tabela[["Mês", "Quantidade Prevista", "Faturamento Previsto (R$)"]])



# Atualizado em 21.10.2025 - (Pet Insights)                 