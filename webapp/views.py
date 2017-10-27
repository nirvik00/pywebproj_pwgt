import os
from . import getData
import math
from .forms import UploadFileForm
import math
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import Node, Adj, RawData

#upload, check
def home(request):
    fstr=''
    FSTR=''
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        for line in myfile:
            fstr+=str(line)
            FSTR+=str(line)
        data=RawData(rawdata=FSTR)
        data.save()
        fs.delete(myfile)
        construct()
        return render(request, 'webapp/home.html' , {'value':FSTR})
    return render(request, 'webapp/home.html')

def construct():
    FSTR = str(RawData.objects.all().last())
    s = FSTR.split('b')
    fs = []
    for i in s:
        try:
            s1 = i.split('\'')[1]
            fs.append(s1)
        except:
            pass
    fsf = []
    for i in fs:
        try:
            s1 = i.split('\\')[0]
            fsf.append(s1)
        except:
            pass
    func_obj = []
    adj_obj = []
    break_index = 0
    for i in range(len(fsf)):
        if (fsf[i] == ''):
            break_index = i
            break
    #############################################
    # values are cleared of punctuation marks   #
    #############################################
    for i in range(0, break_index, 1):
        if (fsf[i] != ''):
            adj_obj.append(fsf[i])

    for i in range(break_index, len(fsf), 1):
        if (fsf[i] != ''):
            func_obj.append(fsf[i])

    names = []
    for i in func_obj:
        names.append(i.split(",")[0])

    adjstr=''
    for i in range(0, len(adj_obj)):
        s0 = adj_obj[i].split(",")
        l=len(s0)
        for j in range(1, len(s0)):
            adjstr+=names[i]+","+names[j-1]+","+s0[j]+";"
    data=Adj(adjString=adjstr)
    data.save()

    nodestr=''
    for i in range(0, len(func_obj)):
        ar = str(int(math.sqrt(float(func_obj[i].split(",")[1]))))
        num = str(int(func_obj[i].split(",")[2]))
        colr = func_obj[i].split(",")[3]
        re = str(colr.split("-")[0])
        gr = str(colr.split("-")[1])
        bl = str(colr.split("-")[2])
        le = str(func_obj[i].split(",")[4])
        de = str(func_obj[i].split(",")[5])
        nodestr+=names[i]+","+ar+","+num+","+re+"-"+gr+"-"+bl+"-"+","+le+","+bl+";"
    data=Node(nodeString=nodestr)
    data.save()


def readfile(request):
    GLOBAL_FUNC=Node.objects.all().last()
    GLOBAL_ADJ=Adj.objects.all().last()
    adj_obj = GLOBAL_ADJ
    func_obj = GLOBAL_FUNC
    return render(request, 'webapp2/home.html', {'adj_data': adj_obj,
                                                 'func_data': func_obj})

def getListFromString(inp):
    s0=str(inp).split(";")
    li=[]
    for i in s0:
        if(i):
            li.append(i)
    return li

"""
#################
# display data  #
#################
"""


def display_data(request):
    # parse data and construct list of cellular relationships
    foo=Node.objects.all().last()
    bar=Adj.objects.all().last()
    GLOBAL_FUNC=getListFromString(foo)
    GLOBAL_ADJ=getListFromString(bar)

    global_rel_li = getData.readfile(GLOBAL_ADJ)

    # from rel_li remove duplicates  a->b = b->a : greater weight
    global_ucell_rel_li = getData.rem_dup(global_rel_li)

    # department cell dictionary - with cells (no Values)
    global_dept_di = getData.getDept(global_rel_li)

    req_dept_cell_str = []
    req_dept_unique_str = []

    for i in global_dept_di:
        str = i + "-"
        if (len(global_dept_di[i]) > 0):
            for j in global_dept_di[i]:
                str += j + ","
            req_dept_cell_str.append(str)
        else:
            req_dept_unique_str.append(i)

    # nodes=getNodes(global_dept_di)
    global_nodes = getData.getNodes(GLOBAL_FUNC)

    # department as nodes
    global_dept_node_li = getData.getDept_asNodes(global_dept_di, global_nodes)

    # calculate connection between departments
    dt_conn_index_li = getData.getDeptConn_as_Indices(global_ucell_rel_li, global_dept_di, global_dept_node_li)

    # calculate connection between departments NAMES (string)
    dt_conn_li_str = getData.getDeptConn_as_Str(dt_conn_index_li, global_dept_node_li)
    print("\nnodes : ", global_nodes)
    print("\nrel li : ", global_ucell_rel_li)
    return render(request, "webapp/data.html", {'nodes': global_nodes,
                                                'global_ucell_rel_li': global_ucell_rel_li,
                                                'req_dept_cell_str': req_dept_cell_str,
                                                'req_dept_unique_str':req_dept_unique_str,
                                                'dt_conn_li_str':dt_conn_li_str})


