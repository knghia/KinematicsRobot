
import numpy as np

class InvalidValue(Exception):
    def _init_(self):
        Exception._init_(self, "Not real solution")

class DeltaRobotB:
    def __init__(self, sb=0.432, SB=0.246, sp=0.127, l=0.264, h=0.6):
        self._sb = sb
        self._SB = SB
        self._sp = sp
        self._l = l
        self._h = h
        
        self.postion = []

        self._WB = np.sqrt(3) * self._SB / 6
        self._UB = np.sqrt(3) * self._SB / 3

        self._wb = np.sqrt(3) * self._sb / 6
        self._ub = np.sqrt(3) * self._sb / 3

        self._wp = np.sqrt(3) * self._sp / 6
        self._up = np.sqrt(3) * self._sp / 3

        self._a = self._SB/2 - self._sp/2
        self._b = self._WB/2 - self._wp / 2
        self._c = self._up - self._UB / 2

    def get_B_P(self):
        B_P_1 = [-self._SB/2, -self._WB, 0]
        B_P_2 = [self._SB/2, -self._WB, 0]
        B_P_3 = [0, self._UB, 0]
        return np.array([B_P_1, B_P_2, B_P_3]).T

    def get_P_P(self):
        P_P_1 = [-self._sp/2, -self._wp, 0]
        P_P_2 = [self._sp/2, -self._wp, 0]
        P_P_3 = [0, self._up, 0]
        return np.array([P_P_1, P_P_2, P_P_3]).T

    def get_b_B(self):
        b_B_1 = [-self._sb/2, -self._wb, 0]
        b_B_2 = [self._sb/2, -self._wb, 0]
        b_B_3 = [0, self._ub, 0]
        return np.array([b_B_1, b_B_2, b_B_3]).T

    def get_h_B(self):
        h_B_1 = [-self._SB/2, -self._WB, -self._h]
        h_B_2 = [self._SB/2, -self._WB, -self._h]
        h_B_3 = [0, self._UB, -self._h]
        return np.array([h_B_1, h_B_2, h_B_3]).T

    @staticmethod
    def square_resolution(a, b, c):
        deltal = b ** 2 - 4 * a * c
        if deltal < 0:
            raise InvalidValue()
        x1 = (-b - np.sqrt(deltal)) / (2 * a)
        x2 = (-b + np.sqrt(deltal)) / (2 * a)
        return x1, x2

    def position_2_L(self, position):
        x, y, z = position[0], position[1], position[2]
        dis = x ** 2 + y ** 2 + z ** 2

        A1 = 1
        B1 = 2*z
        C1 = -self._l**2 + dis + self._a** 2 + self._b**2 + 2*self._a*x + 2*self._b*y

        A2 = 1
        B2 = 2*z
        C2 = -self._l**2 + dis + self._a** 2 + self._b**2 - 2*self._a*x + 2*self._b*y

        A3 = 1
        B3 = 2*z
        C3 = -self._l**2 + dis + self._c** 2 + 2*self._c*y

        L1_1, L1_2 = self.square_resolution(A1, B1, C1)
        L2_1, L2_2 = self.square_resolution(A2, B2, C2)
        L3_1, L3_2 = self.square_resolution(A3, B3, C3)
        return np.round(np.array([L1_1, L2_1, L3_1]).T,3)

    def get_A_B(self, position):
        L = self.position_2_L(position)
        print(L)
        self.postion = L

        B_A_1 = [-self._SB/2, -self._WB, -L[0]]
        B_A_2 = [self._SB/2, -self._WB, -L[1]]
        B_A_3 = [0, self._UB, -L[2]]

        return np.array([B_A_1, B_A_2, B_A_3]).T

    # def get_position(self, angle):
    #     phi_1, phi_2, phi_3 = angle[0], angle[1], angle[2]
    #     Av1 = [0, -self._wb - self._L *
    #            np.cos(phi_1) + self._up, -self._L * np.sin(phi_1)]
    #     Av2 = [np.sqrt(3) * (self._wb + self._L * np.cos(phi_2)) / 2 - self._sp / 2,
    #            (self._wb + self._L * np.cos(phi_2)) / 2 - self._wp,
    #            -self._L * np.sin(phi_2)]
    #     Av3 = [-np.sqrt(3) * (self._wb + self._L * np.cos(phi_3)) / 2 + self._sp / 2,
    #            (self._wb + self._L * np.cos(phi_3)) / 2 - self._wp,
    #            -self._L * np.sin(phi_3)]

    #     x1, y1, z1 = Av1[0], Av1[1], Av1[2]
    #     x2, y2, z2 = Av2[0], Av2[1], Av2[2]
    #     x3, y3, z3 = Av3[0], Av3[1], Av3[2]

    #     w1 = self._l ** 2 - (x1 ** 2 + y1 ** 2 + z1 ** 2)
    #     w2 = self._l ** 2 - (x2 ** 2 + y2 ** 2 + z2 ** 2)
    #     w3 = self._l ** 2 - (x3 ** 2 + y3 ** 2 + z3 ** 2)

    #     d = 4 * (x1 - x2) * (y2 - y3) - 4 * (x2 - x3) * (y1 - y2)

    #     a1 = -4 * ((z1 - z2) * (y2 - y3) - (y1 - y2) * (z2 - z3)) / d
    #     b1 = (-2 * (y2 - y3) * (w1 - w2) + 2 * (y1 - y2) * (w2 - w3)) / d

    #     a2 = -4 * ((x1 - x2) * (z2 - z3) - (z1 - z2) * (x2 - x3)) / d
    #     b2 = (-2 * (x1 - x2) * (w2 - w3) + 2 * (x2 - x3) * (w1 - w2)) / d

    #     i = a1 ** 2 + a2 ** 2 + 1
    #     j = 2 * a1 * b1 + 2 * a2 * b2 - 2 * a1 * x3 - 2 * a2 * y3 - 2 * z3
    #     k = b1 ** 2 + b2 ** 2 - 2 * b1 * x3 - 2 * b2 * y3 - w3
    #     z, h = self.square_resolution(i, j, k)
    #     x = a1 * z + b1
    #     y = a2 * z + b2
    #     return np.round(np.array([x, y, z]).T,3)

    # def get_vector_B_L(self):
    #     phi_1, phi_2, phi_3 = self._angle
    #     L_1 = [0, -self._L * np.cos(phi_1), -self._L * np.sin(phi_1)]
    #     L_2 = [np.sqrt(3) * self._L * np.cos(phi_2) / 2, self._L *
    #            np.cos(phi_2) / 2, -self._L * np.sin(phi_2)]
    #     L_3 = [-np.sqrt(3) * self._L * np.cos(phi_3) / 2, self._L *
    #            np.cos(phi_3) / 2, -self._L * np.sin(phi_3)]
    #     return np.array([L_1, L_2, L_3]).T

    # def get_vector_B_A(self):
    #     phi_1, phi_2, phi_3 = self._angle
    #     A_1 = [0, -self._wb - self._L * np.cos(phi_1), -self._L * np.sin(phi_1)]
    #     A_2 = [np.sqrt(3) * (self._wb + self._L * np.cos(phi_2)) / 2,
    #            (self._wb + self._L * np.cos(phi_2)) / 2, -self._L * np.sin(phi_2)]
    #     A_3 = [-np.sqrt(3) * (self._wb + self._L * np.cos(phi_3)) / 2,
    #            (self._wb + self._L * np.cos(phi_3)) / 2, -self._L * np.sin(phi_3)]
    #     return np.array([A_1, A_2, A_3]).T