Boa noite a todos, hoje eu Matheus, O lucas e o Rafael vamos apresentar o nosso trabalho de conclusão de curso que tem o tema de geração procedural de mapas para Jogos através de técnicas de Segmentação de Imagem.

# Capitulo 1

## Introdução

Vamos começar falando sobre a indústria de jogos digitais que vem crescendo a cada ano e cada vez mais tempo é necessário para desenvolvimento de jogos, uma parte em especial do desenvolvimento são os mapas, que são responsáveis por trazer imersão e a sensação de progresso na jornada do jogo.

E geração procedural de mapa tem um papel de enriquecimento na experiencia e interação com o mundo do jogador, um exemplo de jogo que utiliza como pilar a geração procedural mapa é o Minecraft.

E uma das técnicas para geração procedural de mapas é o diagrama de Voronoi que no ramo de Geometria Computacional é um dos tópicos mais discutidos.

Agora em Inteligência Artificial o ramo de segmentação de imagens está em ascensão e também é muito comum utilizar a geração procedural em conjunto com a inteligência artificial para melhorar e personalizar a experiencia do jogador trazendo história e cenários únicos.

Para criar esses mapas existem técnicas e algoritmos que fazem esse papel e por isso gostaríamos de adicionar a nossa contribuição, desenvolvendo um programa capaz de segmentar e gerar um mapa através da seleção do usuário.

E para juntar tudo temos como hipótese de que quanto maior for a quantidade de pontos no diagrama de Voronoi maior será a precisão.

## Objetivos

E temos os seguintes objetivos

- Selecionar e analisar conjuntos de dados contendo classes relevantes, como pessoas, carros, entre outros, para treinar um modelo de rede neural convolucional específico para segmentação de imagens.

- Utilizar algoritmos para criar diagramas de Voronoi.

- Aplicar um algoritmo para reconhecer a imagem com o contorno selecionado e gerar como resultado a imagem do mapa gerado.

- Utilizar o resultado da segmentação para selecionar indicar o que é terreno em cima do diagrama de Voronoi.

- Gerar os biomas no diagrama de Voronoi.

- Criar testes em prol de mensurar a semelhança entre o contorno do mapa gerado com o contorno escolhido.

# Capitulo 2
Será abordada uma breve fundamentação para compreensão do desenvolvimento.

## Geração procedural de conteúdo

A geração procedural de conteúdo constitui-se de métodos e automações para gerar conteúdo em jogos.

### Diagrama de Voronoi

O diagrama de Voronoi é gerado a partir de um conjunto de pontos onde é calculada distancia euclidianas entre de os pontos vizinhos e pego a interseção do ponto médio da distancia.
A formala a seguir descrive uma região de Voronoi, onde pi são os pontos, e de é a distancia euclidiana.
Nessa imagem conseguimos ver a relação do conjunto de pontos com o diagrama.

### Geração de biomas no diagrama de Voronoi

Primeiro biomas são regiões ecológicas que possuem fauna e flora semelhantes.

Agora para gerar biomas no diagrama de Voronoi é necessario dividir a terra e o mar, calcular a elevação e umidade para cada poligono.

#### Diagrama de Whittaker

E para parte final é utilizar tanto a umidade quanto a elevação em um diagrama de Whittaker (Apontar para imagem), onde para é feito uma classificação do bioma de acordo com a elevação e a umidade.

E por final teremos um resultado parecidos com esse (Apontar para imagem)

## Visão computacional
Uma área que visa interpretação de imagens por meio de algoritmos e técnicas de processamento de imagens.
Para representar uma imagem no computador utiliza-se uma matriz para tal, em uma imagem preto e branco tem apenas 1 canal então só tem uma matriz para simbolizar a cor de cada pixel. Já em rgb tem três canais para representar o RGB.

![Alt text](image-1.png)

Dentre técnicas de processamento de imagem cabe ressaltar a imagem ou máscara binária, que cria um foco em algum objeto da imagem, sendo o alvo a parte branca e o fundo preto, tendo apenas duas tonalidades como a imagem de resultado.

