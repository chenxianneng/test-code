import qrcode
data = 'asdfhwueuawagaakjgagahrgoiehrgoidkfkag;oiergo;agkaegr'
img = qrcode.make(data)
img.save('e:/hello.png')

from PIL import Image
from pyzbar.pyzbar import decode
data = decode(Image.open('e:/hello.png'))
print(data)
