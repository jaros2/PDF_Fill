from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from flask import current_app

def fill_pdf(pdf_data):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    # strona 1
    fill_first_page(can, pdf_data)
    can.showPage()

    # strona 2
    fill_second_page(can, pdf_data)
    can.showPage()

    # strona 3
    fill_third_page(can, pdf_data)
    can.showPage()

    # strona 4 (nie wypelniana)
    can.showPage()

    # strona 5
    fill_fourth_page(can, pdf_data)
    can.showPage()

    # zakonczenie wpisywania 
    can.save()
    packet.seek(0)

    # polacz nowy pdf z istniejacym
    filled_pdf_file_name = merge_with_existing_pdf(packet, pdf_data)
    return filled_pdf_file_name


def fill_first_page(can, pdf_data):
    write_to_squares(pdf_data["pesel"], 244, 409, can)
    write_to_squares(pdf_data["dob"], 244, 381, can)
    can.drawString(245, 297, pdf_data["first_name"])
    can.drawString(245, 271, pdf_data["last_name"])
    can.drawString(245, 244, pdf_data["street"])
    can.drawString(245, 218, pdf_data["bldg_num"])
    can.drawString(410, 218, pdf_data["apt_num"])
    can.drawString(245, 191, pdf_data["postal_code"])
    can.drawString(245, 164, pdf_data["city"])


def fill_second_page(can, pdf_data):
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
    can.drawString(511, 235, 'X')  # orzeczenie o niepelnosprawnosci
    can.drawString(511, 181, 'X')  # Jest domownik, który może zapewnić opiekę dziecku
    can.drawString(511, 110, 'X')  # system pracy zmianowej


def fill_third_page(can, pdf_data):
    can.drawString(440, 680, 'X')  # czy zmieniales platnika
    write_to_squares(pdf_data["spouse_pesel"], 243, 454, can)
    write_to_squares(pdf_data["spouse_dob"], 243, 392, can)
    can.drawString(245, 346, pdf_data["spouse_first_name"])
    can.drawString(245, 320, pdf_data["spouse_last_name"])
    can.drawString(190, 293, 'X')  # czy pracuje
    can.drawString(512, 293, 'X')  # system pracy zmianowej
    # can.drawString(404, 218, 'X') # czy dostal zasilek (NIE)
    can.drawString(350, 218, 'X')  # czy dostal zasilek (TAK)
    can.drawString(65, 183, 'X')  # zasilek na opieke
    can.drawString(190, 173, str(pdf_data["benefit_days_total"]))


def fill_fourth_page(can, pdf_data):
    write_to_squares(pdf_data["sign_date"], 83, 165, can)


def merge_with_existing_pdf(packet, pdf_data):
    new_pdf = PdfReader(packet)
    existing_pdf_path = os.path.join(current_app.root_path, 'static', 'Z-15A.pdf')
    with open(existing_pdf_path, "rb") as pdf_file:
        existing_pdf = PdfReader(pdf_file)
        output = PdfWriter()

        for i in range(len(new_pdf.pages)):
            page = existing_pdf.pages[i]
            page.merge_page(new_pdf.pages[i])
            output.add_page(page)

        filled_pdf_file_name = f"Z-15A_{pdf_data['first_name']}_{pdf_data['last_name']}_{pdf_data['sign_date']}.pdf"
        filled_pdf_file_name_path = os.path.join(current_app.root_path, 'static', filled_pdf_file_name)
        with open(filled_pdf_file_name_path, "wb") as output_stream:
            output.write(output_stream)

    return filled_pdf_file_name

def write_to_squares(text_to_write, x, y, canv):
    spacing = 17.90
    
    for char in text_to_write:
        canv.drawString(x, y, char)
        x = x + spacing