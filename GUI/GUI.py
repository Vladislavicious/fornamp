import tkinter as tk
import customtkinter as ctk
import BaH.product as bh_product
import BaH.order as bh_order
import BaH.step as bh_step

#добавить редактирование шагов и продуктов
#добавить проверку ввода
#реализовать блокировку ввода при нажатии кнопки применить
#добавить возможность редактировать шаги и продукты
#сделать сохранение продукта при нажатии кнопки добавить новый продукт
#исправить баг множетсвенного добавления одного шага при нескольких нажатиях применить
#подправить конструкторы продуктов и шагов
#испрвить баг в котором при создании заказа с несколькими продуктами показывает у продуктов одни и те же шани если после создание этого заказа сначала открыть другой заказа, при переходе в show_info не меняется индекс
#исправить баг при котором кнопка вернуться к заказам не исчезает при добавлении заказа во время просмотра заказа или удалить кнопку добавления заказа


class MainWindow(tk.Frame):
    def __init__(self, root):
        self.root = root

        super().__init__(self.root)

        self.list_order = []
        self.init_main_window()

    def init_main_window(self):

        

        frame_title = ctk.CTkFrame(master=self.root, height=50, border_width=3, fg_color="#FFFFFF")
        self.frame_tools = ctk.CTkFrame(master=self.root, width=150, border_width=3)
        
        

        button_profile = ctk.CTkButton(frame_title, text="Профиль")
        button_profile.pack(side=tk.RIGHT, padx=10)

        name_label = ctk.CTkLabel(frame_title, text="TASK MANAGER", fg_color="transparent",
                                  font=ctk.CTkFont(family="Arial", size=24))
        name_label.place(relx=0.37, rely=0.2)

        button_add_order = ctk.CTkButton(self.frame_tools, text="Добавить", command=self.open_window)
        button_add_order.pack(anchor=tk.N, pady=6)

        self.frame_tools.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        frame_title.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        frame_title.pack_propagate(False)
        self.frame_tools.pack_propagate(False)

        self.create_canvas_order()


    def create_canvas_order(self):
        
        self.frame_order = ctk.CTkFrame(master=self.root, border_width=3)
        self.frame_order.pack(anchor=tk.SW, fill=tk.BOTH, expand=tk.TRUE, padx=5, pady=5)
        #scrol = ctk.CTkScrollableFrame(self.frame_order, label_anchor=ctk.E, height=500)
        #scrol.pack(padx = 10, pady = 10, fill=tk.X)

    def add_list_order(self):
        self.frame_order.destroy()
        self.create_canvas_order()
        for item in self.list_order:
            self.frame_order_info = ctk.CTkFrame(self.frame_order, border_width=3, fg_color="#6F7A71", height=50)
            self.frame_order_info.pack(fill=tk.X, padx = 10, pady=7)
            self.label_order = ctk.CTkLabel(self.frame_order_info, text = item.zakazchik + "  " + str(item.date_of_creation)+ "  " + str(item.date_of_vidacha), font = ctk.CTkFont(family="Arial", size=12))
            self.label_order.pack(fill=tk.X, padx=10, pady = 10)
            self.label_order.bind('<Button-1>', lambda event, order = item: self.open_info(order))


    def open_info(self, order):
        self.frame_order.destroy()
        self.create_canvas_order()
        self.button_close_info = ctk.CTkButton(self.frame_tools, text="Вернуться к заказам", command=self.close_info)
        self.button_close_info.pack(anchor=tk.N, pady=6)
        self.window_info = WindowInfo(self, order)


    def close_info(self):
        del self.window_info
        self.add_list_order()
        self.button_close_info.destroy()


    def open_window(self):
        self.window_add = WindowAdd(self.root, self)


