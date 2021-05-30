import PySimpleGUI as sg
import math
import GUI_JoyStick


js = GUI_JoyStick.JoyStick()

sg.theme('DarkAmber')

layout = [
    [sg.Graph(canvas_size=(750, 750),
              graph_bottom_left=(0, 0),
              graph_top_right=(750, 750),
              change_submits=True,
              drag_submits=True,
              key='graph')],
    [sg.Button('BACK TO THE CENTER'),
     sg.Text('ArrowRotation: ', key='rotation', size=(15+5, 1)),
     sg.Text('ArrowTheta: ', key='theta', size=(12+5, 1))],
]

window = sg.Window('JoyStick_SmallArrowExample', layout, finalize=True, location=(20, 150))
graph = window['graph']

arrowwidth = 20
arrowlength = 30
frontrearratio = 1/3

# define dots
arrowcenter = (375, 375)
arrowtop = (arrowcenter[0], arrowcenter[1] + arrowlength * (1 - frontrearratio))
arrowleft = (arrowcenter[0] - arrowwidth / 2, arrowcenter[1] - arrowlength * frontrearratio)
arrowright = (arrowcenter[0] + arrowwidth / 2, arrowcenter[1] - arrowlength * frontrearratio)
arrowrotation = 0

mainBody = graph.DrawLine(arrowtop, arrowcenter, color='red', width=3)
leftBody = graph.DrawLine(arrowleft, arrowtop, color='red', width=3)
leftBody2 = graph.DrawLine(arrowleft, arrowcenter, color='red', width=3)
rightBody = graph.DrawLine(arrowright, arrowtop, color='red', width=3)
rightBody2 = graph.DrawLine(arrowright, arrowcenter, color='red', width=3)


def cmdcontrol(l_value, r_value, k=0.3):
    '''
    This function accepts parameters, l_value, r_value, and k, where
    l_value indicates magnitude of how lest side of the arrow proceeds,
    r_value indicates magnitude of how right side of the arrow proceeds, and
    k indicates a parameters to multiply, like l_value * k / 99, r_value * k / 99
    '''

    global arrowleft, arrowright, arrowcenter, arrowrotation, mainBody, leftBody, rightBody, leftBody2, rightBody2

    l_dl, r_dl = l_value * k / 99, r_value * k / 99  # apply k to each r/l value

    theta = (r_dl - l_dl) / arrowwidth  # calculate tilt against the position of the arrow
    t = '{:.5f}'.format(theta)
    window['theta'].update(f'ArrowTheta: {t}')

    if -0.001 <= theta <= 0.001:
        #  In this case, the arrow moves straight way
        if l_value == 0. or r_value == 0.:
            pass
        else:
            l_dx, l_dy = l_dl * (-math.sin(arrowrotation)), l_dl * math.cos(arrowrotation)
            # r_dx, r_dy = l_dx, l_dy
            graph.MoveFigure(mainBody, l_dx, l_dy)
            graph.MoveFigure(leftBody, l_dx, l_dy)
            graph.MoveFigure(rightBody, l_dx, l_dy)
            graph.MoveFigure(leftBody2, l_dx, l_dy)
            graph.MoveFigure(rightBody2, l_dx, l_dy)
            arrowleft = l_dx + arrowleft[0], l_dy + arrowleft[1]
            arrowright = l_dx + arrowright[0], l_dy + arrowright[1]
            arrowcenter = (arrowleft[0] + arrowright[0]) / 2, (arrowleft[1] + arrowright[1]) / 2

    else:
        # In here, the arrow needs to move with rotating action
        arrowrotation = arrowrotation + theta

        # To calculate rotated positions to renew the arrow, the point of origin need to be determined.
        # In here, a line passing both arrowleft and arrowright was used to calculate the origin.
        if abs(r_value) >= abs(l_value):
            origin = arrowleft[0] + (arrowleft[0] - arrowright[0]) * l_value / (r_value - l_value), \
                     arrowleft[1] + (arrowleft[1] - arrowright[1]) * l_value / (r_value - l_value)
        else:
            origin = arrowright[0] + (arrowright[0] - arrowleft[0]) * r_value / (l_value - r_value), \
                     arrowright[1] + (arrowright[1] - arrowleft[1]) * r_value / (l_value - r_value)

        # Recalculate each point of the arrow
        # arrowleft and arrowright are easy to recalculate like below
        arrowleft = (arrowleft[0] - origin[0]) * math.cos(theta) - \
                    (arrowleft[1] - origin[1]) * math.sin(theta) + origin[0], \
                    (arrowleft[0] - origin[0]) * math.sin(theta) + \
                    (arrowleft[1] - origin[1]) * math.cos(theta) + origin[1]

        arrowright = (arrowright[0] - origin[0]) * math.cos(theta) - \
                     (arrowright[1] - origin[1]) * math.sin(theta) + origin[0], \
                     (arrowright[0] - origin[0]) * math.sin(theta) + \
                     (arrowright[1] - origin[1]) * math.cos(theta) + origin[1]

        # arrowcenter and arrow top can be calculated using arrowleft, arrowright, and arrowrotation
        # I first calculated shift values (dx_*, dy_*) to calculate points
        # using the center value of arrowleft and arrowright

        dx_center, dy_center = - arrowlength * frontrearratio * math.sin(arrowrotation), \
                               arrowlength * frontrearratio * math.cos(arrowrotation)
        dx_top, dy_top = - arrowlength * math.sin(arrowrotation), \
                         arrowlength * math.cos(arrowrotation)
        arrowcenter = (arrowleft[0] + arrowright[0]) / 2 + dx_center, (arrowleft[1] + arrowright[1]) / 2 + dy_center
        arrowtop = (arrowleft[0] + arrowright[0]) / 2 + dx_top, (arrowleft[1] + arrowright[1]) / 2 + dy_top

        # rewrite arrow with making lines between points calculated
        graph.erase()
        mainBody = graph.DrawLine(arrowtop, arrowcenter, color='red', width=3)
        leftBody = graph.DrawLine(arrowleft, arrowtop, color='red', width=3)
        leftBody2 = graph.DrawLine(arrowleft, arrowcenter, color='red', width=3)
        rightBody = graph.DrawLine(arrowright, arrowtop, color='red', width=3)
        rightBody2 = graph.DrawLine(arrowright, arrowcenter, color='red', width=3)


