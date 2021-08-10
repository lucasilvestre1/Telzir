# Telzir

### Página web para os clientes da empresa calcularem o valor de suas ligações. Aplicação desenvolvida em Python utilizando o framework Flask.

***
### Inicio
#### Após clonar o repositório, navegue até o diretório do projeto pelo seu terminal
```
cd /home/telzir
```
> Esse foi apenas um exemplo, navegue até o repositório na sua máquina.

#### instale todas as dependências usando o seguinte comando:
```
pip install -r requirements.txt
```



<!--#### Crie um virtualenv-->

<!--#### Acesso o diretório e ative a virtualenv-->

<!--```-->
<!-- source env/bin/activate-->
<!--```-->


> Optei por disponibilizar o arquivo de configurações da aplicação para
> facilitar na utilização/teste da mesma.

### Rode a aplicação
```
flask run
```
Pronto! Acesse a aplicação no link: http://localhost:5000/


### Funcionalidades
***

- [x] Página inicial com visualização dos planos promocionais.
- [x] Tela de cálculo com escolha da cidade de origem e destino da
      ligação;
- [x] Tela com histório de todas as cotações realizadas e com opção de
      editar e apagar;
- [ ] Pytest

### Tecnologias
***
- Python
- Flask Framework
- SQLAlchemy
- WTForms
