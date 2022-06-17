
# -*- coding: utf-8 -*-
#quando a tabela for modificada e necessário modificar as chamadas dos campos em: criar pdf (2x pt e lingua) criar html legenda e sem legenda e na revisao de arquivos e campos

import os
import re
import unicodedata
import pandas as pd

def imprimelinha():
    print("----------------------------------------")

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

def listar_novas_colunas(dataframe):
    '''Retorna uma lista de novas colunas adicionadas no planilha original'''
    colunas_padrao = ["ID","ITEM_LEXICAL", "IMAGEM", "ARQUIVO_SONORO", "TRANSCRICAO_FONEMICA",	
                    "TRANSCRICAO_FONETICA",	"CLASSE_GRAMATICAL", "TRADUCAO_SIGNIFICADO",	
                    "DESCRICAO", "EXEMPLO_USO_ARQUIVO_SONORO", "TRANSCRICAO_EXEMPLO",
                    "TRADUCAO_EXEMPLO", "ARQUIVO_VIDEO", "CAMPO_SEMANTICO", "ITENS_RELACIONADOS"]
    colunas_df = list(dataframe.columns)
    novas_colunas = []
    if colunas_padrao != colunas_df:    # pegar possiveis colunas extras
        for i in colunas_df:
            if i not in colunas_padrao:
                novas_colunas.append(i)
    return novas_colunas

def listar_campos_semanticos(dataframe):
    '''Cria duas listas de campos semanticos:
    primeira: lista padrão com os campos semânticos do jeito que estão no csv
    segunda: lista de campos semanticos normalizada e sem acento para criar os arquivos "RMD" com nomeclatura correta.
    '''
    campos_semanticos = []
    campos_semanticos_normalizado = []
    for i in dataframe.index:  # criar a lista de campos semanticos para gerar os arquivos RMD
        campo_semantico = dataframe['CAMPO_SEMANTICO'][i]
        if campo_semantico == '':
            print('Preencha o campo semântico do item: ' + dataframe['ITEM_LEXICAL'][i])
            resposta = 'n'
            while resposta != 's':
                resposta = input("para sair digite 's'? >")
                exit()
        if campo_semantico.capitalize() not in campos_semanticos:
            campos_semanticos.append(campo_semantico.capitalize())
            campos_semanticos_normalizado.append(
                strip_accents(campo_semantico.replace(' ', '-')))
    return campos_semanticos, campos_semanticos_normalizado

def cria_lista_dicionario(dataframe): 
    '''Retorna uma lista chamada dicionario com todos os itens do csv, cada item lexical 
    passa a ser um item no dicionario como uma lista individual'''
    dicionario = dataframe.values.tolist()
    dicionario_ordenado_lingua = sorted(dicionario, key = lambda x: x[1])
    dicionario_ordenado_pt = sorted(dicionario, key = lambda x: x[7])
    return dicionario_ordenado_pt, dicionario_ordenado_lingua

