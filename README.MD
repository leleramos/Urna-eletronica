# 🗳️ Urna Eletrônica em Python

Sistema de votação eletrônica desenvolvido em Python com integração ao banco de dados MariaDB/MySQL, simulando o funcionamento de uma urna eletrônica real.

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MariaDB-MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen?style=for-the-badge)

---

## 📋 Sobre o Projeto

Este projeto foi desenvolvido como atividade acadêmica com o objetivo de simular o processo de uma urna eletrônica, contemplando:

- **Registro de candidatos** com número, nome e partido
- **Cadastro de eleitores** com título de eleitor validado (12 dígitos)
- **Votação** com garantia de integridade (cada eleitor vota apenas uma vez)
- **Apuração dos votos** com porcentagens, destaque do vencedor e detecção de empate
- **Modo demonstração** que executa 10 votações automáticas (requisito do enunciado)

Todo o sistema é executado via terminal com um menu interativo e persistência em banco de dados relacional.

---

## ✨ Funcionalidades

| # | Funcionalidade | Descrição |
|---|----------------|-----------|
| 1 | Cadastrar candidato | Registra número, nome e partido (com validação de número inteiro) |
| 2 | Listar candidatos | Exibe todos os candidatos ordenados por número |
| 3 | Cadastrar eleitor | Valida título de eleitor (12 dígitos numéricos únicos) |
| 4 | Votar | Eleitor escolhe um candidato; sistema impede voto duplicado |
| 5 | Apurar votos | Exibe votos, porcentagens, vencedor (🏆) ou empate (🤝) |
| 6 | Candidatos de exemplo | Carrega 5 candidatos fictícios para testes rápidos |
| 7 | Modo demonstração | Executa 10 votações automáticas (atende ao requisito do enunciado) |
| 8 | Sair | Encerra o sistema |

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+** — linguagem principal
- **PyMySQL** — driver de conexão com o banco
- **MariaDB / MySQL** — banco de dados relacional

---

## 📁 Estrutura do Projeto

```
urna-eletronica/
│
├── urna.py                      # Menu principal (ponto de entrada)
├── README.md                    # Documentação do projeto
│
├── banco_dados/
│   ├── criar_banco.py           # Cria o banco de dados
│   ├── criar_tabelas.py         # Cria as tabelas
│   ├── teste_conexao.py         # Testa a conexão com o banco
│   └── limpar_dados.py          # Zera votos e eleitores (auxiliar)
│
├── sistema/
│   ├── cadastrar_candidatos.py  # Cadastro e listagem de candidatos
│   ├── eleitores.py             # Cadastro de eleitores
│   ├── votacao.py               # Registro de votos
│   └── apuracao.py              # Apuração e resultado
│
└── extras/
    ├── seed.py                  # Candidatos de exemplo
    └── demo.py                  # Modo demonstração (10 votos)
```

### 🗄️ Modelo do Banco de Dados

**Banco:** `urna_eletronica`

#### Tabela `candidatos`
| Coluna | Tipo | Restrições |
|--------|------|------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT |
| `numero` | INT | NOT NULL, UNIQUE |
| `nome` | VARCHAR(100) | NOT NULL |
| `partido` | VARCHAR(50) | — |

#### Tabela `eleitores`
| Coluna | Tipo | Restrições |
|--------|------|------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT |
| `identificacao` | VARCHAR(30) | NOT NULL, UNIQUE (título de eleitor) |
| `votou` | BOOLEAN | NOT NULL, DEFAULT FALSE |

#### Tabela `votos`
| Coluna | Tipo | Restrições |
|--------|------|------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT |
| `eleitor_id` | INT | NOT NULL, UNIQUE, FOREIGN KEY → `eleitores(id)` |
| `candidato_id` | INT | NOT NULL, FOREIGN KEY → `candidatos(id)` |
| `data_voto` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

