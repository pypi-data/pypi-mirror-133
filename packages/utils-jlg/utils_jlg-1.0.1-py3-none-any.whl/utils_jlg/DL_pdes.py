import sympy as sym
from sympy.abc import x,y
import torch
from torch import nn
from torch.autograd import grad
from video_image import make_gif,fig_to_array
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def fun_poisson_linear_1D(u, sigma ):
    """
    from symbolic fun created with from sympy.abc import x

    calculates poisson f 1d and makes it numpy callable

    """

    f = - sigma*sym.diff(sym.diff(u, x), x)
    f = sym.simplify(f)
    fun_f = sym.lambdify((x),f,"numpy")
    fun_u = sym.lambdify((x),u,"numpy")
    u_code = sym.printing.ccode(u)
    f_code = sym.printing.ccode(f)

    return fun_f, fun_u,  u_code, f_code



def fun_poisson_linear_2D(u, sigma ):
    """
    from symbolic fun created with from sympy.abc import x,y

    calculates poisson f  2d and makes it numpy callable

    """


    f = - sigma*(sym.diff(sym.diff(u, x), x)+ sym.diff(sym.diff(u, y), y) )
    f = sym.simplify(f)
    fun_f = sym.lambdify((x,y),f,"numpy")
    fun_u = sym.lambdify((x,y),u,"numpy")
    u_code = sym.printing.ccode(u)
    f_code = sym.printing.ccode(f)

    return fun_f, fun_u,  u_code, f_code



def Nu_poisson_1D(u_pred, x, source_fun, sigma):

    source = torch.Tensor( source_fun(x.clone().detach().numpy().reshape(-1,1)) )

    u_x = grad(u_pred,x, create_graph = True, grad_outputs = torch.ones_like(u_pred))[0]
    u_xx = grad(u_x, x, create_graph = True, grad_outputs = torch.ones_like(u_x))[0]


    f = source + sigma*u_xx

    return f.view(-1,1)


def Nu_poisson_2D(u_pred, X , source_fun, sigma):

    x,y = X[:,0], X[:,1]
    source = torch.Tensor( source_fun(x.clone().detach().numpy().reshape(-1,1), y.clone().detach().numpy().reshape(-1,1)) )

    u_x = grad(u_pred,X, create_graph = True, grad_outputs = torch.ones_like(u_pred))[0].view(-1,1)
    u_xx = grad(u_x, X, create_graph = True, grad_outputs = torch.ones_like(u_x))[0][:,0].view(-1,1)

    u_y = grad(u_pred,X, create_graph = True, grad_outputs = torch.ones_like(u_pred))[0].view(-1,1)
    u_yy = grad(u_y, X, create_graph = True, grad_outputs = torch.ones_like(u_y))[0][:,1].view(-1,1)

    f = source + sigma*(u_yy+u_xx)

    return f.view(-1,1)


def Nu_AC1D(u_pred, X , eps, M):


    u_x = grad(u_pred,X, create_graph = True, grad_outputs = torch.ones_like(u_pred))[0].view(-1,2)
    u_xx = grad(u_x, X, create_graph = True, grad_outputs = torch.ones_like(u_x))[0][:,0].view(-1,1)

    u_t = grad(u_pred,X, create_graph = True, grad_outputs = torch.ones_like(u_pred))[0][:,1].view(-1,1)

    f = u_t-M*(u_xx-(1/eps**2)*(u_pred**2-1)*u_pred)

    return f.view(-1,1)





def make_simulation_gif(eval_sim, real_sim, name, duration = 0.5, skip_time = ""):

    """
    eval_sim, real_sim [Nsamples,H,W]

    skip_time  --> times original sim dt for every frame in eval/real sim 
    """

    assert np.shape(eval_sim) == np.shape(real_sim), "shapes_not equal"


    str_time = skip_time

    _max = np.max(real_sim)
    _min = np.min(real_sim)

    arrays = []
    for i in range(len(eval_sim)):

        if skip_time:

            str_time = "{} x dt".format(skip_time*i)

        im1 = eval_sim[i]
        im2 = real_sim[i]
        plt.close("all")
        fig = plt.figure()
        plt.subplot(121)
        plt.title("Predicted {}".format(str_time),fontdict = {"fontsize":22})
        o = plt.imshow(im1,cmap='gray', vmin=_min, vmax=_max)
        plt.axis('off')
        plt.subplot(122)
        plt.title("Real {}".format(str_time),fontdict = {"fontsize":22})
        o = plt.imshow(im2,cmap='gray', vmin=_min, vmax=_max)
        plt.axis('off')
        fig.tight_layout()

        array = fig_to_array(fig)
        arrays.append(array)

    make_gif(arrays, name , duration = duration)


