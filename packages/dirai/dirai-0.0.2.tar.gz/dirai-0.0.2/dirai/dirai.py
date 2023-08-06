import pymysql

def server(server):
    return server
def usuario(usuario):
    return usuario
def senha(senha):
    return senha
def base(base):
    return base

global connection

def dirai_connet(servidor, usuario, senha, base):

    global connection

    connection = pymysql.Connect(host=servidor,
            user=usuario,
            password=senha,
            db=base,
            charset='utf8mb4',
            autocommit=True)

def dados_hist_fundos(dataini, datafim, cnpj, campos):

    global connection
    dictbase = {}
    for a in campos:
        dictbase[a] = []
    
    consulta_campos = ''
    for a in range(0, (len(campos)-1)):
        consulta_campos += f'{campos[a]}, '
    consulta_campos += f'{campos[-1]}'

    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = f'SELECT {consulta_campos} FROM backoffice_xml.header WHERE (cnpj = "{cnpj}") and (dtposicao between "{dataini}" and "{datafim}") order by dtposicao ASC;'
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        for a in range(0, len(result)):
            for b in dictbase:
                dictbase[b].append(result[a][b])
    
    return dictbase

#print(dados_hist_fundos('2017-01-02', '2017-01-20', '11290670000106', ['dtposicao', 'patliq', 'valorcota']))