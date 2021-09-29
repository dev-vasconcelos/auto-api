# Auto API
## _Tudo que pode ser automatizado, deve ser_

AutoApi é um projeto para se criar API's automaticamente por meio de apenas um arquivo .SQL, ou através de comandos complementares para gerar um "esqueleto" a partir de um Model feito.

## Abstração
O principal foco do AutoApi é o método de abstração, eficiência de código e o mínimo de repetição possível. Ainda esta em desenvolvimento, mas toda corrida começa com o primeiro passo.

A pasta /TemplateFiles possuí os templates para o melhor entendimento da técnica de abstração utilizada. Recomenda-se ver o serviceTemplate, controllerTemplate, dtoTemplate e repositoryTemplate.

## 
> Instalação de Python 3, (listar libs)
> Instalação do .Net

## Comandos de exemplo
O comando phandler aceita uma função para múltiplos projetos.

```sh
$ python3 generator.py -p NomeDoProjeto arquivo.sql
```

Para atualizar vários projetos por exemplo:
```sh
$ python3 generator.py $parametros
```

### Parâmetros
| Parâmetro | Descrição |
| ------ | ------ |
| `-p` | Nome do Projeto em CammelCase |
| `-t` | Tipo de projeto {webapi} |
| `-c` | Gerar configuração |
| `-m` | Gerar control, repository e service a partir de um projeto cru com model |
| `-s` | Arquivo .sql para se  |

### Clique na imagem abaixo para ver um vídeo de demonstração
[![Everything Is AWESOME](https://www.aracruz.es.leg.br/imagens/f2ea1ded4d037633f687ee389a571086logotipodoconedoyoutubebyvexels.png)](https://youtu.be/0QLqWdOPMeQ "Everything Is AWESOME")