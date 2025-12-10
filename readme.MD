# 📅 Gerador de Planilha Automático criado para o CacaoLab
Uma ferramenta em Python eficiente e flexível para gerar cronogramas de reuniões, escalas de trabalho ou apresentações (como *Journal Clubs* e *Lab Meetings*). O script automatiza a distribuição de datas, respeita feriados e garante um sorteio justo entre os participantes.

## 🚀 Funcionalidades

* **Sorteio Justo (Fair Shuffle):** Garante que todos os participantes sejam escalados uma vez antes de qualquer repetição.
* **Gestão de Feriados:** Integração com a biblioteca `holidays` para identificar feriados brasileiros (nacionais e estaduais). Opção de pular o dia ou marcar como "Feriado" na planilha.
* **Seleção de Dias da Semana:** Configurável para gerar escalas em dias específicos (ex: apenas Segundas e Quintas).
* **Intervalo de Datas Dinâmico:** Aceita datas de início (hoje ou futuro) e fim personalizadas.
* **Exportação:** Gera a saída em um DataFrame do Pandas, pronto para exportação (CSV/Excel).

## 🛠️ Pré-requisitos

Para executar este projeto, você precisará ter o Python instalado e as seguintes bibliotecas:

* [pandas](https://pandas.pydata.org/)
* [holidays](https://pypi.org/project/holidays/)

### Instalação

Execute o comando abaixo no terminal para instalar as dependências:

```bash
pip install pandas holidays
````
---

## 📖 Como Usar

Salve o código da função principal em um arquivo (por exemplo, `gerador_escala.py`). Abaixo está um exemplo de como importar e utilizar a função.

```python
from gerador_escala import gerar_escala
from datetime import date

# 1. Defina o intervalo de datas
inicio = date.today()
fim = date(2025, 12, 31)

# 2. Defina os dias da semana (1=Segunda, 7=Domingo)
# Exemplo: Segundas (1) e Quintas (4)
dias_desejados = [1, 4]

# 3. (Opcional) Defina sua lista de pessoas
# Se não passar nada, usará a lista padrão configurada no script
minha_equipe = ["Ana", "Bruno", "Carlos", "Daniela"]

# 4. Gere a escala
df = gerar_escala(
    data_inicio=inicio, 
    data_fim=fim, 
    dias_semana=dias_desejados,
    pessoas=minha_equipe,
    pular_feriados=False, # Se False, o feriado aparece na lista. Se True, a linha é pulada.
    estado_feriado="SP"
)

# 5. Visualize ou Exporte
print(df.head())

# Exportando para CSV (compatível com Excel)
df.to_csv("Minha_Escala.csv", index=False, encoding='utf-8-sig')
```
---

## ⚙️ Parâmetros da Função

A função `gerar_escala` aceita os seguintes argumentos:

| Parâmetro | Tipo | Descrição | Padrão |
| :--- | :--- | :--- | :--- |
| `data_inicio` | `date` ou `str` | Data inicial da escala. | **Obrigatório** |
| `data_fim` | `date` ou `str` | Data limite da escala. | **Obrigatório** |
| `dias_semana` | `list[int]` | Dias da semana a ocupar (1=Seg, 7=Dom). | **Obrigatório** |
| `pessoas` | `list[str]` | Lista de nomes para sorteio. | `None` (Usa padrão) |
| `pular_feriados` | `bool` | Se `True`, não agenda nada no dia. Se `False`, marca como "Feriado". | `True` |
| `estado_feriado` | `str` | Sigla do estado para feriados regionais. | `"SP"` |

---

## 📄 Exemplo de Saída (CSV)

O arquivo gerado terá o seguinte formato:

| Data | Dia da Semana | Pessoa | Tipo |
| :--- | :--- | :--- | :--- |
| 10/06 | Segunda-feira | Bruno | Lab meeting |
| 13/06 | Quinta-feira | Ana | Journal Club |
| 17/06 | Segunda-feira | Daniela | Lab meeting |
| 20/06 | Quinta-feira | FERIADO | Corpus Christi |
| 24/06 | Segunda-feira | Carlos | Journal Club |

---

## 📝 Licença
Este projeto é de uso livre. Sinta-se à vontade para modificar e adaptar às necessidades do seu laboratório ou empresa.