class WindowAdd(ctk.CTkToplevel):
    def __init__(self, root, app):
        super().__init__(root)

        #self.attributes('-topmost',True)

        self.main_window = app
        self.list_frame_product = []
        self.list_product = []
        
        self.current_step = None

        self.init_window_add()

    def init_window_add(self) -> None:
        self.geometry("810x510+250+100")
        self.resizable(False, False)
        #self.overrideredirect(True)
        
        

        self.font_ = ctk.CTkFont(family="Arial", size=16)
        self.fontmini = ctk.CTkFont(family="Arial", size=12)

        self.protocol("WM_DELETE_WINDOW", lambda: self.close_window()) 

        self.panel_add()

        self.add_area_order()
        self.add_area_product()
        self.add_area_step()

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)
        # надо разобраться с колоннами (разметкой)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=10)
        self.columnconfigure(4, weight=1)



        self.bind("<Configure>", self.resize)
        self.minsize(self.winfo_width(), self.winfo_height())
        
        self.main_window.root.withdraw()

    def resize(self, event):    #отвечает за нормальное поведение скроллбара
        region = self.canvas_product.bbox(tk.ALL)
        self.canvas_product.configure(scrollregion=region)

        region_step = self.canvas_step.bbox(tk.ALL)
        self.canvas_step.configure(scrollregion=region_step)

    def panel_add(self):    #панель добавления шагов, продуктов, заказа
        self.frame_order_panel = ctk.CTkFrame(self, border_width=1, width=300, corner_radius=0)
        self.frame_product_panel = ctk.CTkFrame(self, border_width=1, width=400, corner_radius=0)
        self.frame_step_panel = ctk.CTkFrame(self, border_width=1, width=400, corner_radius=0)

        self.frame_order_panel.grid(row=0, column=0, sticky="ensw")
        self.frame_product_panel.grid(row=0, column=1, columnspan=2, sticky="ensw")
        self.frame_step_panel.grid(row=0, column=3, columnspan=2, sticky="ensw")

        button_add_order = ctk.CTkButton(self.frame_order_panel, text="Добавить заказ", 
                                              command=self.add_new_order, width=40, height=10)
        button_add_order.pack(side=tk.TOP, pady=7)

        button_add_product = ctk.CTkButton(self.frame_product_panel, text="Добавить товар",
                                           command=self.add_product_field, width=40, height=10)
        button_add_product.pack(side=tk.TOP, pady=7)

        button_add_step = ctk.CTkButton(self.frame_step_panel, text="Добавить шаг", command=self.add_step_field,
                                        width=40, height=10)
        button_add_step.pack(side=tk.TOP, pady=7)

    def add_area_order(self):   #создание области в которой создается заказ
        self.frame_order = ctk.CTkFrame(self, border_width=1, width=300, height=650, corner_radius=0)

        self.add_order_field()
        self.frame_order.grid(row=1, column=0, sticky="ensw")

    def add_area_product(self):     #создание области в которой создается продукт
        self.number_product = 1

        scroll_y = ctk.CTkScrollbar(self)
        self.canvas_product = tk.Canvas(self, yscrollcommand=scroll_y.set)  # избавиться от Canvas если это возможно
        scroll_y.configure(command=self.canvas_product.yview)

        self.frame_product = tk.Frame(self.canvas_product)

        self.canvas_product.create_window((0, 0), window=self.frame_product,
                                          anchor=tk.N)

        self.canvas_product.grid(row=1, column=1, sticky="ensw")
        scroll_y.grid(row=1, column=2, sticky="ns")

    def add_area_step(self):    #создание области в которой создается шаг
        self.number_step = 1

        scroll_y = ctk.CTkScrollbar(self)
        self.canvas_step = tk.Canvas(self, yscrollcommand=scroll_y.set)
        scroll_y.configure(command=self.canvas_step.yview)

        self.frame_step = tk.Frame(self.canvas_step)

        self.canvas_step.create_window((0, 0), window=self.frame_step,
                                       anchor=tk.N)

        self.canvas_step.grid(row=1, column=3, sticky="ensw")
        scroll_y.grid(row=1, column=4, sticky="ns")

    def add_order_field(self):  #поля ввода для создания заказа и конпка выхода в главное меню
        frame_order_field = ctk.CTkFrame(self.frame_order, width=250, height=700, corner_radius=0)
        frame_order_field.pack(side=tk.TOP, padx=1, pady=1)
        frame_order_field.pack_propagate(False)

        label_date = ctk.CTkLabel(frame_order_field, text="Введите дату выдачи", font=self.font_)
        label_date.pack(anchor=tk.CENTER, pady=5)

        self.entry_data_order = ctk.CTkEntry(frame_order_field)
        self.entry_data_order.pack(fill=tk.X, pady=5)

        label_commentariy = ctk.CTkLabel(frame_order_field, text="Введите описание заказа", font=self.font_)
        label_commentariy.pack(anchor=tk.CENTER, pady=5)

        self.entry_commentariy_order = ctk.CTkEntry(frame_order_field)
        self.entry_commentariy_order.pack(fill=tk.X, pady=5)

        button_close = ctk.CTkButton(frame_order_field, text="Закрыть", command=self.close_window, width=40, height=10)
        button_close.pack(side=tk.BOTTOM, anchor=tk.E)

    def add_step_field(self):   #добавление новго шага
        if (self.number_product == 1):
            return
        step = Step_field(self.main_window)

        self.list_frame_product[self.current_step].append(step)

    def add_product_field(self): #добавление новго продукта и добавление шага в список
        self.product_field = Product_field(self.number_product, self.main_window)
        self.number_product += 1
        
        self.list_frame_product.append(self.product_field.list_frame_step)
        self.product_field.reload(tk.Event)

    def close_window(self):
        self.main_window.add_list_order()
        self.main_window.root.deiconify()
        self.destroy()

    def check_order_field(self):
        if(self.entry_commentariy_order.get() != "" and self.entry_data_order.get()!= ""):
            return True # добавить проверку на то что все поля заполнены в других фреймах
            
    def add_new_order(self):
        if(self.check_order_field() == True):
            dat = bh_order.date.today()
            order = bh_order.Order(1, self.entry_commentariy_order.get(), dat, dat, self.list_product, self.entry_commentariy_order.get()) #это затычка надо поменять принимаемые данные
            self.main_window.list_order.append(order)
            self.close_window()