def cria_pdf(dataframe): 
    print("Digite o codigo da língua")
    codigolingua =  input(">")
    print("Digite o nome da lingua como deve figurar no documento")
    nomelingua =  input(">")
    print("Digite o nome do autor(es):")
    nomeautor =  input(">")   
    lista_portugues, lista_lingua = cria_lista_dicionario(dataframe)
    campos_semanticos, campos_semanticos_normalizado = listar_campos_semanticos(dataframe)
    novas_colunas = listar_novas_colunas(dataframe)
    if not os.path.exists(os.getcwd() + '/pdf/'): 
         os.makedirs(os.getcwd() + '/pdf/')
    
    #Escrever arquivo entrada PT
    id = 0
    arquivo = open(os.getcwd() + "/pdf/" + "PT-" + codigolingua + ".Rmd", mode="a+", encoding="utf-8")
    arquivo.write("# " + "Português - " + nomelingua+ "\n\n")
    for i in campos_semanticos_normalizado: #cria os rmds com entrada em portugues
        arquivo.write("\n\n## " + campos_semanticos[id])
        for item in lista_portugues:
            itemlexical = str(item[1]).replace("'", "\\'")
            imagem = item[2]
            transcricaofonemica = str(item[4]).replace("'", "\\'")
            transcricaofonetica = str(item[5]).replace("'", "\\'")
            classegramatical = item[6]
            significadopt = item[7]
            descricao = item[8]
            transcricaoexemplo = str(item[10]).replace("'", "\\'")
            traducaoexemplo = item[11]
            camposemantico = item[13]
            itensrelacionados = item[14]
            if camposemantico.capitalize() == campos_semanticos[id]:
                arquivo.write("\n\n\n\n" + "**" + significadopt.capitalize() + " — " + itemlexical + ".**" + '\n\n')   
                if transcricaofonemica == "":
                    arquivo.write(transcricaofonetica + " *")
                else:
                    arquivo.write(transcricaofonetica + " / " + transcricaofonemica + " *") 
                if classegramatical == "nome.m":
                    arquivo.write("substantivo, masculino*.\n")
                elif classegramatical == "nome.f":
                    arquivo.write("substantivo, feminino*.\n")
                elif classegramatical == "nome.n\n":
                    arquivo.write("substantivo, neutro*.\n")
                else:
                    arquivo.write(classegramatical + "*. ")
                if descricao != "":
                    arquivo.write(descricao + "\n")
                else:
                    arquivo.write("\n")
                if imagem != "":
                    for filename in os.listdir(os.getcwd() + "/foto"):
                        if filename == imagem:
                            arquivo.write("\n\n\n![](" + "foto/" + filename + "){width=180px}\n\n")
                            break
                if transcricaoexemplo != "":
                    arquivo.write("\nExemplo de uso:\n\n*" + transcricaoexemplo + ".*\n")
                if traducaoexemplo != "":
                    arquivo.write("\n" + traducaoexemplo + ".\n")
                if itensrelacionados != "":
                    arquivo.write("\n" + "Itens relacionados: "+ itensrelacionados + ".")
                cont = 14
                for nova_coluna in novas_colunas:
                    if item[cont] != "":
                        arquivo.write("\n\n" + item[cont] + ".\n")
                    cont += 1
        id += 1
    arquivo.close()

    #Escrever arquivo com entrada lingua
    id = 0
    arquivo = open(os.getcwd() + "/pdf/" +  codigolingua + "-PT" + ".Rmd", mode="a+", encoding="utf-8")
    arquivo.write("# " + nomelingua + " - Português" + "\n\n")
    for i in campos_semanticos_normalizado: #cria os rmds com entrada em portugues
        arquivo.write("\n\n## " + campos_semanticos[id])
        for item in lista_lingua:
            itemlexical = str(item[1]).replace("'", "\\'")
            imagem = item[2]
            transcricaofonemica = str(item[4]).replace("'", "\\'")
            transcricaofonetica = str(item[5]).replace("'", "\\'")
            classegramatical = item[6]
            significadopt = item[7]
            descricao = item[8]
            transcricaoexemplo = str(item[10]).replace("'", "\\'")
            traducaoexemplo = item[11]
            camposemantico = item[13]
            itensrelacionados = item[14]
            if camposemantico.capitalize() == campos_semanticos[id]:
                arquivo.write("\n\n\n\n" + "**" + itemlexical.capitalize() + " - " + significadopt+ ".**" + '\n\n')   
                if transcricaofonemica == "":
                    arquivo.write(transcricaofonetica + " *")
                else:
                    arquivo.write(transcricaofonetica + " / " + transcricaofonemica + " *") 
                if classegramatical == "nome.m":
                    arquivo.write("substantivo, masculino*.\n")
                elif classegramatical == "nome.f":
                    arquivo.write("substantivo, feminino*.\n")
                elif classegramatical == "nome.n\n":
                    arquivo.write("substantivo, neutro*.\n")
                else:
                    arquivo.write(classegramatical + "*. ")
                if descricao != "":
                    arquivo.write(descricao + "\n")
                else:
                    arquivo.write("\n")
                if imagem != "":
                    for filename in os.listdir(os.getcwd() + "/foto"):
                        if filename == imagem:
                            arquivo.write("\n\n\n![](" + "foto/" + filename + "){width=180px}\n\n")
                            break
                if transcricaoexemplo != "":
                    arquivo.write("\nExemplo de uso:\n\n*" + transcricaoexemplo + ".*\n")
                if traducaoexemplo != "":
                    arquivo.write("\n" + traducaoexemplo + ".\n")
                if itensrelacionados != "":
                    arquivo.write("\n" + "Itens relacionados: "+ itensrelacionados + ".")
                cont = 14
                for nova_coluna in novas_colunas:
                    if item[cont] != "":
                        arquivo.write("\n\n" + item[cont] + ".\n")
                    cont += 1
        id += 1
    arquivo.close()
    cria_pdf_yml()
    cria_output_yml_pdf()
    cria_preamble_tex()
    cria_css()
    cria_proj_book()
    cria_index_pdf(nomeautor, nomelingua)

