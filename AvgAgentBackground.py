import numpy as np
import random


class Person:
    def __init__(self, arrival_time=0):

        # Relation to Virions
        self.mask = None
        self.Virions_Breathed_In = [0]
        self.Vol_Breath_In = 10 ** 1  # L / min
        self.Vol_Breath_In_array = []
        self.Virions_in_body = [0]

        # Relation To Spawned
        self.Spawned = False
        self.frames_spawned = 0
        self.arrival_time = arrival_time
        self.Time_Stayed = 0
        self.Exiting = False
        self.marked_for_removal = False
        self.face_direction = random.choice([1, 2, 3, 4])  # Cardinal directions clockwise: 1:N 2:E 3:S 4:W

    def check_mask(self):  # assume N95 or better
        a = np.random.rand()

        if a < 0:
            self.mask = True
        if a >= 0:
            self.mask = False

    def breathe_in(self, Virions, minutes_per_frame):
        # Breathe in number of virions in the cell
        V = self.Vol_Breath_In*minutes_per_frame
        self.frames_spawned += 1

        self.Virions_Breathed_In.append(Virions * V)
        self.Virions_in_body.append(np.sum(self.Virions_Breathed_In))


class Susceptible(Person):
    pass

    def __init__(self, Arrival_Time=0):
        super().__init__(Arrival_Time)
        self.P_inf = 0

    def Prob_of_Infection(self):
        N_inf = 1000
        a = np.random.uniform(0, 1)

        self.P_inf = 1 - np.exp((-self.Virions_in_body[self.frames_spawned]) / N_inf)  # Likelihood of getting infected
        if self.P_inf > a:
            self.__class__ = Infected_Pre_Infectious
        if self.P_inf < a:
            pass


class Infected(Person):
    pass

    def Breathe(self, minutes_per_frame, v_inf_rate, k=1):
        # k is the super-spreading coefficient k = 1, 2, 3
        Vol_Breath = 10 ** (-9)  # L / min
        rho = 10 ** 12  # RNA / L

        Virions = rho * Vol_Breath * v_inf_rate * minutes_per_frame  # Virions/min

        return Virions

    def Talk(self, minutes_per_frame, v_inf_rate, talk_prob=0):

        # talk_prob = .5 is a random guess at the amount of time spent talking (will vary in the end, possibly per person)
        rho = 10 ** 12  # RNA/L
        Volume_Talk_Rate = 10 ** (-8)  # L/min

        Virions = rho * Volume_Talk_Rate * v_inf_rate * minutes_per_frame

        return Virions

    def Cough(self, minutes_per_frame, v_inf_rate):
        rho = 10 ** 12  # RNA / L
        Volume_Cough = 10 ** (-7)  # L

        Virions = Volume_Cough * rho * v_inf_rate * minutes_per_frame

        return Virions

    def Sneeze(self, minutes_per_frame, v_inf_rate):
        rho = 10 ** 12  # RNA/L
        Volume_Sneeze = 10 ** (-6)  # L

        Virions = Volume_Sneeze * rho * v_inf_rate * minutes_per_frame

        return Virions


class Infected_Pre_Infectious(Person):
    pass
