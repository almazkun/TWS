import requests

from datetime import datetime


def IIN_to_DOB(IIN):
    """
    return DOG IIN provided
    http://adilet.zan.kz/rus/docs/P030000565_
    1 - для мужчин, родившихся в 19 веке;
    2 - для женщин, родившихся в 19 веке;
    3 - для мужчин, родившихся в 20 веке;
    4 - для женщин, родившихся в 20 веке;
    5 - для мужчин, родившихся в 21 веке;
    6 - для женщин, родившихся в 21 веке. 
    """
    centuries = {"1": "18", "2": "18", "3": "19", "4": "19", "5": "20", "6": "20"}
    return f"{centuries[IIN[6]]}{IIN[:2]}-{IIN[2:4]}-{IIN[4:6]}"


def calculate_age(born):
    born = datetime.strptime(str(born), "%Y-%m-%d")
    today = datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def is_a_business(IIN):

    API_call_url = f"https://stat.gov.kz/api/juridical/gov/?bin={IIN}&lang=ru"
    try:
        request = requests.get(API_call_url)
    except:
        raise "Connection Error"
    if request.json()["success"] == False:
        return False
    elif request.json()["success"] == True:
        return True


is_a_business("870731300311")
is_a_business("870503399132")
is_a_business("000000200000")


{"success": False, "obj": None, "description": None}