def cria_html(dataframe):
    '''recebe um dataframe e cria os arquivos necessarios para produzir o html'''    
    print("Digite o nome da lingua como deve figurar no documento")
    nomelingua =  input(">")
    print("Digite o nome do autor(es) do documento")
    autor =  input(">")
    lista_portugues, lista_lingua = cria_lista_dicionario(dataframe)
    campos_semanticos, campos_semanticos_normalizado = listar_campos_semanticos(dataframe)
    novas_colunas = listar_novas_colunas(dataframe)
    if not os.path.exists(os.getcwd() + '/html/'): 
         os.makedirs(os.getcwd() + '/html/')
    #Escrever arquivo com entrada lingua
    id = 0
    for i in campos_semanticos_normalizado:  # cria os arquivos RMD com o titulo
        arquivo = open(os.getcwd() + "/html/"+ i + ".Rmd", mode="w+", encoding="utf-8")
        arquivo.write("---\n")
        arquivo.write('title: "Diciónario ' + nomelingua +'"\n')
        arquivo.write('author: "' + autor + '"\n')
        arquivo.write("---")
        for item in lista_lingua:
            itemlexical = str(item[1]).replace("'", "\\'")
            imagem = item[2]
            arquivosom = item[3]
            transcricaofonemica = str(item[4]).replace("'", "\\'")
            transcricaofonetica = str(item[5]).replace("'", "\\'")
            classegramatical = item[6]
            significadopt = item[7]
            descricao = item[8]
            arquivosomexemplo = item[9]
            transcricaoexemplo = str(item[10]).replace("'", "\\'")
            traducaoexemplo = item[11]
            arquivovideo = item[12]
            camposemantico = item[13]
            itensrelacionados = item[14]
            if camposemantico.capitalize() == campos_semanticos[id]:
                arquivo.write("\n\n\n\n"+ '<hr>\n' + "## " + itemlexical.capitalize() + " - " + significadopt+ '\n\n')   
                if transcricaofonemica == "":
                    arquivo.write(transcricaofonetica + " *")
                else:
                    arquivo.write(transcricaofonetica + " / " + transcricaofonemica + " *") 
                if classegramatical == "nome.m":
                    arquivo.write("substantivo, masculino*. ")
                    if descricao != "":
                        arquivo.write(descricao + "\n")
                    else:
                        arquivo.write("\n")
                elif classegramatical == "nome.f":
                    arquivo.write("substantivo, feminino*. ")
                    if descricao != "":
                        arquivo.write( descricao + "\n")
                    else:
                        arquivo.write("\n")
                elif classegramatical == "nome.n":
                    arquivo.write("substantivo, neutro*. ")
                    if descricao != "":
                        arquivo.write(descricao + "\n")
                    else:
                        arquivo.write("\n")
                else:
                    arquivo.write(classegramatical + "*. ")
                    if descricao != "":
                        arquivo.write(descricao + "\n")
                    else:
                        arquivo.write("\n")
                
                if arquivosom != "":
                    for filename in os.listdir(os.getcwd() + "/audio"):
                        if filename == arquivosom:
                            arquivo.write('\n<audio width="320" height="240" controls>\n  <source src="' + "audio/" + filename +'" type="audio/wav">\n</audio>')
                            break

                if imagem != "":
                    for filename in os.listdir(os.getcwd() + "/foto"):
                        if filename == imagem:
                            arquivo.write("\n\n\n![](" + "foto/" + filename + ")\n\n")
                            break
                if transcricaoexemplo != "":
                    arquivo.write("\nExemplo de uso:\n\n*" + transcricaoexemplo + ".*\n")
                if traducaoexemplo != "":
                    arquivo.write("\n" + traducaoexemplo + ".\n")
                

                if arquivovideo != "":
                    for filename in os.listdir(os.getcwd() + "/video"):
                        if filename == arquivovideo:
                            arquivo.write('\n<video width="320" height="240" controls preload="none">\n  <source src="' + "video/" + arquivovideo + '" type="video/mp4"></video><br>')
                            break
                    
                if arquivosomexemplo != "":
                    for filename in os.listdir(os.getcwd() + "/audio"):
                        if filename == arquivosomexemplo:
                            arquivo.write('\n<audio width="320" height="240" controls>\n  <source src="' + "audio/" +filename+'" type="audio/wav">\n</audio>')
                            break
                    
                
                if itensrelacionados != "":
                    arquivo.write("\n" + "Itens relacionados: "+ itensrelacionados + ".")
                cont = 14
                for nova_coluna in novas_colunas:
                    if item[cont] != "":
                        arquivo.write("\n\n" + item[cont] + ".\n")
                    cont += 1
        id += 1
    arquivo.close()
    cria_index()
    cria_site_yml(dataframe, nomelingua)
    cria_proj_site()
    cria_output_yml()