class WindowInfo(tk.Frame):
    def __init__(self, main_win, order):
        self.main_window = main_win
        self.cur_order = order
        self.init_window_info()
        
        

    def init_window_info(self):
        self.frame_info_product = ctk.CTkFrame(self.main_window.frame_order, border_width=3, width=400)
        
        self.frame_info_product.pack(fill=tk.Y, padx=5, pady = 10, side=tk.LEFT, expand=True)
        self.create_step_frame()
        self.show_product()

    def create_step_frame(self):
        self.frame_info_step = ctk.CTkFrame(self.main_window.frame_order, border_width=3, width=400)
        self.frame_info_step.pack(fill=tk.Y, padx=5, pady = 10, side = tk.RIGHT, expand=True)


    def show_product(self):

        self.product = self.cur_order.GetProducts()
        for item in self.product:
            self.frame_product_show = ctk.CTkFrame(self.frame_info_product, border_width=3, fg_color="#6F7A71", height=50, width=400)
            self.frame_product_show.pack(fill=tk.X, padx = 10, pady=7)
            self.frame_product_show.pack_propagate(False)
            self.label_product = ctk.CTkLabel(self.frame_product_show, text = item.name + "  " + str(item.selling_cost) + "  " + str(item.quantity) + "  " + str(item.production_cost), font = ctk.CTkFont(family="Arial", size=12))
            self.label_product.pack(fill=tk.X, padx=10, pady = 10)
            self.label_product.bind('<Button-1>', lambda event, step_index = self.product.index(item): self.open_step_info(step_index))


    def open_step_info(self, s_index):  
        self.frame_info_step.destroy()
        self.create_step_frame()   
        step = self.product[s_index].GetSteps()
        for item in step:
            self.frame_step_show = ctk.CTkFrame(self.frame_info_step, border_width=3, fg_color="#6F7A71", height=50, width=400)
            self.frame_step_show.pack(fill=tk.X, padx = 10, pady=7)
            self.frame_step_show.pack_propagate(False)
            
            self.label_step = ctk.CTkLabel(self.frame_step_show, text = item.name + "  ", font = ctk.CTkFont(family="Arial", size=12))
            self.label_step.pack(fill=tk.X, padx=10, pady = 10)






