import tkinter as tk
import customtkinter as ctk
from GUI.AddWindow import *
from GUI.EmailWindow import *
from BaH.Contribution import *


#подправить конструкторы продуктов и шагов
#испрвить баг в котором при создании заказа с несколькими продуктами показывает у продуктов одни и те же шаги если после создание этого заказа сначала открыть другой заказ  (при переходе в show_info не меняется индекс)

class MainWindow(ctk.CTkToplevel):
    def __init__(self, root, app):
        self.root = root

        super().__init__(root)

        self.app = app
        self.user = self.app.file_manager.user_handler.lastUser
        self.oders_previews_list = self.app.order_previews
        self.order_visibility = False
        self.init_main_window()

    def init_main_window(self):

        self.title("Task manager")
        self.geometry("1000x600+250+100")
        self.resizable(False, False)

        frame_title = ctk.CTkFrame(master=self, height=50, border_width=3, fg_color="#FFFFFF")
        self.frame_tools = ctk.CTkFrame(master=self, width=150, border_width=3)



        button_log_out = ctk.CTkButton(frame_title, text="Выйти", command = self.log_out)
        button_log_out.pack(side=tk.RIGHT, padx=10)

        name_label = ctk.CTkLabel(frame_title, text="TASK MANAGER", fg_color="transparent",
                                  font=ctk.CTkFont(family="Arial", size=24))
        name_label.place(relx=0.37, rely=0.2)

        self.button_add_order = ctk.CTkButton(self.frame_tools, text="Добавить", command=self.open_window)
        if(self.user.isAdministrator == True):
            self.button_add_order.pack(anchor=tk.N, pady=6)

        self.button_send_email = ctk.CTkButton(self.frame_tools, text="Отправить отчет", command=self.send_email)
        self.button_send_email.pack(anchor=tk.N, pady=6)

        if(self.user.email == ""):
            self.button_add_email = ctk.CTkButton(self.frame_tools, text="Добавить почту", command=self.add_email)
        else:
            self.button_add_email = ctk.CTkButton(self.frame_tools, text="Редактировать\n данные почты", command=self.add_email)
        self.button_add_email.pack(anchor=tk.N, pady=6)

        self.button_change_visibility = ctk.CTkButton(self.frame_tools, text="Показать выданные\n заказы", height= 40, command=self.change_visibility)
        self.button_change_visibility.pack(anchor=tk.N, pady=6)


        self.frame_tools.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        frame_title.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        frame_title.pack_propagate(False)
        self.frame_tools.pack_propagate(False)

        self.create_frame_order()
        self.add_list_order()

        self.protocol("WM_DELETE_WINDOW", lambda: self.close_window())
        self.root.withdraw()


    def change_visibility(self):
        self.order_visibility = not self.order_visibility
        if(self.order_visibility == True):
            self.button_change_visibility.configure(text = "Скрыть выданные\n заказы")
        else:
            self.button_change_visibility.configure(text = "Показать выданные\n заказы")
        self.add_list_order()

    def create_frame_order(self):

        self.frame_order = ctk.CTkFrame(master=self, border_width=3)
        self.frame_order.pack(anchor=tk.SW, fill=tk.BOTH, expand=tk.TRUE, padx=5, pady=5)
        self.scroll = ctk.CTkScrollableFrame(master = self.frame_order, height=600)
        self.scroll.pack(padx = 5, pady =5, fill=tk.X)

    def add_list_order(self):
        self.frame_order.destroy()
        self.create_frame_order()
        for item_order in self.oders_previews_list:


            if((item_order.isVidan == True and self.order_visibility == True) or item_order.isVidan == False):

                self.frame_order_info = ctk.CTkFrame(self.scroll, border_width=2, fg_color="#b8bab9", height=120)
                self.frame_order_info.pack(fill=tk.X, padx = 10, pady=7)

                if(item_order.isDone == False):
                    self.frame_order_info.configure(border_color = "#bf6b6b")
                elif(item_order.isDone == True and item_order.isVidan == False):
                    self.frame_order_info.configure(border_color = "#e3a002")

                    if(self.user.isAdministrator == True):
                        self.button_vidat = ctk.CTkButton(self.frame_order_info, text = "Выдано")
                        self.button_vidat.bind('<Button-1>', lambda event,  order = self.app.getOrderByID(item_order.id) : self.vidat_order(order, self.frame_order_info, self.button_vidat))
                        self.button_vidat.place(relx=0.8, rely = 0.3)
                else:
                    self.frame_order_info.configure(border_color = "#77bf6d")
                self.label_order = ctk.CTkLabel(self.frame_order_info, text = "Заказчик: " + item_order.zakazchik + "\nОписание заказа: " + item_order.commentary + "\nДата создания: " + str(item_order.date_of_creation)+ "\nДата выдачи: " + str(item_order.date_of_vidacha), font = ctk.CTkFont(family="Arial", size=12))
                self.label_order.pack( padx=10, pady = 10)
                self.label_order.bind('<Button-1>', lambda event,  order = self.app.getOrderByID(item_order.id) : self.open_info(order))
                self.frame_order_info.bind('<Button-1>', lambda event,  order = self.app.getOrderByID(item_order.id) : self.open_info(order))

    def send_email(self):
        dialog_window = DialogWindow(self, self.app, self)
        dialog_window.grab_set()

    def add_email(self):
        email = EmailWindow(self, self.app, self)
        email.grab_set()


    def open_info(self, order):
        self.button_add_order.configure(state = "disabled")
        self.frame_order.destroy()
        self.button_close_info = ctk.CTkButton(self.frame_tools, text="Вернуться к заказам", command=self.close_info)
        self.button_close_info.pack(anchor=tk.N, pady=6)
        self.window_info = WindowInfo(self, order)



    def vidat_order(self, order, frame_order_info, button_vidat):
        frame_order_info.configure(border_color = "#77bf6d")
        button_vidat.destroy()
        order.isVidan = True
        self.app.deleteOrderByID(order.id)
        self.app.saveOrder(order)
        self.oders_previews_list.append(order.createPreview())
        self.app.saveNewOrderPreviews()



    def close_info(self):
        self.window_info.delete_window_info()
        del self.window_info
        self.add_list_order()
        self.button_add_order.configure(state = "normal")
        self.button_close_info.destroy()

    def log_out(self):
        self.app.file_manager.user_handler.setNoLastUsers()
        self.root.deiconify()
        self.destroy()


    def open_window(self):
        self.window_add = WindowAdd(self, self)

    def close_window(self):
        self.destroy()
        self.root.destroy()




