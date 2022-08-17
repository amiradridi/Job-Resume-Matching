__version__ = '0.13.1+cpu'
git_version = 'bddbd7e6d65ecacc2e40cf6c9e2059669b8dbd44'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
