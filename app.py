import os
import pdfkit
from flask import Flask, render_template, make_response
# from flask_cors import CORS, cross_origin
from utils import table_parser, snowpack_parser, style_BFcst, style_Res, style_Snow, style_Snowpack
from dash import html
# import pandas as pd
import base64

app = Flask(__name__)
# CORS(app)

wkbk = 'OR_BasinReports_2_2022.xlsx'

# basin = 'Owyhee'
# basin = 'Rogue-Umpqua'
# basin = 'Willamette'
# basin = 'Klamath'
# basin = 'Hood-Sandy-Lower Deschutes'
# basin = 'Upper Deschutes-Crooked'
# basin = 'Lake County-Goose Lake'
# basin = 'John Day'
# basin = 'Harney'
# basin = 'Umatilla-Walla Walla-Willow'
# basin = 'Grande Ronde-Burnt-Powder-Imna'  ###fix me!!
# basin = 'Malheur'

@app.route('/Deschutes/<month>', methods=("POST", "GET"))
# @cross_origin()
def Deschutes(month):
    basin = 'Upper Deschutes-Crooked'
    # basin = str(basin)
    BFcst = table_parser(wkbk, 'BFcst', first_row=0)
    BRes = table_parser(wkbk, 'BRes', first_row=0)
    BSnow = table_parser(wkbk, 'BSnow', first_row=0)

    BFcst = style_BFcst(BFcst, basin)
    BRes = style_Res(BRes, basin)
    BSnow = style_Snow(BSnow, basin)
    Snowpack = style_Snowpack(snowpack_parser(wkbk, basin))
    rendered = render_template('Deschutes.html',
                           BFcst_df=[BFcst.to_html(classes='data')],
                           BRes_df=[BRes.to_html(classes='data')],
                           BSnow_df=[BSnow.to_html(classes='data')],
                           Snowpack_df=[Snowpack.to_html(classes='data')],
                           # BPrec_df=[BPrec.to_html(classes='data')],
                           Basin=basin,
                           Month=month
                          )
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename = {basin}_{month}_2022.pdf'

    return response

# @app.route('/GrandeRonde/<month>', methods=("POST", "GET"))
# # @cross_origin()
# def GrandeRonde(month):
#     basin = 'Grande Ronde-Burnt-Powder-Imnaha'
#     # basin = str(basin)
#     BFcst = table_parser(wkbk, 'BFcst', first_row=0)
#     BRes = table_parser(wkbk, 'BRes', first_row=0)
#     BSnow = table_parser(wkbk, 'BSnow', first_row=0)
#
#     BFcst = style_BFcst(BFcst, basin)
#     BRes = style_Res(BRes, basin)
#     BSnow = style_Snow(BSnow, basin)
#     Snowpack = style_Snowpack(snowpack_parser(wkbk, basin))
#     rendered = render_template('GrandeRonde.html',
#                            BFcst_df=[BFcst.to_html(classes='data')],
#                            BRes_df=[BRes.to_html(classes='data') if BRes is not None else ''],
#                            BSnow_df=[BSnow.to_html(classes='data')],
#                            Snowpack_df=[Snowpack.to_html(classes='data')],
#                            # BPrec_df=[BPrec.to_html(classes='data')],
#                            Basin=basin,
#                            Month=month
#                           )
#     config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
#
#     pdf = pdfkit.from_string(rendered, False, configuration=config)
#
#     response = make_response(pdf)
#     response.headers['Content-Type'] = 'application/pdf'
#     response.headers['Content-Disposition'] = f'inline; filename = {basin}_{month}_2022.pdf'
#
#     return response


