from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone
from io import BytesIO
import qrcode

class Url(models.Model):
    url_redirecionado = models.URLField()
    url_personalizado = models.CharField(max_length=8, unique=True)
    senha = models.CharField(max_length=30, blank=True, null=True)
    data_expiracao = models.DateTimeField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def gerar_qr_code(self):
        qr = qrcode.make(self.url_redirecionado)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        self.qr_code.save(f"qrcode_{self.url_personalizado}.png", ContentFile(buffer.getvalue()), save=False)

    def __str__(self) -> str:
        return self.url_personalizado