def cria_html_legenda(dataframe):
    '''recebe um dataframe e cria os arquivos necessarios para produzir o html''' 
    print("Digite o nome da lingua como deve figurar no documento")
    nomelingua =  input(">")
    print("Digite o nome do autor(es) do documento")
    autor =  input(">")   
    lista_portugues, lista_lingua = cria_lista_dicionario(dataframe)
    campos_semanticos, campos_semanticos_normalizado = listar_campos_semanticos(dataframe)
    novas_colunas = listar_novas_colunas(dataframe)
    if not os.path.exists(os.getcwd() + '/html/'): 
         os.makedirs(os.getcwd() + '/html/')
    #Escrever arquivo com entrada lingua
    id = 0
    for i in campos_semanticos_normalizado:  # cria os arquivos RMD com o titulo
        arquivo = open(os.getcwd() + "/html/"+ i + ".Rmd", mode="w+", encoding="utf-8")
        arquivo.write("---\n")
        arquivo.write('title: "Diciónario ' + nomelingua +'"\n')
        arquivo.write('author: "' + autor + '"\n')
        arquivo.write("---") 
        for item in lista_lingua:
            itemlexical = str(item[1]).replace("'", "\\'")
            imagem = item[2]
            arquivosom = item[3]
            transcricaofonemica = str(item[4]).replace("'", "\\'")
            transcricaofonetica = str(item[5]).replace("'", "\\'")
            classegramatical = item[6]
            significadopt = item[7]
            descricao = item[8]
            arquivosomexemplo = item[9]
            transcricaoexemplo = str(item[10]).replace("'", "\\'")
            traducaoexemplo = item[11]
            arquivovideo = item[12]
            camposemantico = item[13]
            itensrelacionados = item[14]
            if camposemantico.capitalize() == campos_semanticos[id]:
                arquivo.write("\n\n\n\n" + '<hr>\n' + "## " + itemlexical.capitalize() + " - " + significadopt+ '\n\n')   
                if transcricaofonemica == "":
                    arquivo.write(transcricaofonetica + " *")
                else:
                    arquivo.write(transcricaofonetica + " / " + transcricaofonemica + " *") 
                if classegramatical == "nome.m":
                    arquivo.write("substantivo, masculino*. ")
                    if descricao != "":
                        arquivo.write(descricao + "\n")
                    else:
                        arquivo.write("\n")
                elif classegramatical == "nome.f":
                    arquivo.write("substantivo, feminino*. ")
                    if descricao != "":
                        arquivo.write( descricao + "\n")
                    else:
                        arquivo.write("\n")
                elif classegramatical == "nome.n":
                    arquivo.write("substantivo, neutro*. ")
                    if descricao != "":
                        arquivo.write(descricao + "\n")
                    else:
                        arquivo.write("\n")
                else:
                    arquivo.write(classegramatical + "*. ")
                    if descricao != "":
                        arquivo.write(descricao + "\n")
                    else:
                        arquivo.write("\n")
                
                if arquivosom != "":
                    for filename in os.listdir(os.getcwd() + "/audio"):
                        if filename == arquivosom:
                            arquivo.write('\n<audio width="320" height="240" controls>\n  <source src="' + "audio/" + filename +'" type="audio/wav">\n</audio>')
                            arquivo.write("\n" + cria_legenda(arquivosom))
                            break
                    
                if imagem != "":
                    for filename in os.listdir(os.getcwd() + "/foto"):
                        if filename == imagem:
                            arquivo.write("\n\n\n![](" + "foto/" + filename + ")\n\n")
                            break
                if transcricaoexemplo != "":
                    arquivo.write("\nExemplo de uso:\n\n*" + transcricaoexemplo + ".*\n")
                if traducaoexemplo != "":
                    arquivo.write("\n" + traducaoexemplo + ".\n")
                

                if arquivovideo != "":
                    for filename in os.listdir(os.getcwd() + "/video"):
                        if filename == arquivovideo:
                            arquivo.write('\n<video width="320" height="240" controls preload="none">\n  <source src="' + "video/" + arquivovideo + '" type="video/mp4"></video><br>')
                            arquivo.write("\n" + cria_legenda(arquivovideo))
                            break
                    
                if arquivosomexemplo != "":
                    for filename in os.listdir(os.getcwd() + "/audio"):
                        if filename == arquivosomexemplo:
                            arquivo.write('\n<audio width="320" height="240" controls>\n  <source src="' + "audio/" +filename+'" type="audio/wav">\n</audio>')
                            arquivo.write("\n" + cria_legenda(arquivosomexemplo))
                            break
                    
                
                if itensrelacionados != "":
                    arquivo.write("\n" + "Itens relacionados: "+ itensrelacionados + ".")
                cont = 14
                for nova_coluna in novas_colunas:
                    if item[cont] != "":
                        arquivo.write("\n\n" + item[cont] + ".\n")
                    cont += 1
        id += 1
    arquivo.close()
    cria_index()
    cria_site_yml(dataframe, nomelingua)
    cria_proj_site()
    cria_output_yml()

