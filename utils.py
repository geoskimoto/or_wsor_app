from collections import OrderedDict
from functools import reduce
import datetime as dt
import re
import pandas as pd
import numpy as np


#-------------Function that parses each worksheet from the cloudkiller using empty rows as separators----------------

def table_parser(spreadsheet, sheet_name, first_row=0):
    if sheet_name == 'BFcst':
        xl = pd.ExcelFile(spreadsheet)
        BFcst = xl.parse(sheet_name='BFcst')
        # mask = BFcst.apply(lambda x: x.str.contains(r'exceedance', na=False))
        # BFcst.loc[mask.any(axis=1)]

        # Removing unnecessary footers using key word from each bullet point.
        BFcst = BFcst[~BFcst.iloc[:, 0].str.contains("exceedance", na=False)]
        BFcst = BFcst[~BFcst.iloc[:, 0].str.contains("Forecasts", na=False)]
        BFcst = BFcst[~BFcst.iloc[:, 2].str.contains("Forecast", na=False)]

        # Subbasin names are above data in their own row.  Shift them down a row.
        BFcst.iloc[:, 0] = BFcst.iloc[:, 0].shift(1)

        # Delete rows that are entirely null:
        BFcst.dropna(how='all', inplace=True)

        # Since many rows were dropped and indices inconsistent now, reset them.
        BFcst.reset_index(inplace=True)
        BFcst.drop(columns='index', inplace=True)

        # Define a row to separate basins.  Choosing the header rows that have "Forecast \n Period" in them.
        separator_rows = BFcst[BFcst.iloc[:, 1].str.contains("Forecast \n Period", na=False)].index.tolist()
        first_row = 0
        last_row = len(BFcst.index)
        separator_rows.insert(0, first_row)
        separator_rows.append(last_row)

        # Use separator_rows to parse tables.
        basins = [BFcst.loc[separator_rows[i] + 1, :][0] for i in range(len(separator_rows) - 1)]
        Tables = OrderedDict([basin, []] for basin in basins)
        for i in range(len(separator_rows[0:-1])):
            try:
                table = BFcst.iloc[separator_rows[i]:separator_rows[i + 1], :]
                # table.columns = list(table.iloc[1,0]) + list(table.iloc[0,:])
                table.columns = [table.iloc[1, 0], 'Forecast Period', '90% (KAF)', '70% (KAF)', '50% (KAF)', '% Median',
                                 '30% (KAF)', '10% (KAF)', '30yr Median (KAF)']
                table = table.iloc[2:, :]
                # table.iloc[:,0] = table.iloc[:,0].fillna(method='ffill', axis=0)
                # table.iloc[:,0] = table.iloc[:,0].replace(" ", float('NaN'), inplace=True)
                table.iloc[:, 0] = table.iloc[:, 0].replace(np.nan, '', regex=True)
                Tables.update({basins[i]: table})
            except:
                pass
        return Tables


    else:
        xl = pd.ExcelFile(spreadsheet)
        sheet = xl.parse(sheet_name=sheet_name)

        # Use indices for empty row breaks between tables to parse tables.
        # First replace empty cells with NaNs
        sheet.replace(np.nan, '', regex=True)

        # Find indices (i.e. empty rows)
        separator_rows = sheet[sheet.iloc[:, 0].isnull()].index.tolist()
        # empty_row_indices_bw_tables = sheet[sheet.iloc[:,0].isnull()].index.tolist()

        # Method above excludes first and last rows, so need to add to list.
        last_row = len(sheet.index)  # xl.book.sheet_by_name(sheet_name).nrows
        separator_rows.insert(0, first_row)
        separator_rows.append(last_row)

        # Grabs names of basins from sheet using empty rows as a reference.
        basins = [sheet.loc[separator_rows[i] + 1, :][0] for i in range(len(separator_rows) - 1)]
        Tables = OrderedDict([basin, []] for basin in basins)
        for i in range(len(separator_rows[0:-1])):
            try:
                table = xl.parse(sheet_name=sheet_name, skiprows=separator_rows[i] + 2,
                                 skipfooter=last_row - separator_rows[i + 1] - 1).replace(np.nan, '', regex=True)

                # Remove "/n" from column indices
                clean_columns = pd.Series(list(table.columns)).replace(r'\n', ' ', regex=True).to_list()
                table.columns = clean_columns

                Tables.update({basins[i]: table})
            except:
                pass
        # The above for loop excludes the last table, so have to add it in manually for now.
        table = xl.parse(sheet_name=sheet_name, skiprows=separator_rows[-2] + 2).replace(np.nan, '', regex=True)
        clean_columns = pd.Series(list(table.columns)).replace(r'\n', ' ', regex=True).to_list()
        table.columns = clean_columns

        Tables.update({basins[-1]: table})

        return Tables


