
import math

def norma(dict):
    soma_dos_quadrados = 0.0
    for x in dict:
        soma_dos_quadrados += dict[x] * dict[x]
    
    return math.sqrt(soma_dos_quadrados)

def similaridade_cosseno(dict_1, dict_2):
    chaves_similares = []
    numerador = 0
    
    if (norma(dict_1) or norma(dict_2)) == 0:
        return (-1)
    
    for chaves in dict_1.keys():
        if chaves in dict_2.keys():
            chaves_similares.append(chaves)
    
    for chaves in chaves_similares:
        numerador += dict_1[chaves] * dict_2[chaves]
            
    return (numerador/(norma(dict_1)*norma(dict_2)))

def constroi_descritores_semanticos(sentencas):
    d={}
    for sentenca in sentencas:
        verificado=[]
        for palavra in sentenca:
            if palavra not in verificado:
                if palavra not in d:
                    d[palavra]={}
                verificando=[]
                for verificacao in sentenca:
                    if verificacao not in verificando:
                        if verificacao != palavra:
                            if verificacao not in d[palavra]:
                                d[palavra][verificacao]=0
                            d[palavra][verificacao]+=1
                            verificando.append(verificacao)
                
                verificado.append(palavra)
    return d           

def constroi_descritores_semanticos_de_arquivos(nomes_arquivos):
    resultado = {}
    for index in range(len(nomes_arquivos)):
        texto = open(nomes_arquivos[index], "r", encoding = "utf-8")
        texto = texto.read()
        texto = texto.lower()
        texto = texto.replace(","," ")
        texto = texto.replace("-"," ")
        texto = texto.replace("--"," ")     
        texto = texto.replace(':', " ")
        texto = texto.replace(';', " ")
        texto = texto.replace('"', " ")
        texto = texto.replace("'", " ")
        texto = texto.replace("? ",".")
        texto = texto.replace("! ",".")
        texto = texto.replace(". ",".")
        texto = texto.split(".")
        
        for i in range(len(texto)):
            texto[i] = texto[i].strip().split()
        dic = constroi_descritores_semanticos(texto)
        for chave in dic:
            if chave == '':
                del chave
            elif chave not in resultado:
                if '' == dic[chave]:
                    continue
                resultado[chave] = dic[chave]
            elif chave in resultado:
                for chave2 in dic[chave]:
                    if chave2 not in resultado[chave]:
                        resultado[chave][chave2] = dic[chave][chave2]
                    elif chave2 in resultado[chave]:
                        resultado[chave][chave2] += dic[chave][chave2]
                        
            
        
    return resultado

def palavra_mais_similar(palavra, escolhas, descritores_semanticos, funcao_similaridade):
    similaridade_maxima = 0
    palavra_similar = ""
    if palavra in descritores_semanticos:
        for i in escolhas:
            if i in descritores_semanticos:
                if funcao_similaridade(descritores_semanticos[palavra], descritores_semanticos[i]) > similaridade_maxima:
                    similaridade_maxima = funcao_similaridade(descritores_semanticos[palavra], descritores_semanticos[i])
                    palavra_similar = i 
        
    return palavra_similar

def executa_teste_similaridade(nome_arquivo, descritores_semanticos, funcao_similaridade):
    file = str((open(nome_arquivo, "r", encoding="utf-8")).read())
    file = file.split("\n")
    teste_lista = []
    
    for f in range(len(file)):
        teste_lista.append(file[f].split(" "))
        
    escolhas = []
    correto = 0
    contador = 0
    for i in range(len(teste_lista) - 1):
        contador += 1
        palavra = teste_lista[i][0]
        escolhas = teste_lista[i][2:]
        if palavra_mais_similar(palavra, escolhas, descritores_semanticos, funcao_similaridade) == teste_lista[i][1]:
            correto += 1
    
        escolhas = []
        
    return ((correto/contador) * 100)


if __name__ == '__main__':
    # A 
    print(similaridade_cosseno({"i": 3, "am": 3, 'a': 2, 'sick': 1, 'spiteful': 1, 'an': 1, 'unattractive': 1},
                               {'i': 1, 'believe': 1, 'my': 1, 'is': 1, 'diseased': 1}))
    print(similaridade_cosseno({"a": 1, "b": 2, 'c': 3}, {'b': 4, 'c': 5, 'd': 6})) 

    # B
    frases = [["i", "am", "a", "sick", "man"],
              ["i", "am", "a", "spiteful", "man"],
              ["i", "am", "an", "unattractive", "man"],
              ["i", "believe", "my", "liver", "is", "diseased"],
              ["however", "i", "know", "nothing", "at", "all", "about", "my",
               "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]
    print(constroi_descritores_semanticos(frases))

    # C
    arquivos = ["war_and_peace.txt", "swanns_way.txt"]
    descritores_semanticos = constroi_descritores_semanticos_de_arquivos(arquivos)

    # D
    print(palavra_mais_similar("cowardice", ["fear", "successive"], descritores_semanticos, similaridade_cosseno))
    print(palavra_mais_similar("connection", ["pipe", "relation", "connecticut", "excited"], descritores_semanticos, similaridade_cosseno))
  
    # E
    print(executa_teste_similaridade("teste.txt", descritores_semanticos, similaridade_cosseno))
    