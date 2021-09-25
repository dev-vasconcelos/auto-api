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

    # @snoop
    def createModel(project_name, file_path):
        print(file_path)
        with open(file_path, 'r') as sql_file:
            lines = sql_file.readlines()
            path_to_template = './TemplateFiles/Models/modelTemplate.txt'
            path_to_target = ''
            customDict = {'projectName' : project_name, 'variables': "", "name":"", "attributes":""}
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
                    customDict['name'] = mdl.name
                    # fh.fileFromTemplate(path_to_template, path_to_target, customDict)

                elif in_table and SqlHandler.is_psql(line):
                    variable = SqlHandler.check_data_converter(line)
                    if variable:
                        mdl.attributes.append(variable)
                        # for atr in mdl.attributes:
                        #     print(atr.atr_string())
                        # print(variable.atr_string())
                # elif in_table and not SqlHandler.is_psql(line):
                elif in_table:
                    atr_string = ""
                    for atr in mdl.attributes:
                        atr_string = atr_string + atr.atr_string() + " \n"
                        customDict["attributes"] = atr_string
                    fh.fileFromTemplate(path_to_template, path_to_target, customDict)
                    in_table = False
                    mdl = Model()
                    
                    
    def get_table_name(line):
        splited_line = line.split(".")
        splited_line[-1] = splited_line[-1].split(" ")
                    
        table_name = splited_line[-1][0]
        table_name = table_name.replace("tb","")

        table_name = SqlHandler.snake_to_cammel(table_name)
        table_name = re.sub('[^A-Za-z0-9]+', '', table_name)
        return table_name

    def snake_to_cammel(string):
        while string.find("_") >= 0 :
            inx = string.find("_")
            string = string[:inx] + string[inx+1:]
            string_list = list(string)
            string_list[inx] = string[inx].upper()
            string_list[0] = string[0].upper()
            final_string = "".join(string_list)
        return final_string

    def check_data_converter(line):
        
        atr = Attribute()
        
        if "text" in line:
            atr.type = "string"
        else:
            return False
        
        split_line = line.split(" ")
        
        atr.privacy = "public"

        name_filter = list(filter(lambda x: (x != ''), split_line))
        atr.name = re.sub('[^A-Za-z0-9]+', '', name_filter[0])
        
        atr.is_getter = True
        atr.is_setter = True

        return atr

    def is_psql(line):
        data_types = ['text','int8','timestamp','int4','float4']
        for data in data_types:
            if data in line:
                return True
        return False

    def create_model_variables():
        pass

    def createNpg():
        pass