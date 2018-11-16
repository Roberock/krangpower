# ,---------------------------------------------------------------------------,
# |  This module is part of the krangpower electrical distribution simulation |
# |  suit by Federico Rosato <federico.rosato@supsi.ch> et al.                |
# |  Please refer to the license file published together with this code.      |
# |  All rights not explicitly granted by the license are reserved.           |
# '---------------------------------------------------------------------------'

import numpy as np

from .._graphview import GraphView
from .._krangsuit import Krang, UM


__all__ = ['BusVoltageView', 'VoltageView', 'CurrentView', 'BaseVoltageView', 'BusTotPowerView', 'AvgCurrentView',
           'BusTotCurrentView', 'EdgeCurrentView']


class VoltageView(GraphView):
    def __init__(self, ckgr: Krang):
        def busV(bus):
            return bus['bus'].Voltages()

        def edgeV(edg):
            return edg['el'][0].Voltages()

        super().__init__(busV, edgeV, ckgr)


class BusVoltageView(GraphView):
    def __init__(self, ckgr: Krang):
        def avgbusV(bus):
            return np.mean(np.abs(bus['bus'].Voltages()))

        super().__init__(avgbusV, None, ckgr)

    def xyz(self):
        return np.asarray([x[0] for x in self.pad_pos.values()]), \
               np.asarray([x[1] for x in self.pad_pos.values()]), \
               np.asarray([self[k].magnitude for k in self.pad_pos.keys()])

    def min_v(self):
        vs = [self[x] for x in self.nodes]
        return min(vs)


class CurrentView(GraphView):
    def __init__(self, ckgr: Krang):

        def edgeI(edg):
            return edg['el'][0].Currents()

        super().__init__(None, edgeI, ckgr)


class BaseVoltageView(GraphView):
    def __init__(self, ckgr: Krang, voltage_bases):

        ckgr.set(voltagebases=voltage_bases)
        ckgr.command('calcvoltagebases')

        def basebuskV(bus):
            return bus['bus'].kVBase()

        super().__init__(basebuskV, None, ckgr)


class BusTotPowerView(GraphView):
    def __init__(self, ckgr: Krang):

        def buspower(bus):
            pwr = [0.0j] * len(ckgr['bus.' + bus['bus'].name].Voltages()) * UM.kW

            if bus.get('el', None) is not None:
                for el in bus['el']:
                    node_index = el.NodeOrder()
                    powers = el.Powers()

                    for node, powa in zip(node_index[0], powers[0]):
                        if node == 0:
                            continue
                        pwr[node-1] += powa
                    
            else:
                pass

            return np.sum(pwr)

        super().__init__(buspower, None, ckgr)


class BusTotCurrentView(GraphView):
    def __init__(self, ckgr: Krang):

        def buscurr_2_elements(bus):

            fincurr = [0.0j] * len(ckgr['bus.' + bus['bus'].name].Voltages()) * UM.A

            if bus.get('el', None) is not None:
                for el in bus['el']:
                    node_index = el.NodeOrder()
                    currents = el.Currents()

                    for node, current in zip(node_index[0], currents[0]):
                        if node == 0:
                            continue
                        fincurr[node-1] += current

            #         try:
            #             # here i am guaranteed that the element has one bus and one or more terminals
            #             totcurr += el.Currents()
            #         except NameError:
            #             totcurr = el.Currents()
            #
            # try:
            #     fincurr[int(phase)-1] = totcurr[0][0]
            #     fincurr[3] = totcurr[0][1]
            # except:
            #     pass

            return fincurr

        super().__init__(buscurr_2_elements, None, ckgr)


class AvgCurrentView(GraphView):
    def __init__(self, ckgr: Krang):

        def edgeavgI(edg):
            return np.sum(np.mean(np.abs(edg['el'][0].Currents()), axis=0))

        super().__init__(None, edgeavgI, ckgr)


class EdgeCurrentView(GraphView):
    def __init__(self, ckgr: Krang):

        def edgeI(edg):
            return edg['el'][0].Currents()

        super().__init__(None, edgeI, ckgr)

