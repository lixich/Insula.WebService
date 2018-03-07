def average(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def forecast(doses):
    values = [value['Insulin'] for value in doses]
    return round(average(values))
