import node.config as config
import pickle
from typing import List


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


def multiple_set(items: List):
    global data
    # Separate items by hash so it only has to open the file once for each hash
    items_by_hash = get_items_by_hash(items)

    # Save in the file all the items that correspond to that hash slot.
    for hash_slot, items_list in items_by_hash.items():
        if not current_slot == hash_slot:
            load(hash_slot)
        for it in items_list:
            data[it['key']] = it['value']
        save(hash_slot)


def multiple_get(items: List):
    global data
    # Separate items by hash so it only has to open the file once for each hash
    items_by_hash = get_items_by_hash(items)

    # Retrieve all the items that correspond to each hash slot.
    response_items = []
    not_found = []
    for hash_slot, items_list in items_by_hash.items():
        if not current_slot == hash_slot:
            load(hash_slot)
        for it in items_list:
            value = data.get(it['key'])
            if not value:
                not_found.append(it['key'])
            else:
                response_items.append({'key': it['key'], 'value': value})
    all_success = len(not_found) == 0
    return all_success, response_items, not_found


def multiple_del(items: List):
    global data
    # Separate items by hash so it only has to open the file once for each hash
    items_by_hash = get_items_by_hash(items)

    # Delete all the items that correspond to each hash slot.
    deleted_items = []
    not_found = []
    for hash_slot, items_list in items_by_hash.items():
        if not current_slot == hash_slot:
            load(hash_slot)
        for it in items_list:
            if it['key'] in data:
                deleted_items.append(it['key'])
                del data[it['key']]
            else:
                not_found.append(it['key'])
        save(hash_slot)
    all_success = len(not_found) == 0
    return all_success, deleted_items, not_found


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


def get_items_by_hash(items: List):
    # Separate items by hash so it only has to open the file once for each hash
    items_by_hash = {}
    for item in items:
        item = item.dict()
        if item['hash'] not in items_by_hash:
            items_by_hash[item['hash']] = []
        items_by_hash[item['hash']].append(item)

    return items_by_hash
