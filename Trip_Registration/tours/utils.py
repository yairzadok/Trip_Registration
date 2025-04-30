import qrcode
from io import BytesIO

def generate_qr_with_text(text):
    """
    יוצרת QR קוד שמכיל את הטקסט שינתן.
    מחזירה אובייקט BytesIO שמוכן לשליחה במייל.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    output = BytesIO()
    img.save(output, format="PNG")
    return output
