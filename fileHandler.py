import sys
from string import Template
import os
from distutils.dir_util import copy_tree
import snoop

class FileHandler():
    def __init__(self):
        print("created")

    def createFolderStructure(paths):
        for p in paths:
            os.makedirs(p, exist_ok=True)

    def fileFromTemplate(path_to_template, path_to_target, customDict):
        with open(path_to_template, 'r') as f:
            src = Template(f.read())
            result = src.substitute(customDict)

            with open(path_to_target, 'w') as t:
                # sys.stdout = t
                # print(result)  
                print(str(result), file=t)
    
    # @snoop
    def createWebBaseFolderStructre(projectName):
        paths = [
            "/DataBase",
            "/Commons/ENUM",
            "/Commons/Helpers",
            "/Controllers/AbstractClass",
            "/Controllers/Interface",
            "/Controllers/AbstractClass",
            "/DTO/AbstractClass",
            "/DTO/Interface",
            "/Models",
            "/Repository/AbstractClass",
            "/Repository/Interface",
            "/Response",
            "/Service/AbstractClass",
            "/Service/Interface"
            ]
        i = 0
        for p in paths:
            paths[i] = str(f"./{projectName}/{str(p)}")
            i += 1

        FileHandler.createFolderStructure(paths)
        copy_tree('./TemplateStructureWeb', str(f"./{projectName}"))

        customDict = {"projectName" : str(projectName)}
        fh = FileHandler
        # walk by files
        f = []
        for (dirpath, dirnames, filenames) in os.walk(str(f"./TemplateStructureWeb")):
            for filename in filenames:
                path_to_template = str(f"{dirpath}/{filename}")
                path_to_target = path_to_template.replace("TemplateStructureWeb", projectName)

                fh.fileFromTemplate(path_to_template, path_to_target, customDict)

    def getFilesFromDir(path_to_dir):
        #os.listdir()
        ## op 1
        # allFiles = [ f for f in os.listdir(path_to_dir) if os.path.isfile(os.path.join(path_to_dir, f))]

        ## op 2 - recursivo
        # allFiles = []
        # for(dirpath, dirnames, filenames) in os.walk(path_to_dir):
        #     allFiles.extend(filenames)

        ## op 3 - op2 mas para na primeira it
        allFiles = next(os.walk(path_to_dir), (None, None, []))[2]

        return allFiles