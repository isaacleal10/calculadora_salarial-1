from django import forms
from django.shortcuts import render
import json

# Create your views here.


def index(request):
    return render(request, 'index.html')


def submitquery(request):
    query = form(request.GET)
    if query.is_valid():
        salary = query.data['query']
        try:
            return render(request, 'index.html', context=CalculatorSalary(salary))
        except:
            return render(request, 'index.html', context={"error": True})
    else:
        return render(request, 'index.html', None)


class form(forms.Form):
    query = forms.FloatField(label='Salary')


def CalculatorSalary(salary):
    def calc(cant, total):
        return round(cant*100/total)

    def format(mount): return "{:,}".format(mount)
    def percentage(num, p): return float(num) / 100 * float(p)

    def solidFundCalc(salary, countSalary):
        solidFun = 0
        if countSalary >= 4 and countSalary < 16:
            solidFun = percentage(salary, 1)
        elif countSalary >= 16 and countSalary < 17:
            solidFun = percentage(salary, 1, 2)
        elif countSalary >= 17 and countSalary < 18:
            solidFun = percentage(salary, 1, 4)
        elif countSalary >= 18 and countSalary < 19:
            solidFun = percentage(salary, 1, 6)
        elif countSalary >= 19 and countSalary < 20:
            solidFun = percentage(salary, 1, 8)
        elif countSalary >= 20:
            solidFun = percentage(salary, 2)
        return solidFun

    fSalary = float(salary)
    MINSALARY = 1000000
    TRANSASS = 117.172

    healthPension = percentage(fSalary, 4)

    solidFundCount = fSalary / MINSALARY
    if solidFundCount > 2:
        TRANSASS = 0

    solidFund = solidFundCalc(fSalary, solidFundCount)
    netoSalary = fSalary - healthPension * 2
    netoSalary -= solidFund

    Tdesc = healthPension + solidFund

    data = {
        "labels": ["Pago Neto", "Descuentos"],
        "data": [calc(netoSalary, fSalary), calc(Tdesc, fSalary)]
    }

    return {
        "salary": format(fSalary),
        "transp": format(TRANSASS),
        "healthPension": format(healthPension),
        "netoSalary": format(netoSalary),
        "solidFund": format(solidFund),
        "data": json.dumps(graphicPie(data))
    }


def graphicPie(data):
    return {
        'chart': {
            'type': 'pie',
            'data': {
                'labels': data['labels'],
                'datasets': [{
                    'label': '',
                    'data': data['data'],
                    'backgroundColor': [
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                    ],
                    'borderColor': [
                        'rgb(54, 162, 235)',
                        'rgb(153, 102, 255)',
                    ],
                    'borderWidth': 1
                }],
                'hoverOffset': 4
            },
            'options': {
                'responsive': True,
            }
        }
    }
