import matplotlib.pyplot as plt

class SolDrawerTotal:
    @staticmethod
    def get_cmap(n, name='hsv'):
        return plt.cm.get_cmap(name, n)

    @staticmethod
    def draw(itr, sol, nodes):
        plt.clf()
        SolDrawerTotal.drawPoints(nodes)
        SolDrawerTotal.drawRoutes(sol)
        plt.savefig(str(itr))

    @staticmethod
    def drawPoints(nodes:list):
        x = []
        y = []
        for i in range(len(nodes)):
            n = nodes[i]
            for j in range(len(n)):
                x.append(n[j].x)
                y.append(n[j].y)
                if n[j].ID == 0:
                    plt.scatter(x, y, c="red")
                else:
                    plt.scatter(x, y, c="blue")


    @staticmethod
    def drawRoutes(sol):
        cmap = SolDrawerTotal.get_cmap(len(sol.routes))
        if sol is not None:
            for r in range(0, len(sol.routes)):
                rt = sol.routes[r]
                for j in range(0, len(rt)):
                    for i in range(0, len(rt[j].sequenceOfNodes) - 1):
                        c0 = rt[j].sequenceOfNodes[i]
                        c1 = rt[j].sequenceOfNodes[i + 1]
                        plt.plot([c0.x, c1.x], [c0.y, c1.y], c=cmap(r))

