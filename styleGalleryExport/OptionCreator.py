class OptionCreator:
    def __init__(self, xml_document):
        self.xml_document = xml_document

    def create_option(self, parent_element, attributes):
        option_element = self.xml_document.createElement("Option")
        for key, value in attributes.iteritems():
            option_element.setAttribute(key, value)
        parent_element.appendChild(option_element)

        return option_element