Além disso será abordado dois algoritmos com propostas parecidas para selecionar um objeto e
destaca-lo em uma imagem binária. Preenchimento por inundação e por cor.

Por cor se baseia em percorrer todos os pixeis da imagem e destacar quando for da mesma faixa de cor inicial.

Preenchimento por inundação é um algoritmo de
expansão a partir de um pixel, validando se contém a mesma faixa de cor.

E para proporcionar essa interação com a imagem existe a biblioteca PyQt5 que possibilita criação de interfaces em Python.

## Inteligência artificial

É uma tentativa de simular o pensamento humano com processamento computacional, dentro dela existe o aprendizado de máquina que detecta padrões importantes de
uma base de dados e dentro existe a rede neural artificial que é uma representação matemática de unidades de processamento conectadas chamadas de neurônios artificiais. Dentro disso existe a área de rede neural convolucional que visa  detectar padrões em imagens contendo uma camada convolucional para extrair matematicamente um mapa de características. Dentro disso existe área de segmentação que visa separar em conjuntos a imagem, existem três principais ramos sendo eles: segmentação semântica que classifica os pixeis da imagem, a segmentação de instância detecta todos objetos separadamente e a segmentação panóptica junta as duas anteriores para ter uma solução mais completa.

![Alt text](image.png)

O artigo denominado segmentação panóptica definiu o conceito desse tipo de segmentação e uma métrica para mensurar a qualidade do modelo de segmentação panóptica chamada de qualidade panóptica PQ. Além disso existem alguns conjuntos de dados para essa solução como Cityscapes, Indian Drive Dataset, Mapilary vistas entre outros, e todos esses estão em um contexto urbano.

Dentro de segmentação com rede neural convolucional existem diversas métricas e técnicas para mensurar a qualidade dos modelos, a principal técnica é criar uma classificação de conjuntos no qual terá os verdadeiros positivos e verdadeiros negativos que é quando o pixel da imagem de predição tem a mesma classificação da imagem verdade e os Falsos negativos e falsos positivos são os erros encontrados na imagem verdade e predição respectivamente.

Por motivos de pesquisa e área de atuação maior escolheu-se a segmentação panóptica para aplicar, portanto restou selecionar o modelo.

Para isso usou-se a tabela do Cityscapes mostrando os modelos de segmentação panóptica que melhor classificam a classe de pessoas. Em primeiro observa-se o EfficientPS que é uma solução eficiente para essa segmentação.


## Trabalhos relacionados

### Panoptic segmentation
Trabalho citado anteriormente que definiou a segmentação panóptica, demonstrou a classificação de conjuntos que serviu para outras métricas e criou uma métricar para mensurar a qualidade de um modelo de segmentação panóptica.


### EfficientPS
Trabalho citado anteriormente com um solução de segmentação panóptica eficiente que cria diversos contextos de resolução para montar uma saída para segmentação de instância e outro para segmentação semântica e depois juntar tudo no módulo de fusão inovador e uma nova função de perda que visa equilibrar as coisas e objetos na segmentação e por fim gerar a saída panóptica.

### Polygonal Map Generation for Games

Trabalho citado anteriormente sobre como gerar mapas procedurais utilizando diagrama de Voronoi e o diagrama de Whittaker.

# Capitulo 3

## Proposta

O nosso trabalho se propôs em criar um protótipo para geração de mapas procedurais, basicamente o usuário seleciona uma imagem, escolhe o método de segmentação, seleciona o local ou a área que será usado como entrada para gerar o mapa, no meio desse processo é gerado um diagrama de Voronoi e o algoritmo irá escolher quais áreas serão terra e oceano com base na seleção e é escolhido os biomas conforme a elevação e umidade e por fim é apresentado na tela o resultado.

## Segmentar imagens

Para implementação vamos começar por segmentação, que utilizamos 2 técnicas.

