from flask import Flask, request, jsonify
import random
import re
import time
import requests

app = Flask(__name__)

type_cc = {'3': 'amex', '4': 'visa', '5': 'master', '6': 'discover'}
all_num = {'amex': 15, 'visa': 16, 'master': 16, 'discover': 16}
cvvs = {'amex': 4, 'visa': 3, 'master': 3, 'discover': 3}
ano_no = ["2024", "2025", "2026", "2027", "2028", "2029", "2030"]
mes_no = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

def gen(bin_part: str, mm: str = None, yy: str = None, cvv: str = None):
    first_digit = bin_part[0]
    if first_digit not in type_cc:
        raise ValueError("Invalid card type")

    cvv_length = cvvs[type_cc[first_digit]]
    card_length = all_num[type_cc[first_digit]]

    bin_part = bin_part.replace('x', '')
    bin_part_len = len(bin_part)
    remaining_length = card_length - bin_part_len - 1

    card_no = [int(i) for i in bin_part]
    card_num = [int(i) for i in bin_part]

    if remaining_length > 0:
        remaining_random = [random.randint(0, 9) for _ in range(remaining_length)]
        for i in remaining_random:
            card_no.append(i)
            card_num.append(i)

    for t in range(0, card_length - 1, 2):
        card_no[t] = card_no[t] * 2
        if card_no[t] > 9:
            card_no[t] -= 9

    s = sum(card_no)
    mod = s % 10
    check_sum = 0 if mod == 0 else (10 - mod)
    card_num.append(check_sum)
    card_num = [str(i) for i in card_num]
    cc = "".join(card_num)

    if mm is None or mm.lower() == 'rnd':
        mm = f'{random.randint(1, 12):02d}'

    if yy is None or yy.lower() == 'rnd':
        yy = random.choice(ano_no)
    elif yy not in ano_no:
        raise ValueError("Invalid year")

    if cvv is None or cvv.lower() == 'rnd':
        cvv = ''.join([str(random.randint(0, 9)) for _ in range(cvv_length)])
    else:
        cvv = f'{int(cvv):0{cvv_length}d}'

    return f'{cc}|{mm}|{yy}|{cvv}'

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    bin_part = data.get('bin')
    mm = data.get('mm', 'rnd')
    yy = data.get('yy', 'rnd')
    cvv = data.get('cvv', 'rnd')

    try:
        result = [gen(bin_part, mm, yy, cvv) for _ in range(10)]
        return jsonify({"cards": result}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/bininfo/<bin>', methods=['GET'])
def bin_info(bin):
    response = requests.get(f'https://anthony086.alwaysdata.net/index.php?bin={bin}')
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Invalid BIN"}), 400

if __name__ == "__main__":
    app.run(host='https://cc-gen-api.onrender.com/', port=5000)
