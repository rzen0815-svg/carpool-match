from flask import Flask, render_template, request, jsonify
from matcher import create_request, match_requests
from storage import (
    load_requests,
    save_requests,
    delete_request_by_contact,
    remove_expired_requests,
)

app = Flask(__name__)


def contact_exists(requests_list, contact):
    for person in requests_list:
        if person["contact"] == contact:
            return True
    return False


def find_user_group(groups, contact):
    for group in groups:
        for person in group:
            if person["contact"] == contact:
                return group
    return None


def find_waiting_person(waiting, contact):
    for person in waiting:
        if person["contact"] == contact:
            return person
    return None


def find_person_in_requests(requests_list, contact):
    for person in requests_list:
        if person["contact"] == contact:
            return person
    return None


@app.route("/", methods=["GET", "POST"])
def index():
    remove_expired_requests()

    if request.method == "POST":
        contact = request.form.get("contact", "").strip()
        time_str = request.form.get("time", "").strip()
        destination = request.form.get("destination", "").strip()
        group_size = request.form.get("group_size", "").strip()

        current_request = create_request(contact, time_str, destination, group_size)

        requests_list = load_requests()

        if contact_exists(requests_list, contact):
            return render_template(
                "message.html",
                title="提交失败",
                message="这个联系方式已经提交过了，请先查询状态或取消原报名后再重新提交。",
                success=False,
            )

        requests_list.append(current_request)
        save_requests(requests_list)

        groups, waiting = match_requests(requests_list)

        user_group = find_user_group(groups, contact)
        waiting_person = find_waiting_person(waiting, contact)

        return render_template(
            "result.html",
            user_group=user_group,
            waiting_person=waiting_person,
            contact=contact,
        )

    return render_template("index.html")


@app.route("/check_contact", methods=["POST"])
def check_contact():
    remove_expired_requests()

    contact = request.form.get("contact", "").strip()
    requests_list = load_requests()

    exists = contact_exists(requests_list, contact)

    return jsonify({"exists": exists})


@app.route("/manage", methods=["GET", "POST"])
def manage():
    remove_expired_requests()

    if request.method == "POST":
        contact = request.form.get("contact", "").strip()

        requests_list = load_requests()
        groups, waiting = match_requests(requests_list)

        user_group = find_user_group(groups, contact)
        waiting_person = find_waiting_person(waiting, contact)
        existing_person = find_person_in_requests(requests_list, contact)

        return render_template(
            "status_result.html",
            user_group=user_group,
            waiting_person=waiting_person,
            existing_person=existing_person,
            contact=contact,
        )

    return render_template("manage.html")


@app.route("/cancel_confirm", methods=["POST"])
def cancel_confirm():
    remove_expired_requests()

    contact = request.form.get("contact", "").strip()
    deleted = delete_request_by_contact(contact)

    if deleted:
        return render_template(
            "message.html",
            title="取消报名成功",
            message="你的报名记录已经删除。",
            success=True,
        )
    else:
        return render_template(
            "message.html",
            title="取消失败",
            message="没有找到这个联系方式对应的报名记录。",
            success=False,
        )


if __name__ == "__main__":
    app.run(debug=True)
