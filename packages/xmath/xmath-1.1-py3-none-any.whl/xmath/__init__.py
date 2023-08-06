####    math   ####
import math  # for sys_xmath
###################

class sys_xmath():

    ###############   BIT   ################

        def x_NOT(value):
            return ~ value

        def x_OR(value_1,  value_2):
            return value_1 | value_2

        def x_XOR(value_1, value_2):
            return value_1 ^ value_2

        def x_LS(value_1, value_2):
            return value_1 << value_2

        def x_RS(value_1, value_2):
            return value_1 >> value_2 

        def x_AND(value_1, value_2):
            return value_1 & value_2

    #############   num_sys   ##############

        def x_bin(value):
            return bin(value) [2:]

        def x_oct(value):
            return oct(value) [2:]

        def x_hex(value):
            return hex(value) [2:]

    ##############   basic   ##############

        def x_sum(*value):
            num = 0
            for number in value:
               num = num + number
            return num

        def x_sub(value_1, value_2):
            return value_1 - value_2
            

        def x_mul(value_1, value_2):
            return value_1 * value_2

        def x_div(value_1, value_2):
            return value_1 /  value_2

        def x_rem(value_1, value_2):
            return value_1 % value_2

    ##############  ADV  ###############
        def x_sq(value):
            return value * value
        
        def x_sqrt(value):
            return math.sqrt(value)

        def x_isqrt(value):
            return math.isqrt(value)

        def xceil(value):
            return math.ceil(value)

        def x_floor(value):
            return math.floor(value)

        def x_factorial(value):
            return math.factorial(value)

        def x_gcd(value_1,  value_2):
            return math.gcd(value_1, value_2)

        def x_exp(value):
            return math.exp(value)

        def x_fmod(value_1, value_2):
            return math.fmod(value_1, value_2)

        def x_copysign(value_1, value_2):
            return math.copysign(value_1, value_2)

        def x_fabs(value):
            return  math.fabs(value)

        def x_pow(value_1, value_2):
            return math.pow(value_1, value_2)

        def x_fsum(value, *value_1):
            return math.fsum(value)

        def x_prod(value):
            return math.prod(value)

        def x_isnan(value):
            return math.isnan(value)

        def x_isfinite(value):
            return math.isfinite(value)

        def x_isclose(value_1, value_2):
            return math.isclose(value_1, value_2)

    ##################################

