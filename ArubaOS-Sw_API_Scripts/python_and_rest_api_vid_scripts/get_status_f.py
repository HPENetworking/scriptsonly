import requests
import os

list_of_tin = ['192.168.1.29', '192.168.1.218', '192.168.1.219']

print('Home Lab Status:')


def g_status(tin_list):
    wrong_code = []
    for ip in tin_list:
        url = 'http://' + ip + '/rest/v1/system/status'
        get_status_response = requests.get(url, timeout=2)
        g_status_dict = get_status_response.json()
        print("HOSTNAME: {} \t IMAGE: {} \t SERIAL_NUMBER: {}".format(g_status_dict['name'],
                                                                  g_status_dict['firmware_version'],
                                                                  g_status_dict['serial_number']))

        if '16.03' not in g_status_dict['firmware_version']:
            wrong_code.append(g_status_dict['name'])

    for x in wrong_code:
        print("Warning! Wrong code running on {}".format(x))

    if wrong_code is not []:
        f = open(os.path.join("wrong_code.txt"), "w")
        f.write("Attention humanoid! The following switches are NON-COMPLIANT:\n")
        for x in wrong_code:
            f.write(x)
        f.close()


def main():
    g_status(list_of_tin)


if __name__ == '__main__':
    main()

