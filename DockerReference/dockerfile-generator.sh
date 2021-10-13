#! /bin/bash

DLLNAME=project

DOTNETVERSION=5.0

echo "FROM mcr.microsoft.com/dotnet/sdk:$DOTNETVERSION AS build" > Dockerfile
echo "WORKDIR /source" >> Dockerfile

echo " " >> Dockerfile

#echo "COPY *.sln ." >> Dockerfile
echo "COPY $DLLNAME/* ./" >> Dockerfile
echo "#RUN dotnet build" >> Dockerfile
echo "RUN dotnet restore" >> Dockerfile

echo  "" >> Dockerfile

echo "COPY $DLLNAME/. ./$DLLNAME/" >> Dockerfile
echo "WORKDIR /source/$DLLNAME" >> Dockerfile
echo "RUN dotnet publish -c release -o /app" >> Dockerfile

echo " " >> Dockerfile

echo "FROM mcr.microsoft.com/dotnet/aspnet:$DOTNETVERSION" >> Dockerfile
echo "WORKDIR /app" >> Dockerfile
echo "COPY --from=build /app ./" >> Dockerfile

echo " " >> Dockerfile

echo EXPOSE 80"" >> Dockerfile

echo  "" >> Dockerfile

echo "ENTRYPOINT \"[dotnet\", \"ProjectName.dll\"]" >> Dockerfile

