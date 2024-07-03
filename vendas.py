import streamlit as st
import pandas as pd
import plotly.express as px

#Configurando o layout da pagina
st.set_page_config(layout='wide')

df = pd.read_csv('vendas.csv', sep=';', decimal=',')

print(df)

#Convertendo coluna data para o formato de data do pandas
df['Data'] = pd.to_datetime(df['Data'])

#Ordenação
df = df.sort_values('Data')

print(df['Data'])

df['Ano'] = df['Data'].dt.year
df['Mês_Num'] = df['Data'].dt.month
df['Mês'] = df['Ano'].astype(str)+"-"+df['Mês_Num'].astype(str)

image_path = 'image.png'
st.sidebar.image(image_path, use_column_width=True)

mes = st.sidebar.selectbox('Mês', df['Mês'].unique())

df_filtro = df[df['Mês']==mes]

generos = st.sidebar.multiselect('Gêneros', df['Gênero'].unique(), default=df['Gênero'].unique())


if generos:
    df_filtro = df_filtro[df_filtro['Gênero'].isin(generos)]

st.title('Fatec Adamantina - Dashboard')
st.write('Oficina de Vendas')

st.markdown('## Resumo')
total_faturamento = df_filtro['Total'].sum()
total_vendas = df_filtro.shape[0]
avaliacao_media = df_filtro['Rating'].mean()
total_produtos = df_filtro['Quantidade'].sum()

#Dividindo a tela em colunas para os cartões
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label='Total Faturamento', value=f"R${total_faturamento:.2f}")

with col2:
    st.metric(label='Total Vendas', value=f"R${total_vendas:.2f}")

with col3:
    st.metric(label='Total Produtos Vendidos', value=f"R${total_produtos:.2f}")

with col4:
    st.metric(label='Avaliação Média', value=f"{avaliacao_media:.2f}")

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)    

fig_date = px.bar(df_filtro, x = 'Data', y='Total', color='Cidade', title='Faturamento por dia')
col1.plotly_chart(fig_date, use_container_width = True)

fig_prod = px.bar(df_filtro, x='Data', y='Linha de produto', color='Cidade', title='Faturamento por tipo de produto', orientation='h')
col2.plotly_chart(fig_prod, use_container_width = True)

cidade_total = df_filtro.groupby('Cidade')[['Total']].sum().reset_index()
fig_cidade = px.bar(cidade_total, x='Cidade', y='Total', title='Faturamento por cidade', color = 'Cidade')
col3.plotly_chart(fig_cidade, use_container_width=True)

fig_kind = px.pie(df_filtro, values='Total', names='Pagamento', title='Faturamento por tipo de pagamento')
col4.plotly_chart(fig_kind, use_container_width=True)

fig_rating = px.bar(df_filtro, y='Rating', x='Cidade', title='Avaliaçaõ média', color='Cidade')
col5.plotly_chart(fig_rating, use_container_width=True)