# Import necessary libraries
# $pip install dash==2.14.2
import dash
from dash import html, callback_context, dcc
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
from module.modules import *
from urllib import parse
import dash_bootstrap_components as dbc
import clr
clr.AddReference("System.Data")
from System.Data import Odbc
from System.Data import CommandType
from System.Data.Odbc import OdbcCommand, OdbcParameter
clr.AddReference("System")
import System
clr.AddReference(r'C:/Users/DSL/Desktop/R&D/dll/web.dll')
from web import Program
from System.Collections.Generic import Dictionary

# 대시 앱 초기화
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
p = Program()
#호기 레이아웃
def create_machine_layout(number_of_machines, keys):
    if number_of_machines == -1 or keys == -1:
        return html.Div([
            html.Div("ERROR")
        ])
    rows = []

    for i in range(number_of_machines):
        # machine_value = get_machine_value("COM3" ,keys[i][1])  # 각 호기의 값을 함수를 통해 가져옵니다.
        # machine_value = get_machine_value(i)  # 각 호기의 값을 함수를 통해 가져옵니다.
        machine = html.Div(className='column', children=[
            html.Div(f'{keys[i][0] + " " + keys[i][1]}호기', className='number-title'),
            html.Div(str(keys[i][2]), id=f'display-value-{i}', className='display-value'),  # 함수로 가져온 값을 여기에 표시합니다.
            html.Button('Reset', id=f'reset-button-{i}', className='reset-button'),
            dbc.Alert("This is an alert!", id=f"alert-output", color="info", dismissable=True, is_open=False)
        ])
        rows.append(machine)
    
    # 기계의 수가 3의 배수가 아닌 경우 마지막 행을 빈 디브로 채웁니다
    while len(rows) % 3 != 0:
        rows.append(html.Div(className='column'))

    # 세 대의 컴퓨터를 한 줄로 묶습니다
    layout = html.Div([
        html.Div(id='total',className='row', children=rows[i:i+3]) for i in range(0, len(rows), 3)
    ])

    return layout


# 호기가 몇개인지 
def get_machine_number(): 
    try:
        query = "SELECT * FROM DPCA;"
        res = p.get(f"http://127.0.0.1:5000/count/{parse.quote(query)}/ ") # table row 개수 알아오기 
        print(res)
        return int(res)
    except Exception as e:
        return -1 # 오류 

# KEY값 받아오기  
def get_machine_key(): 
    query = "SELECT * FROM DPCA;"
    res = p.get(f"http://127.0.0.1:5000/api/{parse.quote(query)}/ ") # table row 개수 알아오기 
    try:
        print(res)
        s = res.text
        s = s[2:len(s)-4]
        print(s)
        s = s.split('\\n')
        print(s)
        s = [_.strip() for _ in s]
        s = [_.split(' ') for _ in s]
        print(s)
        return s
    except Exception as e:
        print(e)
        return -1
app.index_string = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .row {
                display: flex;
                justify-content: space-around;
                margin-bottom: 20px;
            }
            .column {
                background-color: #D3D3D3;
                border-radius: 10px; /* Rounded corners for the counters */
                padding: 20px;
                width: 30%;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                margin: 10px; /* Spacing between counters */
            }
            .reset-button {
                background-color: #778899;
                color: white;
                border: none;
                padding: 20px 40px;
                margin-top: 10px;
                cursor: pointer;
                border-radius: 5px; /* Rounded corners for the buttons */
                transition: background-color 0.3s ease; /* Smooth transition for button hover effect */
            }
            .reset-button:hover {
                background-color: #5F9EA0; /* Slightly lighter color on hover */
            }
            .display-value {
                font-size: 2.5em;
                color: black;
                margin-bottom: 10px; /* Spacing between the number and the button */
            }
            .number-title {
                font-size: 3em;
                margin-bottom: 5px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""



### PLC Read 후 DB에 넣기 
def PLC_TO_DB():
    datas = read_PLC()
    for data in list(datas.keys()):
        query = f"INSERT INTO DPCA VALUES('COM3', '{data}', {datas[data]})" # DB에 중복 없는 경우 INSERT 
        res = p.get(f"http://127.0.0.1:5000/count/{parse.quote(query)}/ ") 
        print(res)
        if int(res) == -1: # 응답은 정상이지만, DB에 이미 존재할 경우는 UPDATE
            print(data)
            query = f"UPDATE DPCA SET Value = {datas[data]} WHERE PLC_ID = 'COM3' AND DeviceAddress = '{data}';" 
            print("query", query)
            res = p.get(f"http://127.0.0.1:5000/count/{parse.quote(query)}/ ")




# PLC_TO_DB() 
number_of_machines = get_machine_number()  # 데이터베이스에서 가져온 동적 값으로 바꾸기
clicked = [None for _ in range(number_of_machines)]
keys = get_machine_key() # 데이터베이스에서 가져온 동적 값으로 바꾸기
outs = create_machine_layout(number_of_machines, keys)

@app.callback(
        Output('total', 'children'),
        [Input('test', 'n_intervals')]
)
def update_layout(n_intervals):
    # PLC_TO_DB() 
    global number_of_machines, clicked, keys, outs
    print(n_intervals)
    number_of_machines = get_machine_number()  # 데이터베이스에서 가져온 동적 값으로 바꾸기
    clicked = [None for _ in range(number_of_machines)]
    keys = get_machine_key() # 데이터베이스에서 가져온 동적 값으로 바꾸기
    outs = create_machine_layout(number_of_machines, keys)
    return [outs]

app.layout = html.Div([
    outs,
    dcc.Interval(
        id = "test",
        interval= 1 * 1000,
        n_intervals= 0
    )
])
# Callback to handle button click
@app.callback(
    Output(f'alert-output', 'children'),
    [Input(f'reset-button-{i}', 'n_clicks') for i in range(number_of_machines)],
    [State(f'reset-button-{i}', 'id') for i in range(number_of_machines)]
)
def handle_button_click(*args):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate
    button_indices = range(0, len(args) // 2)
    idx = -1
    for i in button_indices:
        if args[i] != clicked[i]:
            idx = i 
            clicked[i] = args[i]
    print(idx)
    param1 = keys[idx][0]
    param2 = keys[idx][1]
    print(param2)
    query = f"UPDATE DPCA SET Value = 0 WHERE PLC_ID = '{param1}' AND DeviceAddress = '{param2}';"
    print(f"Button clicked for {param1} and {param2}.")
    res = p.get(f"http://127.0.0.1:5000/api/{parse.quote(query)}/ ") 
    # if res.status_code == 200:
    #     res = res.text
    #     # PLC Write
    #     writeRes = write_PLC(param2, 0) # Addr, Value
    #     print(f"write is : {writeRes}")
    return [f"Alert for {param1} and {param2}"]






# CSS 스타일 정의


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
