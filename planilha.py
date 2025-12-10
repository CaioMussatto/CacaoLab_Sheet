import pandas as pd
from datetime import date, timedelta
import holidays
import random
from itertools import cycle
from typing import List, Optional, Union

# Lista padrão para caso o usuário não forneça uma nova
LISTA_PADRAO_PESSOAS = [
    "Victória", "Afonso", "Mateus", "Amanda", "Iago Silveira",
    "Giovana", "Fernando", "Ana", "Caio", "Maria Raquel",
    "Guilherme", "Isabeli", "Pedro"
]

def gerar_escala_reunioes(
    data_inicio: Union[str, date],
    data_fim: Union[str, date],
    dias_semana: List[int],
    pessoas: Optional[List[str]] = None,
    sortear: bool = False,
    pular_feriados: bool = True,
    estado_br: str = "SP",
    tipos_reuniao: List[str] = ["Lab meeting", "Journal Club"]
) -> pd.DataFrame:
    """
    Gera uma escala de reuniões baseada em datas, dias da semana e lista de pessoas.

    Args:
        data_inicio: Data inicial (objeto date ou string 'YYYY-MM-DD').
        data_fim: Data final (objeto date ou string 'YYYY-MM-DD').
        dias_semana: Lista de inteiros representando os dias (1=Segunda, ..., 7=Domingo).
        pessoas: Lista de nomes. Se None, usa a lista padrão.
        sortear: Se True, embaralha a lista de pessoas antes de gerar a escala.
        pular_feriados: Se True, não agenda nada no feriado. Se False, marca como "Feriado".
        estado_br: Sigla do estado para feriados regionais (ex: 'SP', 'RJ').
        tipos_reuniao: Lista de tipos para alternar (ex: Lab Meeting, Journal Club).

    Returns:
        pd.DataFrame: DataFrame contendo a escala gerada.
    """

    # 1. Padronização das datas
    if isinstance(data_inicio, str):
        data_inicio = date.fromisoformat(data_inicio)
    if isinstance(data_fim, str):
        data_fim = date.fromisoformat(data_fim)

    if data_inicio > data_fim:
        raise ValueError("A data de início não pode ser maior que a data de fim.")

    # 2. Configuração de Feriados e Pessoas
    calendario_feriados = holidays.BR(years=range(data_inicio.year, data_fim.year + 2), subdiv=estado_br)
    
    lista_pessoas = pessoas.copy() if pessoas else LISTA_PADRAO_PESSOAS.copy()
    
    if sortear:
        random.shuffle(lista_pessoas) # Embaralha in-place sem repetir nomes no ciclo inicial

    # Criamos iteradores cíclicos (eles giram infinitamente)
    ciclo_pessoas = cycle(lista_pessoas)
    ciclo_tipos = cycle(tipos_reuniao)

    agenda = []
    cursor_data = data_inicio

    # 3. Loop de Geração (Dia a Dia)
    while cursor_data <= data_fim:
        # isoweekday: 1=Segunda, 7=Domingo
        if cursor_data.isoweekday() in dias_semana:
            
            data_formatada = cursor_data.strftime("%d/%m/%Y")
            e_feriado = cursor_data in calendario_feriados
            nome_feriado = calendario_feriados.get(cursor_data)

            if e_feriado:
                if not pular_feriados:
                    # Se não for pular, registra o feriado na planilha
                    agenda.append({
                        "Data": data_formatada,
                        "Dia da Semana": cursor_data.strftime("%A"),
                        "Pessoa": "FERIADO",
                        "Tipo": f"Feriado ({nome_feriado})"
                    })
                # Se pular_feriados=True, simplesmente não fazemos nada (o loop continua)
            else:
                # Dia útil de reunião
                agenda.append({
                    "Data": data_formatada,
                    "Dia da Semana": cursor_data.strftime("%A"), # Opcional: nome do dia
                    "Pessoa": next(ciclo_pessoas),
                    "Tipo": next(ciclo_tipos)
                })

        cursor_data += timedelta(days=1)

    # 4. Criação e Tratamento do DataFrame
    df_escala = pd.DataFrame(agenda)

    # Tradução opcional dos dias da semana (pandas gera em inglês por padrão dependendo do locale)
    traducao_dias = {
        'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta',
        'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
    }
    if not df_escala.empty:
        df_escala['Dia da Semana'] = df_escala['Dia da Semana'].map(traducao_dias).fillna(df_escala['Dia da Semana'])
    
    return df_escala

# --- Exemplo de Uso ---

if __name__ == "__main__":
    # Configurações
    hoje = date.today()
    fim_do_ano = date(2025, 12, 31)
    
    # 1 = Segunda, 3 = Quarta, 5 = Sexta
    dias_selecionados = [2, 4]  # Ex: Terças (2) e Quintas (4)

    try:
        df_resultado = gerar_escala_reunioes(
            data_inicio=hoje,
            data_fim=fim_do_ano,
            dias_semana=dias_selecionados,
            sortear=True,          # Randomiza a ordem inicial
            pular_feriados=True,   # Pula dias de feriado (mantém a fila andando)
            estado_br="SP"
        )

        print(f"Escala gerada com {len(df_resultado)} encontros.")
        print(df_resultado.head(10))

        # Salvar
        df_resultado.to_csv("Escala_Profissional.csv", index=False, sep=";", encoding="utf-8-sig")
        print("\nArquivo 'Escala_Profissional.csv' salvo com sucesso.")

    except Exception as e:
        print(f"Erro ao gerar escala: {e}")