#-----------------Query Function for retrieving medians from BSnow, BPrec, and BRes-------------------------------

def median_table(spreadsheet):
  BSnow = table_parser(spreadsheet, 'BSnow')
  BPrecip = table_parser(spreadsheet, 'BPrecip')
  BRes = table_parser(spreadsheet, 'BRes')

  # basin_list = list(BSnow.keys())
  basin_list = ['Owyhee', 'Malheur', 'Grande Ronde-Burnt-Powder-Imnaha', 'Umatilla-Walla Walla-Willow', 'John Day', 'Upper Deschutes-Crooked', 'Hood-Sandy-Lower Deschutes', 'Willamette', 'Rogue-Umpqua', 'Klamath', 'Lake County-Goose Lake', 'Harney']
  snow_medians = []
  for i in basin_list:
    filter = BSnow[i].iloc[:, 0] == 'Basin Index'
    medians = BSnow[i][filter].loc[:,['% Median', 'Last Year % Median']]
    snow_medians.append(medians)

  snow_medians = pd.concat(snow_medians)
  snow_medians.index = basin_list
  snow_medians.columns = ['WTEQ % Median', 'Last Year WTEQ % Median']

  prec_medians = []
  for i in basin_list:
    filter = BPrecip[i].iloc[:, 0] == 'Basin Index'
    medians = BPrecip[i][filter].loc[:,['% Median', '% Median.1']]
    prec_medians.append(medians)

  prec_medians = pd.concat(prec_medians)
  prec_medians.index = basin_list
  prec_medians.columns = ['PPT % Median',  'WYTD PPT % Median']

  #excludes John Day and Harney for reservoirs
  basin_list = ['Owyhee', 'Malheur', 'Grande Ronde-Burnt-Powder-Imnaha', 'Umatilla-Walla Walla-Willow', 'Upper Deschutes-Crooked', 'Hood-Sandy-Lower Deschutes', 'Willamette', 'Rogue-Umpqua', 'Klamath', 'Lake County-Goose Lake']
  res_medians = []
  for i in basin_list:
    filter = BRes[i].iloc[:, 0] == 'Basin Index'
    medians = BRes[i][filter].loc[:,['Median % Capacity',	'Current % Median',	'Last Year % Median']]
    res_medians.append(medians)

  res_medians = pd.concat(res_medians)
  res_medians.index = basin_list
  res_medians.columns = ['Res Median % Capacity',	'Res Current % Median',	'Res Last Year % Median']

  medians = [snow_medians, prec_medians, res_medians]
  medians_df = reduce(lambda left,right: pd.merge(left,right,left_index=True, right_index=True, how='outer'), [medians[j] for j in range(len(medians))])
  # medians_df.sort_index()
  sorter = ['Owyhee', 'Malheur', 'Grande Ronde-Burnt-Powder-Imnaha', 'Umatilla-Walla Walla-Willow', 'John Day', 'Upper Deschutes-Crooked', 'Hood-Sandy-Lower Deschutes', 'Willamette', 'Rogue-Umpqua', 'Klamath', 'Lake County-Goose Lake', 'Harney']
  medians_df.reset_index(inplace=True)
  medians_df.rename(columns={medians_df.columns[0]: 'Basin'}, inplace=True)

  medians_df.Basin = medians_df.Basin.astype("category").cat.set_categories(sorter)
  # medians_df.sort_values(['Basin'])
  return medians_df.sort_values(['Basin'])



