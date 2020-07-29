# coding=utf-8
def create_header(xml_document, arc_doc_info):
    """ Creates the Header in the DOM

    :param xml_document: The DOM / Document for writing the QGIS-File
    :return: the header element in the DOM
    """
    header_element = xml_document.createElement("qgis")
    header_element.setAttribute("projectname", arc_doc_info.DocumentTitle)
    header_element.setAttribute("version", unicode("3.10.0-A Coruña", 'UTF-8'))
    xml_document.appendChild(header_element)

    home_path_element = xml_document.createElement("homePath")
    home_path_element.setAttribute("path", "")
    header_element.appendChild(home_path_element)

    title_element = xml_document.createElement("title")
    title_content = xml_document.createTextNode(arc_doc_info.DocumentTitle)
    title_element.appendChild(title_content)
    header_element.appendChild(title_element)

    autotransaction_element = xml_document.createElement("autotransaction")
    autotransaction_element.setAttribute("active", "0")
    header_element.appendChild(autotransaction_element)

    evaluate_default_values_element = xml_document.createElement("evaluateDefaultValues")
    evaluate_default_values_element.setAttribute("active", "0")
    header_element.appendChild(evaluate_default_values_element)

    return header_element