def cria_legenda(filename):
    arquivoatores = os.path.join(os.getcwd(), "atores.csv")
    atoresrecuperado = []
    cont = 5
    while atoresrecuperado == [] and cont != 0:
        siglas = r'[-_][A-Za-z][A-Za-z][A-Za-z]*' * cont
        atoresrecuperado = re.findall(r'\d\d\d\d\d\d\d\d' + siglas,filename)
        cont -= 1
    if atoresrecuperado != []:
        atoresrecuperado = re.sub(r'\d\d\d\d\d\d\d\d',"",atoresrecuperado[0])
        atoresrecuperado = re.sub(r'[_-]'," ",atoresrecuperado)
        atoresrecuperado = atoresrecuperado.strip()
        atoresrecuperado = atoresrecuperado.split(" ")
    data = re.findall(r'\d\d\d\d',filename)
    if data == []:
        data = ["data não encontrada"]
    if atoresrecuperado == []:
        legenda = '<font size="1">'+ "(Falante não informado, " + data[0]+ ")" + '</font><br />'
        return str(legenda)
    try:
        dfatores = pd.read_csv(arquivoatores)
        dfatores = dfatores.fillna('')
        listaatores = dfatores.values.tolist()
    except (FileNotFoundError, IOError):
        legenda = '<font size="1">'+ "(Falante não informado, " + data[0]+ ")" +'</font><br />'
        return str(legenda)
    texto = ""
    for ator in atoresrecuperado:
        for dadosator in listaatores:
            if ator == dadosator[0]:
                texto = texto + dadosator[1] + ", "
    if texto == "":
        return '<font size="1">'+ "(Falante não informado, " + data[0]+ ")" + '</font><br />'
    return str('<font size="1">'+ "("+ texto + data[0] + ")" +'</font><br />')

def abrearquivo():## ABRIR O ARQUIVO
    arquivo = os.path.join(os.getcwd(), "dicionario.csv")
    try:
        df = pd.read_csv(arquivo)
        df = df.fillna('')
    except (FileNotFoundError, IOError):
        resposta = 'n'
        while resposta != 's':
            print("arquivo não encontrado, para sair digite 's'? Caminho não encontrado:" + arquivo)
            resposta = input(">")
        exit()
    else:
        print("Arquivo encontrado: " + arquivo)
    return df
 
