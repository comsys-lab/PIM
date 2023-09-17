"Python 3.11.5"

class Scaleupruntime:
    """Get runtime."""
    #Input: scaleupformat / Return: int | int | int
    def get_operand_dimensions(self, scaleupformat):
        """Get dimension on matrix."""
        dataflow = scaleupformat.dataflow
        if scaleupformat.dataflow == "IS":
            SR = scaleupformat.input_operand.row
            SC = scaleupformat.filter_operand.col
            T = scaleupformat.input_operand.col
        else:
            SR = scaleupformat.filter_operand.row
            SC = scaleupformat.input_operand.col
            T = scaleupformat.filter_operand.col

        return SR, SC, T

    #Input: scaleupformat / Return: int
    def get_runtime(self, scaleupformat):
        """Return OS dataflow runtime."""
        SR, SC, T = self.get_operand_dimensions(scaleupformat)

        row_q = SR // scaleupformat.systolic.row
        col_q = SC // scaleupformat.systolic.col

        row_rest = (SR % scaleupformat.systolic.row)
        col_rest = (SC % scaleupformat.systolic.col)

        row_flag = (SR % scaleupformat.systolic.row) != 0
        col_flag = (SC % scaleupformat.systolic.col) != 0

        #CASE1
        runtime1 = (T + scaleupformat.systolic.row + (scaleupformat.systolic.row + scaleupformat.systolic.col - 2)) * row_q * col_q
        #CASE2
        runtime2 = (T + scaleupformat.systolic.row + (row_rest + scaleupformat.systolic.col - 2)) * row_flag * col_q
        #CASE3
        runtime3 = (T + scaleupformat.systolic.row + (scaleupformat.systolic.row + col_rest - 2)) * row_q * col_flag
        #CASE4
        runtime4 = (T + scaleupformat.systolic.row + (row_rest + col_rest - 2)) * row_flag * col_flag

        runtime = runtime1 + runtime2 + runtime3 + runtime4

        return runtime
