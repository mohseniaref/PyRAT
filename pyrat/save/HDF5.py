import pyrat
import h5py


class HDF5(pyrat.Worker):

    gui = {'menu': 'File|Export to', 'entry': 'HDF5 file'}
    para = [{'var': 'filename', 'value': '', 'type': 'savefile', 'text': 'Save as HDF5'}]

    def __init__(self, *args, **kwargs):
        super(HDF5, self).__init__(*args, **kwargs)
        self.name = "HDF5 EXPORT"
        self.nthreads = 1

    def run(self, *args, **kwargs):
        if isinstance(self.layer, list):
            layers = self.layer
        else:
            layers = [self.layer]

        self.file = h5py.File(self.filename, 'w')
        for k, layer in enumerate(layers):
            query = pyrat.data.queryLayer(layer)
            self.dset = self.file.create_dataset("D"+str(k+1), query['shape'], dtype=query['dtype'])
            self.layer_extract(self.block_writer, silent=False, layer=layer, **kwargs)
            meta = pyrat.data.getAnnotation(layer=layer)
            for key, val in meta.items():
                self.dset.attrs[key] = val
        self.file.close()
        return True

    def block_writer(self, array, **kwargs):
        self.dset[..., kwargs['block'][0]+kwargs['valid'][0]:kwargs['block'][0]+kwargs['valid'][1], :]\
                = array[..., kwargs['valid'][0]:kwargs['valid'][1], :]
        return True


def hdf5(*args, **kwargs):
    return HDF5(*args, **kwargs).run(**kwargs)
