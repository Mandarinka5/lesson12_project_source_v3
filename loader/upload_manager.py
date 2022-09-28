import os
import random

from loader.exeptions import PictureFormatNotSupportedError, PictureNotUploadedError, OutOfFreeNamesError


class UploadManager:

    def get_free_filename(self, folder, file_type):
        attempts = 0
        RANGE_OF_IMAGE_NUMBER = 100
        LIMIT_ATTEMPTS = 1000

        while True:
            pic_name = str(random.randint(0, 10000))
            filename_to_save = f"{pic_name}.{file_type}"
            os_path = os.path.join(folder, filename_to_save)
            is_filename_occupied = os.path.exists(os_path)

            if not is_filename_occupied:
                return filename_to_save

            attempts += 1

            if attempts > LIMIT_ATTEMPTS:
                raise OutOfFreeNamesError("No free names")

    def is_file_type_valid(self, file_type):

        if file_type.lower() in ["jpg", "jpeg", "gif", "png", "WebP"]:
            return True
        return False

    def save_with_random_name(self, picture):

        # Получаем данные картинки

        filename = picture.filename
        file_type = filename.split(".")[-1]

        # Проверяем валидность картинки

        if not self.is_file_type_valid(file_type):
            raise PictureFormatNotSupportedError(f"Формат {file_type} не поддерживается")

        # получим свободное имя

        folder = os.path.join(".", "uploads", "images")
        filename_to_save = self.get_free_filename(folder, file_type)

        # сохраняем под новым именем
        try:
            picture.save(os.path.join(folder, filename_to_save))
        except FileNotFoundError:
            raise PictureNotUploadedError(f"{folder, filename_to_save}")

        return filename_to_save