#------ Forecast Querying Functions-----------

# ----------KEEP for reference----------
# https://stackoverflow.com/questions/53927460/select-rows-in-pandas-multiindex-dataframe

# Queries only the Subbasin Index and only returns first row:
# GR.loc[['Lostine R nr Lostine']]
# same as:
# GR.query("Subbasin == 'Lostine R nr Lostine'")
# same as:
# GR.xs('Lostine R nr Lostine', level=0, axis=0, drop_level=False)
# same as:
# GR[GR.index.get_level_values('Subbasin') == 'Lostine R nr Lostine']

# Queries only the Forecast Period Index
# GR.xs('APR-SEP', level=1, axis=0, drop_level=False)
# same as:
# GR[GR.index.get_level_values('Forecast Period') == 'APR-SEP']
# same as:
# idx = pd.IndexSlice
# GR.loc[idx[:, 'APR-SEP'], :]
# same as:
# GR.query("Forecast Period == 'APR-SEP'") #according to above link, this should work.  Not working for some reason though.

# ------------------

def BFcst_reformat(BFcst, basin_name):
    # INDICES
    # r_tuples = list(zip(list(BFcst[basin_name].iloc[:,0]), list(BFcst[basin_name].iloc[:,1])))
    basin_name_duplicated = [[i] * len(BFcst[basin_name].iloc[:, 0]) for i in [basin_name]][0]
    subbasin_names = list(BFcst[basin_name][basin_name].replace(r'^\s*$', np.nan,
                                                                regex=True))  # replace empty strings with nan so subbasin names can later be forward filled with pd.ffill().
    forecast_period_names = list(BFcst[basin_name].iloc[:, 1])
    r_tuples = list(zip(basin_name_duplicated, subbasin_names, forecast_period_names))
    # c_tuples = [
    #             ('',BFcst[basin_name].columns[0]),
    #             ('','Forecast Period'),
    #             ('←-------Drier----------Future Conditions--------Wetter-------→', '90% (KAF)'),
    #             ('←-------Drier----------Future Conditions--------Wetter-------→', '70% (KAF)'),
    #             ('←-------Drier----------Future Conditions--------Wetter-------→', '50% (KAF)'),
    #             ('←-------Drier----------Future Conditions--------Wetter-------→', '% Median'),
    #             ('←-------Drier----------Future Conditions--------Wetter-------→', '30% (KAF)'),
    #             ('←-------Drier----------Future Conditions--------Wetter-------→', '10%(KAF)'),
    #             ('', '30yr Median(KAF)')
    #             ]

    c_tuples = [
        (BFcst[basin_name].columns[0]),
        ('Forecast Period'),
        ('90% (KAF)'),
        ('70% (KAF)'),
        ('50% (KAF)'),
        ('% Median'),
        ('30% (KAF)'),
        ('10%(KAF)'),
        ('30yr Median(KAF)')
    ]

    index = pd.MultiIndex.from_tuples(r_tuples)
    index.set_names(['Basin', 'Subbasin', 'Forecast Period'], inplace=True)
    columns = c_tuples
    # df = BFcst[basin_name].copy()
    # df.replace("", float('NaN'), inplace=True)
    # df.dropna(inplace=True)
    df = pd.DataFrame(BFcst[basin_name].to_numpy(), columns=columns, index=index)
    # df.reset_index(inplace=True)
    # df.set_index(df.loc[:,''][basin_name], inplace=True)
    # df.loc[0] = ['Streamflow Forecasts for ' + str(dt.datetime.now().strftime("%B %Y")), 'Forecast Period', '90% (KAF)', '70% (KAF)', '50% (KAF)', '% Median', '30% (KAF)', '10% (KAF)', '30yr Median (KAF)'
    # ]
    # df.columns = ['','  d','←-----','Drier','-----','Future Conditions','-----','Wetter', '-------→']
    # df.index = df.iloc[:,0]
    df = df.iloc[:, 2:]

    return df