A primeira utilizada é o EfficientPS que é uma solução eficiente para segmentar imagens, nós utilizamos um modelo pretreinado, a ideia principal era treinar mais esse modelo, mas surgiram diversos desafios e limitações como conseguir autorização de conjunto de dados, preparar esse conjunto de dados e limitações de hardware. Nós tivemos esse primeiro resultado (Apontar para imagem 1), o que não era esperado pois os objetos de mesmas classes possuem a mesma cor, nós tínhamos a expectativa de o resultado da segmentação fosse parecido com esse (Apontar para imagem 2), então nós fomos ao repositório oficial e encontramos uma proposta que explicava como fazer essa alteração e conseguimos essa imagem de resultado (Apontar para imagem 3), mas percebemos que não era satisfatório, porque não conseguíamos distinguir de quais classes pertenciam os objetos.

A segundo é a seleção por contorno que consiste em isolar uma área da imagem, que você pode ou selecionar por cor, onde todo local que contiver a cor escolhida será selecionado, ou por preenchimento de inundação que é um algoritmo que expande pela cor seleciona com um faixa delimitadora.

E para usar esse segmento da imagem temos a imagem binária que é uma imagem de saída de ambos os algoritmos, ela possui pixels brancos, que é o contorno selecionado, e os pretos representam nada.

## Geração procedural do mapa

Agora vamos falar sobre a implementação do algoritmo de geração procedural de mapas

### Ilha gerada no contorno

Antes de tudo vamos falar como gerar o diagrama de Voronoi, nessa imagem (Apontar para imagem 1) tem essa demonstração, basicamente é selecionado um conjunto de pontos vizinhos através de um disco no ponto, após isso é calculado o ponto médio entre o ponto e seus vizinhos, nesses pontos médios é feita uma reta perpendicular, onde houver uma intersecção é adicionado um ponto e assim gerando um polígono, fazendo isso para todos os pontos é gerado o diagrama de Voronoi, nessa outra imagem conseguimos ver um primeiro polígono já gerado através daqueles passos.

Depois que nós temos o diagrama marcamos todos os polígonos como terra e precisamos utilizar a imagem binaria gerada anteriormente como entrada, usamos o OpenCV para desenhar o polígono do diagrama em uma outra imagem que vai ser comparada com a imagem binária, esse processo gera uma outra imagem, se ela contiver pontos o polígono é marcado como terra, esse processo é repetido para todos os polígonos. Com isso temos um mapa com terra e mar separados, o próximo passo é definir o litoral, que são os polígonos que tocam o mar, essencialmente percorre-se todos os polígonos fazendo essa verificação.

E agora é calcular a elevação, é feito uma busca em profundidade que começa em todo vértice de polígono que tocam a borda do mapa, inicialmente todos os vértices têm a elevação infinita e após a busca é definido um valor que começa em 0 nas bordas e vai subindo até o centro do mapa.

E para calcular a umidade primeiro é gerado os rios, para isso é verificado os vértices próximos a corpos d’água que possuem uma altura maior que um valor mínimo definido, após isso é selecionado de forma pseudoaleatória a quantidade de vértices e para cada um é verificado o tipo de terreno, se for do tipo terra é definido aresta como rio. Com isso para calcular a umidade verificado todos os polígonos que estão próximos de um corpo d’agua, e são adicionados em uma fila que será usada para fazer uma busca em profundidade, todos os polígonos que são corpos d’agua terão a umidade máxima e os do tipo terra é calculado conforme a distância e um fator multiplicador, e assim temos a umidade para cada polígono.

Para selecionar o bioma de cada polígono temos o diagrama de Whittaker modificado, onde cada polígono é verificado a umidade e a elevação se tiver dentro dos valores do bioma, esse bioma é escolhido, basicamente é um monte de ifs e elses.

### Unity - Mapa 3d e Terreno