"""
####################
# display contact  #
####################
"""

def contact(request):
    return render(request, "webapp/contact.html")


"""
###################################
# display example Layout - force  #
###################################
"""

def layout_ex(request):
    return render(request, "webapp/py_example_conx.html")


"""
#####################################################
# force layout : connect cells and query by weight  #
#####################################################
"""
def layout_cells(request):
    foo=Node.objects.all().last()
    bar=Adj.objects.all().last()
    GLOBAL_FUNC=getListFromString(foo)
    GLOBAL_ADJ=getListFromString(bar)

    # parse data and construct list of cellular relationships
    rel_li=getData.readfile(GLOBAL_ADJ)
    # from rel_li remove duplicates  a->b = b->a : greater weight
    rel_lix = getData.rem_dup(rel_li)
    # department cell dictionary - with cells (no Values)
    dept_di=getData.getDept(rel_li)
    # nodes=getNodes(global_dept_di)
    nodes=getData.getNodes()
    # edges as links=[(1,2),(2,3),(3,4),(2,4)]
    edges=getData.getEdges_as_indices(rel_lix,nodes)
    return render(request,"webapp/py_cells_conx.html",{'node_li':nodes,'edge_li':edges, 'edge_li_str':rel_lix })


"""
#############################################################
# force layout : connect departments and query by weight    #
#############################################################
"""
def layout_dept(request):
    foo=Node.objects.all().last()
    bar=Adj.objects.all().last()
    GLOBAL_FUNC=getListFromString(foo)
    GLOBAL_ADJ=getListFromString(bar)

    # parse data and construct list of cellular relationships
    rel_li=getData.readfile(GLOBAL_ADJ)

    # from rel_li remove duplicates  a->b = b->a : greater weight
    rel_lix = getData.rem_dup(rel_li)

    # department cell dictionary - with cells (no Values)
    dept_di=getData.getDept(rel_li)

    # nodes=getNodes(global_dept_di)
    nodes=getData.getNodes(GLOBAL_FUNC)

    # edges as links=[(1,2),(2,3),(3,4),(2,4)]
    edges=getData.getEdges_as_indices(rel_lix, nodes)

    # department cell dictionary - with Values
    dept_di=getData.getDept(rel_li)

    # department as nodes
    dept_node_li = getData.getDept_asNodes(dept_di, nodes)
    print(dept_node_li)

    # calculate connection between departments INDICES (int,int,float)
    dept_conn_li_idx=getData.getDeptConn_as_Indices(rel_lix, dept_di, dept_node_li)
    print(dept_conn_li_idx)

    # calculate connection between departments NAMES (string)
    dt_conn_li_str = getData.getDeptConn_as_Str(dept_conn_li_idx, dept_node_li)

    return render(request,"webapp/py_dept_conx.html",{ 'node_li':dept_node_li , 'edge_li':dept_conn_li_idx, 'edge_li_str':dt_conn_li_str })

