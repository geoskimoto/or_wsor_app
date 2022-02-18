from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from utils import table_parser, snowpack_parser, style_BFcst, style_Res, style_Snow, style_Snowpack
from dash import html
# import pandas as pd
import base64

app = Flask(__name__)
CORS(app)

wkbk = 'OR_BasinReports_2_2022.xlsx'
basin = 'Owyhee'

BFcst = table_parser(wkbk, 'BFcst', first_row=0)
# df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
#                    'B': [5, 6, 7, 8, 9],
#                    'C': ['a', 'b', 'c--', 'd', 'e']})
# table_parser(wkbk, 'BFcst', first_row=0)['Owyhee']
BFcst = table_parser(wkbk, 'BFcst', first_row=0)
BRes = table_parser(wkbk, 'BRes', first_row=0)
BSnow = table_parser(wkbk, 'BSnow', first_row=0)
# BPrec = table_parser(wkbk, 'BPrecip', first_row=0)
# BFcst_plot = base64.b64encode(open("OWYHEE January 1 2021.png", 'rb').read())
# BFcst_plot_layout = html.Img(src=f'data:image/png;base64,{BFcst_plot}')


BFcst = style_BFcst(BFcst, basin)
BRes = style_Res(BRes, basin)
BSnow = style_Snow(BSnow, basin)
Snowpack = style_Snowpack(snowpack_parser(wkbk, basin))
# BPrec_df = BPrec['Owyhee']




@app.route('/Owyhee', methods=("POST", "GET"))
@cross_origin()
def html_table():

    return render_template('simple.html',
                           # BFcst_plot=BFcst_plot_layout,
                           BFcst_df=[BFcst.to_html(classes='data')],
                           BRes_df=[BRes.to_html(classes='data')],
                           BSnow_df=[BSnow.to_html(classes='data')],
                           Snowpack_df=[Snowpack.to_html(classes='data')],
                           # BPrec_df=[BPrec.to_html(classes='data')],
                           Basin='Owyhee',
                           Month='February'
                           )
    # return render_template('simple.html',  tables=[df.to_html(classes='data', header="true", index=False)])

if __name__ == '__main__':
    # print(df)
    app.run(host='0.0.0.0', debug=True)
