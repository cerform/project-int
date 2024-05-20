class Search:
    def __init__(self, file_manager):
        self.file_manager = file_manager

    def search_files(self, query):
        results = {}
        for category, files in self.file_manager.get_categories().items():
            for file in files:
                file_path = os.path.join(category, file)
                content = self.file_manager.extract_text(file_path)
                if query.lower() in content.lower():
                    results[file_path] = content
        return results
