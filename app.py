#UI
import streamlit as st

#sqlalchemy
#modelagem
#from sqlalchemy.ext.declarative import declarative_base
#drive 
from sqlalchemy import create_engine, Column, Integer, String
#persistencia ler e salvar
from sqlalchemy.orm import sessionmaker, declarative_base

# url - banco de dados

URL_NEON = f"postgresql://neondb_owner:{DB_PASSWORD}@ep-proud-queen-amw2v2mz.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(URL_NEON, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# classe base itinerario ORM
class Itinerario(Base):
    __tablename__ = 'itinerario_aula'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    descricao = Column(String)

# 5. Tentativa de criação com tratamento de erro
try:
    Base.metadata.create_all(engine)
    st.success("Conectado e tabelas verificadas!")
except Exception as e:
    st.error(f"Erro de conexão: {e}")


# FRame
st.set_page_config(page_title='Formulário de Itinerário')
st.title('Cadastro de itinerário 2026')
st.info('Os dados serão salvos diretamente no PostgresSQL no Neon')

with st.form('formulário',clear_on_submit=True):
    nome_input = st.text_input('Nome do Itinerário')
    desc_input = st.text_input('Descrição')
    botao = st.form_submit_button('Salvar dados')

if botao and nome_input:
    session = Session()
    novo_registro = Itinerario(nome=nome_input, descricao=desc_input)
    session.add(novo_registro)
    session.commit()
    session.close()
    st.success(f'Sucesso {nome_input} foi salvo com sucesso!')
else:
    st.error('Por favor, preencha corretamente')

# Atualização em tempo real
st.divider()
st.subheader('Registro atual')
session = Session()
dados = session.query(Itinerario).all()
session.close()

if dados:
    for item in dados:
        st.write(f'{item.nome}: {item.descricao}')