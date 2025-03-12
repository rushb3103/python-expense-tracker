from models.transactions import transactions
from libraries.functions import functions

class transactions_contoller():

    def insert_transaction(self, request, user_id = 0):

        print(user_id)
        # user_id = request.form.get("user_id", 0 , int)
        transaction_type = request.form.get("transaction_type", "", str)
        transaction_sub_type = request.form.get("transaction_sub_type", "", str)
        amount = request.form.get("amount", 0, float)
        transaction_date = request.form.get("transaction_date", "", str)
        note = request.form.get("note", "", str)

        functionsObj = functions()
        validation_results = {}

        is_valid, message = functionsObj.validate_transaction_type(transaction_type)
        validation_results["transaction_type"] = message if not is_valid else "valid"
        is_valid, message = functionsObj.validate_sub_transaction_type(transaction_sub_type)
        validation_results["sub_transaction_type"] = message if not is_valid else "valid"
        is_valid, message = functionsObj.validate_amount(amount)
        validation_results["amount"] = message if not is_valid else "valid"
        is_valid, message = functionsObj.validate_dob(transaction_date)
        validation_results["transaction_date"] = message if not is_valid else "valid"

        for _, result in validation_results.items():
            if result != "valid":
                return functionsObj.send_response(0, result)
            
        current_time = functionsObj.get_current_datetime()

        req_ip = request.remote_addr
        transactionsObj = transactions()
        insert_dict = {
            "user_id" : user_id,
            "transaction_type" : transaction_type,
            "transaction_sub_type" : transaction_sub_type,
            "amount" : amount,
            "note" : note,
            "created_date" : current_time,
            "updated_date" : current_time,
            "transaction_date" : transaction_date,
            "created_ip" : req_ip,
            "updated_ip" : req_ip
        }
        transactionsObj.insert_dict(insert_dict)
        return functionsObj.send_response(
            1, "Transaction Inserted Successfully."
        )