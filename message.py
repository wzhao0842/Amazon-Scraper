import smtplib 

class Message:
    def __init__(self):
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 475)
        
    def send_email(self, recipient, message):
        self.server.login("noreplyatracker@gmail.com", "awsome#123456")
        self.server.sendmail(
        "from@address.com", 
        recipient, 
        message)
        self.server.quit()
    
if __name__ == '__main__':
    m = Message()
    command = "sudo python -m smtpd -c DebuggingServer -n localhost:465"
    try:
        m.send_email("connor@bigfatplanet.com", "hello world")
        print("....")
    except Exception as e:
        print(e)
    


    

    