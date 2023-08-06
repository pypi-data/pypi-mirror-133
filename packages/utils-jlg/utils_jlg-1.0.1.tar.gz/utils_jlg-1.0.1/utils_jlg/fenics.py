from scipy.interpolate import griddata
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import os
from fenics import *


def fenics_fun_2_grid( fun, mesh, Nx_Ny = None):

    """
    Return regular grid with the interpolated values in Nx_Ny points
    of the fenics function fun evaluated on the fenics mesh vertex values

    used to make plots of 2d sims
    """

    points = mesh.coordinates()
    values = fun.compute_vertex_values(mesh)

    x0 = mesh.coordinates()[:,0].min()
    x1 = mesh.coordinates()[:,0].max()
    y0 = mesh.coordinates()[:,1].min()
    y1 = mesh.coordinates()[:,1].max()

    ratio = (x1-x0)/(y1-y0)

    if not(Nx_Ny):
        Ny = int(np.sqrt(len(mesh.coordinates())/ratio))
        Nx = int( len(mesh.coordinates() )/ Ny )

    else:
        Nx = Nx_Ny[0]
        Ny = Nx_Ny[1]

    X,Y,Z = scatter_2_grid(points, values, (x0,x1), (y0,y1), Nx, Ny)

    return X,Y,Z



def fenics_fun_2_grid1D( fun, mesh, Nx = None):

    """

    Used to make plots of 1d sims

    """

    points = mesh.coordinates()
    values = fun.compute_vertex_values(mesh)

    x0 = mesh.coordinates()[:,0].min()
    x1 = mesh.coordinates()[:,0].max()



    if not(Nx):
        Nx = int( len(mesh.coordinates() ) )

    else:
        Nx = Nx

    X = np.linspace(x0, x1, Nx)

    Z = griddata(points, values, (X))

    return X,Z



def scatter_2_grid(points, values, x_range, y_range, Nx = 100, Ny = 100):
    """

    points array of shape [Npoints, dims]
    values array of shape [Npoints,]
    """


    x = np.linspace(x_range[0], x_range[1], Nx)
    y = np.linspace(y_range[0], y_range[1], Ny)

    X,Y = np.meshgrid(x,y)



    Z = griddata(points , values, (X,Y))

    return X, Y , Z






class PeriodicBoundary1D(SubDomain):

    def __init__(self, L = 1.0):
        super().__init__()
        self._L = L

    def inside(self, x, on_boundary):

        L = self._L
        sides = bool(x[0] < DOLFIN_EPS and (x[0]-L) < DOLFIN_EPS and on_boundary)


        return sides

    def map(self, x, y):

        L = self._L

        if near(x[0], L):
            y[0] = x[0] - L


class PeriodicBoundary2D(SubDomain):

    def __init__(self, L = 1.0):
        super().__init__()
        self._L = L

    def inside(self, x, on_boundary):

        L = self._L
        sides = bool(x[0] < DOLFIN_EPS and (x[0]-L) < DOLFIN_EPS and on_boundary)
        updown = bool(x[1] < DOLFIN_EPS and (x[1]-L) < DOLFIN_EPS and on_boundary)

        return sides or updown

    def map(self, x, y):

        L = self._L

        if near(x[0], L) and near(x[1], L):
            y[0] = x[0] - L
            y[1] = x[1] - L
        elif near(x[0], L):
            y[0] = x[0] - L
            y[1] = x[1]
        else:
            y[0] = x[0]
            y[1] = x[1] - L


def eval_gaussians(x,y, stds, mus, amps = None):

    fun_eval = 0.0
    for i in range(len(stds)):
        std = stds[i]
        mu = mus[i]

        if not(isinstance(amps,np.ndarray) or isinstance(amps,list)):
            amp = 1.0
        else:
            amp = amps[i]
        fun_eval = fun_eval + amp*16*x*(1-x)*y*(1-y)*np.exp(-0.5*(x-mu[0])**2/std[0]**2-0.5*(y-mu[1])**2/std[1]**2)

    return fun_eval

def eval_rectangles(x,y, origins, shapes , amps  = None):

    fun_eval = 0.0
    for i in range(len(origins)):
        shape = shapes[i]
        origin = origins[i]

        if not(isinstance(amps,np.ndarray) or isinstance(amps,list)):
            amp = 1.0
        else:
            amp = amps[i]

        val = 0.0

        if (x>origin[0] and x<(origin[0]+shape[0]) ):
            if (y>origin[1] and y<(origin[1]+shape[1])):
                val = amp

        fun_eval = fun_eval + val

    return fun_eval



def eval_image(x,y, image):

    image = image.T

    dimx, dimy = np.shape(image)

    coordx = int(np.floor(dimx*x))
    coordy = int(np.floor(dimy*y))

    if coordx == dimx:
        coordx = coordx-1
    if coordy == dimy:
        coordy = coordy-1

    val = image[coordx,coordy]

    return val


class InitialConditions1D(UserExpression):

    def __init__(self, mode = "random"):
        super().__init__()
        self._mode = mode


    def eval(self, values, x):

        if self._mode == "random":
            values[0] =  0.02*(0.5 - np.random.random())
        else:
            raise(ValueError("Only mode random"))