@app.route('/Harney/<month>', methods=("POST", "GET"))
# @cross_origin()
def Harney(month):
    basin = 'Harney'
    # basin = str(basin)
    BFcst = table_parser(wkbk, 'BFcst', first_row=0)
    BRes = table_parser(wkbk, 'BRes', first_row=0)
    BSnow = table_parser(wkbk, 'BSnow', first_row=0)

    BFcst = style_BFcst(BFcst, basin)
    BRes = style_Res(BRes, basin)
    BSnow = style_Snow(BSnow, basin)
    Snowpack = style_Snowpack(snowpack_parser(wkbk, basin))
    rendered = render_template('Harney.html',
                           BFcst_df=[BFcst.to_html(classes='data')],
                           BSnow_df=[BSnow.to_html(classes='data')],
                           Snowpack_df=[Snowpack.to_html(classes='data')],
                           # BPrec_df=[BPrec.to_html(classes='data')],
                           Basin=basin,
                           Month=month
                          )
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename = {basin}_{month}_2022.pdf'

    return response

@app.route('/Hood/<month>', methods=("POST", "GET"))
# @cross_origin()
def Hood(month):
    basin = 'Hood-Sandy-Lower Deschutes'
    # basin = str(basin)
    BFcst = table_parser(wkbk, 'BFcst', first_row=0)
    BRes = table_parser(wkbk, 'BRes', first_row=0)
    BSnow = table_parser(wkbk, 'BSnow', first_row=0)

    BFcst = style_BFcst(BFcst, basin)
    BRes = style_Res(BRes, basin)
    BSnow = style_Snow(BSnow, basin)
    Snowpack = style_Snowpack(snowpack_parser(wkbk, basin))
    rendered = render_template('Hood.html',
                           BFcst_df=[BFcst.to_html(classes='data')],
                           BRes_df=[BRes.to_html(classes='data')],
                           BSnow_df=[BSnow.to_html(classes='data')],
                           Snowpack_df=[Snowpack.to_html(classes='data')],
                           # BPrec_df=[BPrec.to_html(classes='data')],
                           Basin=basin,
                           Month=month
                          )
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename = {basin}_{month}_2022.pdf'

    return response

@app.route('/JohnDay/<month>', methods=("POST", "GET"))
# @cross_origin()
def JohnDay(month):
    basin = 'John Day'
    # basin = str(basin)
    BFcst = table_parser(wkbk, 'BFcst', first_row=0)
    BRes = table_parser(wkbk, 'BRes', first_row=0)
    BSnow = table_parser(wkbk, 'BSnow', first_row=0)

    BFcst = style_BFcst(BFcst, basin)
    BRes = style_Res(BRes, basin)
    BSnow = style_Snow(BSnow, basin)
    Snowpack = style_Snowpack(snowpack_parser(wkbk, basin))
    rendered = render_template('JohnDay.html',
                           BFcst_df=[BFcst.to_html(classes='data')],
                           BSnow_df=[BSnow.to_html(classes='data')],
                           Snowpack_df=[Snowpack.to_html(classes='data')],
                           # BPrec_df=[BPrec.to_html(classes='data')],
                           Basin=basin,
                           Month=month
                          )
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename = {basin}_{month}_2022.pdf'

    return response

@app.route('/Klamath/<month>', methods=("POST", "GET"))
# @cross_origin()
def Klamath(month):
    basin = 'Klamath'
    # basin = str(basin)
    BFcst = table_parser(wkbk, 'BFcst', first_row=0)
    BRes = table_parser(wkbk, 'BRes', first_row=0)
    BSnow = table_parser(wkbk, 'BSnow', first_row=0)

    BFcst = style_BFcst(BFcst, basin)
    BRes = style_Res(BRes, basin)
    BSnow = style_Snow(BSnow, basin)
    Snowpack = style_Snowpack(snowpack_parser(wkbk, basin))
    rendered = render_template('Klamath.html',
                           BFcst_df=[BFcst.to_html(classes='data')],
                           BRes_df=[BRes.to_html(classes='data')],
                           BSnow_df=[BSnow.to_html(classes='data')],
                           Snowpack_df=[Snowpack.to_html(classes='data')],
                           # BPrec_df=[BPrec.to_html(classes='data')],
                           Basin=basin,
                           Month=month
                          )
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename = {basin}_{month}_2022.pdf'

    return response

