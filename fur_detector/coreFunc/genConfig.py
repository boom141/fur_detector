
import os,secrets,time,json

def create_config():
    root_path = os.getcwd()
    config_file = root_path + '/device.config.json'

    config = {
        "access_token":  secrets.token_urlsafe(),
        "device_id": str(time.time()).split('.')[0],
        "name": 'Binbong cleaner',
        "type": 'device',
        "user": None
    }

    if not os.path.exists(config_file):
        with open(config_file, 'w') as file:
            json.dump(config, file)
        
        print('[SUCCESSFUL]: Config file created')
    else:
        print('[CANCELLED]: Config file existing')

    return config