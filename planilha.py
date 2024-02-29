import pandas as pd
import datetime
import holidays

Pessoas = ["Victória",
"Afonso",
"Mateus",
"Amanda",
"Iago Silveira",
"Giovana",
"Fernando",
"Ana",
"Caio",
"Maria Raquel",
"Guilherme",
"Isabeli",
"Pedro"]

today = datetime.date.today() + datetime.timedelta(days=57)

last_day = today.replace(month=12, day=31)

data = []
add_two_days = True 

while today <= last_day:
    if add_two_days:
        today += datetime.timedelta(days=5)  
    else:
        today += datetime.timedelta(days=2)  
    data.append(today)
    add_two_days = not add_two_days


day_month = []
br_holidays = holidays.BR(years = 2024, subdiv = "SP",)

for i in data:
    somas = []
    somas.append(str(i.day))
    somas.append(str(i.month))
    dois = "/".join(somas)
    day_month.append(dois)


df = pd.DataFrame(
    {"Dias": day_month}
) 

df["Pessoas"] = None
df["Tipo"] = None

feriados = []

for holiday_date, holiday_name in sorted(br_holidays.items()):
    somas = []
    somas.append(str(holiday_date.day))
    somas.append(str(holiday_date.month))
    dois = "/".join(somas)
    feriados.append(dois)

print(feriados)

for i in range(len(df)):
    pessoa_index = i % len(Pessoas)  
    tipo = "Lab meeting" if i % 2 == 0 else "Journal Club"  
    df.at[i, 'Pessoas'] = Pessoas[pessoa_index]
    df.at[i, 'Tipo'] = tipo

for i in feriados:
    idx = df[df['Dias'] == i].index
    df.loc[idx, ['Pessoas', 'Tipo']] = "Feriado"

df.head()

pd.DataFrame.to_csv(df, "Planilha.csv")