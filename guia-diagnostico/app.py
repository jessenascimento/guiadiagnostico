import streamlit as st
import json
import os

#funções complementares
def carregar_diagnosticos(pasta='diagnosticos'):
    #carrega todos os arquivos de diagnóstico .json da pasta especificada.
    diagnosticos = {}
    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.endswith('.json'):
            caminho_arquivo = os.path.join(pasta, nome_arquivo)
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                logica = json.load(f)

                #usa o titulo do problema no json como a chave
                diagnosticos[logica['problema']] = logica
    return diagnosticos

def executar_guia(logica):
    #mostra perguntas e opções
    st.header(logica['problema'])

    passo_inicial = logica.get("passo_inicial")
    passos = logica.get("passos", {})
    solucoes = logica.get("solucoes", {})
 #inicializa o passo atual para este guia 
    if 'passo_atual' not in st.session_state:
        st.session_state.passo_atual = passo_inicial

    passo_id = st.session_state.passo_atual
    if passo_id.startswith("solucao_"):
        st.success("Diagnóstico Final:")
        st.markdown(f"**{solucoes.get(passo_id, 'Solução não encontrada.')}**")
        if st.button("Diagnosticar Outro Problema"):
           
            # limpa o estado para voltar ao menu principal
            del st.session_state.passo_atual
            del st.session_state.diagnostico_selecionado
            st.rerun()
    else:
        passo_info = passos.get(passo_id)
        if passo_info:
            st.info(passo_info["pergunta"])
            opcoes = passo_info["opcoes"]
            colunas = st.columns(len(opcoes))
            for i, (opcao_texto, proximo_passo_id) in enumerate(opcoes.items()):
                with colunas[i]:
                    if st.button(opcao_texto, key=f"btn_{passo_id}_{i}"):
                        st.session_state.passo_atual = proximo_passo_id
                        st.rerun()
# aplicação principal
st.set_page_config(page_title="Guia de Diagnóstico de TI", layout="centered")
st.title("Assistente de Suporte de TI 🛠️")

todos_diagnosticos = carregar_diagnosticos()

# menu principal
if 'diagnostico_selecionado' not in st.session_state:
    st.session_state.diagnostico_selecionado = None

if not st.session_state.diagnostico_selecionado:
    st.markdown("Bem-vindo! Selecione o problema que você está enfrentando:")
    
    #leva os nomes dos problemas para o menu
    opcoes_problemas = list(todos_diagnosticos.keys())
    
    problema_escolhido = st.selectbox("Selecione um problema:", options=["--"] + opcoes_problemas)
    
    if problema_escolhido != "--":
        st.session_state.diagnostico_selecionado = problema_escolhido
        st.rerun()

#executa o guia se um foi selecionado
else:
    logica_escolhida = todos_diagnosticos[st.session_state.diagnostico_selecionado]
    executar_guia(logica_escolhida)