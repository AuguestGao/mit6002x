# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb        

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        # TODO
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        # TODO
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        # TODO
        return random.random() <= self.clearProb

    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        # TODO
        if random.random() <= self.maxBirthProb * (1 - popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException
        

class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        # TODO
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        # TODO
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        # TODO
        return self.maxPop

    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        # TODO  
        return len(self.viruses)


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - 1 Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - 2 The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - 3 Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        # TODO
        # 1 update surviving viruses
        surviveViruses = []
        for virus in self.viruses:
            if not virus.doesClear():
                surviveViruses.append(virus)
        self.viruses = surviveViruses[:]

                
        # 2 calculate current population density
        currPopDen = len(self.viruses)/self.maxPop
        
        # 3 determine wheather a virus will reproduce by calling reproduce method
        childVirusParticles = []
        for virus in self.viruses:
            try: 
                childVirusParticle = virus.reproduce(currPopDen)
            except NoChildException:
                pass
            else:
                childVirusParticles.append(childVirusParticle)
        self.viruses += childVirusParticles
        return self.getTotalPop()

#
# PROBLEM 2
#
import numpy as np
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    # TODO
    # initial all_pops: list of lists which contain each trail's virus population for 300 steps
    all_pops = []
    
    # start trails
    for _ in range(numTrials):
        
        #initiate numViruses identical viruses
        viruses = np.full(numViruses, SimpleVirus(maxBirthProb, clearProb))
        
        #initiate patient
        patient1 = Patient(viruses.tolist(), maxPop)
        
        pops = []
        #300 steps
        for step in range(300):
            pop = patient1.update()
            pops.append(pop)
        
        all_pops.append(pops)
    
    # convert all_pops from list to np object
    all_pops = np.array(all_pops)
    
    # calculate average pop at X step
    avg_pops = np.average(all_pops, axis = 0)
    
    pylab.plot(np.arange(1, 301), avg_pops, label = "SimpleVirus")
    pylab.title("SimpleVirus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc = "best")
    pylab.show()
    
#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        # TODO
        super().__init__(maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        # TODO
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        # TODO
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        # TODO
        try:
            return self.resistances[drug]
        except KeyError:
            return False


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        # TODO
        # check if this virus resists to ALL the drugs in the activeDrug list
        if len(activeDrugs) == sum([self.isResistantTo(drug) for drug in activeDrugs]):
            # check prob of reproduction of itself   
            if random.random() <= self.maxBirthProb * (1 - popDensity):
                #update resistance before reproduce
                resistances = {}
                for drug, resis in self.resistances.items():
                    if random.random() <= 1 - self.mutProb:
                        resistances[drug] = resis
                    else:
                        resistances[drug] = not resis
                        
                return ResistantVirus(self.maxBirthProb, self.clearProb, resistances, self.mutProb)
        raise NoChildException
        
class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        # TODO
        super().__init__(viruses, maxPop)
        self.drugs = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        # TODO
        if newDrug in self.drugs:
            pass
        else:
            self.drugs.append(newDrug)
        

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        # TODO
        return self.drugs

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        # TODO
        count = 0
        for virus in self.viruses:
            resisStatus = True
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    resisStatus = False
                    break
            if resisStatus:
                count += 1
        return count
            

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - 1 Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - 2 The current population density is calculated. This population density
          value is used until the next call to update().

        - 3 Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        # TODO
        # 1 update surviving viruses
        surviveViruses = []
        for virus in self.viruses:
            if not virus.doesClear():
                surviveViruses.append(virus)
        self.viruses = surviveViruses[:]

                
        # 2 calculate current population density
        currPopDen = len(self.viruses)/self.maxPop
        
        # 3 determine wheather a virus will reproduce by calling reproduce method
        childVirusParticles = []
        
        for virus in self.viruses:
            try: 
                childVirusParticle = virus.reproduce(currPopDen, self.drugs)
            except NoChildException:
                pass
            else:
                childVirusParticles.append(childVirusParticle)
        self.viruses += childVirusParticles
        return self.getTotalPop()


#
# PROBLEM 4
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    # TODO
    # initial all_pops: list of lists which contain each trail's virus population for timestep steps
    timestep = 150
    allTrial_totalPops = []
    allTrial_guttagonolResistPops = []
    
    # start trails
    for _ in range(numTrials):
        #initiate numViruses identical viruses
        viruses = np.full(numViruses, ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
        #print(np.shape(viruses))

        #initiate patient
        patient2 = TreatedPatient(viruses.tolist(), maxPop)
        totalPops = []
        guttagonolResistPops = []
        for step1 in range(timestep):
            totalPop = patient2.update()
            totalPops.append(totalPop)
            guttagonolResistPop = patient2.getResistPop(['guttagonol'])
            guttagonolResistPops.append(guttagonolResistPop)
            
        patient2.addPrescription('guttagonol')
        
        for step2 in range(timestep):
            totalPop = patient2.update()
            totalPops.append(totalPop)
            guttagonolResistPop = patient2.getResistPop(['guttagonol'])
            guttagonolResistPops.append(guttagonolResistPop)          
        
        allTrial_totalPops.append(totalPops)
        allTrial_guttagonolResistPops.append(guttagonolResistPops)
    
    # convert all_pops from list to np object
    allTrial_totalPops = np.array(allTrial_totalPops)
    allTrial_guttagonolResistPops = np.array(allTrial_guttagonolResistPops)
    
    # calculate average pop at X step
    avg_totalPops = np.average(allTrial_totalPops, axis = 0)
    avg_guttagonolResistPops = np.average(allTrial_guttagonolResistPops, axis = 0)
    
    pylab.plot(avg_totalPops, label = "Virus (total)")
    pylab.plot(avg_guttagonolResistPops, label = "Virus (guttagonol resistant)")
    pylab.title("ResistantVirus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc = "best")
    pylab.show()
    