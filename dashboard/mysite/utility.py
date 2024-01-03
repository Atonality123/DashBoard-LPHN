import gspread
from pathlib import Path
from .models import Member
from django.db import transaction

url = "https://docs.google.com/spreadsheets/d/17z0bMg0450f1EZ86QSfulXqo3mMgapnD2n0f654Ipaw/edit?fbclid=IwAR1ZvLXSIibWkHb_RrQ5lV4ZyjL13iR0z3tmPEKaGzET-gwT6UEy_rffP_U#gid=1851865664"


def parse_amount(amount):
    amount = amount.strip()
    if amount == "-":
        return float(0)
    return float(amount.replace(",", ""))


def fetch_data():
    current_path = Path.cwd()
    current_path = current_path.joinpath("mysite\secret\credential.json")
    creds = gspread.service_account(current_path)
    sheet = creds.open_by_url(url).get_worksheet(0)

    status_list = sheet.col_values(1)[6:]
    len_status = len(status_list)

    for status in status_list:
        if status == "ผอ. ไม่เห็นชอบ" or status == "แก้ไขโครงการ":
            status_list.append("ยังไม่ได้ดำเนินการ")
        elif (
            status == "ขอจัดโครงการ"
            or status == "เสนอ สสจ."
            or status == "เสนอภายใน รพ."
        ):
            status_list.append("ขอเสนออนุมัติ")
        elif status == "เบิกค่าใช้จ่าย":
            status_list.append("ระหว่างดำเนินงาน")
        elif status == "สสจ. อนุมัติแล้ว":
            status_list.append("ดำเนินงานเสร็จแล้ว")

    code_list = sheet.col_values(5)[6:]
    name_list = sheet.col_values(6)[6:]
    agency_list = sheet.col_values(10)[6:]
    status_list = status_list[len_status:]
    total_list = [parse_amount(total) for total in sheet.col_values(15)[6:]]
    withdraw_list = [parse_amount(money) for money in sheet.col_values(17)[6:]]

    return code_list, name_list, agency_list, status_list, total_list, withdraw_list


@transaction.atomic
def updateDB(code_list, name_list, agency_list, status_list, total_list, withdraw_list):
    members = Member.objects.all().values_list("projectName", flat=True)
    for i in range(len(name_list)):
        if name_list[i] not in members:
            Member.objects.create(
                code=code_list[i],
                projectName=name_list[i],
                agency=agency_list[i],
                status=status_list[i],
                total=total_list[i],
                withdraw=withdraw_list[i],
            )


def getColor(mymembers):
    for member in mymembers:
        if member["status"] == "ยังไม่ได้ดำเนินการ":
            member["color"] = "🔴"
        elif member["status"] == "ขอเสนออนุมัติ":
            member["color"] = "🟠"
        elif member["status"] == "ระหว่างดำเนินงาน":
            member["color"] = "🟡"
        elif member["status"] == "ดำเนินงานเสร็จแล้ว":
            member["color"] = "🟢"

    return mymembers


def coutMember(mymembers):
    percents = [0, 0, 0, 0]
    total = len(mymembers)

    if total == 0:
        return percents

    for member in mymembers:
        if member["status"] == "ยังไม่ได้ดำเนินการ":
            percents[0] += 1
        elif member["status"] == "ขอเสนออนุมัติ":
            percents[1] += 1
        elif member["status"] == "ระหว่างดำเนินงาน":
            percents[2] += 1
        elif member["status"] == "ดำเนินงานเสร็จแล้ว":
            percents[3] += 1

    percents = [int((x / total) * 100) for x in percents]
    return percents
