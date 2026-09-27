# Scoreboarding

Minha tentativa de criar um simulador do algoritmo *Scoreboarding*. Desenvolvido em `Python 3.10`.

## Execução
Para visualizar o estado final da tabela *Instruction Status*:
```bash
python main.py -p <program-file-path> -o <configuration-file-path>
```

Para visualizar os estados das tabelas *Functional Unit Status*, *Register Status* e *Instruction Status* em cada ciclo de clock:
```bash
python main.py -p <program-file-path> -o <configuration-file-path> --verbose
```

Para executar o simulador para todas as combinações entre arquivo de configuração e arquivo de instrução, respectivamente, nos diretórios `./configurations/` e `./programs/`:
```bash
bash run.sh
```
Estou considerando que todos os arquivos de configuração são `.txt`. Os *outputs* gerados são salvos na pasta `./outputs/`, com padrão de nome:
```
p<program-file-name>_c<configuration-file-name>.txt
```
