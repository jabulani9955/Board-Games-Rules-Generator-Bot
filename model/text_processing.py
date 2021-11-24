def processing(input_string: str) -> str:
    """ Функция для чистки сгенерированного текста. """
    # Удаление всевозможных пробелов
    output_string = ' '.join([i.strip() for i in input_string.split()])
    # Удаление символов кавычек, встречающихся после введённого слова.
    output_string = output_string.replace('»', '', 1).replace('"', '', 1).replace(')', '', 1)
    output_string = output_string.replace(']', '', 1).replace('}', '', 1).replace('>', '', 1)
    # Обрезка текста до знака окончания предложения.
    while not (output_string.endswith('.') or output_string.endswith('!') or output_string.endswith('?')):
        output_string = output_string[:-1]
    return output_string