class WindowInfo(tk.Frame):
    def __init__(self, main_win, order):
        self.main_window = main_win
        self.cur_order = order
        self.cure_product = -1
        self.username = "Igor"
        self.init_window_info()



    def init_window_info(self):
        self.frame_info_product = ctk.CTkFrame(self.main_window, border_width=3, width=410)
        self.frame_info_product.pack(fill=tk.BOTH, padx=5, pady = 5, side=tk.LEFT)
        self.frame_info_product.pack_propagate(False)
        self.scroll_product = ctk.CTkScrollableFrame(master = self.frame_info_product, height=600)
        self.scroll_product.pack(padx = 3, pady =3, fill=tk.X)
        self.create_step_frame()
        self.show_product()

    def create_step_frame(self):
        self.frame_info_step = ctk.CTkFrame(self.main_window, border_width=3, width=410)
        self.frame_info_step.pack(fill=tk.BOTH, padx=5, pady = 5, side = tk.RIGHT)
        self.frame_info_step.pack_propagate(False)
        self.scroll_step = ctk.CTkScrollableFrame(master = self.frame_info_step, height=600)
        self.scroll_step.pack(padx = 3, pady =3, fill=tk.X)


    def show_product(self):

        self.products = self.cur_order.GetProducts()
        for item in self.products:
            self.product_info = ProductInfo(self, item)


    def delete_window_info(self):
        self.frame_info_product.destroy()
        self.frame_info_step.destroy()
        self.main_window.create_frame_order()


class ProductInfo(tk.Frame):
    def __init__(self, info_window, item):
        self.info_window = info_window
        self.prod_index = self.info_window.products.index(item)
        self.step = self.info_window.products[self.prod_index].GetSteps()
        self.init_stepInfo(item)

    def init_stepInfo(self, item):
        self.frame_product_show = ctk.CTkFrame(self.info_window.scroll_product, border_width=2, fg_color= "#b8bab9", height=90, width=150)
        self.frame_product_show.pack(fill=tk.X, padx = 10, pady=7)
        self.frame_product_show.pack_propagate(False)
        self.label_product = ctk.CTkLabel(self.frame_product_show,
                                            text =  "Название продукта: " + item.name[:item.name.find(" ", 15)+1] + "\n" + item.name[item.name.find(" ", 15)+1:] + '\nОписание продукта: ' + item.commentary[:item.commentary.find(" ", 15)+1] + "\n" + item.commentary[item.commentary.find(" ", 15)+1:] + "\nПрибыль с реализации: " + str(item.selling_cost*item.quantity - item.production_cost*item.quantity) + " ₽",
                                        font = ctk.CTkFont(family="Arial", size=12))
        self.label_product.pack(fill=tk.X, padx=10, pady = 10)
        self.label_product.bind('<Button-1>', self.open_step_info)
        if(item.isDone == False):
            self.frame_product_show.configure(border_color= "#bf6b6b")
        else:
            self.frame_product_show.configure(border_color= "#77bf6d")


    def open_step_info(self, event):
        if(self.info_window.cure_product != self.prod_index):
            self.info_window.frame_info_step.destroy()
            self.info_window.create_step_frame()

            for item_step in self.step:
                step_info = StepInfo(self.info_window, item_step, self.frame_product_show, self.prod_index)
            self.info_window.cure_product = self.prod_index





