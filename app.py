import streamlit as st
import upload as up
import pandas as pd
from slugify import slugify

def processar_arquivo(arquivo):
    colunas_banco = [
    "Empresa",
    "Parceiro",
    "Descrição (Tipo de Título)",
    "Descrição (Natureza)",
    "Dt. Negociação",
    "Dt. Vencimento",
    "Vlr do Desdobramento",
    "Valor Líquido",
    "Nome Parceiro (Parceiro)",
    "Data Baixa",
    "Nro Nota",
    "Nome (Usuário)",
    "Histórico",
    "Conta Bancária",
    "Nro Único",
    "Vlr Desconto",
    "Tipo Operação",
    "Origem",
    "Taxa Administradora",
    "Vlr Baixa",
    "Vlr Juros",
    "Vlr Multa",
    "Desdob.",
    "Negativação",
    "Receita/Despesa",
    "Nome (Usuário Baixa)",
    "Cnpj/CPF",
    "Razão Social",
    "Banco",
    "Descrição (Tipo de Operação)",
    "Nome Fantasia (Empresa)",
    "Centro Resultado",
    "Descrição (Centro de Resultado)",
    "Vendedor",
    "Apelido",
    "Prazo",
    "Descrição (Banco)",
    "Descrição (Conta Bancária)",
    "Tipo de Título"
]
    nome_tabela = "contas_a_receber_megaferro"

    st.markdown(f'### -> {arquivo.name}')
    progresso = st.progress(0, "Lendo arquivo...")

    try: 
        data_frame = pd.read_excel(arquivo, header=2, skipfooter=2, usecols=colunas_banco)
    except Exception as e:
        progresso.empty()
        st.error(f'Erro ao abrir arquivo: {e}')
        return
    
    progresso.progress(1/4,'Validando planilha...')
    try:
        up.validar_planilha(data_frame, colunas_banco, ["Dt. Negociação", "Dt. Vencimento",])
    except Exception as e:
        progresso.empty()
        st.error(f'Planilha inválida. Erro: {e}')
        return

    progresso.progress(2/4, 'Formatando Planilha...')
    try: 
        data_frame['data_importacao'] = pd.Timestamp.today().replace(hour=0, minute=0, second=0, microsecond=0)
        data_frame.columns = [slugify(column, separator="_") for column in data_frame.columns.tolist()]
    except Exception as e:
        progresso.empty()
        st.error(f'Erro ao formatar planilha: {e}')
        return
    
    progresso.progress(3/4, 'Enviando Dados...')
    try:
        up.adicionar_registros(data_frame, nome_tabela)
        progresso.progress(4/4, 'Finalizado!')
        progresso.empty()
        st.success(f'Base de dados atualizada com sucesso! {len(data_frame)} registros adicionados')    
    except Exception as e:
        progresso.empty()
        st.error(f'Houve um erro ao enviar dados. Erro: {e}')
        return

def page_upload():
    st.write('# MEGAFERRO')
    col1, col2 = st.columns(2, gap='large')

    with col1:
        st.header('Enviar para o banco de dados')
        st.divider()
        arquivo = st.file_uploader('**Contas a Receber**', ['xlsx', 'xls'], accept_multiple_files=False)
        
        botao = st.button('Enviar')
    with col2:
        st.header('Logs')
        st.divider()

        if arquivo and botao:
                processar_arquivo(arquivo)

def main():
    st.set_page_config(layout='wide', page_title="Megaferro")
    page_upload()

if __name__ == "__main__":
    main()