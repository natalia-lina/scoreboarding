# scoreboarding

Natália, você está tendo um problema dentro da função `write`. O objeto `current_state`, que não recebe qualquer atribuição, está todo fodido mudando de valor sozinho, quando apenas `future_stage` deveria ser mudado. Tem cara de eu estar me embanando com a forma que o Python lida com nomes de variaveis e endereços de memoria de fato. O Joao tinha perguntado se eu estava alterando a tabela diretamente ou se estava encapsulado. Acho que era nesse problema que ele estava pensando! 

Para amanhã, então, bora tentar encapsular essas porra. Eu quero fazer com que o `current_time` seja sempre imutável (read-only).

https://www.reddit.com/r/learnpython/comments/1ggr6d5/why_is_the_wrong_variable_updating/

https://nedbatchelder.com/text/names