class InitialConditions2D(UserExpression):

    def __init__(self, image, mode = "random"):
        super().__init__()
        self._mode = mode

        self._image = image


    def eval(self, values, x):

        if self._mode == "random":
            values[0] =  0.02*(0.5 - np.random.random())
        elif self._mode == "image":
            values[0] =  eval_image(x[0],x[1],self._image)

        elif self._mode == "rectangles":
            values[0] =  eval_rectangles(x[0],x[1], self._origins, self._shapes, self._amps)
        elif self._mode == "gaussians":
            values[0] = eval_gaussians(x[0],x[1], self._stds, self._mus, self._amps)

        elif self._mode == "fourier":
            values[0] = 0.02*np.cos(np.pi*2*2*x[0])*np.cos(np.pi*2*4*x[1])-0.02*np.cos(np.pi*2*3*x[0])*np.cos(np.pi*2*1*x[1])+0.01*np.cos(np.pi*2*5*x[0])*np.cos(np.pi*2*2*x[1])\
                        +0.02*np.cos(np.pi*2*3*x[0])*np.cos(np.pi*2*3*x[1])



def solve_allen_cahn(eps = 0.01, n_elements = 60,T_dt = 200, ratio_speed = 10 ,initial_conditions = "random", dtype_out = np.float32):

    t0 = 100 # iterations to solve with smaller dt

    dt0 = eps*2*1e-3

    ratio_speed = ratio_speed #increasing step when evolution when interfaces are formed

    _dt = dt0*ratio_speed

    dt = Constant(dt0)

    mesh = UnitSquareMesh(n_elements, n_elements)
    V= FunctionSpace(mesh, "P", 1,constrained_domain=PeriodicBoundary())

    u = Function(V)
    v = TestFunction(V)
    u_n = Function(V)


    # Create intial conditions and interpolate
    u_init = InitialConditionsAC(initial_conditions)
    u_n.interpolate(u_init)



    F = (u*v-u_n*v+dt*dot(grad(u),grad(v))+dt*(1/eps**2)*(u**2-1)*u*v)*dx


    sols_first = []

    sols = []
    for i in tqdm(range(T_dt+t0)):

        if i>t0:

            dt.assign(_dt) #increasing dt after initial decomposition

        solve(F == 0, u)



        u_n.assign(u)

        X,Y,Z = fenics_fun_2_grid(u,mesh)

        if i>t0:
            sols.append(Z)
        else:
            sols_first.append(Z)

    sols_first = np.array(sols_first).astype(dtype_out)[::ratio_speed]
    sols = np.array(sols).astype(dtype_out)

    sols = np.concatenate((sols_first,sols), axis = 0)

    return sols
def solve_allen_cahn_1D(tc = 1, xc = 0.1, eps = 1e-2, n_elements = 200,T = 60 ,initial_conditions = "random", dtype_out = np.float32):

    gamma = 1/tc
    D = eps*xc**2/tc
    _dt = tc/20
    T_dt = int(T/_dt)

    dt = Constant(_dt)

    mesh = UnitIntervalMesh(n_elements)
    V= FunctionSpace(mesh, "P", 1,constrained_domain=PeriodicBoundary1D())

    u = Function(V)
    v = TestFunction(V)
    u_n = Function(V)


    # Create intial conditions and interpolate
    u_init = InitialConditions1D(mode = initial_conditions)
    u_n.interpolate(u_init)



    F = (u*v-u_n*v+D*dt*dot(grad(u),grad(v))+gamma*dt*(u**2-1)*u*v)*dx



    sols = []
    for i in tqdm(range(T_dt)):



        solve(F == 0, u)



        u_n.assign(u)

        X,Z = fenics_fun_2_grid1D(u,mesh)

        sols.append(Z)


    sols = np.array(sols).astype(dtype_out)


    return sols


def solve_burgers_1D(nu = 0.5*1e-1, T = 2.0, n_steps = 100, n_elements = 100,initial_condition_n = 1, dtype_out = np.float32):

    T = T            # final time
    dt = T / n_steps # time step size

    # Create mesh and define function space
    nx = n_elements

    x0, xf = (0, 1.0)
    mesh = IntervalMesh(nx, x0, xf)
    V = FunctionSpace(mesh, 'CG', 2)

    # Define boundary condition
    def left(x, on_boundary):
        return on_boundary and near(x[0], x0)
    def right(x, on_boundary):
        return on_boundary and near(x[0], xf)

    bc_l = DirichletBC(V, Constant(0), left)
    bc_r = DirichletBC(V, Constant(0), right)

    bcs = [bc_l, bc_r]

    def eval_1(x):
        val = np.sin(x*np.pi*2)
        return val
    def eval_2(x):
        val = 10*np.sin(x*np.pi/2)*(1-x)**4
        return val

    initial_condition = {1:eval_1, 2:eval_2}

    class InitialConditions(UserExpression):

        def eval(self, values, x):
            values[0] = initial_condition[int(initial_condition_n)](x[0])


    u_n = Function(V)
    u_init = InitialConditions()
    u_n.interpolate(u_init)
    #u_n = interpolate(u_0, V)

    # Define variational problem
    u = Function(V)
    v = TestFunction(V)

    F = (v*(u-u_n)+dt*(v*u*u.dx(0) +nu*dot(grad(u),grad(v))))*dx


    sols = []
    #u = Function(V)
    for i in tqdm(range(n_steps)):



        solve(F == 0, u, bcs)



        u_n.assign(u)

        X,Z = fenics_fun_2_grid1D(u,mesh)

        sols.append(Z)


    sols = np.array(sols).astype(dtype_out)


    return sols
