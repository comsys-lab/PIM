class Efficiency:
    def get_efficiency(self, processor, input_operand, filter_operand, dataflow):
        mapping_eff = self.get_mapping_eff(processor, input_operand, filter_operand, dataflow)
        computation_eff = self.get_computation_eff(processor, input_operand, filter_operand, dataflow)
        return mapping_eff, computation_eff

    def get_mapping_eff(self, processor, input_operand, filter_operand, dataflow):
        if dataflow == "IS":
            row = len(filter_operand)
            col = len(input_operand[0])
        else:
            row = len(input_operand)
            col = len(filter_operand[0])

        r_iter, r_rest = divmod(row, processor[0])
        c_iter, c_rest = divmod(col, processor[1])
        r_total = r_iter + (r_rest != 0)
        c_total = c_iter + (c_rest != 0)
        mapping_eff = (1 * r_iter * c_iter + r_rest / processor[0] * c_iter + c_rest / processor[1] * r_iter + r_rest / processor[0] * c_rest / processor[1]) / (r_total * c_total)
        return mapping_eff

    def get_computation_eff(self, processor, input_operand, filter_operand, dataflow):
        if dataflow == "IS":
            row = len(filter_operand)
            col = len(input_operand[0])
            T = len(filter_operand[0])
        else:
            row = len(input_operand)
            col = len(filter_operand[0])
            T = len(input_operand[0])

        constant = (2 * processor[0] + processor[1] + T - 2)
        r_iter, r_rest = divmod(row, processor[0])
        c_iter, c_rest = divmod(col, processor[1])
        r_total = r_iter + (r_rest != 0)
        c_total = c_iter + (c_rest != 0)
        computation_eff = (1 * r_iter * c_iter + r_rest / processor[0] * c_iter + c_rest / processor[1] * r_iter \
                           + r_rest / processor[0] * c_rest / processor[1]) * T / constant / (r_total * c_total)
        return computation_eff