"""
#################################################################################################
# treemap layout : of cells in one department (only department which have more than 0 cells)    #
#################################################################################################
"""
def dept_cells(request):
    foo=Node.objects.all().last()
    bar=Adj.objects.all().last()
    GLOBAL_FUNC=getListFromString(foo)
    GLOBAL_ADJ=getListFromString(bar)

    # parse data and construct list of cellular relationships
    rel_li = getData.readfile(GLOBAL_ADJ)

    # from rel_li remove duplicates  a->b = b->a : greater weight
    rel_lix = getData.rem_dup(rel_li)

    # department cell dictionary - with cells (no Values)
    dept_di = getData.getDept(rel_li)
    req_dept_cell_str=[]
    req_dept_unique_str = []
    for i in dept_di:
        str=i+"-"
        if(len(dept_di[i])>0):
            for j in dept_di[i]:
                print(j)
                str+=j+","
            req_dept_cell_str.append(str)
        else:
            req_dept_unique_str.append(i)

    # nodes=getNodes(global_dept_di)
    nodes = getData.getNodes(GLOBAL_FUNC)

    return render(request, "webapp/py_dept_cells.html", {'req_dept_cell_str':req_dept_cell_str, 'req_dept_unique_str': req_dept_unique_str , 'nodes': nodes})

"""
#########################################################
#   treemap layout : of all departments taken together  #
#########################################################
"""
def dept_dept(request):
    foo=Node.objects.all().last()
    bar=Adj.objects.all().last()
    GLOBAL_FUNC=getListFromString(foo)
    GLOBAL_ADJ=getListFromString(bar)

    # parse data and construct list of cellular relationships
    rel_li = getData.readfile(GLOBAL_ADJ)

    # from rel_li remove duplicates  a->b = b->a : greater weight
    rel_lix = getData.rem_dup(rel_li)

    # department cell dictionary - with cells (no Values)
    dept_di = getData.getDept(rel_li)
    req_dept_cell_str = []
    req_dept_unique_str = []
    for i in dept_di:
        str = i + "-"
        if (len(dept_di[i]) > 0):
            for j in dept_di[i]:
                print(j)
                str += j + ","
            req_dept_cell_str.append(str)
        else:
            req_dept_unique_str.append(i)

    # nodes=getNodes(global_dept_di)
    nodes = getData.getNodes(GLOBAL_FUNC)
    return render(request, "webapp/py_dept_dept.html",
    {'req_dept_cell_str': req_dept_cell_str, 'req_dept_unique_str': req_dept_unique_str, 'nodes': nodes})

"""
#############################################################
#   treemap layout : of all cells in all departments        #
#############################################################
"""
def cells_treemap(request):
    foo=Node.objects.all().last()
    bar=Adj.objects.all().last()
    GLOBAL_FUNC=getListFromString(foo)
    GLOBAL_ADJ=getListFromString(bar)

    # parse data and construct list of cellular relationships
    rel_li = getData.readfile(GLOBAL_ADJ)

    # from rel_li remove duplicates  a->b = b->a : greater weight
    rel_lix = getData.rem_dup(rel_li)

    # department cell dictionary - with cells (no Values)
    dept_di = getData.getDept(rel_li)
    req_dept_cell_str = []
    req_dept_unique_str = []
    for i in dept_di:
        str = i + "-"
        if (len(dept_di[i]) > 0):
            for j in dept_di[i]:
                print(j)
                str += j + ","
            req_dept_cell_str.append(str)
        else:
            req_dept_unique_str.append(i)

    # nodes=getNodes(global_dept_di)
    nodes = getData.getNodes(GLOBAL_FUNC)
    return render(request, "webapp/py_cells_TM.html",
    {'req_dept_cell_str': req_dept_cell_str, 'req_dept_unique_str': req_dept_unique_str, 'nodes': nodes})

