from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_client_debits_pdf(client, debits):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()

    content = [
        Paragraph(
            "Relatório de Débitos",
            styles["Title"],
        ),
        Spacer(1, 20),
        Paragraph(
            f"<b>Cliente:</b> {client.name}",
        ),
        Paragraph(
            f"<b>Documento:</b> {client.document}",
        ),
        Spacer(1, 20),
    ]

    data = [["Descrição", "Valor", "Vencimento", "Situação"]]

    total = 0
    total_pendente = 0
    total_pago = 0

    for debit in debits:
        valor = float(debit.amount)
        total += valor

        if debit.paid:
            situacao = "Pago"
            total_pago += valor
        else:
            situacao = "Pendente"
            total_pendente += valor

        data.append(
            [
                debit.description,
                f"R$ {valor:.2f}",
                debit.due_date.strftime("%d/%m/%Y"),
                situacao,
            ]
        )

    table = Table(
        data,
        colWidths=[7 * cm, 3 * cm, 3 * cm, 3 * cm],
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1D3557")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 8),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ]
        )
    )

    content.append(table)

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"<b>Total:</b> R$ {total:.2f}",
        )
    )
    content.append(
        Paragraph(
            f"<b>Total pago:</b> R$ {total_pago:.2f}",
        )
    )
    content.append(
        Paragraph(
            f"<b>Total pendente:</b> R$ {total_pendente:.2f}",
        )
    )

    document.build(content)

    buffer.seek(0)

    return buffer
