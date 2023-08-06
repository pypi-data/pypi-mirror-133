import json
import ast


def jsonConvert(data):
    return json.loads(json.dumps(data, indent=4, sort_keys=True, default=str))

def replaceDictIf(data, key, replacement):
    """Método para remplazar un valor de un diccionario en caso de que coincida con una llave
    Args:
        data (dict): Diccionario con los datos de entrada
        key (str): Llave del diccionario
        replacement (any): Valor por defecto

    Returns:
        any: Valor del diccionario o el valor por defecto
    """
    assert isinstance(data, dict)
    return str(data.get(key)).replace(" ", "") or replacement


def replaceIf(value, key, replacement):
    """Método para remplazar un valor en caso de que coincida con una llave

    Args:
        value (any): Valor a comparar
        key (any): Llave a comparar
        replacement (any): Valor por defecto

    Returns:
        any: Valor por defecto o el valor de entrada
    """    
    if value == key:
        return replacement
    return value

def prepareJsonData(data):
    """Prepara datos de  para convertir a JSON con double Quote debido que los atributos vienen con sigle quote

    Args:
        data (dict): data de ingreso

    Returns:
        dict: json procesado
    """
    replaced = json.dumps(str(data).replace("'", '"').replace('"s ', 's '))
    converted = json.loads(jsonConvert(replaced))
    jsondata = (ast.literal_eval(converted))
    return jsondata