import pikepdf
pdf_file_path = str(input('Please enter path to the PDF: '))
password_file_path = str(input('Please enter location of the password file: '))

with open(password_file_path) as f:
    lines = f.readlines()
    for password in lines:
        try:
            password = password.strip()
            pdf = pikepdf.open(pdf_file_path,password=password)
            
            print(f"Password Found {password}")
            break
        except:
            print(f"Wrong Passowrd --> {password}")
