import random
import string
import constant

def generate_session_code(length):
    result1 = ''.join((random.choice(string.ascii_uppercase) for x in range(length)))
    return result1

def decode_form_encoded(data : str) -> str:
    for row in constant.FORM_CODING_TABLE:
        if data.count(row[2]) >0:
            print("DATA BEFORE:"  ,data)
            data=data.replace(row[2], row[0])
            print("DATA AFTER:"  ,data)
    return data
