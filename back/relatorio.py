from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

cvn = canvas.Canvas("teste.pdf", pagesize=A4)

nome_empresa = "Sentra"

cvn.setFont("Times-Roman", 32,)
cvn.drawString(255, 815, nome_empresa)
cvn.setFont("Times-Roman", 18)
cvn.drawString(280, 780, "Teste 2")
cvn.save()