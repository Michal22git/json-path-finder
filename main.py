import json


class FindPath:
    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        try:
            with open('file.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File not found")
        except json.JSONDecodeError:
            print(f"Invalid file content")

    def search(self, data_to_check, path_taken, target, is_key=True):
        path = []
        if type(data_to_check) is dict:
            items_to_search = data_to_check.items()
        elif type(data_to_check) is list:
            items_to_search = enumerate(data_to_check)
        else:
            return path

        for key, value in items_to_search:
            current_path = path_taken.copy()
            current_path.append(key)
            check_value = key if is_key else value
            if check_value == target:
                path.append(current_path)
            if isinstance(value, (dict, list)):
                path.extend(self.search(value, current_path, target, is_key))
        return path

    def seek_path(self, target_key, is_key=True):
        if self.data:
            path_iterator = self.search(self.data, [], target_key, is_key)
            paths_found = list(path_iterator)
            self.save_paths(paths_found, target_key)
            return self.format_paths(paths_found)
        return []

    def format_paths(self, paths):
        formatted_paths = []
        for path in paths:
            formatted_path = ''.join(['["{}"]'.format(item) if isinstance(item, str) else '[{}]'.format(item) for item in path])
            formatted_paths.append(formatted_path)
        return formatted_paths

    def save_paths(self, paths, target):
        with open('result.txt', 'a') as file:
            for path in paths:
                formatted_path = ''.join(['["{}"]'.format(item) if isinstance(item, str) else '[{}]'.format(item) for item in path])
                file.write(f'{target}: {formatted_path}\n')


if __name__ == "__main__":
    target_key = 'age'
    target_value = 'HR'

    seeker = FindPath()

    key_paths = seeker.seek_path(target_key, is_key=True)
    if key_paths:
        print(f"Found {len(key_paths)} paths by key:")
        for path in key_paths:
            print(path)
        print("")

    value_paths = seeker.seek_path(target_value, is_key=False)
    if value_paths:
        print(f"Found {len(value_paths)} paths by value:")
        for path in value_paths:
            print(path)
