import pandas as pd

df = pd.read_csv(r'C:\Users\TETYANA\Desktop\Транспорт\output.csv')

print(df["odometer"][0])