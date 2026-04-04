from fastapi import File, UploadFile, HTTPException
import magic
import hashlib



class FileValidator:
    ALLOWED_IMAGE_TYPES = [
        'image/jpeg', 
        'image/png', 
        'image/gif', 
        'image/webp', 
        'image/avif', 
        'image/bmp',
        'image/jpg'
    ]

    ALLOWED_DOCUMENT_TYPES = [
    'application/pdf',
    'text/plain',
    'text/html',
    'text/markdown',
    'text/csv',
    'application/msword',  # .doc
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx
    'application/vnd.ms-excel',  # .xls
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
    'application/vnd.ms-powerpoint',  # .ppt
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',  
    'application/zip',

    ]


    MAX_IMAGE_SIZE = 10 * 1024 * 1024
    MAX_DOCUMENT_SIZE = 50 * 1024 * 1024 


    @classmethod
    def get_allowed_types(cls, category: str = None) -> list:
        """Получить разрешенные типы по категории"""
        if category == 'image':
            return cls.ALLOWED_IMAGE_TYPES
        elif category == 'document':
            return cls.ALLOWED_DOCUMENT_TYPES
        else:
            return (cls.ALLOWED_IMAGE_TYPES + cls.ALLOWED_DOCUMENT_TYPES)

    @classmethod
    def get_category(cls, content_type: str) -> str:
        """Определить категорию файла"""
        if content_type.startswith('image/'):
            return 'image'
        elif content_type.startswith('video/'):
            return 'video'
        else:
            return 'document'
        
    @classmethod
    def is_allowed(cls, content_type: str) -> bool:
        all_allowed = (cls.ALLOWED_IMAGE_TYPES + cls.ALLOWED_DOCUMENT_TYPES)
        return content_type in all_allowed
    
    @classmethod
    def get_max_size(cls, content_type: str) -> int:
        """Получить максимальный размер для типа файла"""
        if content_type.startswith('image/'):
            return cls.MAX_IMAGE_SIZE
        else:
            return cls.MAX_DOCUMENT_SIZE

    @classmethod
    async def validate_file(cls, file: UploadFile) -> dict:
        contents = await file.read()
        file_size = len(contents)
        
        try:
            mime = magic.Magic(mime=True)
            real_content_type = mime.from_buffer(contents)
        except:
            real_content_type = file.content_type or 'application/octet-stream'


        if not cls.is_allowed(real_content_type):
            allowed_str = ', '.join(cls.get_allowed_types())
            raise HTTPException(
                400,
                f"File type '{real_content_type}' is not allowed. "
                f"Allowed types: {allowed_str}"
            )
        
        max_size = cls.get_max_size(real_content_type)
        if file_size > max_size:
            raise HTTPException(
                400,
                f"File too large. Max size: {max_size // (1024*1024)}MB, "
                f"Your file: {file_size // (1024*1024)}MB"
            )
        

        md5_hash = hashlib.md5(contents).hexdigest()
        await file.seek(0)

        return {
            'filename': file.filename,
            'size_bytes': file_size,
            'size_mb': round(file_size / (1024 * 1024), 2),
            'content_type': file.content_type,
            'category': cls.get_category(real_content_type),
            'md5': md5_hash,
            'is_allowed': True
        }