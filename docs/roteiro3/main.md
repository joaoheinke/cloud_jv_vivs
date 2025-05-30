





- onde de fato a gente cria a cliud
- uma estrutura de nuvem esta sendo criada --> poder de computacao, rede, processamento, armazenamento
- esta sendo criado uma nuvem privada --> algumas partes não estão prontas e eu tenho que criar pra colocar dentro da minha nuvem (AWS ja tem pronto)
- uma instancia e uma maquina virtual
- flavors no openstack--> configuracao da maquina (chama tipo de instancia na AWS)
- criamos a infraestrutura que o cliente que vai comprar a nuvem vai usar
- DNS traduz dominio pro IP
- -p é porta -- nao usa mais a porta 22 por padrao pra evitar que ataques acontecam na maquina
- https da protocolos de web
- rdp da interface grafica
- fizemos as brigdes em todas as maquinas e depois colocamos as tags exigidas em cada uma (controller, reservca, compute, compute)
- instalamos o controller no server1 (que recebeu a tag controller) com o comando:
juju bootstrap --bootstrap-series=jammy --constraints tags=controller maas-one maas-controller

- definimos o modelo de deploy
-- Internamente, o Juju reserva um namespace lógico (openstack) para agrupar as aplicações (charms), máquinas virtuais e relações que vão compor a nuvem OpenStack.
-- Muda o contexto de operação do seu client Juju para apontar ao model openstack no controller chamado maas-controller.
-- Após esse comando, todo comando juju status, juju deploy, juju add-machine etc. será executado no model openstack daquele controller, sem que você precise especificar de novo a qual controller/model está se referindo.

- a todo momento usando o comando 
watch -n 2 --color "juju status --color"
para conferir o status da instalacao do open stack



OSD (Object Storage Daemon)
Cada OSD é responsável por gerenciar e servir os dados armazenados em discos locais 
- criamos o arquivo ceph-osd.yaml que configura quais discos serão usados como OSDs (Object Storage Daemons) em todos os nós. 
com o conteudo 
ceph-osd:
  osd-devices: /dev/sda /dev/sdb
Ou seja, cada nó “compute” deverá usar /dev/sda e /dev/sdb para o Ceph.

-- comando de deploy :
juju deploy -n 3 --channel quincy/stable --config ceph-osd.yaml --constraints tags=compute ceph-osd
cria três unidades (units) da aplicação ceph-osd., aplica as configurações definidas no arquivo e escala as unidades somente em nós "compute"



NOVA COMPUTE
- o nova compute é o componente do OpenStack responsável por criar e gerenciar as máquinas virtuais nos servidores físicos.
- criamos o arquivo nova-compute.yaml
com o conteudo 
nova-compute:
  config-flags: default_ephemeral_format=ext4
  enable-live-migration: true
  enable-resize: true
  migration-auth-type: ssh
  virt-type: qemu

-- Instalar três cópias do serviço de computação. Forçar cada cópia a rodar nas máquinas físicas 0, 1 e 2. Usar a versão estável do OpenStack “Yoga”. Aplicar todas as configurações descritas no arquivo nova-compute.yaml.
juju deploy -n 3 --to 0,1,2 --channel yoga/stable --config nova-compute.yaml nova-compute

Mesmo com poucos servidores, conseguimos oferecer armazenamento e computação ao mesmo tempo, podemos mover máquinas virtuais sem tirá-las do ar e ajustar seus tamanhos e usar ext4 e SSH mantém tudo em formatos conhecidos e simplifica a administração.


MYSQL INNODB CLUSTER
O MySQL InnoDB Cluster exige sempre, no mínimo, três réplicas de banco de dados. O operador implanta a aplicação mysql-innodb-cluster em três nós, utilizando o charm correspondente. Cada instância será executada dentro de um container LXD nas máquinas identificadas como 0, 1 e 2. Para isso, utiliza-se o comando:
juju deploy -n 3 \
  --to lxd:0,lxd:1,lxd:2 \
  --channel 8.0/stable \
  mysql-innodb-cluster

que solicita três unidades da aplicação, direciona cada unidade para ser executada em um container LXD nas máquinas físicas 0, 1 e 2 e garante a instalação da versão estável 8.0 do MySQL.
Dessa forma, assegura-se alta disponibilidade e tolerância a falhas, pois o cluster mantém três cópias sincronizadas dos dados.




VAULT
Vault é responsável por gerar e gerenciar os certificados TLS que garantem comunicação criptografada entre os serviços da nuvem. Certificado TLS é um documento digital que vincula uma chaves criptográfica com uma identidade, garantindo conexão ao servidor para um cliente confiável, permite que o cliente e o servidor troquem dados sem possibilidade de interceptação externa e assegura integridade dos dados.

