from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from matcher import create_request, match_requests
import os
from functools import wraps
from storage import (
    load_requests,
    save_requests,
    delete_request_by_contact,
    remove_expired_requests,
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "123456")


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


def mask_contact(contact):
    if len(contact) <= 4:
        return "*" * len(contact)
    if len(contact) <= 7:
        return contact[:2] + "*" * (len(contact) - 4) + contact[-2:]
    return contact[:3] + "*" * (len(contact) - 5) + contact[-2:]


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return view_func(*args, **kwargs)

    return wrapper


@app.route("/", methods=["GET", "POST"])
def index():
    remove_expired_requests()

    if request.method == "POST":
        contact = request.form.get("contact", "").strip()
        date_str = request.form.get("date", "").strip()
        time_str = request.form.get("time", "").strip()
        destination = request.form.get("destination", "").strip()
        group_size = request.form.get("group_size", "").strip()

        try:
            current_request = create_request(
                contact, date_str, time_str, destination, group_size
            )
        except ValueError as e:
            return render_template(
                "message.html",
                title="提交失败",
                message=str(e),
                success=False,
            )

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

        return render_template(
            "status_result.html",
            user_group=user_group,
            waiting_person=waiting_person,
            contact=contact,
        )

    return render_template("manage.html")


@app.route("/cancel_confirm", methods=["POST"])
def cancel_confirm():
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


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password", "").strip()

        if password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
        else:
            return render_template("admin_login.html", error="密码错误。")

    return render_template("admin_login.html", error="")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))


@app.route("/admin")
@login_required
def admin():
    remove_expired_requests()
    requests_list = load_requests()

    masked_requests = []
    for person in requests_list:
        masked_person = person.copy()
        masked_person["contact"] = mask_contact(person["contact"])
        masked_requests.append(masked_person)

    return render_template("admin.html", requests_list=masked_requests)


@app.route("/clear_data_once")
def clear_data_once():
    save_requests([])
    return "data cleared"


if __name__ == "__main__":
    app.run(debug=True)
