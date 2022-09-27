
import numpy as np

class InvalidValue(Exception):
    def __init__(self):
        Exception.__init__(self, "Not real solution")

class DeltaRobot:
    def __init__(self, sb=0.31, sp=0.065, L=0.118, l=0.33, h=0.04, *args, **kwargs):
        self.__sb = sb
        self.__sp = sp
        self.__L = L
        self.__l = l
        self.load_base_dis()

        self.__angle = np.array([0,0,0]).T
        self.__degree = np.array([0,0,0]).T
        self.__position = self.get_position(np.array([0,0,0]).T)
        self.Degree = np.array([0,0,0]).T

    def load_base_dis(self):
        self.__wb = np.sqrt(3) * self.__sb / 6
        self.__ub = np.sqrt(3) * self.__sb / 3
        self.__wp = np.sqrt(3) * self.__sp / 6
        self.__up = np.sqrt(3) * self.__sp / 3

        self.__a = self.__wb - self.__up
        self.__b = self.__sp / 2 - np.sqrt(3) * self.__wb / 2
        self.__c = self.__wp - self.__wb / 2

    @property
    def Angle(self):
        return np.round(self.__angle,3)

    @Angle.setter
    def Angle(self, angle):
        self.__angle = angle
        self.__position = self.get_position(angle)

    @property
    def Degree(self):
        self.__degree = self.__angle*180/np.pi
        return np.round(self.__degree,3)

    @Degree.setter
    def Degree(self, degree):
        self.__degree = degree
        self.__angle = self.__degree/180 * np.pi
        self.__pass_position = self.__position
        self.__position = self.get_position(self.__angle)

    @property
    def Position(self):
        return np.round(self.__position,3)

    @Position.setter
    def Position(self, position):
        self.__position = position
        self.__angle = self.get_angle(position)

    @property
    def PassPosition(self):
        return np.round(self.__pass_position,3)

    @staticmethod
    def square_resolution(a, b, c):
        deltal = b ** 2 - 4 * a * c
        if deltal < 0:
            raise InvalidValue()
        x1 = (-b - np.sqrt(deltal)) / (2 * a)
        x2 = (-b + np.sqrt(deltal)) / (2 * a)
        return x1, x2

    def get_B_B(self):
        B_B_1 = [0, -self.__wb, 0]
        B_B_2 = [np.sqrt(3) * self.__wb / 2, self.__wb / 2, 0]
        B_B_3 = [-np.sqrt(3) * self.__wb / 2, self.__wb / 2, 0]
        return np.array([B_B_1, B_B_2, B_B_3]).T

    def get_B_b(self):
        B_b_1 = [self.__sb / 2, -self.__wb, 0]
        B_b_2 = [0, self.__ub, 0]
        B_b_3 = [-self.__sb / 2, -self.__wb, 0]
        return np.array([B_b_1, B_b_2, B_b_3]).T

    def get_P_P(self):
        P_P_1 = [0, -self.__up, 0]
        P_P_2 = [self.__sp / 2, self.__wp, 0]
        P_P_3 = [-self.__sp / 2, self.__wp, 0]
        return np.array([P_P_1, P_P_2, P_P_3]).T

    def get_angle(self, position):
        x, y, z = position[0], position[1], position[2]
        dis = x ** 2 + y ** 2 + z ** 2

        E1 = 2 * self.__L * (y + self.__a)
        F1 = 2 * z * self.__L
        G1 = dis + self.__a ** 2 + self.__L ** 2 + 2 * y * self.__a - self.__l ** 2

        E2 = -self.__L * (np.sqrt(3) * (x + self.__b) + y + self.__c)
        F2 = 2 * z * self.__L
        G2 = dis + self.__b ** 2 + self.__c ** 2 + self.__L ** 2 + \
             2 * (x * self.__b + y * self.__c) - self.__l ** 2

        E3 = self.__L * (np.sqrt(3) * (x - self.__b) - y - self.__c)
        F3 = 2 * z * self.__L
        G3 = dis + self.__b ** 2 + self.__c ** 2 + self.__L ** 2 + \
             2 * (-x * self.__b + y * self.__c) - self.__l ** 2

        T1_1, T1_2 = self.square_resolution(G1 - E1, 2 * F1, G1 + E1)
        T2_1, T2_2 = self.square_resolution(G2 - E2, 2 * F2, G2 + E2)
        T3_1, T3_2 = self.square_resolution(G3 - E3, 2 * F3, G3 + E3)

        phi_1_1 = 2 * np.arctan(T1_1)
        phi_2_1 = 2 * np.arctan(T2_1)
        phi_3_1 = 2 * np.arctan(T3_1)

        # phi_1_2 = 2 * np.arctan(T1_2)
        # phi_2_2 = 2 * np.arctan(T2_2)
        # phi_3_2 = 2 * np.arctan(T3_2)

        # return np.round(np.array([phi_1_2, phi_2_2, phi_3_2]).T,3)
        return np.round(np.array([phi_1_1, phi_2_1, phi_3_1]).T,3)

    def get_position(self, angle):
        phi_1, phi_2, phi_3 = angle[0], angle[1], angle[2]
        Av1 = [0, -self.__wb - self.__L *
               np.cos(phi_1) + self.__up, -self.__L * np.sin(phi_1)]
        Av2 = [np.sqrt(3) * (self.__wb + self.__L * np.cos(phi_2)) / 2 - self.__sp / 2,
               (self.__wb + self.__L * np.cos(phi_2)) / 2 - self.__wp,
               -self.__L * np.sin(phi_2)]
        Av3 = [-np.sqrt(3) * (self.__wb + self.__L * np.cos(phi_3)) / 2 + self.__sp / 2,
               (self.__wb + self.__L * np.cos(phi_3)) / 2 - self.__wp,
               -self.__L * np.sin(phi_3)]

        x1, y1, z1 = Av1[0], Av1[1], Av1[2]
        x2, y2, z2 = Av2[0], Av2[1], Av2[2]
        x3, y3, z3 = Av3[0], Av3[1], Av3[2]

        w1 = self.__l ** 2 - (x1 ** 2 + y1 ** 2 + z1 ** 2)
        w2 = self.__l ** 2 - (x2 ** 2 + y2 ** 2 + z2 ** 2)
        w3 = self.__l ** 2 - (x3 ** 2 + y3 ** 2 + z3 ** 2)

        d = 4 * (x1 - x2) * (y2 - y3) - 4 * (x2 - x3) * (y1 - y2)

        a1 = -4 * ((z1 - z2) * (y2 - y3) - (y1 - y2) * (z2 - z3)) / d
        b1 = (-2 * (y2 - y3) * (w1 - w2) + 2 * (y1 - y2) * (w2 - w3)) / d

        a2 = -4 * ((x1 - x2) * (z2 - z3) - (z1 - z2) * (x2 - x3)) / d
        b2 = (-2 * (x1 - x2) * (w2 - w3) + 2 * (x2 - x3) * (w1 - w2)) / d

        i = a1 ** 2 + a2 ** 2 + 1
        j = 2 * a1 * b1 + 2 * a2 * b2 - 2 * a1 * x3 - 2 * a2 * y3 - 2 * z3
        k = b1 ** 2 + b2 ** 2 - 2 * b1 * x3 - 2 * b2 * y3 - w3
        z, h = self.square_resolution(i, j, k)
        x = a1 * z + b1
        y = a2 * z + b2
        return np.round(np.array([x, y, z]).T,3)

    def get_vector_B_L(self):
        phi_1, phi_2, phi_3 = self.__angle
        L_1 = [0, -self.__L * np.cos(phi_1), -self.__L * np.sin(phi_1)]
        L_2 = [np.sqrt(3) * self.__L * np.cos(phi_2) / 2, self.__L *
               np.cos(phi_2) / 2, -self.__L * np.sin(phi_2)]
        L_3 = [-np.sqrt(3) * self.__L * np.cos(phi_3) / 2, self.__L *
               np.cos(phi_3) / 2, -self.__L * np.sin(phi_3)]
        return np.array([L_1, L_2, L_3]).T

    def get_vector_B_A(self):
        phi_1, phi_2, phi_3 = self.__angle
        A_1 = [0, -self.__wb - self.__L * np.cos(phi_1), -self.__L * np.sin(phi_1)]
        A_2 = [np.sqrt(3) * (self.__wb + self.__L * np.cos(phi_2)) / 2,
               (self.__wb + self.__L * np.cos(phi_2)) / 2, -self.__L * np.sin(phi_2)]
        A_3 = [-np.sqrt(3) * (self.__wb + self.__L * np.cos(phi_3)) / 2,
               (self.__wb + self.__L * np.cos(phi_3)) / 2, -self.__L * np.sin(phi_3)]
        return np.array([A_1, A_2, A_3]).T