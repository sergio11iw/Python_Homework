def convert(ru, doll):
    return f'{ru} RUB = {round(ru/doll, 2)} USD'

def adult(age):
    if age >= 18:
        return True
    return False
