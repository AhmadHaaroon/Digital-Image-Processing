def input_text(text,max_option=None):
    selected=False
    option=-1
    while(selected==False):
        try:
            option = int(input(text))
            if(option<=0 or option>max_option):
                print("\nInvalid option entered, please try again.\n")
            else:
                print()
                selected=True
        except:
            print("\nInvalid option entered, please try again.\n")
    
    return option