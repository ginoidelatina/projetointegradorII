
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('tableau-colorblind10')
import s3fs
import os

import matplotlib.patches as mpatches
import pylab as plb
import dask.dataframe as dd
plb.rcParams['font.size'] = 20

# Carregando o arquivo csv.x
@st.cache(allow_output_mutation=True)
def load_data():
    df = dd.read_parquet('s3://pi01.microdadoscensosuperior2019/censo.parquetNO_CO')
    data_estado = pd.read_csv("s3://pi01.microdadoscensosuperior2019/Estados.csv",sep="|", encoding= "ISO-8859-1") 
    return df, data_estado

# Campos selecionados pelo usuário.
def userSelect(dataframe, uf_select, adm_select, research_ies):
    dataframe = dataframe
    dic_TP_CATEGORIA_ADMINISTRATIVA = {
    'Pública Federal':1,
    'Pública Estadual':2,
    'Pública Municipal':3,
    'Privada com fins lucrativos':4,
    'Privada sem fins lucrativos':5,
    'Especial':7}

    if uf_select == 'Todas opções' and adm_select == 'Todas opções':
        df = dataframe.drop(columns = ['TP_CATEGORIA_ADMINISTRATIVA', 'UF', 'NO_IES']) 
        return df
    if uf_select == 'Todas opções' and adm_select != 'Todas opções':
        df = dataframe.loc[dataframe.TP_CATEGORIA_ADMINISTRATIVA == dic_TP_CATEGORIA_ADMINISTRATIVA[adm_select]]
        df = df.drop(columns = ['TP_CATEGORIA_ADMINISTRATIVA', 'UF', 'NO_IES']) # tira o 'TP_CATEGORIA_ADMINISTRATIVA'?
        return df

    if uf_select != 'Todas opções' and adm_select == 'Todas opções':
        if research_ies == 'Não':
            df = dataframe.loc[dataframe.UF == uf_select]
            df = df.drop(columns = ['TP_CATEGORIA_ADMINISTRATIVA', 'UF', 'NO_IES'])
            return df
        if research_ies == 'Sim':
            df_temp = dataframe[['NO_IES', 'UF']].where(dataframe.UF == uf_select).dropna()
            df_temp = df_temp.compute()
            nome_ies = df_temp['NO_IES'].unique()
            nome_ies = nome_ies.tolist()
            nome_ies.sort()
            nome_ies.insert(0,'')
            nome_ies_select = ''
            del df_temp
            nome_ies_select = st.selectbox('Selecione o nome da instituição', options = nome_ies, key = 'ies04')
            if nome_ies_select != '':
                df = dataframe.loc[dataframe.UF == uf_select]
                df = df.loc[df.NO_IES == nome_ies_select ]
                df = df.drop(columns = ['TP_CATEGORIA_ADMINISTRATIVA', 'UF', 'NO_IES'])
                return df
    
    if uf_select != 'Todas opções' and adm_select != 'Todas opções':
        if research_ies == 'Não':
            df = dataframe.loc[dataframe.UF == uf_select]
            df = df.loc[df.TP_CATEGORIA_ADMINISTRATIVA == dic_TP_CATEGORIA_ADMINISTRATIVA[adm_select]]
            df = df.drop(columns = ['TP_CATEGORIA_ADMINISTRATIVA', 'UF', 'NO_IES'])
            return df

        if research_ies == 'Sim':
            df_temp = dataframe[['NO_IES', 'UF', 'TP_CATEGORIA_ADMINISTRATIVA']].where(dataframe.UF == uf_select).dropna()  
            df_temp = df_temp[['NO_IES', 'TP_CATEGORIA_ADMINISTRATIVA']].where(dataframe.TP_CATEGORIA_ADMINISTRATIVA == dic_TP_CATEGORIA_ADMINISTRATIVA[adm_select]).dropna()
            df_temp = df_temp.compute()
            nome_ies = df_temp['NO_IES'].unique()
            nome_ies = nome_ies.tolist()
            nome_ies.sort()
            nome_ies.insert(0,'')
            nome_ies_select = ''
            del df_temp #### sera?
            nome_ies_select = st.selectbox('Selecione o nome da instituição', options = nome_ies, key = 'ies04')
            if nome_ies_select != '':
                df = dataframe.loc[dataframe.UF == uf_select]
                df = df.loc[df.TP_CATEGORIA_ADMINISTRATIVA == dic_TP_CATEGORIA_ADMINISTRATIVA[adm_select]]
                df = df.loc[df.NO_IES == nome_ies_select]
                df = df.drop(columns = ['TP_CATEGORIA_ADMINISTRATIVA', 'UF', 'NO_IES'])
                return df



