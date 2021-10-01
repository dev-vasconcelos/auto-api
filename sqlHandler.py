from typing import final
from Models.Attribute import Attribute
from Models.Model import Model
import os
import re
from fileHandler import FileHandler as fh 
from Models.Attribute import Attribute
from Models.Model import Model
import snoop

class SqlHandler():
    def __init__(self):
        print("created")

    def createModel(project_name, file_path):
        # print(file_path)
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
                elif in_table:
                    atr_string = ""
                    
                    for atr in mdl.attributes:
                        atr_string = atr_string + atr.atr_string() + " \n"
                        customDict["attributes"] = atr_string

                    fh.fileFromTemplate(path_to_template, path_to_target, customDict)
                    
                    customDict = {'projectName' : project_name, 'variables': "", "modelName":"", "attributes":""}
                    
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