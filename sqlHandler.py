from typing import final
from Models.Attribute import Attribute
from Models.Model import Model
import os
import re
from fileHandler import FileHandler as fh 
from Models.Attribute import Attribute
from Models.Model import Model
import snoop

##
# A princípio o sql que aceita relacionamentos deve ser padronizado de acordo com o workbench 
##

class SqlHandler():
    def __init__(self):
        print("created")

    def createModel(project_name, file_path):
        # print(file_path)
        # to faznedo minhas coisas
        # to adicionando
        is_mysql_workbench = True
        with open(file_path, 'r') as sql_file:
            lines = sql_file.readlines()
            path_to_template = './TemplateFiles/Models/modelTemplate.txt'
            path_to_target = ''
            customDict = {'projectName' : project_name, 'variables': "", "modelName":"", "attributes":"", "tableName": ""}
            in_table = False
            mdl = Model()

            for line in lines:

                if "__EFMigrationsHistory" in line:
                    continue
                
                if "CREATE" in line and "TABLE" in line:
                    in_table = True
                    table_name = SqlHandler.get_table_name(line)
                    path_to_target = str(f"./{project_name}/Models/{table_name}.cs")
                    mdl.name = table_name

                    # customDict['model'] = mdl
                    customDict['modelName'] = mdl.name
                    customDict['tableName'] = SqlHandler.entity_to_table_name(customDict['modelName'])

                    # fh.fileFromTemplate(path_to_template, path_to_target, customDict)

                elif in_table and SqlHandler.is_psql(line):
                    variable = SqlHandler.check_data_converter(line)
                    if variable:
                        mdl.attributes.append(variable)
                elif SqlHandler.is_foreign_key(line):
                    SqlHandler.psql_handle_fk(line, mdl.attributes)
                    print(line)
                # MYSQL WORKBENCH
                # elif in_table and "CONSTRAINT" in line.upper():
                #     SqlHandler.relationship_from_mysql_workbench_line(line, mdl.attributes)
                elif in_table and line == "\n":
                    atr_string = ""
                    
                    for atr in mdl.attributes:
                        print(atr.notations)
                        atr.notations = []
                        atr.notations = SqlHandler.get_attribute_notations(atr, line)
                        atr_string = atr_string + atr.atr_string() + " \n \n"
                    customDict["attributes"] = atr_string
                    atr.notations = []

                    fh.fileFromTemplate(path_to_template, path_to_target, customDict)
                    
                    customDict = {'projectName' : project_name, 'variables': "", "modelName":"", "attributes":"", "tableName": ""}
                    
                    in_table = False
                    mdl = Model()
                    mdl.attributes = []
                    
                    
    def get_table_name(line):
        splited_line = line.split(".")
        splited_line[-1] = splited_line[-1].split(" ")
                    
        table_name = splited_line[-1][0]
        table_name = table_name.replace("tb","")

        table_name = SqlHandler.snake_to_cammel(table_name)
        table_name = re.sub('[^A-Za-z0-9]+', '', table_name)
        return table_name

    def table_to_entity_name(table_name):
        has_prefix = False
        if (table_name[:3] == "tb_"):
            has_prefix = True
        entity_name = SqlHandler.snake_to_cammel(table_name)
        if has_prefix:
            entity_name = entity_name[2:]
        return entity_name

    def snake_to_cammel(string):
        final_string = string
        while string.find("_") >= 0 :
            inx = string.find("_")
            string = string[:inx] + string[inx+1:]
            string_list = list(string)
            string_list[inx] = string[inx].upper()
            string_list[0] = string[0].upper()
            final_string = "".join(string_list)

        return final_string

    def cammel_to_snake(string):
        inx = 0
        string_list = list(string)
        final_string = string

        for s in string_list:
            
            if inx == 0:
                s = s.lower()
                string_list[inx] = s
                final_string = "".join(string_list)

            if s.isupper() and inx > 0:
                s = s.lower()
                string_list[inx] = s
                final_string = "".join(string_list[:inx]) + "_" + "".join(string_list[inx:])
            
            inx = inx + 1

        return final_string

    def get_attribute_notations(atr, line):
        atr.notations.append("[Column(\""+ SqlHandler.cammel_to_snake(atr.name) +"\")]")
        if atr.is_fk:
            atr.notations.append("//[ForeignKey(\""+ SqlHandler.cammel_to_snake(atr.name) +"\")]")
        return atr.notations

    def check_data_converter(line):
        atr = Attribute()

        ## NAME ##
        
        splited_line = line.split(" ")
        abstract_names = ['Id', 'UpdatedOn', 'CreatedBy', 'UpdatedBy', 'CreatedOn', 'Scope', 'ScopeId']
        
        name_filter = list(filter(lambda x: (x != ''), splited_line))
        atr.name = re.sub('[^A-Za-z0-9]+', '', name_filter[0])
        
        string_list = list(atr.name)
        string_list[0] = atr.name[0].upper()
        atr.name = "".join(string_list)

        for abname in abstract_names:
            if abname.upper() == atr.name.upper():
                return False

        if "id".upper() == atr.name:
            return False

        atr.name = SqlHandler.snake_to_cammel(atr.name)

        ## TYPE ##
        string_types = ['text', 'varchar(45)', 'varchar']
        int_types = ['int4']
        long_types = ['int8']
        float_types =['float4', 'float8']
        datetime_types = ['datetime', 'timestamp']
        splited_line = line.split(" ")
        
        splited_line = list(map(lambda x : x.upper(), splited_line))

        is_string = set(list(map(lambda x: x.upper(), string_types))) & set(splited_line)
        is_int = set(list(map(lambda x: x.upper(), int_types))) & set(splited_line)
        is_long = set(list(map(lambda x: x.upper(), long_types))) & set(splited_line)
        is_float = set(list(map(lambda x: x.upper(), float_types))) & set(splited_line)
        is_datetime = set(list(map(lambda x: x.upper(), datetime_types))) & set(splited_line)

        if is_string:
            atr.type = "string"
        elif is_int:
            atr.type = "int"
        elif is_long:
            atr.type = "long"
        elif is_float:
            atr.type = "float"
        elif is_datetime:
            atr.type = "DateTime"
        else:
            atr.type = "bool"
                
        atr.privacy = "public"

        atr.is_getter = True
        atr.is_setter = True

        # print(atr.atr_string())
        return atr

    def is_psql(line):
        data_types = ['text','int8','timestamp','int4','float4','VARCHAR']
        for data in data_types:
            if data.upper() in line.upper():
                return True
        return False

    def is_mysql(line):
        data_types = ['VARCHAR(45)','INT']
        for data in data_types:
            if data.upper() in line.upper():
                return True
        return False

    def entity_to_table_name(entity_name):
        table_name = "[Table(\"tb_"
        table_name = table_name + SqlHandler.cammel_to_snake(entity_name)
        table_name = table_name + "\")]"
        return table_name

    def create_model_variables():
        pass

    def createNpg():
        pass

    #POSTGRES
    def is_foreign_key(line):
        key_words = ['CONSTRAINT','FOREIGN KEY', 'REFERENCES']
        for k in key_words:
            if k not in line:
                return False
        return True

    def psql_handle_fk(line, attributes):
        replaced = line.replace(")", "(")    
        splited = replaced.split("(")
        i = 0
        for s in splited:
            print("idx: " + str(i) + "; value: " + s)
            i = i + 1
        # fk da tabela
        splited[1] = re.sub('[^A-Za-z0-9]+', '', splited[1])
        print("fk no model/tabela: " + splited[1])

        # refenencia a tabela:
        splited[2] = splited[2].split(".")[1]
        splited[2] = re.sub('[^A-Za-z0-9]+', '', splited[2])
        print("referencia: " + splited[2])

        # atributo da tabela que é refenciado
        splited[3] = re.sub('[^A-Za-z0-9]+', '', splited[3])
        print("atributo: "+ splited[3] + " da tabela: " + splited[2] + " que é a refernecia")


        for atr in attributes:
            if atr.name == splited[1]:        
                SqlHandler.find_class(replaced.split("(")[2].split('.')[1])
                print("é igual:" + str(atr.name))
                atr.is_fk = True
                # atr.notations.append("//[ForeignKey(\""+ SqlHandler.cammel_to_snake(atr.name) +"\")]")

        return True

    def find_class(table_name):
        print("table name" + table_name)
        print(SqlHandler.table_to_entity_name(table_name)) 


    ## TODO: Como eu faço para saber se é 1-1 ou 1-n?
    
    ####### No caso, se for 1 - N
    #### 1 fica (EntidadeUm.cs)
    ## [ForeignKey]
    ## [Column("entidade_dois_id")]
    ## public long EntidadeDoisId {get; set;}
    ## 
    ## public EntidadeDois EntidadeDois {get; set;}
    ##
    #### n fica
    ##  [Newtonsoft.Json.JsonIgnore] // não me recordo se todos tem json ignore
    ##  public List<EntidadeUm> EntidadesUm {get; set;}
    ##


    # MYSQL WORKBENCH
    # def constraint_handler(line, in_table, atr):
    #     if "constraint".upper() in line.upper():
    #         # print("constraint")
    #         # print("linha inteira:" + line) 
    #         print("---")
    #     if "FOREIGN KEY (".upper() in line.upper():
    #         splited = line.split("`")
    #         print("Foreign Key:" + splited[1])
    #         # algo = atr.index(splited[1])
    #         # print(algo)
            
    #         # print("linha inteira: " + line)
    #     if "REFERENCES".upper() in line.upper():
    #         splited = line.split("`")
    #         print("tabela referenciada: " + splited[3])
    #         print("atributo referenciado: " + splited[5])
    #         # print("linha inteira: " + line)
            


    # def relationship_from_mysql_workbench_line(line, atr):
    #     # SqlHandler.constraint_handler(line, True, atr)
    #     return True