Para instalá-lo, utilizou-se o seguinte comando:
juju deploy --to lxd:2 vault --channel 1.8/stable

- para realizar o comando export VAULT_ADRESS usou-se o comando juju status pra identificar em qual máquina o Vault teria sido instalado. Verificou-se que o Vault foi instalado na máquina virtual do server5. 





















Passo 3: Rede Externa
Configure a rede externa. Usar uma faixa de alocação entre 172.16.7.0 e 172.16.8.255
Passo 4: Rede Interna e Roteador¶
Crie a rede interna e o roteador. Usar a subnet 192.169.0.0/24. Não use DNS.

na criacao da rede externa e da subrede, tivemos que criar um roteador pra conectar a rede interna com a externa





precisa de par de chaves porque quando ocorre a criação da maquina virtual, nao ha a permissao para acessá-la. Assim, o par de chaves insere uma chave publica do MAAS na maquina para que, assim, libere o acesso






[Seu Computador]
      │
      ▼
[Internet / VPN / Insper Wi-Fi]
      │
      ▼
[Firewall / Gateway do Insper]
      │
      ▼
+-----------------------+
|     Rede Interna      |
|  (ex: 10.246.112.0/21)|
+-----------------------+
      │
      ├──▶ [Servidor MAAS] 
      │
      └──▶ [Juju Controller]
               │
               ▼
       +------------------+
       |   OpenStack API  |
       | (Keystone, Nova, |
       |  Neutron, etc.)  |
       +------------------+
               │
               ▼
      +----------------------+
      |     Rede Externa     |
      |     (ext_net)        |
      +----------------------+
               │
            [Roteador]
               │
      +----------------------+
      |     Rede Interna     |
      |    (user1_net)       |
      +----------------------+
               │
               ▼
        [Sua Instância VM]
        (IP interno e opcional
         IP flutuante para SSH)







POS FOTOS
1. Diferenças entre os prints da Tarefa 1 e da Tarefa 2

Compute Overview (Visão Geral de Computação)

Tarefa 1: quotas de instâncias, vCPUs e RAM apareciam todas em zero.

Tarefa 2: quotas passaram a refletir o uso real — há 5 instâncias em execução, 5 vCPUs ocupadas e 5 GB de RAM alocados.

Compute Instances (Instâncias)

Tarefa 1: lista vazia (nenhuma instância criada).

Tarefa 2: cinco instâncias listadas — “postgres”, “nginx”, “api1”, “api2” e “client” — todas no flavor m1.small (exceto “client”, m1.tiny), com IP interno (192.169.0.x) e floating IP (172.16.7.x ou 172.16.8.x).

Network Topology (Topologia de Rede)

Tarefa 1: apenas as duas “colunas” (rede externa e interna) conectadas pelo roteador.

Tarefa 2: além do roteador, agora aparecem ícones de porta ligando cada instância à rede interna, e ícones de floating IPs na coluna externa.

Security Groups & Floating IPs

Tarefa 1: apenas o grupo default com as regras básicas (SSH e ICMP) recém-criadas, sem IPs flutuantes atribuídos.

Tarefa 2: quota de regras de segurança aumentada (foram adicionadas 12 regras), e 5 floating IPs alocados e associados.

2. Como cada recurso foi criado

Flavors

Executado uma vez no início, pela CLI:

m1.tiny (1 vCPU, 1 GB RAM, 20 GB)

m1.small (1 vCPU, 2 GB RAM, 20 GB)

Rede Externa

Rede “ext-net” marcada como externa, com faixa 172.16.7.0/24.

Pool de alocação configurado para fornecer floating IPs de 172.16.7.100–172.16.8.254.

Rede Interna

Rede “client-net” (ou “user1-net”) criada com subnet 192.169.0.0/24, sem DNS.

Roteador Virtual

Roteador “router1” criado e associado à rede externa (“ext-net”) e à rede interna.

Key-pair

A chave pública id_rsa.pub importada como “maas-key”, para permitir SSH sem senha.

Security Group Default

Pelo Horizon (Admin → Rede → Grupos de Segurança) ou CLI, adicionadas regras para SSH (TCP/22) e ICMP (ping) liberadas para 0.0.0.0/0.

Instâncias

Para cada serviço (“postgres”, “nginx”, “api1”, “api2”, “client”):

openstack server create --flavor <flavor> --image jammy-amd64 --nic net-id=<internal-net-id> --key-name maas-key <nome>

“client” usou flavor m1.tiny; as demais, m1.small.

Floating IPs

Cinco endereços flutuantes gerados na rede externa e associados, um para cada instância, garantindo acesso SSH público.

Todos esses comandos foram executados no terminal do nó main, e as alterações refletidas em tempo real no Horizon, conforme mostram os prints da Tarefa 2.


























