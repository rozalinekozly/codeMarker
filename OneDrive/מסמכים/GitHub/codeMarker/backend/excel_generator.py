from openpyxl import Workbook

def generate_excel_report(results, report_path="../reports/report.xlsx"):
    print("ENTERED generate_excel_report()")

    wb = Workbook()
    ws = wb.active
    ws.title = "Results"

    try:
        ws["A1"] = "hi"
        wb.save(report_path)
        print(f"Excel saved at {report_path}")
    except Exception as e:
        print(f"Error while saving Excel: {e}")

    return report_path
