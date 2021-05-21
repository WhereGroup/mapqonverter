class CheckIfStyleFileIsAlreadyInStorageService:
    def __init__(self):
        self.style_file_exists_in_storage = False

    def check_style_file(self, storage, style_file_to_export):
        """ This function checks if the style file to export ist already in storage or not

        :param storage: The storage for the style-files
        :param style_file_to_export: self-explaining
        :return:
        """
        for index in range(0, storage.FileCount):
            style_file_name = storage.File[index]
            if style_file_to_export == style_file_name:
                self.style_file_exists_in_storage = True
                break