@app.route('/LakeCounty/<month>', methods=("POST", "GET"))
# @cross_origin()
def LakeCounty(month):
    basin = 'Lake County-Goose Lake'
    # basin = str(basin)
    BFcst = table_parser(wkbk, 'BFcst', first_row=0)
    BRes = table_parser(wkbk, 'BRes', first_row=0)
    BSnow = table_parser(wkbk, 'BSnow', first_row=0)

    BFcst = style_BFcst(BFcst, basin)
    BRes = style_Res(BRes, basin)
    BSnow = style_Snow(BSnow, basin)
    Snowpack = style_Snowpack(snowpack_parser(wkbk, basin))
    rendered = render_template('LakeCounty.html',
                           BFcst_df=[BFcst.to_html(classes='data')],
                           BRes_df=[BRes.to_html(classes='data')],
                           BSnow_df=[BSnow.to_html(classes='data')],
                           Snowpack_df=[Snowpack.to_html(classes='data')],
                           # BPrec_df=[BPrec.to_html(classes='data')],
                           Basin=basin,
                           Month=month
                          )
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename = {basin}_{month}_2022.pdf'

    return response

@app.route('/Malheur/<month>', methods=("POST", "GET"))
# @cross_origin()
def Malheur(month):
    basin = 'Malheur'
    # basin = str(basin)
    BFcst = table_parser(wkbk, 'BFcst', first_row=0)
    BRes = table_parser(wkbk, 'BRes', first_row=0)
    BSnow = table_parser(wkbk, 'BSnow', first_row=0)

    BFcst = style_BFcst(BFcst, basin)
    BRes = style_Res(BRes, basin)
    BSnow = style_Snow(BSnow, basin)
    Snowpack = style_Snowpack(snowpack_parser(wkbk, basin))
    rendered = render_template('Malheur.html',
                           BFcst_df=[BFcst.to_html(classes='data')],
                           BRes_df=[BRes.to_html(classes='data')],
                           BSnow_df=[BSnow.to_html(classes='data')],
                           Snowpack_df=[Snowpack.to_html(classes='data')],
                           # BPrec_df=[BPrec.to_html(classes='data')],
                           Basin=basin,
                           Month=month
                          )
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename = {basin}_{month}_2022.pdf'

    return response

@app.route('/Owyhee/<month>', methods=("POST", "GET"))
# @cross_origin()
def Owyhee(month):
    basin = 'Owyhee'
    # basin = str(basin)
    BFcst = table_parser(wkbk, 'BFcst', first_row=0)
    BRes = table_parser(wkbk, 'BRes', first_row=0)
    BSnow = table_parser(wkbk, 'BSnow', first_row=0)

    BFcst = style_BFcst(BFcst, basin)
    BRes = style_Res(BRes, basin)
    BSnow = style_Snow(BSnow, basin)
    Snowpack = style_Snowpack(snowpack_parser(wkbk, basin))
    rendered = render_template('Owyhee.html',
                           BFcst_df=[BFcst.to_html(classes='data')],
                           BRes_df=[BRes.to_html(classes='data')],
                           BSnow_df=[BSnow.to_html(classes='data')],
                           Snowpack_df=[Snowpack.to_html(classes='data')],
                           # BPrec_df=[BPrec.to_html(classes='data')],
                           Basin=basin,
                           Month=month
                          )
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename = {basin}_{month}_2022.pdf'

    return response

@app.route('/Rogue/<month>', methods=("POST", "GET"))
# @cross_origin()
def Rogue(month):
    basin = 'Rogue-Umpqua'
    # basin = str(basin)
    BFcst = table_parser(wkbk, 'BFcst', first_row=0)
    BRes = table_parser(wkbk, 'BRes', first_row=0)
    BSnow = table_parser(wkbk, 'BSnow', first_row=0)

    BFcst = style_BFcst(BFcst, basin)
    BRes = style_Res(BRes, basin)
    BSnow = style_Snow(BSnow, basin)
    Snowpack = style_Snowpack(snowpack_parser(wkbk, basin))
    rendered = render_template('Rogue.html',
                           BFcst_df=[BFcst.to_html(classes='data')],
                           BRes_df=[BRes.to_html(classes='data')],
                           BSnow_df=[BSnow.to_html(classes='data')],
                           Snowpack_df=[Snowpack.to_html(classes='data')],
                           # BPrec_df=[BPrec.to_html(classes='data')],
                           Basin=basin,
                           Month=month
                          )
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename = {basin}_{month}_2022.pdf'

    return response