"""
#########################################################################
#   force layout : select multiple departments and draw connections     #
#########################################################################
"""
def se_dept(request):
    foo=Node.objects.all().last()
    bar=Adj.objects.all().last()
    GLOBAL_FUNC=getListFromString(foo)
    GLOBAL_ADJ=getListFromString(bar)

    # parse data and construct list of cellular relationships
    global_rel_li = getData.readfile(GLOBAL_ADJ)

    # from rel_li remove duplicates  a->b = b->a : greater weight
    global_ucell_rel_li = getData.rem_dup(global_rel_li)

    # department cell dictionary - with cells (no Values)
    global_dept_di = getData.getDept(global_rel_li)

    req_dept_cell_str = []
    req_dept_unique_str = []

    for i in global_dept_di:
        str = i + "-"
        if (len(global_dept_di[i]) > 0):
            for j in global_dept_di[i]:
                print(j)
                str += j + ","
            req_dept_cell_str.append(str)
        else:
            req_dept_unique_str.append(i)

    # nodes=getNodes(global_dept_di)
    global_nodes = getData.getNodes(GLOBAL_FUNC)

    # department as nodes
    global_dept_node_li = getData.getDept_asNodes(global_dept_di, global_nodes)

    # calculate connection between departments
    dt_conn_index_li = getData.getDeptConn_as_Indices(global_ucell_rel_li, global_dept_di, global_dept_node_li)

    # calculate connection between departments NAMES (string)
    dt_conn_li_str = getData.getDeptConn_as_Str(dt_conn_index_li, global_dept_node_li)

    return render(request, "webapp/py_search_dept.html", {'req_dept_cell_str': req_dept_cell_str,
                                                          'req_dept_unique_str': req_dept_unique_str,
                                                          'nodes': global_nodes,
                                                          'dt_conn_li_str':dt_conn_li_str})


"""
##################################################################################
#   force layout : select multiple departments and draw connections for cells   #
##################################################################################
"""
def se_dept_cells(request):
    foo=Node.objects.all().last()
    bar=Adj.objects.all().last()
    GLOBAL_FUNC=getListFromString(foo)
    GLOBAL_ADJ=getListFromString(bar)

    # parse data and construct list of cellular relationships
    global_rel_li = getData.readfile(GLOBAL_ADJ)

    # from rel_li remove duplicates  a->b = b->a : greater weight
    global_ucell_rel_li = getData.rem_dup(global_rel_li)

    # department cell dictionary - with cells (no Values)
    global_dept_di = getData.getDept(global_rel_li)

    req_dept_cell_str = []
    req_dept_unique_str = []

    for i in global_dept_di:
        str = i + "-"
        if (len(global_dept_di[i]) > 0):
            for j in global_dept_di[i]:
                print(j)
                str += j + ","
            req_dept_cell_str.append(str)
        else:
            req_dept_unique_str.append(i)

    # nodes=getNodes(global_dept_di)
    global_nodes = getData.getNodes(GLOBAL_FUNC)

    # department as nodes
    global_dept_node_li = getData.getDept_asNodes(global_dept_di, global_nodes)

    # calculate connection between departments
    dt_conn_index_li = getData.getDeptConn_as_Indices(global_ucell_rel_li, global_dept_di, global_dept_node_li)

    # calculate connection between departments NAMES (string)
    dt_conn_li_str = getData.getDeptConn_as_Str(dt_conn_index_li, global_dept_node_li)

    return render(request, "webapp/py_search_dept_cells.html", {'req_dept_cell_str': req_dept_cell_str,
                                                          'req_dept_unique_str': req_dept_unique_str,
                                                          'nodes': global_nodes,
                                                          'dt_conn_li_str':dt_conn_li_str})


"""
######################################################
# OPTIMIZATION OF ADJACENCY - DOUBLE LOADED CORRIDOR #
######################################################
"""

def solver(request):
    foo=Node.objects.all().last()
    bar=Adj.objects.all().last()
    GLOBAL_FUNC=getListFromString(foo)
    GLOBAL_ADJ=getListFromString(bar)

    return render(request, 'webapp/solver.html', {'adj_data': GLOBAL_ADJ,
                                                 'func_data': GLOBAL_FUNC})