def BFcst_Stats(BFcst, basin_name, forecast_period):
    basin_BFcst = BFcst_reformat(BFcst, basin_name).reset_index()
    basin_BFcst.loc[:, 'Subbasin'].ffill(axis=0, inplace=True)

    medians = basin_BFcst[basin_BFcst[
                              'Forecast Period'] == forecast_period]  # ['Subbasin', '% Median']            #basin_BFcst.loc[pd.IndexSlice[:, [forecast_period]], :]['% Median']
    # medians.mean()
    medians2 = medians['% Median'].str.rstrip('%').astype('float')
    mean = medians2.mean()
    median = medians2.median()
    max = medians2.max()
    min = medians2.min()

    medians_df = pd.DataFrame(medians)
    # r_tuples = ()
    # index = pd.MultiIndex.from_tuples(c_tuples)

    # medians_df.droplevel(level=0)
    # medians = {'Basin': basin_name, 'Medians': medians}
    # medians_stats_df = pd.DataFrame({'Mean':[mean], 'Median':[median], 'max':[max], 'min':[min]})
    medians_stats = {'Basin': basin_name, 'Median': median, 'Mean': mean, 'Max': max, 'Min': min}
    # medians_df.index = [basin_name]

    return medians_df, medians_stats


def BFcst_Stats_allbasins(BFcst, forecast_period):
    forecasts_allbasins = []
    forecast_stats_allbasins = []
    for basin in BFcst.keys():
        medians, median_stats = BFcst_Stats(BFcst, basin, forecast_period)
        forecasts_allbasins.append(medians)
        forecast_stats_allbasins.append(median_stats)

    # forecast_all_basins = pd.concat(forecasts_allbasins)
    forecast_stats_allbasins = pd.DataFrame(forecast_stats_allbasins)  # .set_index('Basin')
    sorter = ['Owyhee', 'Malheur', 'Grande Ronde-Burnt-Powder-Imnaha', 'Umatilla-Walla Walla-Willow', 'John Day',
              'Upper Deschutes-Crooked', 'Hood-Sandy-Lower Deschutes', 'Willamette', 'Rogue-Umpqua', 'Klamath',
              'Lake County-Goose Lake', 'Harney']
    forecast_stats_allbasins.Basin = forecast_stats_allbasins.Basin.astype("category").cat.set_categories(sorter)
    forecast_stats_allbasins = forecast_stats_allbasins.sort_values(['Basin'])

    return pd.concat(forecasts_allbasins), forecast_stats_allbasins


#---------------Style functions

