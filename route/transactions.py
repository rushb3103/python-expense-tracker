from controllers.transactions_controller import transactions_contoller
from flask import Blueprint, request, render_template
from libraries.functions import functions


transaction_blueprint = Blueprint("transaction", __name__)
transactions_contollerObj = transactions_contoller()
functionsObj = functions()

@transaction_blueprint.before_request
@functionsObj.token_required


@transaction_blueprint.route("/insert", methods=["POST","GET"])
def insert(user_id=0):
    if request.method == "POST":
        return transactions_contollerObj.insert_transaction(request, user_id)
    else:
        return render_template("/transactions/add-transaction.html")

@transaction_blueprint.route("/get-transaction", methods=["GET"])
def get_transaction(user_id=0):
    transactions = transactions_contollerObj.get_transaction(user_id)
    print(transactions)
    context = {
        "transactions" : transactions
    }
    return render_template("/transactions/get-transaction.html", context=context)