def validacao_tabela_campos(dataframe):
    '''Recebe o dataframe e devolve arquivos 
    de texto contendo os campos vazios 
    da tabela e arquivos ausentes nas pastas'''
    #verificacão dos campos essenciais
    if not os.path.exists(os.getcwd() + '/audio/'): 
        os.makedirs(os.getcwd() + '/audio/')
    if not os.path.exists(os.getcwd() + '/video/'): 
        os.makedirs(os.getcwd() + '/video/')
    if not os.path.exists(os.getcwd() + '/foto/'): 
        os.makedirs(os.getcwd() + '/foto/')
    dicionario = dataframe.values.tolist()
    linha = 2
    preencher = []
    cont_itemlexical = 0
    cont_transcricaofonetica = 0
    cont_classegramatical = 0
    cont_significadopt  = 0
    cont_camposemantico = 0
    for item in dicionario:
        itemlexical = item[1]
        transcricaofonetica = item[5]
        classegramatical = item[6]
        significadopt = item[7]
        camposemantico = item[13]
        if itemlexical == "":
            preencher.append([linha, "ITEM_LEXICAL"])
            cont_itemlexical += 1
        if transcricaofonetica == "":
            preencher.append([linha, "TRANSCRICAO_FONETICA"])
            cont_transcricaofonetica += 1
        if classegramatical == "":
            preencher.append([linha, "CLASSE_GRAMATICAL"])
            cont_classegramatical += 1
        if significadopt == "":
            preencher.append([linha, "TRADUCAO_SIGNIFICADO"])
            cont_significadopt += 1
        if camposemantico == "":
            preencher.append([linha, "CAMPO_SEMANTICO"])
            cont_camposemantico += 1
        linha += 1  
    pendencias_linha = []
    pendencias = []
    linhas = []
    for pendencia in preencher:
        if pendencia[0]  not in linhas:
            linhas.append(pendencia[0])
    for linha in linhas:
        for pendencia in preencher:
            if pendencia[0] == linha:
                pendencias_linha.append(pendencia[1])
        pendencias.append([linha] + pendencias_linha)
        pendencias_linha = []
    if pendencias != []:
        with open('pendencias-campos.txt', 'a+') as arquivo:
            arquivo.write("arquivo: dicionario.csv\n") 
            arquivo.write("Itens Lexicais a preencher: " + str(cont_itemlexical) + "\n")
            arquivo.write("Transcrições fonéticas a preencher: " + str(cont_transcricaofonetica) + "\n")
            arquivo.write("Classes gramaticais a preencher: " + str(cont_classegramatical) + "\n")
            arquivo.write("Significados ou traduções a preencher: " + str(cont_significadopt) + "\n")
            arquivo.write("Campos semânticos a preencher: " + str(cont_camposemantico) + "\n")   
            arquivo.write("Pendências por linha:\n\n")   
            for pendencia in pendencias:
                linha = pendencia[0]
                texto = "Linha" + str(linha) + ": "
                elemento = 1
                for i in range(len(pendencia)-1):
                    texto = texto + pendencia[elemento] + " | "
                    elemento += 1
                arquivo.write(texto + "\n")
    #verificação dos arquivos
    for item in dicionario:
        arquivosom = item[2]
        arquivosomexemplo = item[7]
        arquivovideo = item[10]

def validacao_tabela_arquivos(dataframe):    
    '''Recebe o dataframe e verifica se os arquivos das pastas audio/video/foto especificados na planilha 
    estão na pasta'''            
    dicionario = dataframe.values.tolist() 
    listaarquivossom = []
    arquivosexemplo = []
    arquivosvideo = []
    arquivosimagem = []
    semimagem = 0
    semsom = 0
    semexemplo = 0
    semvideo = 0
    for item in dicionario:
        arquivosom = item[3]
        arquivoexemplo = item[9]
        arquivovideo = item[12]
        imagem = item[2]
        if arquivosom != "":
            listaarquivossom.append(arquivosom.lstrip())
        else:
            semsom += 1
        if arquivoexemplo != "":
            arquivosexemplo.append(arquivoexemplo.lstrip())
        else:
            semexemplo += 1
        if imagem != "":
            arquivosimagem.append(imagem.lstrip())
        else:
            semimagem += 1
        if arquivovideo != "":
            arquivosvideo.append(arquivovideo.lstrip())
        else:
            semvideo += 1
    with open('pendencias-arquivos.txt', 'a+') as arquivotexto:
        arquivotexto.write("Pendências em arquivos:\n")
        arquivotexto.write("Entradas sem imagem: " + str(semimagem) + "\n")
        arquivotexto.write("Entradas sem arquivo de som: " + str(semsom) + "\n")
        arquivotexto.write("Entradas sem arquivo de som de exemplo: " + str(semexemplo) + "\n")
        arquivotexto.write("Entradas sem arquivo de video: " + str(semvideo) + "\n")
        arquivotexto.write("Entradas sem arquivo de som: " + str(semsom) + "\n\n")
        arquivotexto.write("Se houverem pendências em relação aos arquivos contidos na tabela estão abaixo:\n")
        

        for roots, dirs, files in os.walk(os.path.join(os.getcwd(), "audio")):    
            arquivosnapasta = files
        if listaarquivossom != []:
            for arquivo in listaarquivossom:
                if arquivo not in arquivosnapasta:         
                        arquivotexto.write("Arquivo de som não encontrado: " +  arquivo + "\n")
        if arquivosexemplo != []:
            for arquivo in arquivosexemplo:
                if arquivo not in arquivosnapasta:         
                        arquivotexto.write("Arquivo de som de exemplo não encontrado: " +  arquivo + "\n")
        
        for roots, dirs, files in os.walk(os.path.join(os.getcwd(), "video")):    
            arquivosnapasta = files    
        if arquivosvideo != []:
            for arquivo in arquivosvideo:
                if arquivo not in arquivosnapasta:         
                        arquivotexto.write("Arquivo de video não encontrado: " +  arquivo + "\n")

        for roots, dirs, files in os.walk(os.path.join(os.getcwd(), "foto")):    
            arquivosnapasta = files  
        if arquivosimagem  != []:
            for arquivo in arquivosimagem :
                if arquivo not in arquivosnapasta:         
                        arquivotexto.write("Arquivo de imagem não encontrado: " +  arquivo + "\n")

