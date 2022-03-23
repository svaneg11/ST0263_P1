import node.config as config
import pickle


data = {}
current_slot = 0


def set(hash: str, key: str, value: str):
    global data
    if not current_slot == hash:
        load(hash)
    data[key] = value
    save(hash)


def get(hash: str, key: str):
    if not current_slot == hash:
        load(hash)
    return data.get(key, None)


def delete(hash: str, key: str):
    global data
    if not current_slot == hash:
        load(hash)
    if key in data:
        del data[key]
        save(hash)
        return True
    return False


def save(hash: str):
    data_file = open(config.get_data_path(hash), 'wb')
    pickle.dump(data, data_file)
    data_file.close()


def load(hash: str):
    global data, current_slot
    try:
        data_file = open(config.get_data_path(hash), 'rb')
        data = pickle.load(data_file)
        print(data)
        current_slot = hash
        data_file.close()
    except FileNotFoundError:
        data = {}
        current_slot = hash
