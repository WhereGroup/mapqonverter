# coding=utf-8
def create_header(dom):
    """ Creates the Header in the DOM

    :param dom: The DOM / Document for writing the QGIS-File
    :return: the header element in the DOM
    """
    header_element = dom.createElement("qgis")
    header_element.setAttribute("projectname", "")
    header_element.setAttribute("version", unicode("3.10.0-A Coruña", 'UTF-8'))
    dom.appendChild(header_element)

    home_path_element = dom.createElement("homePath")
    home_path_element.setAttribute("path", "")
    header_element.appendChild(home_path_element)

    title_element = dom.createElement("title")
    header_element.appendChild(title_element)

    autotransaction_element = dom.createElement("autotransaction")
    autotransaction_element.setAttribute("active", "0")
    header_element.appendChild(autotransaction_element)

    evaluate_default_values_element = dom.createElement("evaluateDefaultValues")
    evaluate_default_values_element.setAttribute("active", "0")
    header_element.appendChild(evaluate_default_values_element)

    return header_element