Como saída temos dois resultados, o mapa com biomas e rios e o mapa de altura que é utilizado com entrada para um mapa 3D, basicamente esse mapa de altura é uma imagem onde 0 representa a altura mínima e 255 a altura máxima. Essa imagem foi utilizada no motor gráfico Unity onde utilizou-se o a ferramenta Terrain Tools que utiliza o mapa de altura para criar os relevos no mapa 3D e também o Terrain Toolkit 2017 que é um script que altera a textura conforme a elevação do terreno.

### Minimapa

Para o minimapa utilizou-se o mapa 2D onde foi feito um script que possibilita localizar o jogador com base no mundo 3D.

### Jogabilidade

E para a jogabilidade foi criado um personagem com scripts de movimentação e assim foi possível visualizar o mapa tridimensionalmente.

## Testes

Criou-se testes para avaliar a qualidade de combinações de imagens, incluindo a imagem de entrada da geração procedural e as imagens de saída: sendo elas: o mapas de altura e  o mapas 2D.
A avaliação de qualidade baseou-se na técnica de classificação de conjuntos gerando uma nova imagem categorizando pixeis.

em Verdadeiros Positivos, Verdadeiros Negativos, Falsos Positivos e Falsos Negativos e salvando-a.

A partir disso conta-se os pixeis de cada conjunto para utilizar as métricas.
F1 Score, Coeficiente de Correlação de Matthews, União sobre Interseção, Acurácia, Taxa de Descoberta Falsa, Taxa de Falso Negativo.

Além disso, uma métrica para medir o desfoque em uma imagem foi aplicada, detectando bordas em x e y, calculando o gradiente e resultando no desvio padrão para mensurar a harmonia do mapa de alturas.

e também a duração do tempo de execução em segundos do código, focando na parte de geração procedural dos mapas.

Foi desenvolvido um teste genérico para facilitar a reprodução em diferentes cenários, permitindo a definição de diversas combinações de imagens e métricas.

## Pos processamento

Criou-se alguns testes para avaliar o modelo e identificar erros e soluções, o primeiro erro encontrado foi no mapa em 3d que não ficou harmonico, então aplicou-se um desfoque no mapa de altura para gerar essa harmonia e após melhorar isso percebeu-se que piorou os resultados na imagem de classificação de conjuntos, aumentando o erro destacado em vermelho que vem diretamente do mapa de altura, então aplicou-se outros testes para redimensionar a imagem e adicionar uma borda de forma que reduzi-se esses erros porém melhorando o caso do mapa em 3d

## Interface gráfica

Utilizou-se a biblioteca Pyqt5 para criar as telas nas quais o usuário possa interagir com as imagens e gerar os mapas.

Tem como funcionalidades abrir a imagem, processar com EfficientPS, permitir selecionar um contorno e exibir o resultado da geração procedural

Usou-se loading e opções para threads para permitir selecionar imagem e clicar apos o resultado da segmentação panóptica.

# Capitulo 4
Os resultados serão apresentados por meio de tabelas que englobam testes com todas as combinações de imagens, incluindo uma imagem com os resultados finais e outra com todos os passos da aplicação.

 A Tabela 6 compara a imagem de entrada com o mapa 2D utilizando como iterador o número de pontos no diagrama de Voronoi e as métricas,União sobre Interseção (IoU), Acurácia (Acc), F1 Score (F1), Coeficiente de Correlação de Matthews (MCC), Taxa de Descoberta Falsa (FDR), Taxa de Falso Negativo (FNR) além do tempo de execução do código em segundos.

 Essa tabela desempenha um papel crucial ao evidenciar, com base em dados concretos, a semelhança entre o mapa 2D e o contorno do mapa de entrada. Além disso, sustenta a hipótese de que um maior número de pontos no mapa resulta em melhor desempenho. Tendo nas 4 primeiras métricas um resultado maior quando aumenta os pontos, o que é bom pois nelas quanto maior melhor, já nas duas últimas métricas vai diminuindo o erro se somar eles. Vale ressaltar que quanto mais pontos maior a duração também.

![](image-2.png)

