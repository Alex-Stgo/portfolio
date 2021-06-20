import numpy as np

class labyrinth():
    def __init__(self,gamma,alpha):
        self.gamma = gamma
        self.alpha=alpha
        self.locations = ['A','B','C','D','E','F','G','H','I','J','K','L']
        self.labs = [np.array([[0,1,0,0,0,0,0,0,0,0,0,0],
            [1,0,1,0,0,1,0,0,0,0,0,0],
            [0,1,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0],
            [0,1,0,0,0,0,0,0,0,1,0,0],
            [0,0,1,0,0,0,0,1,0,0,0,0],
            [0,0,0,1,0,0,1,0,0,0,0,1],
            [0,0,0,0,1,0,0,0,0,1,0,0],
            [0,0,0,0,0,1,0,0,1,0,1,0],
            [0,0,0,0,0,0,0,0,0,1,0,1],
            [0,0,0,0,0,0,0,1,0,0,1,0]])]
    def get_route(self,lab,start,end,iterations=1000):
        self._qvalues(lab,end,iterations=iterations)
        self._route(start,end)
        return self.route
    def _qvalues(self,lab,target, iterations=1000):
        self.r = self.labs[lab]
        dim = self.r.shape[0]
        end = target
        self.r[end, end] = 10000
        self.q = np.array(np.zeros([dim,dim]))
        for _ in range(iterations):
            start = np.random.randint(0,dim)
            actions = [i for i,j in enumerate(self.r[start,].tolist()) if j>0]
            next = np.random.choice(actions)
            TD = self.r[start, next] + self.gamma * self.q[next, np.argmax(self.q[next,])] - self.q[start, next]
            self.q[start, next] = self.q[start, next] + self.alpha * TD
    def _route(self,start,end):
        route = [self.locations[start]]
        next = start
        while (next != end):
            # start_ = self.locations.index(start)
            next = np.argmax(self.q[start,])
            next_ = self.locations[next]
            route.append(next_)
            start = next
        self.route=route
        return route