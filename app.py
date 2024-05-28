from flask import Flask, jsonify
import random

app = Flask(__name__)

class Tool:
    TYPE_CC = {'3': 'amex', '4': 'visa', '5': 'master', '6': 'discover'}
    ALL_NUM = {'amex': 15, 'visa': 16, 'master': 16, 'discover': 16}
    CVVS = {'amex': 4, 'visa': 3, 'master': 3, 'discover': 3}
    ANO_NO = ["2024", "2025", "2026", "2027", "2028", "2029", "2030"]
    MES_NO = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

    def __init__(self, bin_part, mm=None, yy=None, cvv=None):
        self.bin_part = bin_part.replace('x', '')
        self.first_digit = bin_part[0]
        if self.first_digit not in self.TYPE_CC:
            raise ValueError("Invalid card type")
        
        self.card_type = self.TYPE_CC[self.first_digit]
        self.card_length = self.ALL_NUM[self.card_type]
        self.cvv_length = self.CVVS[self.card_type]
        
        self.mm = self.random_month() if mm is None or mm.lower() == 'rnd' else self.validate_month(mm)
        self.yy = self.random_year() if yy is None or yy.lower() == 'rnd' else self.validate_year(yy)
        self.cvv = self.random_cvv() if cvv is None or cvv.lower() == 'rnd' else self.validate_cvv(cvv)

    def random_month(self):
        return f'{random.randint(1, 12):02d}'

    def random_year(self):
        return random.choice(self.ANO_NO)

    def random_cvv(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(self.cvv_length)])

    def validate_month(self, mm):
        if not (1 <= int(mm) <= 12):
            raise ValueError("Invalid month")
        return f'{int(mm):02d}'

    def validate_year(self, yy):
        if yy not in self.ANO_NO:
            raise ValueError("Invalid year")
        return yy

    def validate_cvv(self, cvv):
        if not cvv.isdigit() or len(cvv) != self.cvv_length:
            raise ValueError("Invalid CVV")
        return f'{int(cvv):0{self.cvv_length}d}'

    def generate_card_number(self):
        bin_part_len = len(self.bin_part)
        lengthGen = self.card_length - bin_part_len - 1

        card_no = [int(i) for i in self.bin_part]
        card_num = card_no.copy()

        if lengthGen > 0:
            randomGen = [random.randint(0, 9) for _ in range(lengthGen)]
            card_no.extend(randomGen)
            card_num.extend(randomGen)

        for t in range(0, self.card_length - 1, 2):
            card_no[t] = card_no[t] * 2
            if card_no[t] > 9:
                card_no[t] -= 9

        s = sum(card_no)
        mod = s % 10
        check_sum = 0 if mod == 0 else (10 - mod)
        card_num.append(check_sum)

        return ''.join(map(str, card_num))

    def generate(self):
        cc_number = self.generate_card_number()
        return f'{cc_number}|{self.mm}|{self.yy}|{self.cvv}'

    @classmethod
    def Generator(cls, data):
        user_input = data.strip()
        parts = user_input.split('|')
        bin_part = parts[0]
        mm = parts[1] if len(parts) > 1 else 'rnd'
        yy = parts[2] if len(parts) > 2 else 'rnd'
        cvv = parts[3] if len(parts) > 3 else 'rnd'

        try:
            ccs = [cls(bin_part, mm, yy, cvv).generate() for _ in range(10)]
            response = "\n".join(ccs)
            return f"\nInput: {bin_part}|{mm}|{yy}|{cvv}\n" + response
        except ValueError as e:
            return str(e)

@app.route('/')
def index():
    info = {
        "Autor": "@gxbyzzz",
        "Creacion": "Mayo del 2024",
        "Descripcion": "API gratuita y de acceso público diseñada para generar números de tarjetas de crédito para pruebas. Esta herramienta está destinada a facilitar el desarrollo y pruebas de software, análisis de datos, y aplicaciones educativas. El servicio es completamente gratuito y cualquier cobro asociado a su uso no está autorizado, pudiendo constituir una actividad fraudulenta.",
        "Proyecto": "Onyx APIs 2024",
        "About API": [
            {
                "Instrucciones": "Utilice las rutas especificadas para generar números de tarjetas de crédito.",
                "Nota": "API sin fines de lucro."
            }
        ]
    }
    return jsonify(info)

@app.route('/generate/<params>', methods=['GET'])
def generate_get(params):
    try:
        response = Tool.Generator(params)
        return jsonify({"result": response}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Invalid input format"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
