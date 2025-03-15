from controllers.transactions_controller import transactions_contoller
from flask import Blueprint, request, render_template
from libraries.functions import functions


transaction_blueprint = Blueprint("transaction", __name__)
transactions_contollerObj = transactions_contoller()
functionsObj = functions()

@transaction_blueprint.route("/insert", methods=["POST","GET"])
@functions.token_required
def insert(user_id=0):
    print(request.method)
    if request.method == "POST":
        print(request.form)
        return transactions_contollerObj.insert_transaction(request, user_id)
    else:
        return render_template("/transactions/add-transaction.html")