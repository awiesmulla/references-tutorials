from IPython.display import HTML, display, clear_output
import uuid

from operator import iadd
from functools import reduce
from random import randint

_TABLE = ('<style type="text/css">'
          'table.blockgrid {{border: none;}}'
          ' .blockgrid tr {{border: none;}}'
          ' .blockgrid td {{padding: 0px;}}'
          ' #blocks{0} td {{border: {1}px solid black;}}'
          '</style>'
          '<table id="blocks{0}" class="blockgrid"><tbody>{2}</tbody></table>')
_TR = '<tr>{0}</tr>'
_TD = ('<td title="{0}" style="width: {1}px; height: {1}px;'
       'background-color: {2};">{3}</td>')
_RGB = 'rgb({0}, {1}, {2})'
_IMG = '<img src="data:image/png;base64,{0}"/>'


level = 0
board = None

def make_grid(r=10, c=10, size=30, fill_color=(240,240,240)):
    grid_prop = []
    (rc,gc,bc) = fill_color
    for i in range(r):
        row_prop = []
        for j in range(c):
            row_prop.append({'state':1, 'row':i, 'col':j, 'red':rc,
                             'green':gc, 'blue':bc, 'img':0, 'imgdata':None})
        grid_prop.append(row_prop)
    return {'moves':0, 'lights':0, 'beetle':None, 'rows':r, 'cols':c, 'size': size,'grid':grid_prop}

def get_pixel(i,j):
    return board['grid'][i][j]

def set_pixel(i,j,img=0, imgdata=None,fill_color=(60,60,60), state=0):
    rc,gc,bc = fill_color
    board['grid'][i][j] = {'state':state, 'row':i, 'col':j, 'red':rc,
                           'green':gc, 'blue':bc, 'img':img, 'imgdata':imgdata}
    return board['grid'][i][j]


def show():
    r = board['rows']
    c = board['cols']
    sz = board['size']
    tmp_tr =[]
    for i in range(r):
        tmp_td = []
        for j in range(c):
            gr = board['grid'][i][j]
            if gr['img']:
                myimage = _IMG.format(gr['imgdata'])
                tmp_td.append(_TD.format(str(i)+" "+str(j),sz,
                                         _RGB.format(gr['red'],gr['green'],gr['blue']),myimage))
            else:
                tmp_td.append(_TD.format(str(i)+" "+str(j),sz,
                                         _RGB.format(gr['red'],gr['green'],gr['blue']),""))
        tds = reduce(iadd,tmp_td)
        tmp_tr.append(_TR.format(tds))
        #tmp_tr.reverse()
    trs = reduce(iadd,tmp_tr)
    return display(HTML(_TABLE.format(uuid.uuid4(), 1, trs)))

def make_wall(lst):
    for i,j in lst:
        set_pixel(i,j, fill_color=(200,0,0), state=3)
    return True


def create_grid(r,c):
    global board
    board = make_grid(r,c)
    return True

def paint_black(i,j):
    board['grid'][i][j]['red']=60
    board['grid'][i][j]['blue']= 60
    board['grid'][i][j]['green']= 60
    board['grid'][i][j]['state']=0

def paint_white(i,j):
    board['grid'][i][j]['red']  = 240
    board['grid'][i][j]['blue'] = 240
    board['grid'][i][j]['green']= 240
    board['grid'][i][j]['state']= 1

def decode_run_length(lst):
    for j,r in enumerate(lst):
        index = 0
        for i,v in enumerate(r):
            if i%2:
                for k in range(v):
                    paint_black(j,index+k)
            else:
                for k in range(v):
                    paint_white(j,index+k)
            index += v
    return True


def make_random_board(r=10, c=10, size=30):
    grid_prop = []
    for i in range(r):
        row_prop = []
        for j in range(c):
            if randint(0,1):
                row_prop.append({'state':1, 'row':i, 'col':j, 'red':240,
                             'green':240, 'blue':240, 'img':0, 'imgdata':None})
            else:
                row_prop.append({'state':0, 'row':i, 'col':j, 'red':0,
                             'green':0, 'blue':0, 'img':0, 'imgdata':None})

        grid_prop.append(row_prop)
    return {'moves':0, 'lights':0, 'beetle':None, 'rows':r, 'cols':c, 'size': size,'grid':grid_prop}

def create_random_grid(r,c):
    global board
    board = make_random_board(r,c)
    show()
    return True

def is_white(i,j):
    return board['grid'][i][j]['state']

def grid_size():
    return (board['rows'], board['cols'])
