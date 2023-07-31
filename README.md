1. Enter the configuration files
2. There are five sections:
    Form_Factor, NPU_Parameters, PIM_Parameters, DNN_Parameters, Save_Parameters

3. In case of Form_Factor, there are two types; Mobile and PC, Server and Supecomputer.
    1) For Mobile and PC, its throughput has to be converted into number of PEs in systolic array, and we set npu_flag with true.
    2) For Server and Supercomputer, its systolic array dimension can be entered, and we set npu_flag as false.

4. In case of NPU_Parameters, there are several parameters to be entered.
    1) If its npu_flag is true, we have to convert host NPU's throughput into number of PEs. We can get throughput of any systolic array with this formula; 2 (OPS) * Number of PEs * Clock Frequency. Thus, we can get the number of PEs inversely with this formula.
    2) If its npu_flag is false, we can use its entered parameters.

5. In case of PIM_Parameters, thre are several parameters to be entered.
    1) 
    