import pandas as pd
import os
import s3fs
from s3fs.core import S3FileSystem
import streamlit as st
import matplotlib.pyplot as plt
import pylab as plb
plb.rcParams['font.size'] = 20

# Carregando o arquivo csv.
@st.cache(ttl=600)
def load_data():
    s3 = S3FileSystem(anon=False)
    bucket = "pi01.microdadoscensosuperior2019"
    key = 'dataframe.csv'
    df = pd.read_csv(s3.open('{}/{}'.format(bucket, key), mode='rb'))
    df = pd.read_csv(s3.open(f'{bucket}/{key}', mode='rb'))
    return df

#st.title('Acesso à Educação Superior')
st.sidebar.title('Menu')
paginaselect =st.sidebar.empty()
paginaselect = st.sidebar.selectbox('Selecione a página', ['Início', 'Buscar infográficos'])

### Seleção das Páginas ###
if paginaselect == 'Início':
    #st.header('Home')
    st.title('Acesso à Educação Superior')
    st.header('Início')
    '''
    Este site tem como objetivo partilhar análises descritas e visuais com a intenção de observar o acesso à Educação Superior no Brasil. 
    Ele busca apresentar os aspectos sobre o acesso a edução de alunos, utilizando dados sociais relativos à raça ou cor, gênero, idade e 
    portabilidade de deficiência.

    Em face da perspectiva de utilização de infográficos interativos, compreende-se que poderemos responder questionamentos sobre a questão
    foco, considerando a necessidade de cada usuário. 

    Importante observar que o conjunto de dados trabalhado é o Censo do Ensino do Superior do ano de 2019, que é o censo mais atualizado 
    no momento presente deste projeto.

    Aproveite os dados disponibilizados. Em breve estaremos publicando análises mais detalhadas relativas à portabilidade de deficiência e além
    de novos modelos para a visualização de dados. '''


    st.write('') 
    st.write('')


    st.header('Sobre o Projeto')
    '''
    Este projeto é consequência da pesquisa desenvolvida para realização do Projeto Integrador I, disciplina da Universidade Virtual do Estado
    de São Paulo (UNIVESP), bem como, do desejo de facilitar a obtenção de infográficos que descrevem os aspectos sociais relacionados ao acesso 
    à educação superior.
    
    Atualmente estamos na fase de ampliar os mecanismos de busca da aplicação.
    '''
    
