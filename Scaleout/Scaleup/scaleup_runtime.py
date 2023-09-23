"Python 3.11.5"

class Scaleupruntime:
    """Get runtime."""
    #Input: scaleup / Return: int | int | int
    #scaleup, operand
    def get_operand_dimensions(self, scaleup, operand):
        """Get dimension on matrix."""
        dataflow = scaleup.others.dataflow
        if dataflow == "IS":
            sr = operand.input_operand.shape[0]
            sc = operand.filter_operand.shape[1]
            t = operand.input_operand.shape[1]
        else:
            sr = operand.filter_operand.shape[0]
            sc = operand.input_operand.shape[1]
            t = operand.filter_operand.shape[1]

        return sr, sc, t

    #Input: scaleup / Return: int
    def get_runtime(self, scaleup, operand):
        """Return OS dataflow runtime."""
        sr,sc, t = self.get_operand_dimensions(scaleup, operand)

        row_q = sr // scaleup.systolic.row
        col_q = sc // scaleup.systolic.col

        row_rest = (sr % scaleup.systolic.row)
        col_rest = (sc % scaleup.systolic.col)

        row_flag = (sr % scaleup.systolic.row) != 0
        col_flag = (sc % scaleup.systolic.col) != 0

        #CASE1
        runtime1 = (t + scaleup.systolic.row + (scaleup.systolic.row + scaleup.systolic.col - 2)) * row_q * col_q
        #CASE2
        runtime2 = (t + scaleup.systolic.row + (row_rest + scaleup.systolic.col - 2)) * row_flag * col_q
        #CASE3
        runtime3 = (t + scaleup.systolic.row + (scaleup.systolic.row + col_rest - 2)) * row_q * col_flag
        #CASE4
        runtime4 = (t + scaleup.systolic.row + (row_rest + col_rest - 2)) * row_flag * col_flag

        runtime = runtime1 + runtime2 + runtime3 + runtime4

        return runtime
