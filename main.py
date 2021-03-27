import sys
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))
    print(text)

    with open(r'C:\Users\Matvey\Desktop\Feniks7\TEST\error.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    quit()
sys.excepthook = log_uncaught_exceptions
from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
from ui_main import Ui_MainWindow
from functions import *
from dataBase import *
from delegate_combo import *
from add_obj_choice import *
from add_key import *
from exebody_edit import *
from taxpayer_edit import *
from animation import *
from settings import *
from graph import open_plot_graph
from del_window import open_del_window

# dbConfig = {'dataBase' : 'feniks', 'host' : '127.0.0.1', 'port' : 3306, 'userName' : 'root', 'password' : '0000'}


# Create application
app = QtWidgets.QApplication(sys.argv)


# Create form and init UI
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
app.setStyle('Fusion')
app.setFont(QFont('Calibri Light', 10))
MainWindow.show()

# Hook logic
# ANIMATION
rise_label(ui.label_info)
# ANIMATION

# Get Config
try:
    config = read_config()
except:
    config = {'dataBase' : '', 'host' : '', 'port' : 0, 'userName' : '', 'password' : '', 'remind_birthday' : 0, 'remind_ekey' : 0, 'objects_size_editable' : '0'}
    write_config(config)

if config['objects_size_editable'] == '1':
    edit_size_objects(ui)
# Menu
ui.action.triggered.connect(lambda: open_settings(config, app))


# Connect to Base Data 
flag_error = False
db_total = connectToBase(config, ui)
if db_total != -1:
    Qdb = db_total[0]
    db = db_total[1]
    cursor = db_total[2]
else:
    flag_error = True

del db_total

# LOGIC
if flag_error == False:
    # TEST LOGIC
    model = showCalls(Qdb, ui)
    modelService = modelService_init(Qdb, ui)
    modelPlans = init_model_tablePlans(ui, Qdb)
    modelBoxEkeys = init_comboBox_ekeysModel(ui, Qdb, ui.box_ekeys)
    ui.box_ekeys.currentTextChanged.connect(lambda: change_show_ekey(ui, db, cursor))

    advSearch_exebody_model = init_model_for_searchAdv_exebody(ui, Qdb)
    advSearch_ekeys_model = init_model_for_searchAdv_ekeys(ui, Qdb)

    # TREE
    tree = Tree_init(ui)
    search(ui, db, tree, cursor)

    ui.tree_search.pressed.connect(ui.get_current_Item)
    ui.tree_search.clicked.connect(ui.get_current_Item)
    ui.tree_search.doubleClicked.connect(lambda: select(ui, db, cursor, modelService, modelBoxEkeys))

    ui.delete_treeItem_action.triggered.connect(lambda: open_del_window('treeItem', ui, db, cursor, tree, model))
    ui.delete_service_action.triggered.connect(lambda: open_del_window('service_or_call', ui, db, cursor, tree, modelService))
    ui.delete_call_action.triggered.connect(lambda: open_del_window('service_or_call', ui, db, cursor, tree, model))
    ui.delete_plan_action.triggered.connect(lambda: open_del_window('service_or_call', ui, db, cursor, tree, modelPlans))
    # TREE

    ui.button_search_call.clicked.connect(lambda: search_calls(ui, model))
    ui.button_add_call.clicked.connect(lambda: add_call(ui, model))

    ui.button_add_service.clicked.connect(lambda: add_service(ui, modelService))
    ui.button_search_service.clicked.connect(lambda: search_service(ui, modelService, ui.current_id))

    ui.button_search.clicked.connect(lambda: pre_search(ui, db, tree, cursor))
    ui.button_add.clicked.connect(lambda: open_obj_choice(db, cursor, Qdb))
    ui.button_add_ekey.clicked.connect(lambda: open_add_key(ui, db, cursor))
    ui.button_edit_exeBody.clicked.connect(lambda: open_exebody_edit(ui, db, cursor, Qdb))
    ui.button_edit_tax.clicked.connect(lambda: open_taxpayer_edit(ui, db, cursor))

    ui.button_advSearch.clicked.connect(lambda: open_adv_search(ui))
    ui.button_search_ekeys.clicked.connect(lambda: search_ekey(ui, advSearch_ekeys_model))
    ui.button_searchAdv_exebody.clicked.connect(lambda: search_exebody_advSearch(ui, advSearch_exebody_model))

    ui.button_graphique.clicked.connect(lambda: open_plot_graph(Qdb, db, cursor))


    ui.tree_search.customContextMenuRequested.connect(ui.call_context_menu_tree)
    ui.table_service.customContextMenuRequested.connect(ui.call_context_menu_tableService)
    ui.table_calls.customContextMenuRequested.connect(ui.call_context_menu_tableCalls)
    ui.table_plans.customContextMenuRequested.connect(ui.call_context_menu_tablePlans)

    ui.table_service.pressed.connect(ui.get_cell)
    ui.table_calls.pressed.connect(ui.get_cell)
    ui.table_plans.pressed.connect(ui.get_cell)

    ui.button_search_plan.clicked.connect(lambda: search_plan(ui, modelPlans))
    ui.button_add_plan.clicked.connect(lambda: add_plan(ui, modelPlans))

    remind_birthday(ui, db, cursor, config['remind_birthday'])
    remind_expEKey(ui, db, cursor, config['remind_ekey'])
    delete_empty_str(db, cursor)
    delete_all_str_grapgh(db, cursor)

# Run main loop
sys.exit(app.exec_())