A tabela 7 tem uma comparação entre a imagem de entrada e o mapa de altura, e tem a mesma estrutura da tabela anterior além de resultados bem parecidos como tendo nas 4 primeiras métricas um resultado maior quando aumenta e nas duas últimas métricas vai diminuindo o erro se somar eles. e também quanto mais pontos maior a duração.

![Alt text](image-3.png)

A tabela 8 mantém a estrutura e colunas porém compara o mapa 2d com o 3d  e nesse caso mantém um resultado aceitável em todas métricas pois eles são baseados na mesma saída logo não ocorre tantas variações com o aumento de pontos. O que favorece para a utilização dessas saídas em conjunto como previsto.

![Alt text](image-4.png)

A Figura 38 ilustra a classificação dos conjuntos para cada combinação. Sendo a imagem (a) a representação da última execução do cenário da Tabela 6. A imagem (b) retrata a última execução do cenário da Tabela 7. Por fim, a imagem (c) mostra a última execução do cenário da Tabela 8.

![Alt text](image-5.png)

A Figura 39 apresenta os passos da execução do programa Python. As imagens incluem a captura da interface gráfica com PyQt5 (a), a abertura de uma imagem para segmentação (b), a execução do modelo EfficientPS na imagem selecionada (c), a saída da segmentação panóptica (d), o carregamento pós-seleção do usuário (e), o resultado do mapa 2D com o contorno escolhido (f), a automação usando Unity para atualizar um terreno com o mapa de altura gerado (g) e, por fim, uma captura de tela do Unity rodando a aplicação, abrindo o minimapa e marcando a localização atual do personagem (h).

![](image-6.png)

## Análise dos resultados

Com base nos dados das Tabelas 6 e 7, confirma-se a validade da hipótese inicial, pois há uma correlação positiva entre a quantidade de pontos no diagrama de Voronoi e a compatibilidade com o contorno. A presença de mais pontos resulta em polígonos menores no diagrama, levando a uma maior precisão na definição dos tipos de terreno.

A duração da geração procedural, no entanto, aumenta com o número de pontos, sendo crucial avaliar o cenário de processamento para determinar o melhor custo-benefício. A eficácia do método é respaldada pelas ilustrações na Figura 39, especialmente na última execução com 300 pontos, onde erros (vermelho e verde) são mínimos e acertos (branco e cinza) predominam.

A Tabela 8 reforça a confiabilidade entre a imagem 2D (minimapa) e o mapa de altura (formador do mapa 3D), sustentando a funcionalidade de localização em tempo real dentro da execução do jogo.

# Capitulo 5

A monografia apresenta uma solução para criar mapas 2D e 3D a partir do contorno de uma imagem usando segmentação panóptica, dividida em seis fases: segmentação de imagens, seleção de contornos, geração procedural de mapas, testes de eficácia, análise de pós-processamento e integração via interface gráfica.

Dentre os trabalhos relacionados, panoptic segmentation, foi fundamental para entender o conceito desse tipo inovador de segmentação além de dar base as métricas que utilizou-se para mensurar as segmentações. O EfficientPS ajudou muito pois é um modelo eficiente e pronto para essa solução e o Map generation for games auxiliou para a geração procedural do mapa com biomas.

O objetivo de aproximar o mapa gerado do contorno inicial foi alcançado, comprovando a eficácia da abordagem. E também a hipótese da relação entre adicionar mais pontos no diagrama de Voronoi e melhorar os resultados se comprovou.


Porém o o tempo de execução, pode ser desafiador em cenários com poder de processamento inferior. A dependência da biblioteca CUDA Toolkit pode limitar a aplicabilidade.

Para melhorias futuras, sugere-se a utilização de modelos de segmentação panóptica multiplataforma, a implementação de paralelismo e rasterização para otimizar o tempo de execução, e a realização de testes com outros métodos de geração procedural. A proposta pode evoluir para oferecer resultados mais eficientes e acessíveis, abrindo possibilidades para desenvolvedores e consumidores de jogos.