class LogFile():
    def __init__(self, user_data):
        """@param : user_data -> dictionnary containing user-defined data, such as:
        archive_file_path, temp_archive_file_path, card_line_separator..."""
        self.user_data = user_data


    def write_log_file(self, args, path):
        log = self.user_data["CARD_LINE_CHAR"] + self.user_data["CARD_LINE_CHAR"].join(str(arg) for arg in args) + self.user_data["CARD_LINE_CHAR"]
        with open(path, 'w') as file:
            file.write(log + "\n")

        