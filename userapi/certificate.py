
from reportlab.pdfgen import canvas
import datetime

def create_certificate(fname, person_name, course_name):
    '''
    :fname: real path
    '''
    c = canvas.Canvas(fname)
    c.setTitle("Certificate")
    init_y = 800
    c.drawString(100, init_y,"Certificate Awarded To")
    init_y -= 20
    c.drawString(100, init_y, person_name)
    init_y -= 20
    c.drawString(100, init_y,"For")
    init_y -= 20
    c.drawString(100, init_y, course_name)
    init_y -= 20
    c.drawString(100, init_y, "On")
    init_y -= 20
    datetime_now = datetime.datetime.now()
    datenow = '{} - {} - {}'.format(
        datetime_now.year, 
        datetime_now.month, 
        datetime_now.day)
    c.drawString(100, init_y, datenow)
    c.save()