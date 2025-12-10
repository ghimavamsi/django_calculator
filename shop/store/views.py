from django.shortcuts import render
import operator

def home(request):
    products = [
        {"name": "Note bok", "price": 199, "image": "no_image.png"},
        {"name": "Pen", "price": 99, "image": "no_image.png"},
        {"name": "tag", "price": 399, "image": "no_image.png"},
    ]
    return render(request,"store/home.html",{"products": products})




# Allowed operations
ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": lambda a, b: "Zero Division Error" if b == 0 else a // b
}


def evaluate_expression(expr):

    try:
        if not expr:
            return "Invalid Expression"

        tokens = []
        num = ""

        # TOKENIZATION
        for char in expr:
            if char.isdigit():
                num += char
            elif char in "+-*/":
                if num == "":
                    return "Invalid Syntax"
                tokens.append(int(num))
                tokens.append(char)
                num = ""
            else:
                return "Invalid Character"
        
        if num == "":
            return "Invalid Ending"
        tokens.append(int(num))

        # MULTIPLICATION AND DIVISION FIRST
        i = 0
        while i < len(tokens):
            if tokens[i] in ("*", "/"):
                op = tokens[i]
                a = tokens[i-1]
                b = tokens[i+1]

                result = ops[op](a, b)
                if isinstance(result, str):   # error string
                    return result

                tokens[i-1:i+2] = [result]
            else:
                i += 1

        # ADDITION AND SUBTRACTION
        result = tokens[0]
        i = 1

        while i < len(tokens):
            op = tokens[i]
            b = tokens[i + 1]
            result = ops[op](result, b)
            i += 2

        return result

    except Exception as e:
        return f"Error: {str(e)}"
    
def calculator_view(request):
    expression = request.GET.get("expression", "")
    action = request.GET.get("action", "")

    # CLEAR
    if action == "AC":
        return render(request, "store/calculator.html", {"expression": ""})

    # Append numbers and operators
    if action.isdigit() or action in ["+", "-", "*", "/"]:
        expression += action

    # Evaluate expression
    elif action == "=":
        expression = str(evaluate_expression(expression))

    return render(request, "store/calculator.html", {"expression": expression})