# Plotagem dos dados
#@st.cache(suppress_st_warning=True)
def plotData(df1, options):

    pd.set_option('max_colwidth', 400)

    dataframe = df1.compute()
    if ('Cor ou raça' in options):
        
        st.write('') 
        st.subheader('Dados relativos à cor e raça')
        st.write('') 
 

        st.write('') 

        ############# GRAPH

        st.write('') 

        #with st.container():
        data_temp = dataframe[['ID_ALUNO', 'TP_COR_RACA']]
        columns_r = ['Não declarado', 'Branca','Preta', 'Parda', 'Amarela', 'Indígena', 'Não coletado'] #EEEEEEEEEEEEEEEIIIII
        values_r = [[data_temp['TP_COR_RACA'].where(data_temp.TP_COR_RACA == 0).count(),\
            data_temp['TP_COR_RACA'].where(data_temp.TP_COR_RACA == 1).count(),\
                data_temp['TP_COR_RACA'].where(data_temp.TP_COR_RACA == 2).count(),\
                    data_temp['TP_COR_RACA'].where(data_temp.TP_COR_RACA == 3).count(),\
                        data_temp['TP_COR_RACA'].where(data_temp.TP_COR_RACA == 4).count(),\
                            data_temp['TP_COR_RACA'].where(data_temp.TP_COR_RACA == 5).count(),\
                                data_temp['TP_COR_RACA'].where(data_temp.TP_COR_RACA == 9).count()]]

        data_r = pd.DataFrame(values_r, columns=columns_r) 
        result_pct = data_r.div(data_r.sum(1), axis=0)


        ax = result_pct.plot(kind='bar', figsize=(16,10),width = 2.0, edgecolor='black') #sharex=True, sharey=y
        

        bars = ax.patches
        hatches = ('//', '.', '*', 'o', '.O', 'xx','++')
        for bar, hatch in zip(bars, hatches):
            bar.set_hatch(hatch)
  
        plt.legend(labels=data_r.columns,fontsize= 'x-large')
        plt.suptitle('Taxa percentual de alunos, por cor ou raça', size=25)


        
        plt.xticks(fontsize=18) 
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

        del data_r, values_r, columns_r


        dic_cor_raca = {
        0:'Não declarado',
        1:'Branca',
        2:'Preta',
        3:'Parda',
        4:' Amarela',
        5:'Indígena',
        9:'Não coletado'}
        
        #dataframe.insert(1,'nameMapRC', [dic_cor_raca[resp] for resp in dataframe.TP_COR_RACA])  # 'no_TP_COR_RACA' -> nameMap
        
       # dataframe.insert(valr)
        data_temp['nameMapRC'] = [dic_cor_raca[resp] for resp in data_temp.TP_COR_RACA]
        valr = data_temp[['ID_ALUNO', 'nameMapRC']].groupby('nameMapRC')\
            .count().sort_values(by='ID_ALUNO', ascending=False)
        valr= valr.reset_index() # .reset_index(drop= true)?
        valr = valr.rename(columns={'ID_ALUNO': 'Quantidade de alunos'})
        valr = valr.rename(columns={'nameMapRC': 'Cor ou raça' })
        st.table(valr)

        del valr



    ##############################################################################################################
    if ('Gênero' in options):
       
        st.write('') 
        st.subheader('Dados relativos à gênero')
        st.write('') 

        st.write('') 

        ############# GRAPH

        st.write('') 

        data_temp = dataframe[['TP_SEXO', 'ID_ALUNO']]
        labels_g = ['Feminino', 'Masculino']
        values_g = [data_temp['TP_SEXO'].where(data_temp.TP_SEXO == 1).count(), data_temp['TP_SEXO'].where(data_temp.TP_SEXO == 2).count()]
        
        #colors = ['blueviolet','orange']
        fig, axg = plt.subplots(figsize=(16,10))
        axg.pie(values_g, autopct='%1.1f%%', shadow=False, startangle=60, pctdistance=0.5)  ####### shadow = False
        fig.suptitle('Taxa percentual de alunos, por gênero', size=25)

        
        fig = plt.gcf()

        axg.axis('equal')
        plt.tight_layout()
        plt.legend(labels=labels_g, fontsize = 'x-large')
        st.pyplot(plt) 
        plt.clf()

        del labels_g, values_g

        st.text('O Censo da Educação Superior coletou apenas gêneros binários.')

        st.write('') 

        ############# TABLE

        st.write('') 

        dic_genero = {
        1:'Feminino',
        2:'Masculino'}
        data_temp['nameMapGENERO'] = [dic_genero[resp] for resp in data_temp.TP_SEXO]  
        
        valr = data_temp[['ID_ALUNO', 'nameMapGENERO']].groupby('nameMapGENERO')\
            .count().sort_values(by='ID_ALUNO', ascending=False)
        valr= valr.reset_index()
        valr = valr.rename(columns={'ID_ALUNO': 'Quantidade de alunos'})
        valr = valr.rename(columns={'nameMapGENERO': 'Gênero'})
        st.table(valr)

        del valr

    ############################################################################################################################3
    if ('Idade' in options):

        st.write('') 
        st.subheader('Dados relativos à idade')
        st.write('') 

        st.write('') 

        ############# TABLE

        st.write('') 

        data_temp = dataframe[['ID_ALUNO', 'NU_IDADE']]
        axi= data_temp[['ID_ALUNO', 'NU_IDADE']].groupby('NU_IDADE').count()\
            .plot(figsize=(20,10)) #fillstyle = 'full'  ##### mudar para todos
        axi.get_legend().remove()

        axi.set_ylabel('Quantidade de alunos', fontsize = 18)
        axi.set_xlabel('Idade', fontsize = 18)
        plt.suptitle('Taxa de distribuição de alunos, por idade', size=25)
        ticks = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110]
        plt.xticks(ticks, ticks)
        
        st.pyplot(plt) 
        plt.clf()

        st.write('') 

        ############# TABLE

        st.write('') 

        st.write('') 

        col1, col2 = st.columns(spec=[10,10])
        with col1:
            st.markdown('Dados relativos à idade, organizados por ordem de valor (Rol).')  

            valage = data_temp[['ID_ALUNO', 'NU_IDADE']].groupby('NU_IDADE')\
                .count().sort_values(by='NU_IDADE', ascending=True)
            valage = valage.reset_index()
            valage = valage.astype(int) 

            st.write((pd.DataFrame({
                'QUANTIDADE DE ALUNOS': valage.ID_ALUNO,
                'IDADE' : valage.NU_IDADE})))

        with col2:
            st.markdown('Dados relativos à idade, organizados por frequência.')
            

            valage1 = data_temp[['ID_ALUNO', 'NU_IDADE']].groupby('NU_IDADE')\
                .count().sort_values(by='ID_ALUNO', ascending=False)
            valage1 = valage1.reset_index()
            valage1 = valage1.astype(int)
            
            st.write(pd.DataFrame({
                'QUANTIDADE DE ALUNOS': valage1.ID_ALUNO,
                'IDADE' : valage1.NU_IDADE}))
        del valage, valage1

            

            

    ######################################################################################################
    if ('Portabilidade de deficiência' in options):
        st.write('') 
        st.write('') 
        st.subheader('Dados relativos à portabilidade de deficiência')
        st.write('') 
        st.write('') 

        st.write('') 

        ############# GRAPH

        st.write('') 

        data_temp = dataframe[['ID_ALUNO', 'IN_DEFICIENCIA']]

        values_d = [[data_temp['IN_DEFICIENCIA'].where(data_temp.IN_DEFICIENCIA == 0).count(),\
            data_temp['IN_DEFICIENCIA'].where(data_temp.IN_DEFICIENCIA == 1).count(),\
                data_temp['IN_DEFICIENCIA'].where(data_temp.IN_DEFICIENCIA == 9).count()]]

        data_d = pd.DataFrame(values_d, columns=['Não', 'Sim', 'Não coletado'])

        result_pct = data_d.div(data_d.sum(1), axis=0)

        axd = result_pct.plot(kind='bar',figsize=(16,10),width = 1.0, edgecolor=None)

        bars = axd.patches
        hatches = ('//', '.', 'o')
        for bar, hatch in zip(bars, hatches):
            bar.set_hatch(hatch)


        plt.legend(labels=data_d.columns,fontsize= 'x-large')
        plt.suptitle('Taxa percentual de alunos, por portabilidade de deficiência', size=25)

        plt.xticks(fontsize=18)
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

        del values_d, data_d

        st.write('') 

        ############# TABLE

        st.write('') 

        dic_IN_DEF = {
        0:'Não',
        1:'Sim',
        9:'Não coletado'}

        ################

        dataframe['nameMapDEF'] = [dic_IN_DEF[resp] for resp in dataframe.IN_DEFICIENCIA]       
        valr = dataframe.filter(items=['ID_ALUNO', 'nameMapDEF']).groupby('nameMapDEF')\
                .count().sort_values(by='ID_ALUNO', ascending=False)
        valr= valr.reset_index()
        valr = valr.rename(columns={'ID_ALUNO': 'Quantidade de alunos'})
        valr = valr.rename(columns={'nameMapDEF': 'Portabilidade de deficiência' })
        st.table(valr)


        labels_d = ['pessoa com deficiência auditiva', 'pessoa com deficiência física', 'pessoa com deficiência intelectual',\
            'pessoa com deficiência múltipla','pessoa surda','pessoa com surdocegueira']
        
        values_d = [[dataframe['IN_DEFICIENCIA_AUDITIVA'].where(dataframe.IN_DEFICIENCIA_AUDITIVA == 1).count(),\
                            dataframe['IN_DEFICIENCIA_FISICA'].where(dataframe.IN_DEFICIENCIA_FISICA == 1).count(),\
                                dataframe['IN_DEFICIENCIA_INTELECTUAL'].where(dataframe.IN_DEFICIENCIA_INTELECTUAL == 1).count(),\
                                    dataframe['IN_DEFICIENCIA_MULTIPLA'].where(dataframe.IN_DEFICIENCIA_MULTIPLA == 1).count(),\
                                        dataframe['IN_DEFICIENCIA_SURDEZ'].where(dataframe.IN_DEFICIENCIA_SURDEZ == 1).count(),\
                                            dataframe['IN_DEFICIENCIA_SURDOCEGUEIRA'].where(dataframe.IN_DEFICIENCIA_SURDOCEGUEIRA == 1).count()]]
                         
        df1 = pd.DataFrame(values_d, columns=labels_d).dropna() 
        color_list = ['#d73027', '#fc8d59', '#fee090', '#91bfdb', '#4575b4', '#7bccc4']
        

        result_pct = df1.div(df1.sum(1), axis=0)
        ax = result_pct.plot(kind='bar',figsize=(16,10),width = 4.0, color = color_list, edgecolor='black', linewidth=1, linestyle='dashed') 
        
        bars = ax.patches
        hatches = ('//', '.', '*', 'o', '.O', 'xx','++')
        for bar, hatch in zip(bars, hatches):
            bar.set_hatch(hatch)

        plt.legend(labels=df1.columns,fontsize= 20, loc = 'upper right', bbox_to_anchor=(0.8, 0., 0.5, 1.0))
        plt.suptitle('Percentual de alunos com deficiência, transtorno global do desenvolvimento ou altas habilidades/superdotação', size=25)


        plt.xticks(fontsize=20)
        for spine in plt.gca().spines.values():
            spine.set_visible(False)
        plt.yticks([])

        for p in ax.patches:
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy() 
            ax.annotate('{:.00001%}'.format(height), (p.get_x()+.5*width, p.get_y() + height + 0.01), ha = 'center')

        st.pyplot(plt) 
        plt.clf()


        labels_d = ['pessoa com baixa visão', 'pessoa cega','pessoa com altas habilidades/superdotação', 'pessoa com autismo', 'pessoa com Síndrome de Asperger',\
            'pessoa com Síndrome de Rett', 'pessoa com Transtorno Desintegrativo da Infância']

        values_d = [[dataframe['IN_DEFICIENCIA_BAIXA_VISAO'].where(dataframe.IN_DEFICIENCIA_BAIXA_VISAO == 1).count(),\
            dataframe['IN_DEFICIENCIA_CEGUEIRA'].where(dataframe.IN_DEFICIENCIA_CEGUEIRA == 1).count(),\
                dataframe['IN_DEFICIENCIA_SUPERDOTACAO'].where(dataframe.IN_DEFICIENCIA_SUPERDOTACAO == 1).count(),\
                    dataframe['IN_TGD_AUTISMO'].where(dataframe.IN_TGD_AUTISMO == 1).count(),\
                        dataframe['IN_TGD_SINDROME_ASPERGER'].where(dataframe.IN_TGD_SINDROME_ASPERGER == 1).count(),\
                            dataframe['IN_TGD_SINDROME_RETT'].where(dataframe.IN_TGD_SINDROME_RETT == 1).count(),
                                 dataframe['IN_TGD_TRANSTOR_DESINTEGRATIVO'].where(dataframe.IN_TGD_TRANSTOR_DESINTEGRATIVO == 1).count()]]

        df1 = pd.DataFrame(values_d, columns=labels_d).dropna()

        color_list = ['#d73027', '#fc8d59', '#fee090', '#91bfdb', '#4575b4', '#bae4bc', '#7bccc4']

        result_pct = df1.div(df1.sum(1), axis=0)
        ax = result_pct.plot(kind='bar',figsize=(16,10),width = 4.0, color = color_list, edgecolor='black', linewidth=1, linestyle='dashed') 

        bars = ax.patches
        hatches = ('//', '.', '*', 'o', '.O', 'xx','++', '|', '-')
        for bar, hatch in zip(bars, hatches):
            bar.set_hatch(hatch)

        plt.legend(labels=df1.columns,fontsize= 20, loc = 'upper right', bbox_to_anchor=(0.8, 0., 0.5, 1.0))

        plt.xticks(fontsize=20) 
        for spine in plt.gca().spines.values():
            spine.set_visible(False)
        plt.yticks([])

        for p in ax.patches:
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy() 
            ax.annotate('{:.00001%}'.format(height), (p.get_x()+.5*width, p.get_y() + height + 0.01), ha = 'center')

        st.pyplot(plt) 
        plt.clf()

        del values_d, labels_d,df1


        st.text(""" Os nomes dos atributos das legendas acima seguem a descrição do Censo da Educação Superior do Inep.
        Por esse motivo algumas nomenclaturas e definições podem estar desatualizadas. """)


 ###################################################################################################################################
    


    

