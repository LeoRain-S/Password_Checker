import requests
import hashlib 
import sys
from tkinter import *

pw = ''

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again.')
    return res

def get_pw_leaks_count(hashes, hast_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines()) 
    for h, count in hashes:
        if h == hast_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1pw = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1pw[:5], sha1pw[5:]
    response = request_api_data(first5_char) 
    return get_pw_leaks_count(response, tail)



# def main(args):
#     for pw in args:
#         count = pwned_api_check(pw)
#         if count:
#             print(f'{pw} was found {count} times... you should probably use a better password!')
#         else:
#             print(f'{pw} was NOT found. Carry on!')
#     return 'done'
# if __name__ == '__main__':
#     main(sys.argv[1:])
    
    
root = Tk()  # create a root widget
root.title("Password_Checker")
root.configure(background="white")
root.minsize(500, 500)  # width, height
root.maxsize(900, 900)
width = 500 # Width 
height = 500 # Height
screen_width = root.winfo_screenwidth()  # Width of the screen
screen_height = root.winfo_screenheight() # Height of the screen
 
# Calculate Starting X and Y coordinates for Window
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry('%dx%d+%d+%d' % (width, height, x, y))

# Create Label in our window
text = Label(root, text="Enter your password below", font=("Font", 20))
text.pack(padx=50, pady=70)

e1 = Entry(root, width=30, font=('18'))
e1.pack(padx=10, pady=20)
r = Label(root, text='')
def check():
    pw = e1.get()
    count = pwned_api_check(pw)
    if pw == '':
        r.config(text='Please input a password!')
    elif count:
        r.config(text=f'{pw} was found {count} times... you should probably use a better password!')
    else:
        r.config(text=f'{pw} was NOT found. Carry on!')
    r.pack()
    return
vol_up = Button(root, text="Enter", command=check, width=10)
vol_up.pack(pady=20)

root.mainloop()