def calculate_lrPow(r, theta):
    pow_level = r * 99 / 250
    theta = 0 if -0.05 <= theta <= 0.05 else theta
    rot = math.cos(theta)
    lin = math.sin(theta)
    lPow = int((rot + lin) * pow_level)
    rPow = int((-rot + lin) * pow_level)
    lPow = 99 if lPow > 99 else -99 if lPow < -99 else lPow
    rPow = 99 if rPow > 99 else -99 if rPow < -99 else rPow
    return (lPow, rPow)


def rotation_fixer():
    global arrowrotation
    arrowrotation = arrowrotation % (2 * math.pi)
    if arrowrotation < - math.pi:
        arrowrotation = arrowrotation + 2 * math.pi
    elif arrowrotation > math.pi:
        arrowrotation = arrowrotation - 2 * math.pi


if __name__ == '__main__':
    dotmode = False
    automove = False
    while True:
        js.update()
        rt = js.rt_coordinates
        cmd = calculate_lrPow(rt[0], rt[1])
        cmdcontrol(cmd[0], cmd[1], k=1)
        rotation_fixer()
        event, values = window.read(timeout=10)
        rot = '{:.3f}'.format(arrowrotation)
        window['rotation'].update(f'ArrowRotation: {rot}')
        if event == sg.WIN_CLOSED:
            break
        elif event == 'graph+UP':
            a = 1
        elif event == 'graph':
            position = values['graph']
        elif event == 'BACK TO THE CENTER':
            # define dots
            arrowcenter = (375, 375)
            arrowtop = (arrowcenter[0], arrowcenter[1] + arrowlength * (1 - frontrearratio))
            arrowleft = (arrowcenter[0] - arrowwidth / 2, arrowcenter[1] - arrowlength * frontrearratio)
            arrowright = (arrowcenter[0] + arrowwidth / 2, arrowcenter[1] - arrowlength * frontrearratio)
            arrowrotation = 0
            # rewrite arrow
            graph.erase()
            mainBody = graph.DrawLine(arrowtop, arrowcenter, color='red', width=3)
            leftBody = graph.DrawLine(arrowleft, arrowtop, color='red', width=3)
            leftBody2 = graph.DrawLine(arrowleft, arrowcenter, color='red', width=3)
            rightBody = graph.DrawLine(arrowright, arrowtop, color='red', width=3)
            rightBody2 = graph.DrawLine(arrowright, arrowcenter, color='red', width=3)

        if js.close:
            break
        # print(str(math.sqrt((arrowright[0] - arrowleft[0]) ** 2 + (arrowright[1] - arrowleft[1]) ** 2)))

    window.close()