# Exibição da página
def main():

    dataframeBruto, data_estado = load_data()

    st.title('Infográficos do Censo da Educação Superior no Brasil')  
    st.markdown('**Hospedagem da base de dados utilizada** -> https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior ')

    st.write('') 
    st.write('')

    st.markdown("Esta página web tem como objetivo partilhar análises descritas sobre o acesso à Educação Superior no Brasil, "
                "por meio de atributos sociais relativos à raça ou cor, gênero, idade e portabilidade de deficiência. " 
                "Em face da perspectiva de utilização de infográficos interativos, compreende-se que poderemos facilitar "
                "o fomento de questionamentos sobre a questão de inclusão no ensino superior."
                )
    st.markdown(" A criação deste site é consequência da pesquisa desenvolvida para realização do Projeto Integrador, "
                "disciplina da Universidade Virtual do Estado de São Paulo (UNIVESP), bem como, do desejo de facilitar a "
                 "obtenção de infográficos que descrevem os aspectos sociais relacionados ao acesso à educação superior. "
                 )

    

    st.markdown("Por último, para este projeto utilizamos a otimização de mapas de cores levando em consideração a deficiência "
                "de visão de cores para permitir a interpretação mais precisa dos infográficos. Para tornar a visualização de " 
                "dados mais amigáveis e acessíveis,também aplicamos diferentes formas/marcadores para pontos de dados (círculos, "
                "estrelas, quadrados...), bem como diferentes estilos de linhas (linhas sólidas, tracejadas, pontilhadas). "
                "Aproveitem os dados disponibilizados. Em breve estaremos publicando análises mais detalhadas e, também, novos " 
                "modelos para manipulação e visualização de dados. ")
    
    st.write('') 
    st.write('')


    st.subheader('Buscar infográficos')

    uf = data_estado['UF'].unique()
    uf = uf.tolist()
    uf.sort()
    uf.insert(0,'')
    uf.insert(1,'Todas opções')
    uf_select = st.selectbox('Selecione a Unidade Federativa', options = uf, key='uf01')

    adm_select = st.selectbox('Selecione o tipo de categoria administrativa',\
        options= ['','Todas opções', 'Pública Federal', 'Pública Estadual', 'Pública Municipal', 'Privada com fins lucrativos', 'Privada sem fins lucrativos', 'Especial'], key='adm02')
    if uf_select != '' and adm_select != '':
        if uf_select == 'Todas opções' and adm_select == 'Todas opções':
            options = st.multiselect('Escolha os atributos de interesse para a geração de infográficos.',\
                ['Cor ou raça', 'Gênero', 'Idade', 'Portabilidade de deficiência'])
            if len(options) != 0:
                   datafiltred = userSelect(dataframeBruto, uf_select, adm_select, research_ies='Não')
                   plotData(datafiltred, options)

        if uf_select != 'Todas opções' or adm_select != 'Todas opções':
            options = st.multiselect('Escolha os atributos de interesse para a geração de infográficos.',\
                ['Cor ou raça', 'Gênero', 'Idade', 'Portabilidade de deficiência'])
            research_ies = st.selectbox("Buscar os resultados pelo nome da instituição", ['', 'Sim', 'Não'], key='rs03')
            if research_ies !='' and len(options) != 0:
                datafiltred = userSelect(dataframeBruto, uf_select, adm_select, research_ies)
                plotData(datafiltred, options)
main()