elif paginaselect == 'Buscar infográficos':

    st.title('Acesso à Educação Superior')
    st.subheader('Buscar infográficos')
    ''' 
    '''
    '''Selecione os campos de interesse para obter os infográficos correspondentes ao acesso à Educação Superior.\
    Os dados sociais apresentados são relativos à raça ou cor, gênero, idade e portabilidade de deficiência.'''
    '''
    '''


    
    # Chamar o método que retorna o dataframe.
    dataframe = load_data()

    uf_temp = dataframe['UF'].unique()
    uf = uf_temp.tolist()
    uf.sort()
    uf.insert(0,'')
    uf.insert(1,'Todas opções')
    uf_select = st.selectbox('Selecione a Unidade Federativa', options = uf, key='uf01')

    adm_select = st.selectbox('Selecione o tipo de categoria administrativa',\
        options= ['','Todas opções', 'Pública Federal', 'Pública Estadual', 'Pública Municipal', 'Privada com fins lucrativos', 'Privada sem fins lucrativos', 'Especial'], key='adm02')
    
    if uf_select != '' and adm_select != '': 
        if uf_select != 'Todas opções' and adm_select != 'Todas opções':
            df_uf = dataframe.filter(items=['TP_COR_RACA', 'TP_SEXO','NU_IDADE', 'IN_DEFICIENCIA', 'NO_IES', 'TP_CATEGORIA_ADMINISTRATIVA', 'ID_ALUNO', "CO_IES",'CO_UF', 'UF'])\
                .where(dataframe.UF == uf_select).dropna()
            df1 = df_uf.filter(items=['TP_COR_RACA', 'TP_SEXO','NU_IDADE', 'IN_DEFICIENCIA', 'NO_IES', 'TP_CATEGORIA_ADMINISTRATIVA', 'ID_ALUNO', "CO_IES"])\
                .where(df_uf.TP_CATEGORIA_ADMINISTRATIVA == adm_select).dropna()       

            research_ies = st.radio("Buscar os resultados pelo nome da instituição", ['Não', 'Sim'], key='rs03')

            if research_ies == 'Sim':
                nome_ies_temp = df1['NO_IES'].unique()
                nome_ies = nome_ies_temp.tolist()
                nome_ies.sort()
                nome_ies.insert(0,'')
                nome_ies_select = ''
                nome_ies_select = st.selectbox('Selecione o nome da instituição', options = nome_ies, key = 'ies04')
                if nome_ies_select != '':   
                    st.write('') 
                    st.write('')                 
                    st.subheader('Dados relativos à raça ou cor')
                    st.write('') 
                    st.write('')   
                    df0 = df1.filter(items=['TP_COR_RACA', 'TP_SEXO','NU_IDADE', 'IN_DEFICIENCIA', 'NO_IES', 'TP_CATEGORIA_ADMINISTRATIVA', 'ID_ALUNO'])\
                        .where(df1.NO_IES == nome_ies_select).dropna()
                    
                    ## Descrição dos alunos, por raça ou cor. ###
                    axr0 = df0.filter(items=['ID_ALUNO', 'TP_COR_RACA']).groupby('TP_COR_RACA').count().sort_values(by='ID_ALUNO', ascending=False)\
                        .plot.barh(figsize=(16,10), width = 0.8, colormap='jet', edgecolor = 'black')

                    axr0.get_legend().remove()
                    axr0.set_title('Taxa de distribuição de alunos, por cor ou raça', fontsize='25')
                    axr0.set_xlabel("Quantidade de alunos")
                    axr0.set_ylabel('Cor ou raça')

                    st.pyplot(plt) 
                    plt.clf()

                    st.write('')   
                        
                    labels_r0 = ['Amarela', 'Branca','Indígena', 'Parda', 'Preta', 'Não coletado', 'Não declarado']
                    values_r0 = [[df0['TP_COR_RACA'].where(df0.TP_COR_RACA == 'Amarela').count(),\
                        df0['TP_COR_RACA'].where(df0.TP_COR_RACA == 'Branca').count(),\
                            df0['TP_COR_RACA'].where(df0.TP_COR_RACA == 'Indígena').count(),\
                                df0['TP_COR_RACA'].where(df0.TP_COR_RACA == 'Parda').count(),\
                                    df0['TP_COR_RACA'].where(df0.TP_COR_RACA == 'Preta').count(),\
                                        df0['TP_COR_RACA'].where(df0.TP_COR_RACA == 'Não coletado').count(),\
                                            df0['TP_COR_RACA'].where(df0.TP_COR_RACA == 'Não declarado').count()]]

                    data_r0 = pd.DataFrame(values_r0, columns=['Amarela', 'Branca','Indígena', 'Parda', 'Preta', 'Não coletado', 'Não declarado']) 

                    result_pct = data_r0.div(data_r0.sum(1), axis=0) 

                    ax = result_pct.plot(kind='bar',figsize=(16,10),width = 0.8,edgecolor=None)
                    plt.legend(labels=data_r0.columns,fontsize= 14)
                    plt.suptitle('Taxa percentual de alunos, por cor ou raça', size=22)

                    plt.xticks(fontsize=14)
                    for spine in plt.gca().spines.values():
                        spine.set_visible(False)
                    plt.yticks([])

                    for p in ax.patches:
                        width = p.get_width()
                        height = p.get_height()
                        x, y = p.get_xy() 
                        ax.annotate('{:.00001%}'.format(height), (p.get_x()+.5*width, p.get_y() + height + 0.01), ha = 'center')

                    ax.set_xlabel('Cor ou Raça')
                    st.pyplot(plt) 
                    plt.clf()

                    st.write('')   

                    valr = df0.filter(items=['ID_ALUNO', 'TP_COR_RACA']).groupby('TP_COR_RACA')\
                        .count().sort_values(by='ID_ALUNO', ascending=False)
                    valr= valr.reset_index()
                    valr = valr.rename(columns={'ID_ALUNO': 'Quantidade de alunos'})
                    valr = valr.rename(columns={'TP_COR_RACA': 'Cor ou raça' })
                    st.table(valr)


                    ### Descrição dos alunos, por gênero. ###
                    st.write('') 
                    st.write('')   
                    st.subheader('Dados relativos à gênero')
                    st.write('') 
                    st.write('')  

                    labels_g = ['Feminino', 'Masculino']
                    values_g = [df0['TP_SEXO'].where(df0.TP_SEXO == 'Feminino')\
                        .count(), df0['TP_SEXO'].where(df0.TP_SEXO == 'Masculino').count()]

                    colors = ['blueviolet','orange'] #steelblue goldenrod indianred cadetblue 'blueviolet'
                    fig, axg = plt.subplots(figsize=(16,10))
                    axg.pie(values_g, autopct='%1.1f%%', startangle=60, colors=colors)
                    fig.suptitle('Taxa percentual de alunos, por gênero', size=25)

                    text = 'O Censo da Educação Superior coletou apenas gêneros binários.'
                    axg.text(0.25, 0, text, transform=axg.transAxes, fontsize=18)  

                    #draw circle
                    centre_circle = plt.Circle((0,0),0.70,fc='white') 
                    fig = plt.gcf()

                    axg.axis('equal')
                    plt.tight_layout()
                    plt.legend(labels=labels_g)
                    st.pyplot(plt) 
                    plt.clf()
                    
                    st.write('') 

                    valg = df0.filter(items=['ID_ALUNO', 'TP_SEXO']).groupby('TP_SEXO').count().sort_values(by='ID_ALUNO', ascending=False)

                    valg= valg.reset_index()
                    valg = valg.rename(columns={'ID_ALUNO': 'Quantidade de alunos'})
                    valg = valg.rename(columns={'TP_SEXO': 'Gênero' })
                    st.table(valg)


                    ### Descrição dos alunos, por idade. ###
                    st.write('') 
                    st.write('')  
                    st.subheader('Dados relativos à idade')
                    st.write('') 
                    st.write('')  


                    axi= df0.filter(items=['ID_ALUNO', 'NU_IDADE']).groupby('NU_IDADE').count().plot(figsize=(20,10), colormap='PiYG_r') 
                    axi.get_legend().remove()

                    axi.set_ylabel('Quantidade de alunos')
                    axi.set_xlabel('Idade')
                    plt.suptitle('Taxa de distribuição de alunos, por idade', size=25)
                    #axi.set_title('Taxa de distribuição de alunos, por idade', fontsize=18)
                    ticks = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105]
                    #fig.tight_layout()
                    plt.xticks(ticks, ticks)

                    st.pyplot(plt) 
                    plt.clf()

                    st.write('') 
                    st.markdown('###### Dados relativos à idade, organizados por ordem de valor (Rol).')
            
                    valage = df0.filter(items=['ID_ALUNO', 'NU_IDADE']).groupby('NU_IDADE').count().sort_values(by='NU_IDADE', ascending=True)
                    
                    valage = valage.reset_index()
                    valage = valage.rename(columns={'ID_ALUNO': 'QUANTIDADE DE ALUNOS' })
                    valage = valage.rename(columns={'NU_IDADE':'IDADE'})
                    valage = valage.astype(int)
                    st.write(valage)

                    st.write('')  
                    st.markdown('###### Dados relativos à idade, organizados por frequência.')
                    
                    valage1 = df0.filter(items=['ID_ALUNO', 'NU_IDADE']).groupby('NU_IDADE').count().sort_values(by='ID_ALUNO', ascending=False)
                    valage1 = valage1.reset_index()
                    valage1 = valage1.rename(columns={'ID_ALUNO': 'QUANTIDADE DE ALUNOS' })
                    valage1 = valage1.rename(columns={'NU_IDADE':'IDADE'})
                    valage1 = valage1.astype(int)
                    st.write(valage1)

                    ### Descrição dos alunos, por portabilidade de deficiência. ###
                    st.write('') 
                    st.write('')  
                    st.subheader('Dados relativos à portabilidade de deficiência')
                    st.write('') 
                    st.write('')  

                    labels_d = ['Não', 'Sim', 'Não coletado']
                    values_d = [[df0['IN_DEFICIENCIA'].where(df0.IN_DEFICIENCIA == 'Não')\
                        .count(), df0['IN_DEFICIENCIA'].where(df0.IN_DEFICIENCIA == 'Sim')\
                            .count(), df0['IN_DEFICIENCIA'].where(df0.IN_DEFICIENCIA == 'Não coletado').count()]]
                    data_d = pd.DataFrame(values_d, columns=['Não', 'Sim', 'Não coletado'])

                    colors_list = ['#4fa280', '#564fa2','#f2a132'] #'#b6704f' #a2804f #a2804f' '#a2564f', '#4fa280', '#a24f9b'

                    result_pct = data_d.div(data_d.sum(1), axis=0)

                    axd = result_pct.plot(kind='bar',figsize=(16,10),width = 0.6,color = colors_list,edgecolor=None)
                    plt.legend(labels=data_d.columns,fontsize= 14)
                    plt.suptitle('Taxa percentual de alunos, por portabilidade de deficiência', size=22)

                    plt.xticks(fontsize=14)
                    for spine in plt.gca().spines.values():
                        spine.set_visible(False)
                    plt.yticks([])

                    for p in axd.patches:
                        width = p.get_width()
                        height = p.get_height()
                        x, y = p.get_xy() 
                        axd.annotate('{:.00001%}'.format(height), (p.get_x()+.5*width, p.get_y() + height + 0.01), ha = 'center')

                    axd.set_xlabel('Portabilidade de deficiência')
                    st.pyplot(plt) 
                    plt.clf()

                    st.write('') 

                    valdef = df0.filter(items=['ID_ALUNO', 'IN_DEFICIENCIA']).groupby('IN_DEFICIENCIA').count().sort_values(by='ID_ALUNO', ascending=False)
                    valdef = valdef.reset_index()
                    valdef = valdef.rename(columns={'ID_ALUNO': 'Quantidade de alunos' })
                    valdef = valdef.rename(columns={'IN_DEFICIENCIA': 'Portabilidade de deficiência'})
                    st.table(valdef)

                os.system("pause")

            if research_ies != 'Sim': # Isto é, não buscar pelo nome da instituição.
                ### Descrição dos alunos, por raça ou cor. ###
                st.write('') 
                st.write('')  
                st.subheader('Dados relativos à raça ou cor')
                st.write('') 
                st.write('')  

                # Gráfico
                axr = df1.filter(items=['ID_ALUNO', 'TP_COR_RACA']).groupby('TP_COR_RACA').count().sort_values(by='ID_ALUNO', ascending=False)\
                    .plot.barh(figsize=(16,10), colormap='jet', edgecolor = 'black', width = 0.8)
                axr.get_legend().remove()
                plt.suptitle('Taxa de distribuição de alunos, por raça ou cor', size=25)
                axr.set_xlabel("Quantidade de alunos")
                axr.set_ylabel('Cor ou raça')

                st.pyplot(plt) 
                plt.clf()

                st.write('')

                labels_r = ['Amarela', 'Branca','Indígena', 'Parda', 'Preta', 'Não coletado', 'Não declarado']
                values_r = [[df1['TP_COR_RACA'].where(df1.TP_COR_RACA == 'Amarela').count(),\
                    df1['TP_COR_RACA'].where(df1.TP_COR_RACA == 'Branca').count(),\
                        df1['TP_COR_RACA'].where(df1.TP_COR_RACA == 'Indígena').count(),\
                            df1['TP_COR_RACA'].where(df1.TP_COR_RACA == 'Parda').count(),\
                                df1['TP_COR_RACA'].where(df1.TP_COR_RACA == 'Preta').count(),\
                                    df1['TP_COR_RACA'].where(df1.TP_COR_RACA == 'Não coletado').count(),\
                                        df1['TP_COR_RACA'].where(df1.TP_COR_RACA == 'Não declarado').count()]]

                data_r = pd.DataFrame(values_r, columns=labels_r) ######### labels_r?
                result_pct = data_r.div(data_r.sum(1), axis=0) 
                ax = result_pct.plot(kind='bar',figsize=(16,10),width = 0.8,edgecolor=None)

                plt.legend(labels=data_r.columns,fontsize= 14)
                plt.suptitle('Taxa percentual de alunos, por raça ou cor', size=22)
                plt.xticks(fontsize=14)
                for spine in plt.gca().spines.values():
                    spine.set_visible(False)
                plt.yticks([])

                for p in ax.patches:
                    width = p.get_width()
                    height = p.get_height()
                    x, y = p.get_xy() 
                    ax.annotate('{:.00001%}'.format(height), (p.get_x()+.5*width, p.get_y() + height + 0.01), ha = 'center')

                ax.set_xlabel('Cor ou Raça')
                st.pyplot(plt) 
                plt.clf()

                st.write('') 

                valr = df1.filter(items=['ID_ALUNO', 'TP_COR_RACA']).groupby('TP_COR_RACA')\
                    .count().sort_values(by='ID_ALUNO', ascending=False)
                valr= valr.reset_index()
                valr = valr.rename(columns={'ID_ALUNO': 'Quantidade de alunos'})
                valr = valr.rename(columns={'TP_COR_RACA': 'Cor ou raça' })
                st.table(valr)

                ### Descrição dos alunos, por gênero. ###
                st.write('') 
                st.write('')  
                st.subheader('Dados relativos à gênero')
                st.write('') 
                st.write('')  

                # Gráfico:
                labels_g = ['Feminino', 'Masculino']
                values_g = [df1['TP_SEXO'].where(df1.TP_SEXO == 'Feminino').count(), df1['TP_SEXO'].where(df1.TP_SEXO == 'Masculino').count()]
                colors = ['blueviolet','orange']
                fig, axg = plt.subplots(figsize=(16,10))
                axg.pie(values_g, autopct='%1.1f%%', startangle=60, colors=colors)
                fig.suptitle('Taxa percentual de alunos, por gênero', size=25)
                text = 'O Censo da Educação Superior coletou apenas gêneros binários.'
                axg.text(0.27, 0, text, transform=axg.transAxes, fontsize=16) 

                #draw circle
                centre_circle = plt.Circle((0,0),0.70,fc='white')
                fig = plt.gcf()

                axg.axis('equal')
                plt.tight_layout()
                plt.legend(labels=labels_g)
                st.pyplot(plt) 
                plt.clf()

                st.write('')

                valg = df1.filter(items=['ID_ALUNO', 'TP_SEXO']).groupby('TP_SEXO')\
                    .count().sort_values(by='ID_ALUNO', ascending=False)

                valg= valg.reset_index()
                valg = valg.rename(columns={'ID_ALUNO': 'Quantidade de alunos' })
                valg = valg.rename(columns={'TP_SEXO': 'Gênero' })
                st.table(valg)


                ### Descrição dos alunos, por idade. ###
                st.write('') 
                st.write('')  
                st.subheader('Dados relativos à idade')
                st.write('') 
                st.write('')  

                # Gráfico:
                axi= df1.filter(items=['ID_ALUNO', 'NU_IDADE']).groupby('NU_IDADE').count().plot(figsize=(20,10), colormap='PiYG_r') 
                axi.get_legend().remove()

                axi.set_ylabel('Quantidade de alunos')
                axi.set_xlabel('Idade')
                plt.suptitle('Taxa de distribuição de alunos, por idade', size=25)
                ticks = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110]
                plt.xticks(ticks, ticks)

                st.pyplot(plt) 
                plt.clf()
            
                st.write('')  
                st.markdown('###### Dados relativos à idade, organizados por ordem de valor (Rol).')

                valage = df1.filter(items=['ID_ALUNO', 'NU_IDADE']).groupby('NU_IDADE')\
                    .count().sort_values(by='NU_IDADE', ascending=True)
                valage = valage.reset_index()
                valage = valage.rename(columns={'ID_ALUNO': 'QUANTIDADE DE ALUNOS' })
                valage = valage.rename(columns={'NU_IDADE':'IDADE'})
                valage = valage.astype(int)
                st.write(valage)

                st.write('') 
                st.markdown('###### Dados relativos à idade, organizados por frequência.')
                
                valage1 = df1.filter(items=['ID_ALUNO', 'NU_IDADE']).groupby('NU_IDADE')\
                    .count().sort_values(by='ID_ALUNO', ascending=False)
                valage1 = valage1.reset_index()
                valage1 = valage1.rename(columns={'ID_ALUNO': 'QUANTIDADE DE ALUNOS' })
                valage1 = valage1.rename(columns={'NU_IDADE':'IDADE'})
                valage1 = valage1.astype(int)
                st.write(valage1)


                ### Descrição dos alunos, por portabilidade de deficiência. ###
                st.write('') 
                st.write('')  
                st.subheader('Dados relativos à portabilidade de deficiência')
                st.write('') 
                st.write('')  

                # Gráfico:
                labels_d = ['Não', 'Sim', 'Não coletado']      
                values_d = [[df1['IN_DEFICIENCIA'].where(df1.IN_DEFICIENCIA == 'Não')\
                    .count(), df1['IN_DEFICIENCIA'].where(df1.IN_DEFICIENCIA == 'Sim')\
                        .count(), df1['IN_DEFICIENCIA'].where(df1.IN_DEFICIENCIA == 'Não coletado').count()]]

                data_d = pd.DataFrame(values_d, columns=['Não', 'Sim', 'Não coletado'])

                colors_list = ['#4fa280', '#564fa2','#f2a132']

                result_pct = data_d.div(data_d.sum(1), axis=0)

                axd = result_pct.plot(kind='bar',figsize=(16,10),width = 0.6,color = colors_list,edgecolor=None)
                plt.legend(labels=data_d.columns,fontsize= 14)
                plt.suptitle('Taxa percentual de alunos, por portabilidade de deficiência', size=22)

                plt.xticks(fontsize=14)
                for spine in plt.gca().spines.values():
                    spine.set_visible(False)
                plt.yticks([])

                for p in axd.patches:
                    width = p.get_width()
                    height = p.get_height()
                    x, y = p.get_xy() 
                    axd.annotate('{:.00001%}'.format(height), (p.get_x()+.5*width, p.get_y() + height + 0.01), ha = 'center')

                axd.set_xlabel('Portabilidade de deficiência')

                st.pyplot(plt) 
                plt.clf()

                st.write('')  

                valdef = df1.filter(items=['ID_ALUNO', 'IN_DEFICIENCIA']).groupby('IN_DEFICIENCIA').count().sort_values(by='ID_ALUNO', ascending=False)
                valdef = valdef.reset_index()
                valdef = valdef.rename(columns={'ID_ALUNO': 'Quantidade de alunos' })
                valdef = valdef.rename(columns={'IN_DEFICIENCIA': 'Portabilidade de deficiência'})
                st.table(valdef)

      
        elif uf_select == 'Todas opções' and adm_select != 'Todas opções':
            df_adm = dataframe.filter(items=['TP_COR_RACA', 'TP_SEXO','NU_IDADE', 'IN_DEFICIENCIA', 'NO_IES', 'TP_CATEGORIA_ADMINISTRATIVA', 'ID_ALUNO', "CO_IES",'CO_UF', 'UF'])\
                .where(dataframe.TP_CATEGORIA_ADMINISTRATIVA == adm_select).dropna()
            
            ### Descrição dos alunos, por raça ou cor. ###
            st.write('') 
            st.write('')  
            st.subheader('Dados relativos à raça ou cor')
            st.write('') 
            st.write('')  

            # Gráfico
            axr = df_adm.filter(items=['ID_ALUNO', 'TP_COR_RACA']).groupby('TP_COR_RACA').count().sort_values(by='ID_ALUNO', ascending=False)\
                .plot.barh(figsize=(16,10), colormap='jet', edgecolor = 'black', width = 0.8)
            axr.get_legend().remove()
            plt.suptitle('Taxa de distribuição de alunos, por raça ou cor', size=25)
            axr.set_xlabel("Quantidade de alunos")
            axr.set_ylabel('Cor ou raça')

            st.pyplot(plt) 
            plt.clf()

            st.write('')  

            labels_r = ['Amarela', 'Branca','Indígena', 'Parda', 'Preta', 'Não coletado', 'Não declarado']
            values_r = [[df_adm['TP_COR_RACA'].where(df_adm.TP_COR_RACA == 'Amarela').count(),\
                df_adm['TP_COR_RACA'].where(df_adm.TP_COR_RACA == 'Branca').count(),\
                    df_adm['TP_COR_RACA'].where(df_adm.TP_COR_RACA == 'Indígena').count(),\
                        df_adm['TP_COR_RACA'].where(df_adm.TP_COR_RACA == 'Parda').count(),\
                            df_adm['TP_COR_RACA'].where(df_adm.TP_COR_RACA == 'Preta').count(),\
                                df_adm['TP_COR_RACA'].where(df_adm.TP_COR_RACA == 'Não coletado').count(),\
                                    df_adm['TP_COR_RACA'].where(df_adm.TP_COR_RACA == 'Não declarado').count()]]

            data_r = pd.DataFrame(values_r, columns=labels_r) ######### labels_r?
            result_pct = data_r.div(data_r.sum(1), axis=0) 
            ax = result_pct.plot(kind='bar',figsize=(16,10),width = 0.8,edgecolor=None)

            plt.legend(labels=data_r.columns,fontsize= 14)
            plt.suptitle('Taxa percentual de alunos, por raça ou cor', size=22)
            plt.xticks(fontsize=14)
            for spine in plt.gca().spines.values():
                spine.set_visible(False)
            plt.yticks([])

            for p in ax.patches:
                width = p.get_width()
                height = p.get_height()
                x, y = p.get_xy() 
                ax.annotate('{:.00001%}'.format(height), (p.get_x()+.5*width, p.get_y() + height + 0.01), ha = 'center')

            ax.set_xlabel('Cor ou Raça')
            st.pyplot(plt) 
            plt.clf()

            # Valores raça
            st.write('') 
            
            valr = df_adm.filter(items=['ID_ALUNO', 'TP_COR_RACA']).groupby('TP_COR_RACA')\
                .count().sort_values(by='ID_ALUNO', ascending=False)
            valr= valr.reset_index()
            valr = valr.rename(columns={'ID_ALUNO': 'Quantidade de alunos'})
            valr = valr.rename(columns={'TP_COR_RACA': 'Cor ou raça' })
            st.table(valr)

            ### Descrição dos alunos, por gênero. ###
            st.write('') 
            st.write('')  
            st.subheader('Dados relativos à gênero')
            st.write('') 
            st.write('')  

            # Gráfico:
            labels_g = ['Feminino', 'Masculino']
            values_g = [df_adm['TP_SEXO'].where(df_adm.TP_SEXO == 'Feminino').count(), df_adm['TP_SEXO'].where(df_adm.TP_SEXO == 'Masculino').count()]
            colors = ['blueviolet','orange']
            fig, axg = plt.subplots(figsize=(16,10))
            axg.pie(values_g, autopct='%1.1f%%',  startangle=60, colors=colors)
            fig.suptitle('Taxa percentual de alunos, por gênero', size=25)
            text = 'O Censo da Educação Superior coletou apenas gêneros binários.'
            axg.text(0.27, 1.0, text, transform=axg.transAxes, fontsize=16)

            #draw circle
            centre_circle = plt.Circle((0,0),0.70,fc='white')
            fig = plt.gcf()

            axg.axis('equal')
            plt.tight_layout()
            plt.legend(labels=labels_g)
            st.pyplot(plt) 
            plt.clf()

            st.write('')  

            valg = df_adm.filter(items=['ID_ALUNO', 'TP_SEXO']).groupby('TP_SEXO')\
                .count().sort_values(by='ID_ALUNO', ascending=False)
            valg= valg.reset_index()
            valg = valg.rename(columns={'ID_ALUNO': 'Quantidade de alunos' })
            valg = valg.rename(columns={'TP_SEXO': 'Gênero' })
            st.table(valg)


            ### Descrição dos alunos, por idade. ###
            st.write('') 
            st.write('')  
            st.subheader('Dados relativos à idade')
            st.write('') 
            st.write('')  

            # Gráfico:
            axi= df_adm.filter(items=['ID_ALUNO', 'NU_IDADE']).groupby('NU_IDADE').count().plot(figsize=(20,10), colormap='PiYG_r') 

            axi.get_legend().remove()
            axi.set_ylabel('Quantidade de alunos')
            axi.set_xlabel('Idade')
            plt.suptitle('Taxa de distribuição de alunos, por idade', size=22)

            ticks = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110]
            plt.xticks(ticks, ticks)

            st.pyplot(plt) 
            plt.clf()

            st.write('') 
            st.markdown('###### Dados relativos à idade, organizados por ordem de valor (Rol).')
            
            valage = df_adm.filter(items=['ID_ALUNO', 'NU_IDADE']).groupby('NU_IDADE')\
                .count().sort_values(by='NU_IDADE', ascending=True)
            valage = valage.reset_index()
            valage = valage.rename(columns={'ID_ALUNO': 'QUANTIDADE DE ALUNOS' })
            valage = valage.rename(columns={'NU_IDADE':'IDADE'})
            valage = valage.astype(int)
            st.write(valage)

            st.write('') 
            st.markdown('###### Dados relativos à idade, organizados por frequência.')

            valage1 = df_adm.filter(items=['ID_ALUNO', 'NU_IDADE']).groupby('NU_IDADE')\
                .count().sort_values(by='ID_ALUNO', ascending=False)
            valage1 = valage1.reset_index()
            valage1 = valage1.rename(columns={'ID_ALUNO': 'QUANTIDADE DE ALUNOS' })
            valage1 = valage1.rename(columns={'NU_IDADE':'IDADE'})
            valage1 = valage1.astype(int)
            st.write(valage1)

            ### Descrição dos alunos, por portabilidade de deficiência. ###
            st.write('')  
            st.write('')  
            st.subheader('Dados relativos à portabilidade de deficiência')
            st.write('')  
            st.write('')  

            # Gráfico:
            labels_d = ['Não', 'Sim', 'Não coletado']      
            values_d = [[df_adm['IN_DEFICIENCIA'].where(df_adm.IN_DEFICIENCIA == 'Não').count(),\
                df_adm['IN_DEFICIENCIA'].where(df_adm.IN_DEFICIENCIA == 'Sim').count(),\
                    df_adm['IN_DEFICIENCIA'].where(df_adm.IN_DEFICIENCIA == 'Não coletado').count()]]

            data_d = pd.DataFrame(values_d, columns=['Não', 'Sim', 'Não coletado'])

            colors_list = ['#4fa280', '#564fa2','#f2a132']

            result_pct = data_d.div(data_d.sum(1), axis=0)

            axd = result_pct.plot(kind='bar',figsize=(16,10),width = 0.6,color = colors_list,edgecolor=None)
            plt.legend(labels=data_d.columns,fontsize= 14)
            plt.suptitle('Taxa percentual de alunos, por portabilidade de deficiência', size=22)

            plt.xticks(fontsize=14)
            for spine in plt.gca().spines.values():
                spine.set_visible(False)
            plt.yticks([])

            for p in axd.patches:
                width = p.get_width()
                height = p.get_height()
                x, y = p.get_xy() 
                axd.annotate('{:.00001%}'.format(height), (p.get_x()+.5*width, p.get_y() + height + 0.01), ha = 'center')

            axd.set_xlabel('Portabilidade de deficiência')

            st.pyplot(plt) 
            plt.clf()

            st.write('')  

            valdef = df_adm.filter(items=['ID_ALUNO', 'IN_DEFICIENCIA']).groupby('IN_DEFICIENCIA').count().sort_values(by='ID_ALUNO', ascending=False)
            valdef = valdef.reset_index()
            valdef = valdef.rename(columns={'ID_ALUNO': 'Quantidade de alunos' })
            valdef = valdef.rename(columns={'IN_DEFICIENCIA': 'Portabilidade de deficiência'})
            st.table(valdef)

            
        elif uf_select != 'Todas opções' and adm_select == 'Todas opções':
            df_uf = dataframe.filter(items=['TP_COR_RACA', 'TP_SEXO','NU_IDADE', 'IN_DEFICIENCIA', 'NO_IES', 'TP_CATEGORIA_ADMINISTRATIVA', 'ID_ALUNO', "CO_IES",'CO_UF', 'UF'])\
                .where(dataframe.UF == uf_select).dropna()

            ### Descrição dos alunos, por raça ou cor. ###
            st.write('')  
            st.write('')  
            st.subheader('Dados relativos à raça ou cor')
            st.write('')  
            st.write('')  
            # Gráfico
            axr = df_uf.filter(items=['ID_ALUNO', 'TP_COR_RACA']).groupby('TP_COR_RACA').count().sort_values(by='ID_ALUNO', ascending=False)\
                .plot.barh(figsize=(16,10), colormap='jet', edgecolor = 'black', width = 0.8)
            axr.get_legend().remove()
            plt.suptitle('Taxa de distribuição de alunos, por raça ou cor', size=25)
            axr.set_xlabel("Quantidade de alunos")
            axr.set_ylabel('Cor ou raça')

            st.pyplot(plt) 
            plt.clf()

            st.write('')  

            labels_r = ['Amarela', 'Branca','Indígena', 'Parda', 'Preta', 'Não coletado', 'Não declarado']
            values_r = [[df_uf['TP_COR_RACA'].where(df_uf.TP_COR_RACA == 'Amarela').count(),\
                df_uf['TP_COR_RACA'].where(df_uf.TP_COR_RACA == 'Branca').count(),\
                    df_uf['TP_COR_RACA'].where(df_uf.TP_COR_RACA == 'Indígena').count(),\
                        df_uf['TP_COR_RACA'].where(df_uf.TP_COR_RACA == 'Parda').count(),\
                            df_uf['TP_COR_RACA'].where(df_uf.TP_COR_RACA == 'Preta').count(),\
                                df_uf['TP_COR_RACA'].where(df_uf.TP_COR_RACA == 'Não coletado').count(),\
                                    df_uf['TP_COR_RACA'].where(df_uf.TP_COR_RACA == 'Não declarado').count()]]

            data_r = pd.DataFrame(values_r, columns=labels_r) 
            result_pct = data_r.div(data_r.sum(1), axis=0) 
            ax = result_pct.plot(kind='bar',figsize=(16,10),width = 0.8,edgecolor=None)

            plt.legend(labels=data_r.columns,fontsize= 14)
            plt.suptitle('Taxa percentual de alunos, por raça ou cor', size=22)
            plt.xticks(fontsize=14)
            for spine in plt.gca().spines.values():
                spine.set_visible(False)
            plt.yticks([])

            for p in ax.patches:
                width = p.get_width()
                height = p.get_height()
                x, y = p.get_xy() 
                ax.annotate('{:.00001%}'.format(height), (p.get_x()+.5*width, p.get_y() + height + 0.01), ha = 'center')

            ax.set_xlabel('Cor ou Raça')
            st.pyplot(plt) 
            plt.clf()

            # Valores raça
            st.write('')  

            valr = df_uf.filter(items=['ID_ALUNO', 'TP_COR_RACA']).groupby('TP_COR_RACA')\
                .count().sort_values(by='ID_ALUNO', ascending=False)
            valr= valr.reset_index()
            valr = valr.rename(columns={'ID_ALUNO': 'Quantidade de alunos'})
            valr = valr.rename(columns={'TP_COR_RACA': 'Cor ou raça' })
            st.table(valr)

            ### Descrição dos alunos, por gênero. ###
            st.write('')  
            st.write('')  
            st.subheader('Dados relativos à gênero')
            st.write('')  
            st.write('')  

            # Gráfico:
            labels_g = ['Feminino', 'Masculino']
            values_g = [df_uf['TP_SEXO'].where(df_uf.TP_SEXO == 'Feminino').count(), df_uf['TP_SEXO'].where(df_uf.TP_SEXO == 'Masculino').count()]
            colors = ['blueviolet','orange']
            fig, axg = plt.subplots(figsize=(16,10))
            axg.pie(values_g, autopct='%1.1f%%', startangle=60, colors=colors)
            fig.suptitle('Taxa percentual de alunos, por gênero', size=25)
            
            text = 'O Censo da Educação Superior coletou apenas gêneros binários.'
            axg.text(0.27, 1.0, text, transform=axg.transAxes, fontsize=16)

            #draw circle
            centre_circle = plt.Circle((0,0),0.70,fc='white')
            fig = plt.gcf()

            axg.axis('equal')
            plt.tight_layout()
            plt.legend(labels=labels_g)
            st.pyplot(plt) 
            plt.clf()

            st.write('')  

            valg = df_uf.filter(items=['ID_ALUNO', 'TP_SEXO']).groupby('TP_SEXO')\
                .count().sort_values(by='ID_ALUNO', ascending=False)

            valg= valg.reset_index()
            valg = valg.rename(columns={'ID_ALUNO': 'Quantidade de alunos' })
            valg = valg.rename(columns={'TP_SEXO': 'Gênero' })
            st.table(valg)


            ### Descrição dos alunos, por idade. ###
            st.write('')  
            st.write('')  
            st.subheader('Dados relativos à idade')
            st.write('')  
            st.write('')  

            # Gráfico:
            axi= df_uf.filter(items=['ID_ALUNO', 'NU_IDADE']).groupby('NU_IDADE').count().plot(figsize=(20,10), colormap='PiYG_r') 

            axi.get_legend().remove()
            axi.set_ylabel('Quantidade de alunos')
            axi.set_xlabel('Idade')
            plt.suptitle('Taxa de distribuição de alunos, por idade', size=25)

            ticks = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110]
            plt.xticks(ticks, ticks)

            st.pyplot(plt) 
            plt.clf()

            st.write('')  
            st.markdown('###### Dados relativos à idade, organizados por ordem de valor (Rol).')
            
            valage = df_uf.filter(items=['ID_ALUNO', 'NU_IDADE']).groupby('NU_IDADE')\
                .count().sort_values(by='NU_IDADE', ascending=True)
            valage = valage.reset_index()
            valage = valage.rename(columns={'ID_ALUNO': 'QUANTIDADE DE ALUNOS' })
            valage = valage.rename(columns={'NU_IDADE':'IDADE'})
            valage = valage.astype(int)
            st.write(valage)

            st.write('')  
            st.markdown('###### Dados relativos à idade, organizados por frequência.')
            
            valage1 = df_uf.filter(items=['ID_ALUNO', 'NU_IDADE']).groupby('NU_IDADE')\
                .count().sort_values(by='ID_ALUNO', ascending=False)
            valage1 = valage1.reset_index()
            valage1 = valage1.rename(columns={'ID_ALUNO': 'QUANTIDADE DE ALUNOS' })
            valage1 = valage1.rename(columns={'NU_IDADE':'IDADE'})
            valage1 = valage1.astype(int)
            st.write(valage1)

            #####################################################################################################

            st.write('') 
            st.write('') 
            st.subheader("Dados relativos à portabilidade de deficiência")
            st.write('') 
            st.write('') 

            # Gráfico:
            labels_d = ['Não', 'Sim', 'Não coletado']      
            values_d = [[df_uf['IN_DEFICIENCIA'].where(df_uf.IN_DEFICIENCIA == 'Não').count(),\
                df_uf['IN_DEFICIENCIA'].where(df_uf.IN_DEFICIENCIA == 'Sim').count(),\
                    df_uf['IN_DEFICIENCIA'].where(df_uf.IN_DEFICIENCIA == 'Não coletado').count()]]

            data_d = pd.DataFrame(values_d, columns=['Não', 'Sim', 'Não coletado'])

            colors_list = ['#4fa280', '#564fa2','#f2a132']

            result_pct = data_d.div(data_d.sum(1), axis=0)

            axd = result_pct.plot(kind='bar',figsize=(16,10),width = 0.6,color = colors_list,edgecolor=None)
            plt.legend(labels=data_d.columns,fontsize= 14)
            plt.suptitle('Taxa percentual de alunos, por portabilidade de deficiência', size=22)

            plt.xticks(fontsize=14)
            for spine in plt.gca().spines.values():
                spine.set_visible(False)
            plt.yticks([])

            for p in axd.patches:
                width = p.get_width()
                height = p.get_height()
                x, y = p.get_xy() 
                axd.annotate('{:.00001%}'.format(height), (p.get_x()+.5*width, p.get_y() + height + 0.01), ha = 'center')

            axd.set_xlabel('Portabilidade de deficiência')
            st.pyplot(plt) 
            plt.clf()

            st.write('') 

            valdef = df_uf.filter(items=['ID_ALUNO', 'IN_DEFICIENCIA']).groupby('IN_DEFICIENCIA').count().sort_values(by='ID_ALUNO', ascending=False)
            valdef = df_uf.reset_index()
            valdef = df_uf.rename(columns={'ID_ALUNO': 'Quantidade de alunos' })
            valdef = df_uf.rename(columns={'IN_DEFICIENCIA': 'Portabilidade de deficiência'})
            st.table(valdef)


        elif uf_select == 'Todas opções' and adm_select == 'Todas opções':
            st.write('') 
            st.write('') 
            st.subheader('Dados relativos à raça ou cor')
            st.write('') 
            st.write('') 

            axr = dataframe.filter(items=['ID_ALUNO', 'TP_COR_RACA']).groupby('TP_COR_RACA').count().sort_values(by='ID_ALUNO', ascending=False)\
                    .plot.barh(figsize=(16,10), width = 0.8, colormap='jet', edgecolor = 'black')
            axr.get_legend().remove()
            axr.set_title('Taxa de distribuição de alunos, por cor ou raça', fontsize='25')
            axr.set_xlabel("Quantidade de alunos")
            axr.set_ylabel('Cor ou raça')
        
            st.pyplot(plt) 
            plt.clf()

            st.write('') 

            labels_r = ['Amarela', 'Branca','Indígena', 'Parda', 'Preta', 'Não coletado', 'Não declarado']
            values_r = [[dataframe['TP_COR_RACA'].where(dataframe.TP_COR_RACA == 'Amarela').count(),\
                dataframe['TP_COR_RACA'].where(dataframe.TP_COR_RACA == 'Branca').count(),\
                    dataframe['TP_COR_RACA'].where(dataframe.TP_COR_RACA == 'Indígena').count(),\
                        dataframe['TP_COR_RACA'].where(dataframe.TP_COR_RACA == 'Parda').count(),\
                            dataframe['TP_COR_RACA'].where(dataframe.TP_COR_RACA == 'Preta').count(),\
                                dataframe['TP_COR_RACA'].where(dataframe.TP_COR_RACA == 'Não coletado').count(),\
                                    dataframe['TP_COR_RACA'].where(dataframe.TP_COR_RACA == 'Não declarado').count()]]

            data_r = pd.DataFrame(values_r, columns=['Amarela', 'Branca','Indígena', 'Parda', 'Preta', 'Não coletado', 'Não declarado']) 

            result_pct = data_r.div(data_r.sum(1), axis=0)
            ax = result_pct.plot(kind='bar',figsize=(16,10),width = 0.8,edgecolor=None)
            plt.legend(labels=data_r.columns,fontsize= 14)
            plt.suptitle('Taxa percentual de alunos, por cor ou raça', size=22)

            plt.xticks(fontsize=14)
            for spine in plt.gca().spines.values():
                spine.set_visible(False)
            plt.yticks([])

            for p in ax.patches:
                width = p.get_width()
                height = p.get_height()
                x, y = p.get_xy() 
                ax.annotate('{:.00001%}'.format(height), (p.get_x()+.5*width, p.get_y() + height + 0.01), ha = 'center')

            ax.set_xlabel('Cor ou Raça')
            st.pyplot(plt) 
            plt.clf()

            st.write('') 
            
            valr = dataframe.filter(items=['ID_ALUNO', 'TP_COR_RACA']).groupby('TP_COR_RACA')\
                .count().sort_values(by='ID_ALUNO', ascending=False)
            valr= valr.reset_index()
            valr = valr.rename(columns={'ID_ALUNO': 'Quantidade de alunos'})
            valr = valr.rename(columns={'TP_COR_RACA': 'Cor ou raça' })
            st.table(valr)

            ##############################################################################################################
            st.write('') 
            st.write('') 
            st.subheader('Dados relativos à gênero')
            st.write('') 
            st.write('') 

            labels_g = ['Feminino', 'Masculino']
            values_g = [dataframe['TP_SEXO'].where(dataframe.TP_SEXO == 'Feminino').count(), dataframe['TP_SEXO'].where(dataframe.TP_SEXO == 'Masculino').count()]
            
            colors = ['blueviolet','orange']
            fig, axg = plt.subplots(figsize=(16,10))
            axg.pie(values_g, autopct='%1.1f%%', shadow=False, startangle=60, colors=colors) 
            fig.suptitle('Taxa percentual de alunos, por gênero', size=25)


            text = 'O Censo da Educação Superior coletou apenas gêneros binários.'
            axg.text(0.27, 1.0, text, transform=axg.transAxes, fontsize=16)             

            #draw circle
            centre_circle = plt.Circle((0,0),0.70,fc='white')
            fig = plt.gcf()

            axg.axis('equal')
            plt.tight_layout()
            plt.legend(labels=labels_g)
            st.pyplot(plt) 
            plt.clf()

            st.write('') 

            valg = dataframe.filter(items=['ID_ALUNO', 'TP_SEXO']).groupby('TP_SEXO')\
                .count().sort_values(by='ID_ALUNO', ascending=False)

            valg= valg.reset_index()
            valg = valg.rename(columns={'ID_ALUNO': 'Quantidade de alunos' })
            valg = valg.rename(columns={'TP_SEXO': 'Gênero' })
            st.table(valg)


            ############################################################################################################################
            st.write('') 
            st.write('') 
            st.subheader('Dados relativos à idade')
            st.write('') 
            st.write('') 
            axi= dataframe.filter(items=['ID_ALUNO', 'NU_IDADE']).groupby('NU_IDADE').count().plot(figsize=(20,10), colormap='PiYG_r')   
            axi.get_legend().remove()

            axi.set_ylabel('Quantidade de alunos')
            axi.set_xlabel('Idade')
            plt.suptitle('Taxa de distribuição de alunos, por idade', size=25)
            ticks = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110]
            plt.xticks(ticks, ticks)
            
            st.pyplot(plt) 
            plt.clf()

            st.write('') 
            st.markdown('###### Dados relativos à idade, organizados por ordem de valor (Rol).')  

            valage = dataframe.filter(items=['ID_ALUNO', 'NU_IDADE']).groupby('NU_IDADE')\
                .count().sort_values(by='NU_IDADE', ascending=True)
            valage = valage.reset_index()
            valage = valage.rename(columns={'ID_ALUNO': 'QUANTIDADE DE ALUNOS' })
            valage = valage.rename(columns={'NU_IDADE':'IDADE'})
            valage = valage.astype(int)
            st.write(valage)

            st.write('') 
            st.markdown('###### Dados relativos à idade, organizados por frequência.')
            
            valage1 = dataframe.filter(items=['ID_ALUNO', 'NU_IDADE']).groupby('NU_IDADE')\
                .count().sort_values(by='ID_ALUNO', ascending=False)
            valage1 = valage1.reset_index()
            valage1 = valage1.rename(columns={'ID_ALUNO': 'QUANTIDADE DE ALUNOS' })
            valage1 = valage1.rename(columns={'NU_IDADE':'IDADE'})
            valage1 = valage1.astype(int)
            st.write(valage1)


            ######################################################################################################
            st.write('') 
            st.write('') 
            st.subheader('Dados relativos à portabilidade de deficiência')
            st.write('') 
            st.write('') 
            
            labels_d = ['Não', 'Sim', 'Não coletado']
            values_d = [[dataframe['IN_DEFICIENCIA'].where(dataframe.IN_DEFICIENCIA == 'Não')\
                .count(), dataframe['IN_DEFICIENCIA'].where(dataframe.IN_DEFICIENCIA == 'Sim')\
                    .count(), dataframe['IN_DEFICIENCIA'].where(dataframe.IN_DEFICIENCIA == 'Não coletado').count()]]

            data_d = pd.DataFrame(values_d, columns=['Não', 'Sim', 'Não coletado'])

            colors_list = ['#4fa280', '#564fa2','#f2a132']

            result_pct = data_d.div(data_d.sum(1), axis=0)

            axd = result_pct.plot(kind='bar',figsize=(16,10),width = 0.6,color = colors_list,edgecolor=None)
            plt.legend(labels=data_d.columns,fontsize= 14)
            plt.suptitle('Taxa percentual de alunos, por portabilidade de deficiência', size=22)

            plt.xticks(fontsize=14)
            for spine in plt.gca().spines.values():
                spine.set_visible(False)
            plt.yticks([])
            x, y = p.get_xy() 

            for p in axd.patches:
                width = p.get_width()
                height = p.get_height()
                axd.annotate('{:.00001%}'.format(height), (p.get_x()+.5*width, p.get_y() + height + 0.01), ha = 'center')

            axd.set_xlabel('Portabilidade de deficiência')
            st.pyplot(plt) 
            plt.clf()

            st.write('') 
            valdef = dataframe.filter(items=['ID_ALUNO', 'IN_DEFICIENCIA']).groupby('IN_DEFICIENCIA').count().sort_values(by='ID_ALUNO', ascending=False)
            valdef = valdef.reset_index()
            valdef = valdef.rename(columns={'ID_ALUNO': 'Quantidade de alunos' })
            valdef = valdef.rename(columns={'IN_DEFICIENCIA': 'Portabilidade de deficiência'})
            st.table(valdef)
