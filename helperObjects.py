'''

Abandoned Code

'''
import pandas as pd
import numpy as np

class grid():
    def __init__(self, zone_id, zone_dat):
        self.energySources = self.powerGroup(zone_dat['energySources'],zone_dat['energyStores'])
        self.coords = (zone_dat['topLeftX'],
                       zone_dat['topLeftY'],
                       zone_dat['bottomRightX'],
                       zone_dat['bottomRightY'],)
        self.id = zone_id

class powerObject():
    def __init__(self, info, linkedPower = None):
        if 'type' in info:
            self.capacity = info['generationCapacity']
            self.type = 'Generator'
        else:
            self.storage = info['capacityMWh']/60
            self.stored = 0
            self.efficiency = info['efficiency']
            self.capacity = info['maxDischargePowerMw']/60
            self.type = 'Storage'
            self.linkedPower = linkedPower
            if self.linkedPower is None:
                raise ValueError('No Linked Power object when creating a power storage')
        self.allocated = 0
        self.free = self.capacity

    def getCapacity(self):
        if self.type == 'Generator':
            return self.capacity()
        if self.type == 'Storage':
            return max(self.capacity, self.stored)
    
    def step(self, draw):
        self.allocated = min(self.getCapacity(), draw)
        self.free = self.capacity - draw
        if self.type == 'Storage':
            self.stored += self.linkedPower.free - self.allocated
        return self.allocated    
    
    @staticmethod
    def isGreen(arg):
        if isinstance(arg, str):
            match arg:
                case: 'Nuclear'
            

class powerGroup():
    def __init__(self, energySources, energyStores):
        '''
        Three types of power source (simplified):
            Green
            Fossil
            Stored

            At a given time, and demand, the flow is this
            GreenFufillment = min(Demand, GreenCapacity) -> recipricol (RemainingDemand)
            StoredFufillment = min(RemainingDemand, StoredCapcity) -> --||--
            FossilFufillment = min(RemainingDemand, FossilCapcity) -> --||--
            Brownout = RemainingDemand > 0

            GreenCapacity = f(weather)
            StoredCapcity = min(StoredEnergy, DischargeRate)
            FossilCapacity = k

            So given a discretized time grid, the amount stored as a function of a demand series is
            Sum[(GreenCapacity - GreenFufillment) - StoredFufillment]
            ie. the rate of change per tick is
            m(GreenCapacity - GreenFufillment) - StoredFufillment

            Again given a discretized time grid, the fastest charge is then to use at every tick
            GreenCapacity + StoredCapacity + FossilCapacity
            # And the greenest charge
            GreenCapacity + StoredCapacity
            # And the fastest charge targeting a specific 'greenness' level
            GreenCapcity + StoredCapcity + (FossilCapacity when FossilFufillment < FossilFraction*TotalDemand)
        '''
        self.orderedEnergy = energySources




        
'''

Abandoned Code

'''