def style_BFcst(BFcst, basin_name):
    # INDICES
    # r_tuples = list(zip(list(BFcst[basin_name].iloc[:,0]), list(BFcst[basin_name].iloc[:,1])))
    symbol = '<-------Drier----------Future Conditions--------Wetter------->'
    c_tuples = [
        (' ', 'Streamflow Forecasts'),
        (' ', 'Forecast Period'),
        (symbol, '90% (KAF)'),
        (symbol, '70% (KAF)'),
        (symbol, '50% (KAF)'),
        (symbol, '% Median'),
        (symbol, '30% (KAF)'),
        (symbol, '10% (KAF)'),
        (' ', '30yr Median (KAF)')
    ]

    columns = pd.MultiIndex.from_tuples(c_tuples)
    # columns = c_tuples
    # df = BFcst[basin_name].copy()
    # df.replace("", float('NaN'), inplace=True)
    # df.dropna(inplace=True)
    df = pd.DataFrame(BFcst[basin_name].to_numpy(), columns=columns)
    df.replace("", float('NaN'), inplace=True)
    f = {
        (symbol, '90% (KAF)'): '{:.0f}',
        (symbol, '70% (KAF)'): '{:.0f}',
        (symbol, '50% (KAF)'): '{:.0f}',
        (symbol, '30% (KAF)'): '{:.0f}',
        (symbol, '10% (KAF)'): '{:.0f}',
        (' ', '30yr Median (KAF)'): '{:.0f}'
    }
    s = df.style.format(f)  # .set_index('Hood-Sandy-Lower Deschutes')

    cell_hover = {  # for row hover use <tr> instead of <td>
        'selector': 'tr:hover',
        'props': [('background-color', 'red')]
    }
    index_name = {
        'selector': '.index_name',
        'props': 'font-style: normal; color: black; font-weight:900;'
    }

    headers = [
        {'selector': 'th:not(.index_name)', 'props': 'background-color: white; color: black;'},
        {'selector': 'th.col_heading', 'props': 'text-align: center;'},
        {'selector': 'th.col_heading.level0', 'props': 'font-size: 1.2em;'},
        {'selector': 'th.col_heading.level1', 'props': 'font-size: 1.3em;'},
        {'selector': 'td', 'props': 'text-align: center; font-weight: bold;'},
        # {'selector': 'th:nth-child(1)','props': [('background-color', '#D3D3D3')]},
        {'selector': 'th:nth-child(5)', 'props': [('background-color', '#D3D3D3')]},
        {'selector': 'th:nth-child(6)', 'props': [('background-color', '#D3D3D3')]},

        # {'selector': 'th:nth-child(2)','props': [('border-right', '2.5px solid black')]},
        # {'selector': 'th:nth-child(2)','props': [('border-left', '2.5px solid black')]},

        #  {'selector': 'th:nth-child(1)','props': [('border-right', '2.5px solid black')]},
        #  {'selector': 'th:nth-child(1)','props': [('background-color', '#D3D3D3')]},

    ]
    # all_table = {'selector': 'table',
    #            'props': 'border: 15px solid red; border-collapse: collapse'
    # }

    all_table = {"selector": "", "props": [("border",
                                            "5px solid black")]}  # bit of a hack to give a table a border; unconventional way to do it with an empty selector.

    s.set_properties(**{'border': '1.3px solid white',
                        'color': 'black',
                        'background-color': 'white'})

    # def highlight_max(s, props=''):
    #     return np.where(s == np.nanmax(s.values), props, '')

    idx = pd.IndexSlice
    # for multiindex/multicolumns use this template for slicing
    slice_ = idx[idx[:, :], idx[:, ['50% (KAF)', '% Median']]]

    slice_ = idx[idx[:], idx[symbol, ['50% (KAF)', '% Median']]]
    s.set_properties(subset=slice_, **{'border': '1.3px solid #D3D3D3',
                                       'color': 'black',
                                       'background-color': '#D3D3D3'})

    slice_ = idx[idx[:], idx[' ', ['30yr Median(KAF)']]]
    s.set_properties(subset=slice_, **{'border-left': '2px solid black'})

    slice_ = idx[idx[0], idx[:, :]]
    s.set_properties(subset=slice_, **{'border-top': '2.5px solid black'})

    slice_ = idx[idx[:], idx[' ', ['Forecast Period']]]
    s.set_properties(subset=slice_, **{'border-right': '2.5px solid black',
                                       'border-left': '2.5px solid black'})

    # s.applymap_index(lambda v: "background:#D3D3D3;" if v=='Owyhee' else "color:darkblue;", axis=0)

    # s.apply(highlight_max, props='color:blue;', axis=0, subset=slice_)

    # s.style.apply(highlight_max, props='color:red;', axis=0, subset=slice_)

    # s.set_properties(subset=[idx[:,:], idx['50% (KAF)',	'% Median']], **{'border': '1.3px solid grey',
    #                           'color': 'black',
    #                           'background-color':'grey'})

    s.set_table_styles([cell_hover, index_name, all_table])
    s.set_table_styles(headers)
    s.hide_index()

    # s.bar(subset=idx[idx[:], idx[symbol,['50% (KAF)']]], color='#d65f5f')

    return s


# -----------Other available table css properties-------------------

# border-collapse: collapse   - removes the padding between cells when using .to_html
# vertical-align
# border-color: inherit
# background: blue
# border-left:2px solid red
#-----------