class StepInfo(tk.Frame):
    def __init__(self, info_window, item_step, frame_product, prod_index):
        self.info_window = info_window
        self.item_step = item_step
        self.frame_product = frame_product
        self.prod_index = prod_index
        self.init_stepInfo()

    def init_stepInfo(self):

        self.frame_step_show = ctk.CTkFrame(self.info_window.scroll_step, border_width=2, fg_color= "#b8bab9", height=60, width=150)

        if(self.item_step.isDone == False):
            self.frame_step_show.configure(border_color= "#b86161")
        else:
            self.frame_step_show.configure(border_color= "#77bf6d")

        self.frame_step_show.pack(fill=tk.X, padx = 10, pady=7)
        self.frame_step_show.pack_propagate(False)

        if(self.item_step.isDone == False and self.info_window.main_window.user.isAdministrator==True):
            self.label_step = ctk.CTkLabel(self.frame_step_show, text = "Описание шага: " + self.item_step.name[:self.item_step.name.find(" ", 12)+1] + "\n" + self.item_step.name[self.item_step.name.find(" ", 12)+1:] + "\nВыполнено шагов: " + str(self.item_step.number_of_made) + "/" + str(self.item_step.quantity), font = ctk.CTkFont(family="Arial", size=12), justify = tk.CENTER)
            self.label_step.pack(side = tk.TOP, padx=5, pady = 10)
        elif(self.item_step.isDone == False and self.info_window.main_window.user.isAdministrator==False):
            self.label_step = ctk.CTkLabel(self.frame_step_show, text = "Описание шага: " + self.item_step.name[:self.item_step.name.find(" ", 12)+1] + "\n" + self.item_step.name[self.item_step.name.find(" ", 12)+1:] + "\nВыполнено шагов: " + str(self.item_step.number_of_made) + "/" + str(self.item_step.quantity), font = ctk.CTkFont(family="Arial", size=12), justify = tk.LEFT)
            self.label_step.pack(side = tk.LEFT, padx=5, pady = 10)
        else:
            self.label_step = ctk.CTkLabel(self.frame_step_show, text = "Описание шага:\n" + self.item_step.name, font = ctk.CTkFont(family="Arial", size=12), justify = tk.CENTER)
            self.label_step.pack(side = tk.TOP, padx=5, pady = 15)

        if(self.item_step.isDone == False and self.info_window.main_window.user.isAdministrator==False):
            self.button_redy = ctk.CTkButton(self.frame_step_show, width=10, text = "Выполнено", command = lambda: self.change_status(self.item_step, self.frame_step_show, self.button_redy))
            self.button_redy.pack(side = tk.RIGHT, padx = 5)

            self.entry_quantity = ctk.CTkEntry(self.frame_step_show, height=12, width=40, justify=tk.CENTER)
            self.entry_quantity.insert(0, "1")
            self.entry_quantity.pack(pady = 5,side = tk.RIGHT)
            self.entry_quantity.pack_propagate(False)

    def change_status(self, item_step, frame, button):
        count = item_step.quantity - item_step.number_of_made
        if(int(self.entry_quantity.get()) < count):
            count = int(self.entry_quantity.get())

        for i in range(count):

            item_step.Contribute(self.info_window.username)

        self.label_step.configure(text = "Описание шага: " + item_step.name[:item_step.name.find(" ", 12)+1] + "\n" + item_step.name[item_step.name.find(" ", 12)+1:] + "\nВыполнено шагов: " + str(item_step.number_of_made) + "/" + str(item_step.quantity))
        item_step.isDone = True

        if(item_step.isDone == True):
            frame.configure(border_color= "#77bf6d")
            self.label_step.configure(text = "Описание шага:\n" + self.item_step.name, justify = tk.CENTER)
            self.label_step.pack(side = tk.TOP, padx=5, pady = 15)
            button.destroy()
            self.info_window.products[self.prod_index].CheckIfDone()
            self.info_window.products[self.prod_index].DeleteStep(self.item_step.name)
            self.info_window.products[self.prod_index].AddStep(self.item_step)


        if(self.info_window.products[self.prod_index].isDone == True):
            self.frame_product.configure(border_color= "#77bf6d")
            self.info_window.cur_order.CheckIfDone()

        self.info_window.main_window.app.saveOrder(self.info_window.cur_order)
        self.info_window.main_window.app.saveNewOrderPreviews()
