# coding=utf-8
def create_header(doc):
    """ Creates the Header in the DOM

    :param doc: The DOM / Document for writing the QGIS-File
    :return: the qgis element in the DOM
    """
    # Create the <qgis> base element
    qgis = doc.createElement("qgis")
    qgis.setAttribute("projectname", "")
    qgis.setAttribute("version", unicode("3.10.0-A Coruña", 'UTF-8'))
    doc.appendChild(qgis)

    # Create the <homepath> element
    home_path = doc.createElement("homePath")

    home_path.setAttribute("path", "")
    qgis.appendChild(home_path)

    # Create the <title> element
    title = doc.createElement("title")
    qgis.appendChild(title)

    # Create the <autostransaction> element
    autotransaction = doc.createElement("autotransaction")
    autotransaction.setAttribute("active", "0")
    qgis.appendChild(autotransaction)

    # Create the <evaluateDefaultValues> element
    evaluate_default_values = doc.createElement("evaluateDefaultValues")
    evaluate_default_values.setAttribute("active", "0")
    qgis.appendChild(evaluate_default_values)

    return qgis