def plot_save_error_time(pred_batch,real_batch, skip_time , name = "time_error", results_dir = "./"):
    """
    batch_sim  (Nsims,steps,H,W)

    skip time, n times ahead used in training
    """

    assert len(np.shape(pred_batch)) == 4
    assert np.shape(pred_batch)==np.shape(real_batch)

    error_time = np.mean( np.square(pred_batch-real_batch) ,axis = (0,2,3))

    skip_time = int(skip_time)

    t = np.arange(0,len(pred_batch[0]),1)*skip_time

    fig = plt.figure(figsize = ( 12, 12))

    o = plt.plot(t,error_time)
    plt.ylabel("MSE")
    plt.xlabel("time steps")
    plt.title("Prediction error vs time")

    fig.savefig(os.path.join(results_dir,name)+".png")


    return fig


def make_batch_simulation_gif(batch_sim,name, results_dir = "./", size = (200,200), duration = 0.2):
    """
    batch_sim  (Nsims,steps,H,W)
    """

    assert len(np.shape(batch_sim)) == 4

    for i in tqdm(range(len(batch_sim))):
        _name = name+"{}.gif".format(i)
        _name = os.path.join(results_dir,_name)
        gif = make_gif(batch_sim[i],_name, size = size,duration = duration)








def plot_2D_comparison(pred, real, X_Y = None, title = ""):

    Zu = real
    Zpred = pred

    if not(X_Y):
        Xl = np.linspace(0,1, int(np.sqrt(real.size)) )
        Yl = np.linspace(0,1, int(np.sqrt(real.size) ) )
        X,Y = np.meshgrid(Xl,Yl)

    fig = plt.figure()

    fig.set_size_inches(16,16)
    # Plot the surface.

    ax1 = fig.add_subplot(3,2,1, projection = "3d")
    surf = ax1.plot_surface(X, Y, Zu,
                           linewidth=0, )
    ax1.set_title("Analytic solution")

    ax2 = fig.add_subplot(3,2,2, projection = "3d")
    surf = ax2.plot_surface(X, Y, Zpred,
                           linewidth=0,)

    ax2.set_title("NN solution")



    ax3 = fig.add_subplot(3,2,3)
    plt.imshow(Zu)

    ax4 = fig.add_subplot(3,2,4)
    plt.imshow(Zpred)


    fig.add_subplot(3,2,5)

    ax5 = fig.add_subplot(3,2,5)
    o = ax5.imshow(Zpred-Zu)

    ax5.set_title("Error")
    fig.colorbar(o)

    if title:
        fig.suptitle(title)

    return fig

def _make_grid_plot_2D(Npoints, xa = 0, xb = 1, ya = 0, yb = 1):

    Np = Npoints
    _x = np.linspace(xa, xb,Np)
    _y = np.linspace(ya,yb,Np)
    X,Y = np.meshgrid(_x,_y)


    return X,Y



def plot_2D_comparison_analytical(model_2D, fun_validation,Npoints = 80, xa = -1, xb = 1, ya = -1, yb = 1, title = ""):

    fun_u = fun_validation
    Np = Npoints

    X, Y = _make_grid_plot_2D(Np,xa = xa, xb = xb, ya = ya, yb = yb)

    _X, _Y = X.reshape(-1), Y.reshape(-1)

    Xnp = np.concatenate((_X.reshape((-1,1)), _Y.reshape((-1,1))), axis = 1)

    outu = fun_u(_X,_Y)
    Zreal  = outu.reshape((Np,Np))

    with torch.no_grad():
        Zpred = model_2D(torch.Tensor(Xnp)).detach().numpy()
        Zpred = Zpred.reshape((Np,Np))

    fig = plot_2D_comparison(Zpred, Zreal, title = title)

    return fig
