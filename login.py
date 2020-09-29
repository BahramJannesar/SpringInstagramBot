import codecs
import os.path
import json

try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)
except ImportError:
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)


def login(username, password, user_agent='Instagram 121.0.0.29.119 Android (26/8.0.0; 560dpi; 1440x2792; samsung; SM-G955F; dream2lte; samsungexynos8895; en_US; 185203708)'):
    device_id = None
    try:
        settings_file = "latest_client.json"
        if not os.path.isfile(settings_file):
            api = Client(
                username, password,
                user_agent=user_agent,
                on_login=lambda x: onlogin_callback(x, "latest_client.json"),
            )
        else:
            with open(settings_file) as file_data:
                cached_settings = json.load(file_data, object_hook=from_json)
            device_id = cached_settings.get('device_id')
            api = Client(
                username, password,
                user_agent=user_agent,
                settings=cached_settings,
            )

    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        api = Client(
            username, password,
            device_id=device_id,
            user_agent=user_agent,
            on_login=lambda x: onlogin_callback(x, "latest_client.json"))

    except ClientLoginError as e:
        print('ClientLoginError {0!s}'.format(e))
        exit(9)
    except ClientError as e:
        print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
        exit(9)
    except Exception as e:
        print('Unexpected Exception: {0!s}'.format(e))
        exit(99)

    return api