#arquivos para o html

def cria_index():
    arquivo = open(os.getcwd() + "/html/" + "index.Rmd", mode="w+", encoding="utf-8")
    arquivo.write('''---
title: "Introdução"
output: html_document
---


        
        
        ''')
    arquivo.close
def cria_site_yml(dataframe, lingua):
    arquivo = open(os.getcwd() + "/html/" + "_site.yml", mode="w+", encoding="utf-8")
    arquivo.write('''    
name: my-website
output_dir: _site
navbar:\n''')
    arquivo.write('  title: "Dicionário ' + lingua + '"\n')  
    arquivo.write('''  left:
    - text: "Introdução"
      href: index.html\n''')
    campos, campos_norm = listar_campos_semanticos(dataframe)
    campos = sorted(campos)
    campos_norm = sorted(campos_norm)
    id = 0
    for campo in campos:
        arquivo.write('    - text: "'+ campo + '"\n')
        arquivo.write('      href: ' + campos_norm[id] + ".html\n")
        id += 1
    arquivo.close
def cria_output_yml():
    arquivo = open(os.getcwd() + "/html/" + "_output.yml", mode="w+", encoding="utf-8")
    arquivo.write('''html_document:
    theme: simplex
    highlight: tango
    toc: true
    toc_float: true''')
    arquivo.close
def cria_proj_site():
    arquivo = open(os.getcwd() + "/html/" + "site.Rproj", mode="w+", encoding="utf-8")
    arquivo.write('''Version: 1.0

RestoreWorkspace: Default
SaveWorkspace: Default
AlwaysSaveHistory: Default

EnableCodeIndexing: Yes
UseSpacesForTab: Yes
NumSpacesForTab: 2
Encoding: UTF-8

RnwWeave: Sweave
LaTeX: pdfLaTeX

BuildType: Website''')
    arquivo.close

#arquivos para o pdf

def cria_pdf_yml():
    arquivo = open(os.getcwd() + "/pdf/" + "_bookdown.yml", mode="w+", encoding="utf-8")
    arquivo.write('''delete_merged_file: true
language:
  label:
    chapter_name: "Capítulo"\n''')
    arquivo.close
def cria_output_yml_pdf():
    arquivo = open(os.getcwd() + "/pdf/" + "_output.yml", mode="w+", encoding="utf-8")
    arquivo.write('''bookdown::pdf_document2:
  latex_engine: lualatex
  pandoc_args: ["-V", "classoption=twocolumn"]
  includes:
    in_header: preamble.tex''')
    arquivo.close
def cria_css():
    arquivo = open(os.getcwd() + "/pdf/" + "style.css", mode="w+", encoding="utf-8")
    arquivo.write('''p.caption {
  color: #777;
  margin-top: 10px;
}
p code {
  white-space: inherit;
}
pre {
  word-break: normal;
  word-wrap: normal;
}
pre code {
  white-space: inherit;
}
    
    
    ''')
    arquivo.close
def cria_preamble_tex():
    arquivo = open(os.getcwd() + "/pdf/" + "preamble.tex", mode="w+", encoding="utf-8")
    arquivo.write(r'''\usepackage{booktabs}
\usepackage{fontspec}
\setmainfont{Arial Unicode MS}
\let\cleardoublepage\clearpage
\renewcommand{\contentsname}{Sumário}
\renewcommand{\chaptername}{Capítulo}
\usepackage{textcomp}''')
    arquivo.close
