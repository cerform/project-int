class Preview:
    def __init__(self, file_manager):
        self.file_manager = file_manager

    def get_file_content(self, file_path):
        absolute_file_path = os.path.join(self.file_manager.upload_folder, file_path)
        return self.file_manager.extract_text(absolute_file_path)
