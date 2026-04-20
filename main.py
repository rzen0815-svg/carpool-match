from matcher import create_request, match_requests


def input_request():
    while True:
        try:
            contact = input("请输入联系方式: ").strip()
            if contact == "":
                print("联系方式不能为空。")
                continue

            time_str = input("请输入出发时间(格式如 14:20): ").strip()
            destination = input("请输入目的地(福州站/福州南站): ").strip()

            request = create_request(contact, time_str, destination)
            return request

        except ValueError as e:
            print(f"输入有误：{e}，请重新输入。")


requests = []
existing_contacts = set()

while True:
    try:
        count = int(input("请输入本次要录入多少个人: "))
        if count <= 0:
            print("人数必须大于 0。")
            continue
        break
    except ValueError:
        print("请输入正确的整数。")

for i in range(count):
    print(f"\n正在录入第{i + 1}个人的信息")

    while True:
        request = input_request()

        if request["contact"] in existing_contacts:
            print("这个联系方式已经录入过了，请重新输入。")
            continue

        existing_contacts.add(request["contact"])
        requests.append(request)
        break

groups, waiting = match_requests(requests)

print("匹配成功的组：")
for group in groups:
    print("-----")
    for person in group:
        print(
            person["contact"], person["time"].strftime("%H:%M"), person["destination"]
        )

print("\n等待中的人：")
for person in waiting:
    print(person["contact"], person["time"].strftime("%H:%M"), person["destination"])
