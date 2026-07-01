# Introdução e Notas de Aprendizado: Linguagem C

Nesta semana, tive o meu primeiro contato prático com a sintaxe e a estrutura da Linguagem C. A transição da lógica puramente visual (blocos) para uma linguagem textual e compilada trouxe novos conceitos fundamentais sobre o funcionamento dos computadores.

## Principais Conceitos Aprendidos

* **Estrutura Básica e Boilerplate:** Compreendi a necessidade de incluir bibliotecas padrão (como `#include <stdio.h>`) para habilitar funções de entrada e saída, além da obrigatoriedade da função principal `int main()`, que serve como o ponto de partida para a execução de qualquer programa em C.
* **Tipagem Estática e Variáveis:** Diferente de modelos mais flexíveis, em C é obrigatório declarar explicitamente o tipo de dado que uma variável vai armazenar (como `int` para inteiros, `float` para números reais e `char` para caracteres) antes de utilizá-la. A variável funciona como uma "caixa" de tamanho fixo na memória do computador.
* **Entrada e Saída de Dados:** Aprendi a utilizar a função `printf()` para exibir informações na tela e a função `scanf()` para capturar o que o usuário digita. O uso do operador `&` (E comercial) no `scanf` foi um conceito novo importante, servindo para indicar o endereço de memória onde o valor deve ser guardado.

## Reflexão sobre o Progresso

A maior diferença e dificuldade inicial em relação ao Code.org foi a rigidez da sintaxe. Esquecer um ponto e vírgula (`;`) ou errar um caractere de formatação (como `%d` ou `%f`) faz com que o código não compile. No entanto, passar por esse processo foi fundamental para entender como o computador organiza as informações na memória e como as instruções são processadas passo a passo.
