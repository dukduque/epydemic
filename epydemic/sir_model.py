# SIR as a compartmented model
#
# Copyright (C) 2017--2019 Simon Dobson
# 
# This file is part of epydemic, epidemic network simulations in Python.
#
# epydemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# epydemic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with epydemic. If not, see <http://www.gnu.org/licenses/gpl.html>.

from epydemic import *

class SIR(CompartmentedModel):
    '''The Susceptible-Infected-Removed :term:`compartmented model of disease`.
    Susceptible nodes are infected by infected neighbours, and recover to
    removed.'''
    
    # the model parameters
    P_INFECTED = 'pInfected'  #: Parameter for probability of initially being infected.
    P_INFECT = 'pInfect'      #: Parameter for probability of infection on contact.
    P_REMOVE = 'pRemove'      #: Parameter for probability of removal (recovery).
    
    # the possible dynamics states of a node for SIR dynamics
    SUSCEPTIBLE = 'S'         #: Compartment for nodes susceptible to infection.
    INFECTED = 'I'            #: Compartment for nodes infected.
    REMOVED = 'R'             #: Compartment for nodes recovered/removed.

    # the edges at which dynamics can occur
    SI = 'SI'                 #: Edge able to transmit infection.

    def __init__( self ):
        super(SIR, self).__init__()

    def build( self, params ):
        '''Build the SIR model.

        :param params: the model parameters'''
        pInfected = params[self.P_INFECTED]
        pInfect = params[self.P_INFECT]
        pRemove = params[self.P_REMOVE]

        self.addCompartment(self.SUSCEPTIBLE, 1 - pInfected)
        self.addCompartment(self.INFECTED, pInfected)
        self.addCompartment(self.REMOVED, 0.0)

        self.trackEdgesBetweenCompartments(self.SUSCEPTIBLE, self.INFECTED, name=self.SI)
        self.trackNodesInCompartment(self.INFECTED)

        self.addEventPerElement(self.SI, pInfect, self.infect)
        self.addEventPerElement(self.INFECTED, pRemove, self.remove)

    def infect( self, t, e ):
        '''Perform an infection event. This changes the compartment of
        the susceptible-end node to :attr:`INFECTED`. It also marks the edge
        traversed as occupied.

        :param t: the simulation time
        :param e: the edge transmitting the infection, susceptible-infected'''
        (n, _) = e
        self.changeCompartment(n, self.INFECTED)
        self.markOccupied(e, t)

    def remove( self, t, n ):
        '''Perform a removal event. This changes the compartment of
        the node to :attr:`REMOVED`.

        :param t: the simulation time (unused)
        :param n: the node'''
        self.changeCompartment(n, self.REMOVED)
    
                
   