def style_Res(BRes, basin_name):
  # global df2, df
  df = BRes[basin_name].loc[:,[f'{basin_name}', 'Current (KAF)', 'Last Year (KAF)',	'Median (KAF)',	'Median % Capacity', 'Capacity (KAF)']]
  df = df.iloc[:-3,:]
  df.rename(columns={f'{basin_name}':'Reservoir Storage', 	'Median % Capacity': '% of Median', 'Capacity (KAF)': 'Usable Capacity (KAF)'}, inplace=True)

  # #Got to be a better way to round these values; have to create whole new dataframe using df.round().  df.apply(np.round) would work but can't specify # of decimals.  So stupid.
  # # df.set_index('Reservoir Storage', inplace=True)
  # df2 = df[['Current (KAF)', 'Last Year (KAF)', 'Median (KAF)', 'Usable Capacity (KAF)']].astype(float).round(1)
  # df2.insert(3,'% of Median', np.array(df['% of Median']))
  # df2.insert(0,'Reservoir Storage', np.array(df['Reservoir Storage']))

  #Round values when styling!!!!
  df.replace("", float('NaN'), inplace=True)
  f = {'Current (KAF)':'{:.2f}', 'Last Year (KAF)':'{:.2f}', 'Median (KAF)':'{:.2f}', 'Usable Capacity (KAF)':'{:.2f}'}
  s = df.style.format(f)

  # Headers
  headers = [
              {'selector': 'th:not(.index_name)','props': 'background-color: white; color: black;'},
              {'selector': 'th.col_heading', 'props': 'text-align: center;'},
              {'selector': 'th.col_heading.level0', 'props': 'font-size: 1.2em;'},
              {'selector': 'td', 'props': 'text-align: center; font-weight: bold;'},
              {'selector': 'th:nth-child(1)','props': [('background-color', '#D3D3D3'), ('border-right', '2.5px solid black')]},
  ]
  s.set_table_styles(headers)

  ## Cells
  #set cell color to white, background to white, text color to black:
  s.set_properties(**{'border': '1.3px solid white',
                        'color': 'black',
                        'background-color':'white'})
  idx = pd.IndexSlice
  slice_ = idx[0, :]
  s.set_properties(subset=slice_, **{'border-top': '2.5px solid black'})

  slice_ = idx[:, 'Reservoir Storage']
  s.set_properties(subset=slice_, **{'border-right': '2.5px solid black'})

  # slice_ = df.columns #idx[idx[:], idx[symbol,['50% (KAF)', '% Median']]]
  # s.set_properties(subset=slice_, **{'border': '1.3px solid #D3D3D3',
  #                                   'color': 'black',
  #                                   'background-color':'#D3D3D3'})


  s.hide_index()
  return s

