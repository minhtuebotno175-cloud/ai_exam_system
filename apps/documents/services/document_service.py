"""
Main business logic service for documents
"""
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError
from ..models import Document
from .document_processor import DocumentProcessor
from .text_extractor import TextExtractor
import logging

logger = logging.getLogger(__name__)


class DocumentService:
    """Main business logic for documents"""
    
    def __init__(self):
        self.processor = DocumentProcessor()
        self.extractor = TextExtractor()
    
    def upload_and_process(
        self, 
        file: UploadedFile, 
        user,
        extract_immediately: bool = True
    ) -> Document:
        """Upload file and extract text"""
        try:
            # Validate
            logger.info(f"Validating file: {file.name}")
            self.processor.validate_file(file)
            
            # Create document
            document = Document.objects.create(
                user=user,
                filename=file.name,
                file_path=file,
                file_size=file.size,
                file_type=file.content_type,
                status='uploaded'
            )
            
            logger.info(f"Document created: ID={document.id}")
            
            # Extract text
            if extract_immediately:
                self.extract_text(document)
            
            return document
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Upload error: {str(e)}")
            raise Exception(f"Lỗi upload: {str(e)}")
    
    def extract_text(self, document: Document) -> Document:
        """Extract text from document"""
        try:
            document.status = 'processing'
            document.save()
            
            logger.info(f"Extracting text: {document.filename}")
            
            # Extract
            file_path = document.file_path.path
            extracted_text = self.extractor.extract(file_path)
            
            # Update
            document.extracted_text = extracted_text
            document.status = 'completed'
            document.save()
            
            logger.info(f"Extraction completed: {len(extracted_text)} chars")
            
            return document
            
        except Exception as e:
            logger.error(f"Extraction error: {str(e)}")
            document.status = 'failed'
            document.save()
            raise Exception(f"Lỗi trích xuất: {str(e)}")
    
    def delete_document(self, document: Document) -> bool:
        """Delete document and file"""
        try:
            if document.file_path:
                document.file_path.delete(save=False)
            document.delete()
            logger.info(f"Document deleted: {document.filename}")
            return True
        except Exception as e:
            logger.error(f"Delete error: {str(e)}")
            raise Exception(f"Lỗi xóa file: {str(e)}")
