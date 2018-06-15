import requests
import pprint as pp

tin = ['192.168.1.29', '192.168.1.218', '192.168.1.219']

wrong_code = []
for ip in tin:
    url = 'http://' + ip + '/rest/v1/system/status'
    get_status_response = requests.get(url, timeout=2)
    #pp.pprint(get_status_response.json())
    g_status_dict = get_status_response.json()
    print("HOSTNAME: {} \t IMAGE: {} \t SERIAL_NUMBER: {}".format(g_status_dict['name'],
                                                                  g_status_dict['firmware_version'],
                                                                  g_status_dict['serial_number']))
    if '16.03' not in g_status_dict['firmware_version']:
        wrong_code.append(g_status_dict['name'])

print('List of devices with wrong code:')
print(' ,'.join(wrong_code))