#------------------
def style_Snow(BSnow, basin_name):
    # c_tuples = [
    #             ('Basin Snowpack Measurement Sites', 'Basin Snowpack Measurement Sites'),
    #             ('Network', 'Network'),
    #             ('Elevation (ft)', 'Elevation (ft)'),
    #             ('Snow Depth (ft)', 'Snow Depth (ft)'),
    #             ('Snow Water Equivalent (in)', 'Current SWE'),
    #             ('Snow Water Equivalent (in)', 'Median'),
    #             ('Snow Water Equivalent (in)', 'Last Yr SWE'),
    #             ('Snow Water Equivalent (in)', '% of Median')
    #             ]
    c_tuples = [
        ('Basin Snowpack Measurement Sites', ''),
        ('', 'Network'),
        ('', 'Elevation (ft)'),
        ('', 'Snow Depth (in)'),
        ('Snow Water Equivalent (in)', 'Current SWE (in)'),
        ('Snow Water Equivalent (in)', 'Median (in)'),
        ('Snow Water Equivalent (in)', 'Last Yr SWE (in)'),
        ('Snow Water Equivalent (in)', '% of Median'),
        # ('','')
    ]

    columns = pd.MultiIndex.from_tuples(c_tuples)
    df = BSnow[basin_name].iloc[:-3, :].copy()
    df = df[(df['Network'] != 'SNOWLITE') & (df['Network'] != 'SNOLITE')]
    # df['Elevation (ft)'].astype(float)
    df.sort_values(by=['Elevation (ft)'], inplace=True, ascending=False)
    df = pd.DataFrame(df.loc[:, [f'{basin_name}', 'Network', 'Elevation (ft)', 'Depth (in)', 'SWE (in)', 'Median (in)',
                                 'Last Year SWE (in)', '% Median']].to_numpy(), columns=columns)
    # df = df.iloc[:-3,:]

    df.replace("", float('NaN'), inplace=True)
    f = {
        ('', 'Elevation (ft)'): '{:.0f}',
        ('', 'Snow Depth (in)'): '{:.0f}',
        ('Snow Water Equivalent (in)', 'Current SWE (in)'): '{:.1f}',
        ('Snow Water Equivalent (in)', 'Median (in)'): '{:.1f}',
        ('Snow Water Equivalent (in)', 'Last Yr SWE (in)'): '{:.1f}',
    }
    s = df.style.format(f)
    # Headers
    headers = [
        {'selector': 'th:not(.index_name)', 'props': 'background-color: white; color: black;'},
        {'selector': 'th.col_heading', 'props': 'text-align: center;'},
        {'selector': 'th.col_heading.level0', 'props': 'font-size: 1.2em;'},
        # {'selector': 'td', 'props': 'text-align: right; font-weight: bold;'},
        {'selector': 'th:not(.index_name)', 'props': 'background-color: white; color: black;'},
        {'selector': 'th.col_heading', 'props': 'text-align: center;'},
        {'selector': 'th.col_heading.level0', 'props': 'font-size: 1.2em;'},
        {'selector': 'td', 'props': 'text-align: center; font-weight: bold;'},
        {'selector': 'th:nth-child(1)',
         'props': [('background-color', '#D3D3D3'), ('border-right', '2.5px solid black')]},
        {'selector': 'th:nth-child(5)', 'props': [('border-left', '2.5px solid black')]},
    ]
    s.set_table_styles(headers)

    ## Cells
    # set cell color to white, background to white, text color to black:
    s.set_properties(**{'border': '1.3px solid white',
                        'color': 'black',
                        'background-color': 'white'})
    idx = pd.IndexSlice
    slice_ = idx[0, :]
    s.set_properties(subset=slice_, **{'border-top': '2.5px solid black'})

    slice_ = idx[:, ['Basin Snowpack Measurement Sites']]  #
    s.set_properties(subset=slice_, **{'border-right': '2.5px solid black',
                                       'text-align': 'right',
                                       #  'vertical-align': 'middle'
                                       }
                     )

    s.hide_index()
    # s.data.replace(float('NaN'),"", inplace=True)

    return s

#-------------

def snowpack_parser(spreadsheet, basin_name):

    table = table_parser(spreadsheet, basin_name, first_row=0)
    if basin_name == 'Malheur':
        index = 5
    else:
        index = 4

    table = [i for i in table.items()][index][1]
    table = table.iloc[:, :4]

    return table

def style_Snowpack(snowpack):
  snowpack.columns = ['Snowpack Summary by Basin', '# of Sites', '% Median', 'Last Yr % Median']
  s = snowpack.style
  #
  headers = [
                {'selector': 'th:not(.index_name)','props': 'background-color: white; color: black;'},
                {'selector': 'th.col_heading', 'props': 'text-align: center;'},
                {'selector': 'th.col_heading.level0', 'props': 'font-size: 1.2em;'},
                {'selector': 'td', 'props': 'text-align: center; font-weight: bold;'},
                {'selector': 'th:nth-child(1)','props': [('background-color', '#D3D3D3'), ('border-right', '2.5px solid black')]},
    ]
  s.set_table_styles(headers)

  ## Cells
  #set cell color to white, background to white, text color to black:
  s.set_properties(**{'border': '1.3px solid white',
                        'color': 'black',
                        'background-color':'white'})
  idx = pd.IndexSlice
  slice_ = idx[0, :]
  s.set_properties(subset=slice_, **{'border-top': '2.5px solid black'})

  slice_ = idx[:, 'Snowpack Summary by Basin']
  s.set_properties(subset=slice_, **{'border-right': '2.5px solid black'})


  s.hide_index()

  return s