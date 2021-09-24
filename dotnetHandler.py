import os

class DotnetHandler:
    def __init__(self):
        print("created")

    def createWebApiProject(projectName):
        tmpStream = os.popen('dotnet new webapi -o ' + str(projectName))
        output = tmpStream.read()
        return output

    def addPackage(projectName, packageName):
        command = str(f"cd {projectName} && dotnet add package {packageName}")
        tmpStream = os.popen(command)
        output = tmpStream.read()
        return output

    def restore(project_name):
        command = str(f"cd {project_name} && dotnet restore")
        tmpStream = os.popen(command)
        output = tmpStream.read()
        return output
