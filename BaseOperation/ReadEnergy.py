import configparser as cp
import numpy as np

class ReadEnergy:
    def read_energy(self, path):
        config = cp.ConfigParser()
        config.read(path)
        
        sections = {
            'NPU_SRAM': ['NPU_SRAM_input_read', 'NPU_SRAM_filter_read', 'NPU_SRAM_output_write'],
            'PIM_SRAM': ['PIM_SRAM_input_read', 'PIM_SRAM_filter_read', 'PIM_SRAM_output_write'],
            'DRAM': ['DRAM_input_read', 'DRAM_filter_read', 'DRAM_output_write'],
            'PIM_DRAM': ['PIM_input_read', 'PIM_filter_read', 'PIM_output_write'],
            'MAC': ['MAC_random', 'MAC_reuse', 'MAC_constant', 'MAC_idle']
        }

        energy_data = {}
        for section, keys in sections.items():
            energy_data[section] = {key: config.get(section, key) for key in keys}

        result = []
        for components in energy_data.values():
            temp = []
            for parameters in components:
                temp.append(components[parameters])
            result.append(temp)
        return  result
