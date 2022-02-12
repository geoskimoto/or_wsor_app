from flask import Flask, request, render_template, session, redirect
from utils import table_parser
import pandas as pd


app = Flask(__name__)

# df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
#                    'B': [5, 6, 7, 8, 9],
#                    'C': ['a', 'b', 'c--', 'd', 'e']})
df = table_parser('OR_BasinReports_2_2022.xlsx', 'BFcst', first_row=0)['Malheur']


@app.route('/', methods=("POST", "GET"))
def html_table():

    return render_template('simple.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
    # return render_template('simple.html',  tables=[df.to_html(classes='data', header="true", index=False)])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    print(df)