class Product_field():  #класс продукта
    def __init__(self, count: int, app) -> None:
        self.main_window = app
        self.window_add = self.main_window.window_add
        self.list_frame_step: Step_field = []
        self.list_step = []

        self.prod: bh_product
        self.count = count
        self.font_ = ctk.CTkFont(family="Arial", size=16)
        self.fontmini = ctk.CTkFont(family="Arial", size=12)

        self.label_count: ctk.CTkLabel
        self.frame_product_field: ctk.CTkFrame
        self.label_name: ctk.CTkLabel
        self.entry_name: ctk.CTkEntry
        self.label_selling_cost: ctk.CTkLabel
        self.entry_selling_cost: ctk.CTkEntry
        self.label_production_cost: ctk.CTkLabel
        self.entry_production_cost: ctk.CTkEntry
        self.label_commentariy: ctk.CTkLabel
        self.entry_commentariy: ctk.CTkEntry
        self.label_quantity: ctk.CTkLabel
        self.entry_quantity: ctk.CTkEntry

        self.button_aply: ctk.CTkButton

        self.add_product()

    def add_product(self):  #создание поля нового пустого продукта
        self.label_count = ctk.CTkLabel(self.window_add.frame_product, text="Товар № " + str(self.count),
                                        font=self.font_)
        self.label_count.pack(anchor=tk.CENTER, pady=5)

        self.frame_product_field = ctk.CTkFrame(self.window_add.frame_product, border_width=2, width=350, height=415)
        self.frame_product_field.pack(side=tk.TOP, padx=1, pady=1)
        self.frame_product_field.pack_propagate(False)
        self.frame_product_field.bind('<Button-1>', self.reload)
        

        self.label_name = ctk.CTkLabel(self.frame_product_field, text="Введите название товара", font=self.fontmini)
        self.label_name.pack(anchor=tk.CENTER, pady=5)

        self.entry_name = ctk.CTkEntry(self.frame_product_field)
        self.entry_name.pack(fill=tk.X, pady=5, padx=5)

        self.label_selling_cost = ctk.CTkLabel(self.frame_product_field, text="Введите стоимость продажи",
                                               font=self.fontmini)
        self.label_selling_cost.pack(anchor=tk.CENTER, pady=5)

        self.entry_selling_cost = ctk.CTkEntry(self.frame_product_field)
        self.entry_selling_cost.pack(fill=tk.X, pady=5, padx=5)

        self.label_production_cost = ctk.CTkLabel(self.frame_product_field, text="Введите себестоимость товара",
                                                  font=self.fontmini)
        self.label_production_cost.pack(anchor=tk.CENTER, pady=5)

        self.entry_production_cost = ctk.CTkEntry(self.frame_product_field)
        self.entry_production_cost.pack(fill=tk.X, pady=5, padx=5)

        self.label_quantity = ctk.CTkLabel(self.frame_product_field, text="Введите количество товаров",
                                           font=self.fontmini)
        self.label_quantity.pack(anchor=tk.CENTER, pady=5)

        self.entry_quantity = ctk.CTkEntry(self.frame_product_field)
        self.entry_quantity.pack(fill=tk.X, pady=5, padx=5)

        self.label_commentariy = ctk.CTkLabel(self.frame_product_field, text="Введите описание ",
                                              font=self.fontmini)
        self.label_commentariy.pack(anchor=tk.CENTER, pady=5)

        self.entry_commentariy = ctk.CTkEntry(self.frame_product_field)
        self.entry_commentariy.pack(fill=tk.X, pady=5, padx=5)

        self.button_aply = ctk.CTkButton(self.frame_product_field, text="Применить", command = self.aply)
        self.button_aply.pack(anchor=tk.CENTER)


    def aply(self):     #кнопка подтверждения продукта и добавление его в список
        if(self.chek_field()==True):
            self.prod = bh_product.Product(self.entry_name.get(),
                                        int(self.entry_selling_cost.get()),
                                        self.list_step)
            self.main_window.window_add.list_product.append(self.prod)
            self.button_aply.configure(fg_color = "#2dba52", hover_color = "#189e3b")

    def chek_field(self):   #проверка на введеные поля
        if(self.entry_name.get() != "" and self.entry_commentariy.get() != "" and self.entry_selling_cost.get() != "" and self.entry_production_cost.get() != "" and self.entry_quantity.get() != ""):
            return True #наверное сюда надо добавить проверку на корректность введеных полей

    def reload(self, event):    #отображение шагов связанных с этим продуктом
        if(self.window_add.current_step != self.count - 1):
            self.window_add.canvas_step.delete(tk.ALL)
            self.window_add.add_area_step()
            self.window_add.current_step = self.count - 1
            for element in self.window_add.list_frame_product[self.count - 1]:
                element.add_step()

