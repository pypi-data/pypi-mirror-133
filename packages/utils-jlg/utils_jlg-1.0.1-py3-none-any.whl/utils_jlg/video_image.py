import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import Image
import imageio
import io
from io import BytesIO


plt.style.use('ggplot')




def make_gif(list_ims, save_name, duration = 0.05, size = (200,200)):

    with imageio.get_writer(save_name,mode = "I", duration = duration) as writer:
        for sol in list_ims:

            s = sol
            im = ( (s-np.min(s))*(255.0/(np.max(s)-np.min(s))) ).astype(np.uint8)
            im = Image.fromarray(im).resize(size)
            writer.append_data(np.array(im))
    writer.close()



def make_gif_1D_arrays(list_arrays, duration = 0.1, name = "default_name.gif", ylim = None, xlim = (0,1)):

    if not(ylim):
        _max,_min = np.max(np.array(list_arrays)), np.min(np.array(list_arrays))
        ylim = (_min,_max)

    outs = []
    for array in list_arrays:
        plt.close("all")
        fig = plt.figure()

        x = np.linspace(0,1,len(array))

        p = plt.plot(x,array)

        plt.xlim(xlim)
        plt.ylim(ylim)

        _array = fig_to_array(fig)

        outs.append(_array)

    make_gif(outs,name, duration = duration)



def fig_to_array(fig):

    io_buf = io.BytesIO()
    fig.savefig(io_buf, format='raw')
    io_buf.seek(0)
    img_arr = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                         newshape=(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1))
    io_buf.close()

    return img_arr




class mplib_gif_wrapper():
    """
    Example
    -------
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax=mplib_gif_wrapper(ax,"test_wrapper.gif")


    #optional ax.reset_gif()
    for i in range(100):
        x=np.random.random((50))
        y=x**(i*0.02)
        x=np.random.random((100,100,3))
        ax.set_ylim(0,1)
        ax.set_xlim(0,1)
        ax.scatter(x,y)
    ---->gif saved as test_wrapper.gif

    Inputs:

    save_every: if None, save is only done explicitly withax.save()

    frames_per_second number of frames to display in one second of animation

    """
    def __init__(self,axes,fp,clear=True, save_every=10, frame_duration = 0.1,size = (255,255)):

        self.fp=fp
        self.axes=axes
        self._clear=clear
        self.save_every=save_every
        self.counter=0
        self.list_plots=["scatter","plot","imshow"]
        self.list_ims=[]
        self._frame_duration = frame_duration
        self._size = size

    def __getattr__(self,item):

        attr=getattr(self.axes,item)

        if item in self.list_plots:
            self.counter+=1
            self.list_ims.append(mplib_fig_2_image(self.axes.get_figure(),out="PIL"))

            if not(self.save_every == None):
                if self.counter%self.save_every==0:
                    self.save( duration = self._frame_duration, size = self._size)

            if self._clear:
                self.axes.clear()

        return attr

    def reset_gif(self, ):

        self.counter=0
        self.list_ims=[]

    def save(self, duration = 0.5, size = (255,255)):

        make_gif(self.list_ims,self.fp, duration = duration, size = size)





def _pil_2_image(im_pil,out=None,format="JPEG"):
    if out=="bytes":
        buf=BytesIO()
        im_pil.save(buf,format=format)
        bytes_out=buf.seek(0)
        return bytes_out
    elif out=="PIL":
        return im_pil
    else:
        im_pil.save(out,format=format)







def mplib_fig_2_image(fig,out="PIL",format="JPEG"):
    """ matplotlib figure to image
            input: matplotlib figure
            out : BytesIO instance,file_path,"bytes"
        specify the output, if BytesIO instance, bytes will be writen in the instance
    """
    buf=BytesIO()
    fig.savefig(buf)
    im_pil=Image.open(buf)
    im_pil = im_pil.convert('RGB')
    return _pil_2_image(im_pil,out=out,format=format)


def numpy_2_image(np_array,out=None,format="JPEG", size = (255,255)):
    """Np array (Width,Height,Channels)  to image bytes or pil
    Input
    -----
        np_array : (w,h,c) or filepath of .npy file
        out : BytesIO instance,file_path,"bytes"
        specify the output, if BytesIO instance, bytes will be writen in the instance
    """
    if isinstance(np_array,str):
        np_array=np.load(np_array)
    array=np_array.astype(np.uint8)
    im_pil=Image.fromarray(array).resize(size)

    return _pil_2_image(im_pil,out=out,format=format)




def image_2_numpy(fp):
    """
    fp might be bytes, Buf, filepath, or PIL Jpeg image
    """
    if isinstance(fp,bytes):
        read=BytesIO(fp)
        read=Image.open(read)
    elif isinstance(fp,Image.Image):
        read=fp
    else:
        read=Image.open(fp)
    out=np.array(read)
    return out















def old_make_gif(ims_list,fp,optimize=False,duration=40,loop=0,size = (255,255),**kwargs):
    """ims_list list of np array (w,h,c) or list of pil ims
    out filepath
    """
    if isinstance(ims_list[0],Image.Image):
        ims=ims_list
    elif isinstance(ims_list[0],np.ndarray):
        ims=[numpy_2_image(im,out="PIL", size = size) for im in ims_list]

    ims[0].save(fp,
               save_all=True, append_images=ims[1:],
                optimize=False, duration = duration, loop = loop,**kwargs)
