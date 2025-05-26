# utils/qrgen.py
import qrcode
from io import BytesIO

def generate_qr_code(data: str) -> BytesIO:
    qr = qrcode.QRCode(
        version=1,
        box_size=8,
        border=2
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="cyan", back_color="black")

    # Convert to BytesIO
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
