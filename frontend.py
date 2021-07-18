import tkinter as tk 
from PIL import ImageTk, Image
import os 
import threading
import json
import time 
import datetime
from backend import BackendAPI 
from message import Message
    
win = tk.Tk()
win.title("Amazon Tracker")

win.geometry("700x500")

json_file = '/Users/weijiazhao/Desktop/Python/projects/amazonScraper/search.json'    //change it to the path where your serach.json is located 
def send_mail(recipient, message):
    try:
        m = Message()
        m.send_email(recipient, message)
        print("Email Message Sent")
    except:
        print("Invalid Email Address")

def sorted_dic(dictionary):
    sorted_values = sorted([dictionary[i]['price'] for i in dictionary])
    k = 1
    product = 'product_'
    sorted_dic = {}
    for value in sorted_values:
        for i in dictionary:
            if value == dictionary[i]['price']:
                product_num = product+str(k)
                sorted_dic[product_num] = dictionary[i]
                k+=1
    return sorted_dic


def file_read(file, mode):
    with open(file, mode) as f:
        data = f.read()
    jsdata = json.loads(data)
    return jsdata

def forget_frame(frame):
    frame.pack_forget()

def forget_grid(page, pages):
    pages.grid_forget()
    page.grid_forget()

def manual_mode(page, pages):
    page.grid(row=7,column=7)
    pages.grid(row=7, column=6)

def track_manual(opt1_name, opt1):
    opt1_name.grid(row=5, column=5, columnspan=2)
    opt1.grid(row=5, column=7, columnspan=1)

def initial_page():
    mf = tk.Frame(master=win)
    mf.pack()
    
    

    for i in range(10):
        mf.columnconfigure(i,weight=1,minsize=70)
        mf.rowconfigure(i,weight=1,minsize=50)


    #image
     
    img = ImageTk.PhotoImage(Image.open("AT.png").resize((60, 60), Image.ANTIALIAS))
    label = tk.Label(master=mf, image=img)
    label.image = img
    label.grid(row=8,column=1)

    # panel.place(x=0, y=0, relwidth=1, relheight=1)
   

    r = tk.IntVar()
    #initial page
    pages = tk.Label(master=mf, text="pages:")
    page = tk.Entry(master=mf, text="pages")
    search = tk.Entry(master=mf,width=60,borderwidth=4,font=('Helvetica',20))
    button1 = tk.Button(master=mf,text="Track",padx=40,pady=20,command = lambda: [forget_frame(mf), track_page(search.get())])
    button2 = tk.Button(master=mf,text="Search",padx=35,pady=20,command = lambda: [forget_frame(mf),search_page(search.get(), page.get())])
    
    manual1 = tk.Entry(master=mf, text="time range")
    option1 = tk.Radiobutton(master=mf,text="Default",variable=r,value= 1, command= lambda: forget_grid(page, pages))
    option2 = tk.Radiobutton(master=mf,text="Manual",variable=r,value=2, command= lambda: manual_mode(page, pages))

    search.grid(row=1, column=1,sticky="EW",columnspan=8)
    button1.grid(row=3,column=1,columnspan=4,rowspan=2)
    button2.grid(row=3,column=5,columnspan=4,rowspan=2)
    option1.grid(row=5,column=5,columnspan=3)
    option2.grid(row=6,column=5,columnspan=3)
    
#second page:



def search_page(search_item, page):
    if page == "":
        page = 3
    else:
        page = int(page)
    
    sp = tk.Frame(master=win)
    sp.pack()

    for i in range(10):
        sp.columnconfigure(i,weight=1,minsize=70)
        sp.rowconfigure(i,weight=1,minsize=50)
    
    if search_item == "":
        jsdata = file_read(json_file, 'r')
        jsdata = sorted_dic(jsdata)
        name = "sadlfkjs"
        price = 1000000
        link = "aslkdjflkasdjf"
        for product in jsdata:
            if jsdata[product]['price'] < price:
                price = jsdata[product]['price']
                name = jsdata[product]['product_name']
                link = jsdata[product]['link']
        
        back = tk.Button(master=sp,text="back",padx=40,pady=40,command= lambda: [forget_frame(sp), initial_page()])
        product = tk.Text(master=sp, height=100, wrap=tk.WORD, width=200, xscrollcommand=True)
        search_results = tk.Text(master=sp, height=100, wrap=tk.WORD, width=200, yscrollcommand=True, xscrollcommand=True)
        go_button = tk.Button(master=sp, text="Link", command=lambda: [api().open_link(link)])

        cheapest_name = "Name: {}".format(name)
        cheapest_price = "\n\nPrice: ${}".format(price)
        cheapest_link = "\n\nLink: {}".format(link)

        go_button.grid(row=7,column=1, columnspan=2,rowspan=2)
        
        search_results.grid(row=1, column=5, columnspan=5, rowspan=7)
        product.grid(row=1,column=0, columnspan=4, rowspan=7)

        for obj in jsdata:
            content = jsdata[obj]
            search_results.insert(tk.END, obj + "\n")
            a = ""
            for item in content:
                a += item + ": "
                a += str(content[item])
                a += "\n"
            search_results.insert(tk.END, a + "\n")


        product.insert(tk.END, cheapest_name)
        product.insert(tk.END, cheapest_price)
        product.insert(tk.END, cheapest_link)
        # product.config(state=tk.DISABLED)

        back.grid(row=8,column=8,columnspan=2,rowspan=2)
    else:
        back = tk.Button(master=sp,text="back",padx=40,pady=40,command= lambda: [forget_frame(sp), initial_page()])
        back.grid(row=8,column=8,columnspan=2,rowspan=2)

        thread = threading.Thread(target=search_start, args=(search_item, page, sp))
        thread.start()


