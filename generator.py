import os
from string import Template
import sys
from dictionaryHandler import DictionaryHandler as dh
from dotnetHandler import DotnetHandler as dnethandler
from fileHandler import FileHandler as fh
from abstractHandler import AbstractHandler as ah
import argparse
import getopt
import snoop

class StartupGenerator:
    def __init__ (self):
        print("created")
        
    def prepareConfigFiles(dictExpressions):
        lowerDict = dh.dictToLower(dictExpressions, "projectName")
        fh.fileFromTemplate('./TemplateFiles/appsettings.Development.txt', str(f"./{dictExpressions['projectName']}/appsettings.Development.json"), lowerDict)
        fh.fileFromTemplate('./TemplateFiles/appsettings.txt', str(f"./{dictExpressions['projectName']}/appsettings.json"), lowerDict)

def handleArguments(argv):
    result = {}
    try:
        opts, args = getopt.getopt(argv, "hp:t:cm", ["project=","type=","config=","model="])
    except getopt.GetoptError:
        print("note: handler error in the future")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h': #vacilo do python não ter switch
            print("python3 generator.py --project (project name) --type (project type, only webapi now) --config (generate config files) --model (model added)")
            sys.exit()
        elif opt in ("-p", "--project"):
            result['projectName'] = str(arg)
        elif opt in ("-t", "--type"):
            result['projectType'] = str(arg)
        elif opt in ("-c", "--config"):
            result['config'] = 1
        elif opt in ("-m", "--model"):
            result["model"] = 1
    if(result['projectName'] is None):
        print("Project name missing")
    else:
        return result

@snoop        
def main():
    # parser = argparse.ArgumentParser("generator")
    # parser.add_argument("")
    #get arguments
    d = handleArguments(sys.argv[1:])
    # d = {
    #     'projectName': 'nomeInSaNoTaLigado'
    # }
    if "model" in d:
        ah.createFromModel(d['projectName'])
    else:
        dnethandler.createWebApiProject(d['projectName'])
        dnethandler.addPackage(d['projectName'], "Microsoft.EntityFrameworkCore.InMemory")
        dnethandler.addPackage(d['projectName'], "Newtonsoft.Json --version 13.0.1")
        dnethandler.addPackage(d['projectName'], "Microsoft.AspNetCore.Mvc.NewtonsfotJson --version 3.0.0")
        dnethandler.addPackage(d['projectName'], "Npgsql --version 5.0.7")
        dnethandler.addPackage(d['projectName'], "Serilog --version 2.10.0")
        dnethandler.addPackage(d['projectName'], "Npgsql.EntityFrameworkCore.PostgreSQL --version 5.0.7")
        dnethandler.addPackage(d['projectName'], "Serilog.AspNetCore")
        dnethandler.addPackage(d['projectName'], "Serilog.Settings.Configuration")
        dnethandler.addPackage(d['projectName'], "System.IdentityModel.Tokens.Jwt")
        dnethandler.addPackage(d['projectName'], "Microsoft.AspNetCore.Authentication.JwtBearer")
        dnethandler.addPackage(d['projectName'], "Microsoft.AspNetCore.Authentication.OpenIdConnect")
        dnethandler.addPackage(d['projectName'], "Microsoft.AspNetCore.Mvc.NewtonsoftJson")
        print(dnethandler.restore(d['projectName']))
        fh.createWebBaseFolderStructre(d['projectName'])

    if "config" in d:
        StartupGenerator.prepareConfigFiles(d)

if __name__ == "__main__":
    main()