def cria_proj_book():
    arquivo = open(os.getcwd() + "/pdf/" + "book.Rproj", mode="w+", encoding="utf-8")
    arquivo.write('''Version: 1.0

RestoreWorkspace: Default
SaveWorkspace: Default
AlwaysSaveHistory: Default

EnableCodeIndexing: Yes
UseSpacesForTab: Yes
NumSpacesForTab: 2
Encoding: UTF-8

RnwWeave: Sweave
LaTeX: pdfLaTeX

BuildType: Website
''')
    arquivo.close   
def cria_index_pdf(autor, lingua):
    arquivo = open(os.getcwd() + "/pdf/" + "index.Rmd", mode="w+", encoding="utf-8")
    arquivo.write("---\n")
    arquivo.write('title: "Dicionário ' + lingua + '"\n')
    arquivo.write('author: "' + autor + '"\n')
    arquivo.write('''date: "`r Sys.Date()`"
documentclass: book
site: bookdown::bookdown_site
biblio-style: apalike
---

# Introdução''')
    arquivo.close



opcao = 0
opcoesvalidas = ['1','2','3','4']
textoopcao = "Opção > "


while opcao != "4":
    print("----------------CSV2RMD-----------------")
    print('''
1 - Validar tabela ("dicionario.csv").
2 - Gerar arquivos RMD para criar PDF.
3 - Gerar arquivos RMD para criar HTML.
4 - Sair
    ''')
    print("Digite o número da opção desejada:")
    opcao = input(textoopcao)
    if opcao not in opcoesvalidas:
        textoopcao = "Digite uma opção válida >"
    if opcao == "1":
        imprimelinha()
        print("Validação do arquivo 'dicionario.csv'\n\n")
        dicionario = abrearquivo()
        validacao_tabela_campos(dicionario)
        validacao_tabela_arquivos(dicionario)
        print("Validação terminada (Encontre os arquivos referentes na mesma pasta do 'dicionario.csv')")
        opcaovalidacao = "0"
        while opcaovalidacao != "1" and opcaovalidacao != "2":
            print("Para voltar ao menu inicial digite '1' para sair digite 2:")
            opcaovalidacao = input("Opção >")
            if opcaovalidacao == "2":
                opcao = "4"
    if opcao == "2":
        imprimelinha()
        print("Gerar arquivos RMD para criar PDF\n\n")
        dicionario = abrearquivo()
        cria_pdf(dicionario)
        print("Arquivos RMD criados na pasta 'pdf")
        opcaocriapdf = "0"
        while opcaocriapdf != "1" and opcaocriapdf != "2":
            print("Para voltar ao menu inicial digite '1' para sair digite 2:")
            opcaocriapdf = input("Opção >")
            if opcaocriapdf == "2":
                opcao = "4"
    if opcao == "3":
        imprimelinha()
        print("Gerar arquivos RMD para criar HTML\n\n")
        dicionario = abrearquivo()        
        print('''Para adicionar informação de autor e data aos arquivos de áudio e vídeo, e necessário 
adicionar junto ao 'dicionario.csv' um arquivo 'atores.csv' com uma coluna para sigla 
do falante (código) e outra para o nome como deve aparecer no html. Para essa opção 
os arquivos devem ter sido nomeados de acordo com o padrão de nomeclatura do Museu 
Goeldi''')
        opcaolegenda = 0
        while opcaolegenda != "s" and opcaolegenda != "n":
            print("Deseja adicionar informação de autor e data aos arquivos de áudio e vídeo,? Digite 's' para sim e 'n' para não:")
            opcaolegenda = input("Opção >")
            if opcaolegenda == "s":
                cria_html_legenda(dicionario)
                print("Arquivos RMD criados na pasta html")
                opcaohtmllegenda = "0"
                while opcaohtmllegenda != "1" and opcaohtmllegenda != "2":
                    print("Para voltar ao menu inicial digite '1' para sair digite 2:")
                    opcaohtmllegenda = input("Opção >")
                    if opcaohtmllegenda == "2":
                        opcao = "4"
            if opcaolegenda == "n":
                cria_html(dicionario)
                print("Arquivos RMD criados na pasta html")
                opcaohtml = "0"
                while opcaohtml != "1" and opcaohtml != "2":
                    print("Para voltar ao menu inicial digite '1' para sair digite 2:")
                    opcaohtml = input("Opção >")
                    if opcaohtml == "2":
                        opcao = "4"