class Step_field():     #класс шага
    def __init__(self, app) -> None:
        self.main_window = app
        self.window_add = self.main_window.window_add
        self.font_ = ctk.CTkFont(family="Arial", size=16)
        self.fontmini = ctk.CTkFont(family="Arial", size=12)

        self.text = ""
        self.complex = ""

        self.label_count: ctk.CTkLabel
        self.frame_step_field: ctk.CTkFrame
        self.label_name: ctk.CTkLabel
        self.entry_name: ctk.CTkEntry
        self.label_complexity: ctk.CTkLabel
        self.entry_complexity: ctk.CTkEntry
        self.label_commentariy: ctk.CTkLabel
        self.entry_commentariy: ctk.CTkEntry

        self.button_aply: ctk.CTkButton

        self.add_step()

    def add_step(self):     #создание поля нового пустого шага
        self.label_count = ctk.CTkLabel(self.window_add.frame_step, text="Шаг № " + str(self.window_add.number_step),
                                        font=self.font_)
        self.label_count.pack(anchor=tk.CENTER, pady=5)
        self.window_add.number_step += 1

        self.frame_step_field = ctk.CTkFrame(self.window_add.frame_step, border_width=2, width=350, height=190)
        self.frame_step_field.pack(side=tk.TOP, padx=1, pady=1)
        self.frame_step_field.pack_propagate(False)

        self.label_name = ctk.CTkLabel(self.frame_step_field, text="Введите название шага", font=self.fontmini)
        self.label_name.pack(anchor=tk.CENTER, pady=5)

        self.entry_name = ctk.CTkEntry(self.frame_step_field)
        self.entry_name.insert(0, self.text)
        self.entry_name.pack(fill=tk.X, pady=5, padx=5)

        self.label_complexity = ctk.CTkLabel(self.frame_step_field, text="Введите сложность шага",
                                                  font=self.fontmini)
        self.label_complexity.pack(anchor=tk.CENTER, pady=5)

        self.entry_complexity = ctk.CTkEntry(self.frame_step_field)
        self.entry_complexity.insert(0, self.complex)
        self.entry_complexity.pack(fill=tk.X, pady=5, padx=5)

        self.button_aply = ctk.CTkButton(self.frame_step_field, text="Применить", command = self.aply)
        self.button_aply.pack(anchor=tk.CENTER)



    def aply(self):     #кнопка подтверждения продукта и добавление его в список
        if(self.chek_field()==True):
            contributions: list = []
            self.step = bh_step.Step(self.entry_name.get(),
                                     contributions,
                                     self.window_add.number_step,
                                     False,
                                     int(self.entry_complexity.get()),
                                     1)# ЭТО КОСТЫЛЬ НАДО ПЕРЕДЕЛАТЬ  
            self.window_add.product_field.list_step.append(self.step)    
            self.button_aply.configure(fg_color = "#2dba52", hover_color = "#189e3b")
            self.text = self.entry_name.get()
            self.complex = self.entry_complexity.get()


    def chek_field(self):   #проверка на введеные поля
        if(self.entry_name.get() != "" and self.entry_complexity.get() != ""):
            return True #наверное сюда надо добавить проверку на корректность введеных полей