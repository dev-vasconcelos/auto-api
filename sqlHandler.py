import os
import re
from fileHandler import FileHandler as fh 
class SqlHandler():
    def __init__(self):
        print("created")

    def createModel(project_name, file_path):
        print(file_path)
        with open(file_path, 'r') as sql_file:
            lines = sql_file.readlines()
            path_to_template = './TemplateFiles/Models/modelTemplate.txt'
            customDict = {'projectName' : project_name}
            for line in lines:
                if "__EFMigrationsHistory" in line:
                    continue

                if "CREATE" in line and "TABLE" in line:
                    splited_line = line.split(".")
                    splited_line[-1] = splited_line[-1].split(" ")
                    
                    table_name = splited_line[-1][0]
                    table_name = table_name.replace("tb","")

                    table_name = SqlHandler.snake_to_cammel(table_name)
                    table_name = re.sub('[^A-Za-z0-9]+', '', table_name)

                    path_to_target = str(f"./{project_name}/Models/{table_name}.cs")
                    customDict['entity'] = table_name
                    
                    fh.fileFromTemplate(path_to_template, path_to_target, customDict)
                    
    def snake_to_cammel(string):
        while string.find("_") >= 0 :
            inx = string.find("_")
            string = string[:inx] + string[inx+1:]
            string_list = list(string)
            string_list[inx] = string[inx].upper()
            string_list[0] = string[0].upper()
            final_string = "".join(string_list)

        return final_string

    def createModelFile(project_name , model_name):
        pass

    def createNpg():
        pass