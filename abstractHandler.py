from fileHandler import FileHandler as fh

class AbstractHandler:
    def __init__(self):
        print("created")

    def createFromModel(projectName):
        path_to_files = str(f"./{projectName}/Models")
        files = fh.getFilesFromDir(path_to_files)
        tables = []

        for f in files:
            if "AbstractEntity.cs" in str(f) or "Scope.cs" in str(f):
                continue
            
            f = f[:-3]

            customDict = {"projectName" : str(projectName), "modelName" : str(f)}
            
            AbstractHandler.generateRepository(customDict)
            AbstractHandler.generateService(customDict)
            AbstractHandler.generateController(customDict)
            AbstractHandler.generateDTO(customDict)

            tables.append(f)

        AbstractHandler.npg_file(projectName, tables)

    def generateRepository(modelDict):
        path_to_template = str("./TemplateFiles/Repository/repositoryTemplate.txt")
        path_to_target = str(f"./{modelDict['projectName']}/Repository/{modelDict['modelName']}Repository.cs")
        fh.fileFromTemplate(path_to_template, path_to_target, modelDict)

    def generateService(modelDict):
        path_to_template = str("./TemplateFiles/Service/serviceTemplate.txt")
        path_to_target = str(f"./{modelDict['projectName']}/Service/{modelDict['modelName']}Service.cs")
        fh.fileFromTemplate(path_to_template, path_to_target, modelDict)

    def generateController(modelDict):
        path_to_template = str("./TemplateFiles/Controller/controllerTemplate.txt")
        path_to_target = str(f"./{modelDict['projectName']}/Controllers/{modelDict['modelName']}Controller.cs")
        fh.fileFromTemplate(path_to_template, path_to_target, modelDict)

    def generateDTO(modelDict):
        variables = ""
        print(modelDict['projectName'])
        print(modelDict['modelName'])

        with open(f"./{modelDict['projectName']}/Models/{modelDict['modelName']}.cs", 'r') as f:
            Lines = f.readlines()
            for l in Lines:
                if "get" in l or "set" in l:
                    ## get string ##
                    variables = variables + l + " \n"
                    ## get var name ##
                    # syntaxes = l.split(" ")
                    # print(f"linha: {l}")
                    # print(syntaxes)
                    # syntaxes = list(filter(lambda x: (x != ''), syntaxes))
                    # print(syntaxes[2])
        
        modelDict['variables'] = variables

        path_to_template = str("./TemplateFiles/DTO/dtoTemplate.txt")
        path_to_target = str(f"./{modelDict['projectName']}/DTO/{modelDict['modelName']}DTO.cs")
        fh.fileFromTemplate(path_to_template, path_to_target, modelDict)

    def generateNpgContext(modelDict):
        # path_to_template = str("./TemplateFiles/DTO/dtoTemplate.txt")
        # path_to_target = str(f"./{modelDict['projectName']}/DTO/{modelDict['modelName']}DTO.cs")
        # fh.fileFromTemplate(path_to_template, path_to_target, modelDict)
        pass

    def addNpgContext():
        pass

    def modelCreate(project_name, model_name, properties):
        for p in properties:
            print(f" {p['privacy']} {p['type']} {p['name']} get; set")
            print(model_name)

    def npg_file(project_name, tables):
        modelDict = []
        dbsets = ""
        
        path_to_template = str("./TemplateFiles/DataBase/NpgContext-dbset.txt")
        path_to_target = str(f"./{project_name}/DataBase/NpgContext.cs")
        
        for t in tables:
            dbsets = dbsets + "public DbSet<" + t + "> " + t + "s {get;set;} \n"

        modelDict = {"projectName": project_name, "dbsets" : dbsets, "relationships": ""}
        
        fh.fileFromTemplate(path_to_template, path_to_target, modelDict)