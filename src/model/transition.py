from model.link import Link


class Transition:
    def __init__(self, unique_name, fa_name, next_state, input_link,
                 output_link, observable_label, relevant_label):
        self.unique_name = unique_name
        self.fa_name = fa_name
        self.next_state = next_state
        self.input_link = input_link
        self.output_link = output_link
        self.observable_label = observable_label
        self.relevant_label = relevant_label

    def __init__(self, ta):
        self.unique_name = ta["unique_name"]
        self.fa_name = ta["fa_name"]
        self.next_state = ta["next_state"]
        input = ta["input_link"]
        if input != None:
            self.input_link = Link(
                input["name"], input["event"])
        else:
            self.input_link = None

        self.output_link = []
        for out_link in ta["output_link"]:
            self.output_link.append(Link(out_link["name"], out_link["event"]))
        self.observable_label = ta["observable_label"]
        self.relevant_label = ta["relevant_label"]

    def __str__(self):
        string_out = self.unique_name + " " + self.fa_name + \
            " " + self.next_state + " " + str(self.input_link) + " "
        for el in self.output_link:
            string_out += str(el) + " "
        string_out += self.observable_label + " " + self.relevant_label
        return string_out
