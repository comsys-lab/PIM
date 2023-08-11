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
    1) Systolic array dimension: Row, Column
    2) Number of systolic array pods per DRAM chips
    3) Chips per DIMM
    4) On-PIM buffer: Input, Filter
    5) Internal Bandwidth

6. In case of DNN_Parameters, topology path, batch size, dataflow must be entered.
    1) Path of topology
    2) Batch size (Must be integer)
    3) NPU dataflow (Must be among OS, WS, IS)
    4) PIM dataflow (Must be among OS, WS, IS)

7. In case of Save_Parameters, Using PIM flag, storing path must be entered.
    1) PIM flag
        i. If flag is False, it means you will use only host NPU.
        ii. If flag is True, it means you will use PIM with host NPU.
    2) Storing path
        Simulation result will be stored in this storing path.

8. Simulation configuration
    You can choose dataflow among Output Stationary (OS), Weight Stationary (WS), Input Stationary (IS).
    