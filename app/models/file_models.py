import os


class FileModel:
    upload_url = f"{os.environ['FLET_APP_STORAGE_TEMP']}/uploads"

    def __init__(self):
        self.selected_files = []

    def set_selected_files(self, files) -> list:
        self.selected_files = files
        return self.selected_files

    def get_file_path(self, file_name):
        if file_name not in self.selected_files:
            return None

        if not os.path.exists(f"{self.upload_url}/{file_name}"):
            return None
        return f"{self.upload_url}/{file_name}"

if __name__ == "__main__":
    file_model = FileModel()
    file_model.set_selected_files(["test1.txt", "test2.txt"])
    print(file_model.selected_files)

    if not os.path.exists(f"{file_model.upload_url}/test1.txt"):
        # テストファイルがない場合は作成
        with open(f"{file_model.upload_url}/test1.txt", "w") as f:
            f.write("test1.txt")
    print(file_model.get_file_path("test1.txt")) # /tmp/uploads/test1.txt
    print(file_model.get_file_path("test2.txt")) # None
    print(file_model.get_file_path("test3.txt")) # None
