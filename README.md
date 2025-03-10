# Sistema de Gestão Hospitalar (SGH)

## Introdução

O projeto tem como objetivo o desenvolvimento de um Sistema de Gestão Hospitalar (SGH), que visa otimizar e coordenar as operações dentro de uma unidade de saúde. O sistema será responsável por gerenciar diversos aspectos da administração hospitalar, como agendamento de consultas, internamentos, prescrições de medicamentos, faturação e alocação de recursos.

## Descrição

O Sistema de Gestão Hospitalar (SGH) tem como objetivo principal centralizar as operações de gestão dentro de um hospital. Ele permitirá:

- **Gestão de consultas e internamentos**: Os assistentes poderão agendar consultas e internamentos (cirúrgicos ou não cirúrgicos) e atribuir os recursos necessários, como médicos e enfermeiros.
- **Prescrição de medicamentos**: O sistema irá registrar as prescrições de medicamentos e seus efeitos secundários.
- **Faturação**: O SGH gerenciará a faturação de consultas e internamentos, incluindo a atualização das faturas.
- **Gestão de recursos materiais e humanos**: Atribuição de camas, quartos e recursos materiais, além de garantir que os médicos e enfermeiros sejam alocados corretamente para evitar conflitos.

## Funcionalidades Principais

### Transações

O SGH inclui várias transações que devem ser tratadas como unidades atômicas:

- **Marcação de Consulta**: O sistema cria registos na tabela de Consultas e atribui médicos.
- **Internamento (Cirúrgico/Não Cirúrgico)**: Regista internamentos, atribuindo médicos e enfermeiros.
- **Prescrição de Medicamentos**: Regista a prescrição e administração de medicamentos.
- **Faturação**: Geração de faturas para consultas e internamentos.
- **Pagamentos**: Registra pagamentos correspondentes às faturas emitidas.
- **Atualização de Dados do Paciente**: Atualizações nos dados dos pacientes são tratadas como transações.

### Conflitos de Concorrência

O SGH trata de potenciais conflitos de concorrência, como:

- **Disponibilidade de Recursos Humanos**: Previne a sobreposição de horários de médicos.
- **Concorrência para Acesso aos Dados**: Garante que múltiplos usuários não acessem os mesmos dados simultaneamente, usando bloqueios de registros e mecanismos de isolamento.
- **Prescrição e Administração de Medicamentos**: Garante que os medicamentos prescritos não sejam administrados de forma duplicada.
- **Atribuição de Recursos Materiais**: Previne conflitos na atribuição de quartos e camas.

## Plano de Desenvolvimento

### 1. Análise de Requisitos e Design Inicial
- Definição dos requisitos do sistema.
- Elaboração do diagrama ER e modelo de dados.

### 2. Implementação da Estrutura da Base de Dados
- Criação das tabelas conforme o modelo de dados.
- Definição das chaves primárias e estrangeiras.

### 3. Desenvolvimento das Funcionalidades Principais
- Implementação das funcionalidades de agendamento de consultas e cirurgias.
- Desenvolvimento do sistema de prescrição e administração de medicamentos.

### 4. Implementação da Lógica de Negócio e Controle de Concorrência
- Desenvolvimento da lógica de gestão de conflitos.
- Implementação dos mecanismos de controle de concorrência.

### 5. Testes e Depuração
- Realização de testes unitários e de integração.
- Depuração e otimização do código.

### 6. Documentação e Entrega Final
- Elaboração do relatório final do projeto.
- Preparação para a apresentação do projeto.

## Cronograma

- **Semana 1-2**: Análise de Requisitos e Design Inicial.
- **Semana 3-4**: Implementação da Estrutura da Base de Dados.
- **Semana 5-7**: Desenvolvimento das Funcionalidades Principais.
- **Semana 8-9**: Implementação da Lógica de Negócio e Controle de Concorrência.
- **Semana 10-11**: Testes e Depuração.
- **Semana 12**: Documentação e Entrega Final.

## Conclusão

Este projeto visa melhorar a eficiência na gestão de hospitais, otimizando processos, garantindo a integridade dos dados e permitindo uma melhor coordenação de recursos. O desenvolvimento da base de dados e a implementação de transações e controle de concorrência são elementos cruciais para o sucesso do SGH.
