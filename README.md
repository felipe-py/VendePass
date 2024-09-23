<h3 align="center">VendePass</h3>

<div align="justify"> 
<div id="sobre-o-projeto"> 
<h2> Descrição do Projeto</h2>

O setor de aviação de baixo custo democratizou as viagens áereas, desenvolvendo estratégias para obter um baixo custo em viagens que potencializam diversos setores da economia. Em resposta a essa importância, este software busca desenvolver uma forma de comunicação entre o cliente que busca a sua passagem e o servidor da empresa áerea.

O protocolo de comunicação do projeto possui como base principal os subsistemas TCP/IP e tem como objetivo cumprir os seguintes requisitos:

- **Comunicação Cliente/Servidor:** Estabelecer a comunicação entre o cliente que busca e compra passagens e o servidor central da empresa áerea
- **Concorrência e prioridade:** Garantir que o cliente que inicia o processo de compra de uma passagem tenha prioridade, não permitindo que um outro cliente tenha posse do assento.

</div>
</div>

<h2> Autor <br></h2>
<uL>
  <li><a href="https://github.com/felipe-py">Felipe Silva</a></li>
  <li><a href="https://github.com/Lucas-L-Rodrigues">Lucas Lima</a></li>
</ul>


<h1 align="center"> Sumário </h1>
<div id="sumario">
	<ul>
        <li><a href="#Software"> Softwares Utilizadas </a></li>
        <li><a href="#arquitetura"> Arquitetura do Projeto </a></li>
        <li><a href="#conclusao"> Conclusão </a></li>
        <li><a href="#execucaoProjeto"> Execução do Projeto </a></li>
        <li><a href="#referencias"> Referências </a></li>
	</ul>	
</div>

<div id="Software">
<h2> Softwares Utilizadas</h2>
<div align="justify">

Nesta seção, são apresentados os softwares utilizados durante o desenvolvimento do projeto.

<h3> Linguagem Python</h3>

O *Python* foi escolhido para o desenvolvimento do projeto devido a sua síntaxe simplificada, além da grande integração com as mais diversas funções e bibliotecas disponíveis para elaborar o software. A versão utilizada foi a 3.12.6.

<h3> Docker</h3>

O *Docker* é uma plataforma de implantação e execução de aplicativos em contêineres. 
Um contêiner é uma unidade leve e portátil que inclui tudo o que um aplicativo precisa 
para ser executado de forma independente, como código, bibliotecas, dependências e configurações.
O Docker oferece uma plataforma consistente para desenvolver, testar e implantar aplicativos, 
garantindo que os ambientes de desenvolvimento e produção sejam consistentes e reproduzíveis.

<h3>VS Code</h3>

O Visual Studio Code, também conhecido como *VSCode*, é um ambiente de desenvolvimento muito popular. Desenvolvido pela Microsoft, é um editor de código aberto e gratuito que oferece recursos como realce de sintaxe, conclusão automática de código e depuração integrada. Foi escolhido para o processo de desenvolvimento do software devido a variedade de extensões que facilitam o processo de programação com as ferramentas utilizadas.

</div>
</div>

</div id="arquitetura">
<h2> Arquitetura do Projeto </h2>
<div align="justify">

Nesta seção, serão destacados os pricnipais pontos que envolvem a arquitetura do software desenvolvido, o que engloba todas as funções e regras de negócio que estão relacionadas a comunicação entre o cliente e o servidor.

<h3> Comunicação entre Cliente e Servidor </h3>

Neste tópico serão abordados as questões relacionadas a conexão mantida entre cliente e servidor, abrangendo as responsabilidades de cada um e os protocolos e paradgmas utilizados.

<h4> Visão Geral e Protocolo de Comunicação</h4>

O projeto utiliza uma arquitetura de comunicação entre cliente e servidor baseado no sistema TCP/IP, as mensagens enviadas pela conexão estão em formato JSON visando uma melhor estruturação e facilidade nos momentos de decodificação das requisições do cliente e respostas do servidor.

O papel principal do cliente é a solicitação das operações a serem realizadas pelo servidor, são elas: login no sistema, compra e cancelamento de passagens. Em relação ao servidor, este ficará responsável por processar as requisições e manipular os dados nencessários em cada uma delas, retornando uma resposta adequada para cada situação.

O protocolo de comunicação de cada requisição que esteja de forma direta(login, compra e cancelamento de passagem) ou indireta(visualizar rotas ou passagens) sendo solicitada ao servidor, possuirá um opcode. Este opcode é responsável por indentificar a operação que deve ser realizada pelo servidor, são 5 ao todo.

* opcode 1: Solicitação de login
* opcode 2: Solicitação para visualizar rotas disponíveis
* opcode 3: Solicitação para comprar passagens
* opcode 4: Solicitação para visualização de passagens compradas
* opcode 5: Solicitação para cancelar passagem comprada

