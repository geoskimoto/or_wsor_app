from flask import Flask, request, render_template, session, redirect
from utils import table_parser, style_BFcst, style_Res, style_Snow
import pandas as pd


app = Flask(__name__)

BFcst = table_parser('OR_BasinReports_2_2022.xlsx', 'BFcst', first_row=0)
# df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
#                    'B': [5, 6, 7, 8, 9],
#                    'C': ['a', 'b', 'c--', 'd', 'e']})
# table_parser('OR_BasinReports_2_2022.xlsx', 'BFcst', first_row=0)['Owyhee']
BFcst = table_parser('OR_BasinReports_2_2022.xlsx', 'BFcst', first_row=0)
BRes = table_parser('OR_BasinReports_2_2022.xlsx', 'BRes', first_row=0)
BSnow = table_parser('OR_BasinReports_2_2022.xlsx', 'BSnow', first_row=0)
# BPrec = table_parser('OR_BasinReports_2_2022.xlsx', 'BPrecip', first_row=0)

BFcst_df = style_BFcst(BFcst, 'Owyhee')
BRes_df = style_Res(BRes, 'Owyhee')
BSnow_df = style_Snow(BSnow, 'Owyhee')
# BPrec_df = BPrec['Owyhee']


@app.route('/Owyhee', methods=("POST", "GET"))
def html_table():

    return render_template('simple.html',
                           BFcst_df=[BFcst_df.to_html(classes='data')],
                           BRes_df=[BRes_df.to_html(classes='data')],
                           BSnow_df=[BSnow_df.to_html(classes='data')],
                           # BPrec_df=[BPrec_df.to_html(classes='data')],
                           titles='Owyhee'
                           )
    # return render_template('simple.html',  tables=[df.to_html(classes='data', header="true", index=False)])

if __name__ == '__main__':
    # print(df)
    app.run(host='0.0.0.0', debug=True)
