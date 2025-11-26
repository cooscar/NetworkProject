import requests

try:
    response = requests.get('https://api.ipify.org/?format=json')
    ip = response.json()
    print("Your ip is {}".format(ip["ip"]))

    
        

except:
    print(f"An error occurued: \n", Exception)