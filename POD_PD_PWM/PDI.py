####### This file is aimed at plotting the PD-I PWM's low
####### common mode voltage area and its proportion
import CBB.three_phase_3d as tp3d

class Pd1_cmv(tp3d.ThreePhase3D):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    test_instance = Pd1_cmv()
    test_instance.data_3d_calculate()
    test_instance.data_3d_plot()
