from core.experience import Experience, ExperienceParameter, ExperienceParameter
from core.topo import Topo, TopoParameter

from mininet_builder import MininetBuilder

from experiences import EXPERIENCES
from topos import TOPO_CONFIGS, TOPOS


class MpXpRunner:
    def __init__(self, builderType, topoParamFile, xpParamFile):
        self.defParamXp(xpParamFile)
        self.topoParam = TopoParameter(topoParamFile)
        self.defBuilder(builderType)
        self.defTopo()
        self.defConfig()
        self.startTopo()
        self.runXp()
        self.stopTopo()

    def defParamXp(self, xpParamFile):
        self.xpParam = ExperienceParameter(xpParamFile)

    def defBuilder(self, builderType):
        if builderType == Topo.mininetBuilder:
            self.topoBuilder = MininetBuilder()
        else:
            raise Exception("I can not find the builder " +
                    builderType)
    def defTopo(self):
        t = self.topoParam.getParam(Topo.topoAttr)
        if t in TOPOS:
            self.Topo = TOPOS[t](self.topoBuilder, self.topoParam)
        else:
            raise Exception("Unknown topo: {}".format(t))
        print(self.Topo)

    def defConfig(self):
        t = self.topoParam.getParam(Topo.topoAttr)
        if t in TOPO_CONFIGS:
            self.TopoConfig = TOPO_CONFIGS[t](self.Topo, self.topoParam)
        else:
            raise Exception("Unknown topo config: {}".format(t))

    def startTopo(self):
        self.Topo.startNetwork()
        self.TopoConfig.configureNetwork()

    def runXp(self):
        xp = self.xpParam.getParam(ExperienceParameter.XPTYPE)
        if xp in EXPERIENCES:
            EXPERIENCES[xp](self.xpParam, self.Topo, self.TopoConfig)
        else:
            raise Exception("Unknown experience {}".format(xp))

    def stopTopo(self):
        self.Topo.stopNetwork()