> A **restrição `UNIQUE`** em `eleitor_id` é a garantia no nível do banco de que cada eleitor só pode registrar **um único voto**.

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- MariaDB ou MySQL instalado e em execução
- `pip` disponível

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU-USUARIO/urna-eletronica.git
cd urna-eletronica
```

### 2. Instalar dependências

```bash
pip install pymysql
```

### 3. Configurar o banco

O projeto assume por padrão:

- Host: `localhost`
- Porta: `3306`
- Usuário: `root`
- Senha: *(vazia)*
- Banco: `urna_eletronica`

Se a sua configuração for diferente, ajuste os dados de conexão nos arquivos `.py` (função `conectar_banco()`).

### 4. Criar o banco e as tabelas

```bash
python criar_banco.py
python criar_tabelas.py
```

### 5. (Opcional) Testar a conexão

```bash
python teste_conexao.py
```

### 6. Executar a urna

```bash
python urna.py
```

> 💡 No Windows, se `python` não for reconhecido, use `py urna.py`.

---

## 🎮 Como Usar

Ao iniciar o sistema, o seguinte menu é exibido:

```
===== URNA ELETRÔNICA =====
1 - Cadastrar candidato
2 - Listar candidatos
3 - Cadastrar eleitor
4 - Votar
5 - Apurar votos
6 - Carregar candidatos de exemplo
7 - Modo demonstração (10 votos automáticos)
8 - Sair
```

### Fluxo básico de teste

1. **Opção 6** — Carregue candidatos de exemplo (atalho para testes)
2. **Opção 7** — Rode o modo demonstração para gerar 10 votos automaticamente
3. A apuração é exibida no final, com destaque para o vencedor ou empate

### Fluxo manual

1. **Opção 1** — Cadastre um ou mais candidatos
2. **Opção 3** — Cadastre um eleitor (título de 12 dígitos, ex.: `123456789012`)
3. **Opção 4** — Vote informando o título e o número do candidato
4. **Opção 5** — Veja a apuração completa

---

## 🖼️ Exemplo de Saída

### Apuração com vencedor único

```
===== APURAÇÃO DOS VOTOS =====

Número: 10
Candidato: Ana Silva
Partido: Partido A
Total de votos: 5 (50.0%)

Número: 22
Candidato: Carla Mendes
Partido: Partido C
Total de votos: 3 (30.0%)

...
------------------------------
Total geral de votos: 10

===== RESULTADO =====
🏆 VENCEDOR:
   Número: 10
   Nome: Ana Silva
   Partido: Partido A
   Votos: 5 (50.0%)
```

### Apuração com empate

```
===== RESULTADO =====
🤝 EMPATE entre:
   - Ana Silva (número 10) — 2 votos (20.0%)
   - Carla Mendes (número 22) — 2 votos (20.0%)
   - Beatriz Silva (número 33) — 2 votos (20.0%)
```

---

## 🛡️ Integridade do Processo

O sistema garante a integridade da votação em **duas camadas**:

1. **Aplicação:** antes de registrar o voto, verifica se o eleitor já votou (`votou = TRUE`) e recusa a segunda tentativa.
2. **Banco de dados:** restrição `UNIQUE` na coluna `eleitor_id` da tabela `votos` impede duplicação mesmo em caso de falha da camada de aplicação.

Isso atende ao requisito do enunciado de *"permitir que cada eleitor vote apenas uma vez"*.

---

## 🧪 Modo Demonstração

A opção **7** executa **10 iterações de votação automáticas**, atendendo ao requisito do enunciado de *"realizar, no mínimo, 10 iterações de votação"*.

O modo demonstração:

- Cria 10 eleitores fictícios com títulos únicos de 12 dígitos
- Distribui os votos **aleatoriamente** entre os candidatos cadastrados
- Exibe o progresso em tempo real
- Ao final, oferece exibir a apuração automaticamente

**⚠️ Proteção:** o modo demonstração só é executado se **não houver votos registrados** no sistema, evitando misturar dados reais com dados de teste. Para limpar, use o `limpar_dados.py`.

---

## 👩‍💻 Autora

**lETICIA** — Estudante de Análise E Desenvolvimento De Sistemas
📧 [TICI.RAAMOS@GMAIL.COM]  
🔗 [github.com/SEU-USUARIO](https://github.com/leleramos)

---

## 📄 Licença

Este projeto foi desenvolvido para fins **acadêmicos**. Sinta-se livre para estudar, adaptar e reutilizar o código.

---

<p align="center">
  Feito com 💙 e Python
</p>