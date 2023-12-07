
# Capitulo 2
Será abordada uma breve fundamentação para compreensão do desenvolvimento.

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


