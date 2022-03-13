import config
import pickle


data = {}


def set(key: str, value: str):
    global data
    data[key] = value
    save()


def get(key: str):
    return data.get(key, None)


def delete(key: str):
    global data
    if key in data:
        del data[key]
        save()
        return True
    return False


def save():
    data_file = open(config.get_data_path(), 'wb')
    pickle.dump(data, data_file)
    data_file.close()


def load():
    global data, data_file
    try:
        data_file = open(config.get_data_path(), 'rb')
        data = pickle.load(data_file)
        print(data)
        data_file.close()
    except FileNotFoundError:
        data = {}
