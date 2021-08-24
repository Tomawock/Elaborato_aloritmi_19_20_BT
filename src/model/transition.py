from model.link import Link


class Transition:
    def __init__(self, unique_name, fa_name, next_state, input_link,
                 output_link, label):
        self.unique_name = unique_name
        self.fa_name = fa_name
        self.next_state = next_state
        self.input_link = input_link
        self.output_link = output_link
        self.label = label
