from time import sleep


class MLX90614():

    # RAM offsets with 16-bit data, MSB first
    # Raw data IR channel 1
    MLX90614_RAWIR1 = 0x04
    # Raw data IR channel 2
    MLX90614_RAWIR2 = 0x05
    # Ambient temperature
    MLX90614_TA = 0x06
    # Object 1 temperature
    MLX90614_TOBJ1 = 0x07
    # Object 2 temperature
    MLX90614_TOBJ2 = 0x08

    # EEPROM offsets with 16-bit data, MSB first
    # Object temperature max register
    MLX90614_TOMAX = 0x20
    # Object temperature min register
    MLX90614_TOMIN = 0x21
    # PWM configuration register
    MLX90614_PWMCTRL = 0x22
    # Ambient temperature register
    MLX90614_TARANGE = 0x23
    # Emissivity correction register
    MLX90614_EMISS = 0x24
    # Configuration register
    MLX90614_CONFIG = 0x25
    # Slave address register
    MLX90614_ADDR = 0x2E
    # 1 ID register (read-only)
    MLX90614_ID1 = 0x3C
    # 2 ID register (read-only)
    MLX90614_ID2 = 0x3D
    # 3 ID register (read-only)
    MLX90614_ID3 = 0x3E
    # 4 ID register (read-only)
    MLX90614_ID4 = 0x3F

    comm_retries = 5
    comm_sleep_amount = 0.1

    def __init__(self, bus, address=0x5A):
        self.bus = bus
        self.address = address

    def read_reg(self, reg_addr):
        err = None
        for i in range(self.comm_retries):
            try:
                return self.bus.read_word_data(self.address, reg_addr)
            except IOError as e:
                err = e
                # "Rate limiting" - sleeping to prevent problems with sensor
                # when requesting data too quickly
                sleep(self.comm_sleep_amount)
        # By this time, we made a couple requests and the sensor didn't respond
        # (judging by the fact we haven't returned from this function yet)
        # So let's just re-raise the last IOError we got
        raise err

    def read_temp(self, reg):
        data = self.read_reg(reg)
        temp = (data * 0.02) - 273.15
        return temp

    def get_ambient(self):
        return self.read_temp(self.MLX90614_TA)

    def get_object_1(self):
        return self.read_temp(self.MLX90614_TOBJ1)

    def get_object_2(self):
        return self.read_temp(self.MLX90614_TOBJ2)