<h4> Comunicação no Cliente </h4>

No arquivo *cliente_threads.py* podemos ter acesso as funções do cliente que são utilizadas para a sua conexão e comunicação com o servidor, sendo elas: *conectar()*, *desconectar()* e *enviar_dados()*

Na função *conectar()* é criado um socket para estabelecer a conexão TCP/IP com o servidor, as funções *socket.AF_INET* e *socket.SOCK_STREAM* são utilizadas para gerar este socket. Elas iram definir respesctivamente o protocolo de comunicação como IPv4 e o uso do protocolo TCP para a comunicação.

O HOST(endereço IP) e PORT(número da porta que o servidor esta escutando) são atribuidos ao cliente por meio da função connect, é impoprtante salientar que a configuração é feita de forma que o cliente e servidor terão a mesma porta e IP.

Para fechar a conexão é utilizada a função close em *desconectar()*, importante para que não exita nehum cliente oscioso ocupando recursos operacionais do software que podem ocasionar em problemas de desempenho.

Em *enviar_dados()* o dicionário em que são armazenadas as requisições enviadas pelo cliente é construindo, contendo o opcode e os dados a serem manipulados pelo servidor, o que pode incluir credenciais de login, indentificação de rotas, entre outros. Para enviar os dados ao servidor o socket utiliza a função sendall juntamente com um json.dumps, que transforma o dicionário construido para JSON.

Os dados são enfim codificados em bytes e enviados de forma garantida, devido ao uso da função sendall.

Para o recebimento da resposta enviada pelo servidor é utilizada a função recv(1024) dentro de um loop, é importante a utilização do loop while pois os dados podem ser recebidos de forma fracionada. É feita a junção da informação e esta é novamente carregada em um dicionário.

<h4> Comunicação no Servidor </h4>

Em *servidor_threads.py* podemos encontrar as funções de comunicação do servidor, são elas: *main()*, *tratar_cliente()*, *enviar_resposta()*. Na main é feita a abertura do socket nos mesmos moldes explicados anteriormente na parte do cliente, para garantir que o servidor seja reiniciado rapidamente sem interferências do sistema operacional é usada a função setsockopt, com os parâmetros SOL_SOCKET e SO_REUSADOR.

Para realizar o biding do socket do servidor a um IP e porta específicos, é utilizada a função bind. O endereço 0.0.0.0 é utilizado neste caso para garantir a aceitação de qualquer interface de rede.

Para cada novo cliente conectado ao servidor é criada uma nova thread, este processo e sua motivação serão explicados posteriomente.

É nencessário realizar a decodificação e tratamento das requisições enviadas pelo cliente, este processo é realizado em *tratar_cliente()*. A mensagem recebida em formato JSON é convertida para um dicionário, e o opcode extraído é alocado em condicionais que definirão o rumo de execução do servidor a partir da chamada de função pertinente a cada código recebido.

Para cada chamada feita é retornada uma resposta, decodificada e enviada de volta ao cliente em *enviar_resposta()*. O processo de construção do JSON é realizado, e este enviado em blocos de 1024 bytes conttrolados por um loop for.

O processo de controle de envio da mensagem em um loop do tipo for é importante para evitar que o buffer exceda o tamanho máximo permitido de bytes, garantindo que a mensagem seja enviada corretetamente ao cliente.

<h4> Paradigma de Comunicação </h4>

O stateful foi utilizado no projeto devido a necessidade de manter uma conexão contínua entre o cliente e servidor para manutenção dos dados durante a sessão mantida entre eles, os dados informados pelo cliente no login podem ser utilizados pelo servidor em quaisquer uma das situações que envolvem a compra ou o cancelamento de uma passagem.

Isto se faz necessário para manter a indentificação do cliente relacionada a estes processos no banco de dados do software, ou seja, é feito o gerenciamento de um estado longo de interação que pode ser modificado durante qualquer momento da conexão durante uma requisição.

<h3> Responsabilidades Gerais do Cliente e Servidor </h3>

Os arquivos *cliente_threads.py* e *servidor_threads.py* são também responsáveis pelas funções de interface a ser exibida ao cliente e lógica da aplicação, respectivamente. Funções de login e logout, compra e cancelamento de passagens, assim como os menus e inputs a serem visualizados pelo usuário estão presentes em *cliente_threads.py*.

Em *servidor_threads.py* as informações enviadas pelo usuário em cada uma das funções citadas acima serão decodificadas e manipularemos os dados necessários para executa-las corretamente.



<div id="conclusao">
<h2> Conclusão</h2>
<div align="justify">


</div>
</div>

<div id="execucaoProjeto">
<h2> Execução do Projeto</h2>
<div align="justify">


</div>
</div>

<div id="referencias">  
<h2> Referências</h2>
<div align="justify">

</div>
</div>