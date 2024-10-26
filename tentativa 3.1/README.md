


# Projeto  Web Site para cadastro de Usuarios e quantidade de Pets com Python, Flask e MySQL.






* Criei um arquivo "requirements.txt" para gerenciamento de dependencias https://www.freecodecamp.org/news/python-requirementstxt-explained/
* Corrigi o método POST criando a variável responsável dentro de uma tupla ao invés de um objeto, também aproveitei para
adicionar o campo senha que estava faltando
* Alterei os parametros def execute_query adionei if else para padronizar o SELECT
* Adicionado a def write_responsavel TRY e ecessão 
* Criei o Template consulta.htmla e a Rota consulta em app.py para buscar a tabela responsavel no banco de dados bem_animal2 retornando responsaveis 
* Criei o template edit.html e as rotas edit e delete para editar  e excluir os dados da tabela responsavel 
* Criei as funções get_responsavel_by_id, update_responsavel e delete_responsavel para manipular os Bancp de dados 
* Modifiquei o template register.html para exibir a mensagem flash
* Criei o template login.html e as rotas login e logout para o login e logout na pagina por email e senha 
* Alterei o template index.html para receber os botoes de login/logout e acesso a consulta.
* Alterei o template login para acertar o login e logout do site 
* Adicionei botão login/logout no template index.html e template edit.html
* Criei a verificação de sessão para que os dados seja exibidos e editados apenas quando o usuário estiver logado 
* Padronização das paginas Consulta, Edit, Login e Register 
* Atulaização codigo para BD
* Alterei o Link de localização de postaos de vacinação para avrin em nova guia 
* Foi implementado uma API para enviar um email de confirmação de cadastro 
* Implementei um Script em Javascript para padronizar o numero telefone e conferir o email 