@app.route('/Umatilla/<month>', methods=("POST", "GET"))
# @cross_origin()
def Umatilla(month):
    basin = 'Umatilla-Walla Walla-Willow'
    # basin = str(basin)
    BFcst = table_parser(wkbk, 'BFcst', first_row=0)
    BRes = table_parser(wkbk, 'BRes', first_row=0)
    BSnow = table_parser(wkbk, 'BSnow', first_row=0)

    BFcst = style_BFcst(BFcst, basin)
    BRes = style_Res(BRes, basin)
    BSnow = style_Snow(BSnow, basin)
    Snowpack = style_Snowpack(snowpack_parser(wkbk, basin))
    rendered = render_template('Umatilla.html',
                           BFcst_df=[BFcst.to_html(classes='data')],
                           BRes_df=[BRes.to_html(classes='data')],
                           BSnow_df=[BSnow.to_html(classes='data')],
                           Snowpack_df=[Snowpack.to_html(classes='data')],
                           # BPrec_df=[BPrec.to_html(classes='data')],
                           Basin=basin,
                           Month=month
                          )
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename = {basin}_{month}_2022.pdf'

    return response

@app.route('/Willamette/<month>', methods=("POST", "GET"))
# @cross_origin()
def Willamette(month):

    basin = 'Willamette'
    BFcst = table_parser(wkbk, 'BFcst', first_row=0)
    BRes = table_parser(wkbk, 'BRes', first_row=0)
    BSnow = table_parser(wkbk, 'BSnow', first_row=0)

    BFcst = style_BFcst(BFcst, basin)
    BRes = style_Res(BRes, basin)
    BSnow = style_Snow(BSnow, basin)
    Snowpack = style_Snowpack(snowpack_parser(wkbk, basin))
    rendered = render_template('Willamette.html',
                           BFcst_df=[BFcst.to_html(classes='data')],
                           BRes_df=[BRes.to_html(classes='data')],
                           BSnow_df=[BSnow.to_html(classes='data')],
                           Snowpack_df=[Snowpack.to_html(classes='data')],
                           # BPrec_df=[BPrec.to_html(classes='data')],
                           Basin=basin,
                           Month=month
                          )
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename = {basin}_{month}_2022.pdf'

    return response


#











#-------------single template-------------------


# @app.route('/<string:basin>/<month>', methods=("POST", "GET"))
# # @cross_origin()
# def html_table(basin, month):
#
#     # basin = str(basin)
#     BFcst = table_parser(wkbk, 'BFcst', first_row=0)
#     BRes = table_parser(wkbk, 'BRes', first_row=0)
#     BSnow = table_parser(wkbk, 'BSnow', first_row=0)
#
#     BFcst = style_BFcst(BFcst, basin)
#     BRes = style_Res(BRes, basin)
#     BSnow = style_Snow(BSnow, basin)
#     Snowpack = style_Snowpack(snowpack_parser(wkbk, basin))
#     rendered = render_template('simple.html',
#                            BFcst_df=[BFcst.to_html(classes='data')],
#                            BRes_df=[BRes.to_html(classes='data') if BRes is not None else ''],
#                            BSnow_df=[BSnow.to_html(classes='data')],
#                            Snowpack_df=[Snowpack.to_html(classes='data')],
#                            # BPrec_df=[BPrec.to_html(classes='data')],
#                            Basin=basin,
#                            Month=month
#                           )
#     config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
#
#     pdf = pdfkit.from_string(rendered, False, configuration=config)
#
#     response = make_response(pdf)
#     response.headers['Content-Type'] = 'application/pdf'
#     response.headers['Content-Disposition'] = f'inline; filename = {basin}_{month}_2022.pdf'
#
#     return response


if __name__ == '__main__':
    # print(basin)

    app.run(host='0.0.0.0', debug=True)
