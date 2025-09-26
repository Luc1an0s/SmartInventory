# SmartInventory

🔧 Projeto de automação para monitoramento inteligente de estoque, desenvolvido em Python e SQLite, com execução diária automatizada via GitHub Actions.

## Descrição

O SmartInventory é um sistema simples, eficiente e seguro para controle de estoque, pensado para mostrar como é possível criar soluções robustas sem depender de interfaces gráficas. O foco está na automação real e na engenharia de dados, utilizando boas práticas de desenvolvimento e segurança.

## Principais Recursos

- ✅ **Geração de dados fictícios**: Criação automática de mais de 150 produtos para simulação de cenários reais.
- ✅ **Verificação automática de estoque crítico**: Identificação de produtos com estoque abaixo do mínimo definido.
- ✅ **Envio de alertas por e-mail**: Notificações automáticas para responsáveis, utilizando variáveis de ambiente para proteger credenciais.
- ✅ **Agendamento diário**: Execução automatizada do sistema via GitHub Actions, garantindo monitoramento contínuo.

## Tecnologias Utilizadas

- Python
- SQLite
- GitHub Actions

## Como funciona

1. O sistema gera uma base de dados fictícia (`estoque.db` e `estoque.xlsx`) com produtos e seus respectivos estoques.
2. Diariamente, o script verifica quais produtos estão com estoque abaixo do mínimo.
3. Caso haja produtos críticos, um alerta é enviado por e-mail automaticamente.
4. Todo o processo é agendado e executado via GitHub Actions, sem necessidade de intervenção manual.

## Segurança

- As credenciais de e-mail são protegidas por variáveis de ambiente.
- O projeto segue boas práticas de automação e manipulação de dados sensíveis.

## Como executar localmente

1. Clone o repositório:
	```bash
	git clone https://github.com/Luc1an0s/SmartInventory.git
	```
2. Instale as dependências necessárias (se houver).
3. Configure as variáveis de ambiente para o envio de e-mails.
4. Execute o script principal:
	```bash
	python automation.py
	```

## Automação com GitHub Actions

O workflow de automação está configurado para rodar diariamente, garantindo que o estoque seja monitorado sem falhas.

## Contribuição

Sugestões, melhorias e novas ideias são sempre bem-vindas! Se você trabalha com tecnologia, dados ou DevOps, vamos trocar ideias.

## Licença

Este projeto está sob a licença MIT.

