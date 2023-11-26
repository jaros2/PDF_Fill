from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def fill_pdf(pdf_data):
    packet = io.BytesIO()

    can = canvas.Canvas(packet, pagesize=A4)

    write_to_squares(pdf_data["pesel"], 244, 409, can)
    write_to_squares(pdf_data["dob"], 244, 381, can)
    can.drawString(245, 297, pdf_data["first_name"])
    can.drawString(245, 271, pdf_data["last_name"])
    can.drawString(245, 244, pdf_data["street"])
    can.drawString(245, 218, pdf_data["bldg_num"])
    can.drawString(410, 218, pdf_data["apt_num"])
    can.drawString(245, 191, pdf_data["postal_code"])
    can.drawString(245, 164, pdf_data["city"])
    
    can.showPage()

    write_to_squares(pdf_data["employer_tax_id"], 244, 710, can)
    can.drawString(245, 580, pdf_data["employer_name"])
    write_to_squares(pdf_data["bank_acct"], 47, 534, can)
    can.drawString(50, 462, pdf_data["date_from"])
    can.drawString(125, 462, '-')
    can.drawString(145, 462, pdf_data["date_to"])
    can.drawString(230, 462, pdf_data["l4_num"])
    write_to_squares(pdf_data["child_pesel"], 243, 396, can)
    can.drawString(245, 336, pdf_data["child_name"])
    can.drawString(245, 309, pdf_data["child_last_name"])
    write_to_squares(pdf_data["child_dob"], 243, 283, can)
    can.drawString(511, 235, 'X') # orzeczenie o niepelnosprawnosci
    can.drawString(511, 181, 'X') # Jest domownik, który może zapewnić opiekę dziecku
    can.drawString(511, 110, 'X') # system pracy zmianowej
    
    can.showPage()

    can.drawString(440, 680, 'X') # czy zmieniales platnika
    
    write_to_squares(pdf_data["spouse_pesel"], 243, 454, can)
    write_to_squares(pdf_data["spouse_dob"], 243, 392, can)
    can.drawString(245, 346, pdf_data["spouse_first_name"])
    can.drawString(245, 320, pdf_data["spouse_last_name"])
    can.drawString(190, 293, 'X') # czy pracuje
    can.drawString(512, 293, 'X') # system pracy zmianowej
    can.drawString(404, 218, 'X') # czy dostal zasilek
    # can.drawString(65, 183, 'X') # zasilek na opieke 
    # can.drawString(190, 173, pdf_data["benefit_days_total"])

    can.showPage()

    can.showPage()

    write_to_squares(pdf_data["sign_date"], 83, 165, can)

    can.showPage()
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfReader(packet)
    # read your existing PDF
    existing_pdf = PdfReader(open("Z-15A.pdf", "rb"))
    output = PdfWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    for i in  range(5):
        page = existing_pdf.pages[i]
        page.merge_page(new_pdf.pages[i])
        output.add_page(page)

    # finally, write "output" to a real file
    output_stream = open("Z-15A-filled.pdf", "wb")
    output.write(output_stream)
    output_stream.close()

def write_to_squares(text_to_write, x, y, canv):
    spacing = 17.90
    
    for char in text_to_write:
        canv.drawString(x, y, char)
        x = x + spacing

        
    

moje_dane = dict(first_name='Mateusz', 
                 last_name='Jaros',
                 pesel='84021809532',
                 dob='18021984',
                 street='Rzemieslnicza',
                 bldg_num='34',
                 apt_num='36',
                 postal_code='30-363',
                 city='Kraków',
                 phone_num='',
                 employer_tax_id='5220019702',
                 employer_name='GE Medical Systems Polska',
                 bank_acct='45114020040000370277130441',
                 date_from='06.11.2023',
                 date_to='09.11.2023',
                 l4_num='ZK 3772689',
                 child_pesel='22291401371',
                 child_name='Filip',
                 child_last_name='Jaros',
                 child_dob='14092022',
                 spouse_pesel='91041803482',
                 spouse_dob='18041991',
                 spouse_first_name='Karolina',
                 spouse_last_name='Jaros',
                 spouse_received_benefit='No',
                 benefit_days_total='',
                 sign_date='23112023'



                )

fill_pdf(moje_dane)
