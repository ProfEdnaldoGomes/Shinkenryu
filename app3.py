import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout='wide')

def plot_radar_chart_plotly(labels, values, style='light'):
    """
    Função para criar um radar plot (gráfico de aranha) interativo com Plotly.

    Parâmetros:
    - labels: lista de strings representando os nomes das variáveis.
    - values: lista de números representando os valores de cada variável (de 1 a 5).
    - style: string indicando o estilo do gráfico ('light' para claro ou 'dark' para escuro).

    Retorna:
    - Um objeto Figure do Plotly.
    """
    # Configuração inicial com base no estilo escolhido
    if style == 'dark':
        bg_color = '#121212'  # Fundo escuro
        line_color = 'white'  # Cor das linhas no estilo escuro
        fill_color = 'rgba(0, 255, 255, 0.3)'  # Cor do preenchimento no estilo escuro
        text_color = 'white'  # Cor dos rótulos no estilo escuro
    else:
        bg_color = '#FFFFFF'  # Fundo claro
        line_color = 'black'  # Cor das linhas no estilo claro
        fill_color = 'rgba(0, 0, 255, 0.3)'  # Cor do preenchimento no estilo claro
        text_color = 'black'  # Cor dos rótulos no estilo claro

    # Criando o radar plot com Plotly
    fig = go.Figure()

    # Adicionando o traço (trace) do radar plot
    fig.add_trace(go.Scatterpolar(
        r=values + values[:1],  # Fechando o gráfico (voltando ao início)
        theta=labels + [labels[0]],  # Fechando o gráfico (voltando ao início)
        fill='toself',  # Preenchimento da área interna
        fillcolor=fill_color,  # Cor do preenchimento
        line=dict(color=line_color, width=2),  # Cor e largura da linha
        name='Intensidade'
    ))

    # Configurando o layout do gráfico
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],  # Limites do eixo radial
                color=text_color  # Cor dos rótulos do eixo radial
            ),
            bgcolor=bg_color  # Cor de fundo do gráfico polar
        ),
        paper_bgcolor=bg_color,  # Cor de fundo do papel (área externa)
        font_color=text_color,  # Cor do texto
        title=dict(
            text='Composição de Katas - Intensidade das Variáveis',
            font=dict(size=16),
            x=0.5  # Centraliza o título
        )
    )

    return fig

# Configuração do aplicativo Streamlit
st.title("Composição de Katas estilo Shinkenryu")

# Descrição e instruções
st.markdown("""
Este aplicativo permite que você crie um gráfico de radar interativo para visualizar a intensidade de diferentes variáveis.
- Use os campos na barra lateral para definir os nomes e níveis de intensidade das variáveis.
- Salve o gráfico como um arquivo HTML ou PNG.
""")


# Inserir logo na sidebar
st.sidebar.title('Shinkenryu', )
logo_path = "logo.jpg"  # Substitua pelo caminho da sua imagem local ou use uma URL
st.sidebar.image(logo_path, caption="Logo", use_container_width=True)

# Barra lateral para configurações
st.sidebar.header("Configurações")

# Estilo do gráfico
style = st.sidebar.selectbox("Escolha o estilo do gráfico:", ["light", "dark"])

# Número de variáveis
num_variables = st.sidebar.number_input("Número de variáveis", min_value=1, max_value=10, value=4)

# Gerenciamento de variáveis
labels = []
values = []
for i in range(num_variables):
    # Campo para inserir o nome da variável
    label = st.sidebar.text_input(f"Nome da variável {i+1}", value=f"Variável {i+1}")
    # Slider para ajustar a intensidade
    value = st.sidebar.slider(f"Intensidade de {label}", min_value=1, max_value=5, value=3)
    labels.append(label)
    values.append(value)

# Botão para salvar o gráfico
save_option = st.sidebar.selectbox("Salvar gráfico como:", ["Nenhum", "HTML", "PNG"])
if save_option == "HTML":
    file_name = st.sidebar.text_input("Nome do arquivo HTML", value="radar_plot.html")
elif save_option == "PNG":
    file_name = st.sidebar.text_input("Nome do arquivo PNG", value="radar_plot.png")

# Gerando o gráfico
fig = plot_radar_chart_plotly(labels, values, style=style)

# Salvando o gráfico, se necessário
if save_option == "HTML":
    fig.write_html(file_name)
    st.sidebar.success(f"Gráfico salvo como '{file_name}'!")
elif save_option == "PNG":
    fig.write_image(file_name)
    st.sidebar.success(f"Gráfico salvo como '{file_name}'!")

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)