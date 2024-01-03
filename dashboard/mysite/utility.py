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

    status_list = sheet.col_values(1)[13:]
    detail_list = []

    for status in status_list:
        if status == "ยังไม่ได้ดำเนินการ":
            detail_list.append("ยังไม่ได้ดำเนินการ")
        elif (
            status == "ขอเสนอโครงการภายใน รพ."
            or status == "ไม่ผ่านการพิจารณาอนุมัติจาก ผอก."
            or status == "พิจารณาอนุมัติและดำเนินการจัดส่ง สสจ.ลำพูน"
            or status == "โครงการมีการแก้ไขจาก สสจ.ลำพูน"
        ):
            detail_list.append("ขอเสนออนุมัติ")
        elif (
            status == "พิจารณาอนุมัติจาก นพ.สสจ.ลำพูน แล้ว"
            or status == "ขออนุมัติจัดโครงการ"
            or status == "เสนอพิจารณาอนุมัติจัดโครงการ"
            or status == "อนุมัติจัดโครงการ"
        ):
            detail_list.append("ระหว่างดำเนินงาน")
        elif (
            status == "ขออนุมัติเบิกค่าใช้จ่าย"
            or status == "ตรวจสอบความถูกต้องขออนุมัติเบิกค่าใช้จ่าย"
            or status == "เสนอพิจารณาอนุมัติเบิกค่าใช้จ่ายโครงการ"
        ):
            detail_list.append("ดำเนินงานเสร็จแล้ว")

    code_list = sheet.col_values(5)[13:]
    name_list = sheet.col_values(6)[13:]
    agency_list = sheet.col_values(10)[13:]
    total_list = [parse_amount(total) for total in sheet.col_values(15)[13:]]
    withdraw_list = [parse_amount(money) for money in sheet.col_values(17)[13:]]

    return (
        code_list,
        name_list,
        agency_list,
        status_list,
        total_list,
        withdraw_list,
        detail_list,
    )


@transaction.atomic
def updateDB(
    code_list,
    name_list,
    agency_list,
    status_list,
    total_list,
    withdraw_list,
    detail_list,
):
    for i in range(len(name_list)):
        member, created = Member.objects.update_or_create(
            projectName=name_list[i],
            defaults={
                "code": code_list[i],
                "agency": agency_list[i],
                "status": status_list[i],
                "detail": detail_list[i],
                "total": total_list[i],
                "withdraw": withdraw_list[i],
            },
        )


def getColor(mymembers):
    for member in mymembers:
        if member["detail"] == "ยังไม่ได้ดำเนินการ":
            member["color"] = "🔴"
        elif member["detail"] == "ขอเสนออนุมัติ":
            member["color"] = "🟠"
        elif member["detail"] == "ระหว่างดำเนินงาน":
            member["color"] = "🟡"
        elif member["detail"] == "ดำเนินงานเสร็จแล้ว":
            member["color"] = "🟢"

    return mymembers


def coutMember(mymembers):
    percents = [0, 0, 0, 0]
    total = len(mymembers)

    if total == 0:
        return percents

    for member in mymembers:
        if member["detail"] == "ยังไม่ได้ดำเนินการ":
            percents[0] += 1
        elif member["detail"] == "ขอเสนออนุมัติ":
            percents[1] += 1
        elif member["detail"] == "ระหว่างดำเนินงาน":
            percents[2] += 1
        elif member["detail"] == "ดำเนินงานเสร็จแล้ว":
            percents[3] += 1

    percents = [int((x / total) * 100) for x in percents]
    return percents
