from fastapi import UploadFile, File, HTTPException, status

import os


def generate_filename(base_name, extension, counter):
    new_filename = f"{base_name}_{counter}{extension}"
    generated_name = MediaHandler.photo_dir + new_filename

    if os.path.exists(generated_name):
        return generate_filename(base_name, extension, counter + 1)
    
    return generated_name

class MediaHandler:
    media_url = "http://localhost:8000"
    photo_dir = "./static/photos/"
    ALLOWED_PHOTO_CONTENT_TYPES = ["image/jpeg", "image/png"]
    @staticmethod
    async def save_photos_of_project(
         photos: list[UploadFile]
    ) -> list:
        
        response = []
        for photo in photos:
            if photo.content_type not in MediaHandler.ALLOWED_PHOTO_CONTENT_TYPES:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid file format. Only photos (JPEG/PNG)  are allowed.")
            photo_name = photo.filename
            base_name, extension = os.path.splitext(photo_name)
            #recursive func
            generated_name = generate_filename(base_name, extension, 1)                
            
            file_content = await photo.read()
            with open(generated_name, 'wb') as photo:
                photo.write(file_content)
            photo.close()
            photo_url = MediaHandler.media_url + generated_name[1:]
            response.append(photo_url)
        return response
    
    @staticmethod
    async def update_photo_of_design_project(
         photo: UploadFile
    ):
        if photo.content_type not in MediaHandler.ALLOWED_PHOTO_CONTENT_TYPES:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid file format. Only photo (JPEG/PNG)  is allowed.")
        photo_name = photo.filename
        base_name, extension = os.path.splitext(photo_name)
        #recursive func
        generated_name = generate_filename(base_name, extension, 1)                
        
        file_content = await photo.read()
        with open(generated_name, 'wb') as photo:
            photo.write(file_content)
        photo.close()
        photo_url = MediaHandler.media_url + generated_name[1:]

        return photo_url