def track_page(search_item):

    tp = tk.Frame(master=win)
    tp.pack()
    r = tk.IntVar()
    for i in range(10):
        tp.columnconfigure(i,weight=1,minsize=70)
        tp.rowconfigure(i,weight=1,minsize=50)
    back = tk.Button(master=tp,text="back",padx=40,pady=40,command= lambda: [forget_frame(tp), initial_page()])
    email_entry = tk.Entry(master=tp,  width=50, borderwidth=4, font=('Helvetica',18))
    email_name = tk.Label(master=tp, text="Email: ", font=('Helvetica',18))
    
    track_rate = tk.Entry(master=tp, borderwidth=4)
    track_name = tk.Label(master=tp, text="track rate")
    option1 = tk.Radiobutton(master=tp, variable=r, value=2, text="Default", font=('Helvetica', 16), command=lambda: forget_grid(track_name, track_rate))
    option2 = tk.Radiobutton(master=tp, variable=r, value=1, text="Manual", font=('Helvetica', 16), command=lambda: track_manual(track_name, track_rate))
    
    thread = threading.Thread(target=track_start, args=(search_item, track_rate.get(), email_entry.get()))
    init = tk.Button(master=tp, text="Start", padx=20, pady=20, command=lambda: thread.start())

    option1.grid(row=4, column=1, columnspan=3)
    option2.grid(row=4, column=4, columnspan=3)
    
    email_name.grid(row=1,column=1)
    email_entry.grid(row=1,column=2, columnspan=5)
    init.grid(row=7, column=4, columnspan=2, rowspan=2)
    back.grid(row=8,column=8,columnspan=2,rowspan=2)

def api():
    api = BackendAPI()
    return api 

def search_start(text, page, sp):
    back = tk.Button(master=sp,text="back",padx=40,pady=40,command= lambda: [forget_frame(sp), initial_page()])
    back.grid(row=8,column=8,columnspan=2,rowspan=2)
    api().search_products(text, page)
    jsdata = file_read(json_file, 'r')
    jsdata = sorted_dic(jsdata)

    name = "!!!!!!!!"
    price = 1000000
    link = "????????"
    for product in jsdata:
        if jsdata[product]['price'] < price:
            price = jsdata[product]['price']
            name = jsdata[product]['product_name']
            link = jsdata[product]['link']
    
    
    product = tk.Text(master=sp, height=100, wrap=tk.WORD, width=200, xscrollcommand=True)
    search_results = tk.Text(master=sp, height=100, wrap=tk.WORD, width=200, yscrollcommand=True, xscrollcommand=True)
    go_button = tk.Button(master=sp, text="Link", command=lambda: [api().open_link(link)])

    cheapest_name = "Name: {}".format(name)
    cheapest_price = "\n\nPrice: ${}".format(price)
    cheapest_link = "\n\nLink: {}".format(link)

    go_button.grid(row=7,column=1, columnspan=2,rowspan=2)
    
    search_results.grid(row=1, column=5, columnspan=5, rowspan=7)
    product.grid(row=1,column=0, columnspan=4, rowspan=7)

    for obj in jsdata:
        content = jsdata[obj]
        search_results.insert(tk.END, obj + "\n")
        a = ""
        for item in content:
            a += item + ": "
            a += str(content[item])
            a += "\n"
        search_results.insert(tk.END, a + "\n")


    product.insert(tk.END, cheapest_name)
    product.insert(tk.END, cheapest_price)
    product.insert(tk.END, cheapest_link)
   

def track_start(text, time, email):
    send_mail(email, "Connected! Tracking Now! \n Current Time: {datetime.now().strftime('%H:%M:%S')}")
    if time == "":
        time = int(5)
    api().track_product(text, time)

initial_page()
win.mainloop()
