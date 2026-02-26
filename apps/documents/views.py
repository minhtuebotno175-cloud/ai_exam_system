from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Document
from .forms import DocumentUploadForm

@login_required
def upload_view(request):
    """Upload document"""
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            
            # Lấy thông tin file
            uploaded_file = request.FILES['file_path']
            document.filename = uploaded_file.name
            document.file_size = uploaded_file.size
            document.file_type = uploaded_file.content_type
            
            document.save()
            
            messages.success(request, f'Tải lên file "{document.filename}" thành công!')
            return redirect('core:dashboard')
    else:
        form = DocumentUploadForm()
    
    return render(request, 'documents/upload.html', {'form': form})

@login_required
def document_list_view(request):
    """List all documents"""
    documents = Document.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'documents/list.html', {'documents': documents})

@login_required
def document_detail_view(request, pk):
    """Document detail"""
    document = get_object_or_404(Document, pk=pk, user=request.user)
    return render(request, 'documents/detail.html', {'document': document})

@login_required
def document_delete_view(request, pk):
    """Delete document"""
    document = get_object_or_404(Document, pk=pk, user=request.user)
    
    if request.method == 'POST':
        filename = document.filename
        document.file_path.delete()  # Xóa file trong media/
        document.delete()  # Xóa record trong database
        
        messages.success(request, f'Đã xóa file "{filename}"!')
        return redirect('core:dashboard')
    
    return render(request, 'documents/delete_confirm.html', {'document': document})