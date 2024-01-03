# BCC-Senac | TCC
## Geração de mapas procedurais a partir de visão computacional
### Lucas da Silva Santos | Matheus Zanivan Andrade | Rafael Nascimento Lourenço

```sh
conda env create -n senac-tcc --file=environment.yml
conda activate senac-tcc
conda install pytorch==1.7.0 torchvision==0.8.0 torchaudio==0.7.0 cudatoolkit=10.2 cudatoolkit-dev -c pytorch -c conda-forge
pip install -r requirements.txt

cd src/efficientNet
python setup.py develop

cd ..
python setup.py develop
```
