from controllers.transactions_controller import transactions_contoller
from flask import Blueprint, request

transaction_blueprint = Blueprint("transaction", __name__)
transactions_contollerObj = transactions_contoller()

@transaction_blueprint.route("/insert", methods=["POST"])
def insert():
    return transactions_contollerObj.insert_transaction(request)