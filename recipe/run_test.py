import numpy as np
import time
import os
import glob

from obspy import Trace, Stream


def test_multi_channel_xcorr():
    from eqcorrscan.utils.correlate import get_stream_xcorr

    chans = ['EHZ', 'EHN', 'EHE']
    stas = ['COVA', 'FOZ', 'LARB', 'GOVA', 'MTFO', 'MTBA']
    n_templates = 20
    stream_len = 10000
    template_len = 200
    templates = []
    stream = Stream()
    for station in stas:
        for channel in chans:
            stream += Trace(data=np.random.randn(stream_len))
            stream[-1].stats.channel = channel
            stream[-1].stats.station = station
    for i in range(n_templates):
        template = Stream()
        for station in stas:
            for channel in chans:
                template += Trace(data=np.random.randn(template_len))
                template[-1].stats.channel = channel
                template[-1].stats.station = station
        templates.append(template)
    print("Running time serial")
    tic = time.time()
    multichannel_normxcorr = get_stream_xcorr(
        "time_domain", concurrency=None)
    cccsums_t_s, no_chans, chans = multichannel_normxcorr(
        templates=templates, stream=stream)
    toc = time.time()
    print('Time-domain in serial took: %f seconds' % (toc-tic))
    print("Running time parallel")
    tic = time.time()
    multichannel_normxcorr = get_stream_xcorr(
        "time_domain", concurrency="multiprocess")
    cccsums_t_p, no_chans, chans = multichannel_normxcorr(
        templates=templates, stream=stream, cores=4)
    toc = time.time()
    print('Time-domain in parallel took: %f seconds' % (toc-tic))
    print("Running frequency serial")
    tic = time.time()
    multichannel_normxcorr = get_stream_xcorr(
        "fftw", concurrency=None)
    cccsums_f_s, no_chans, chans = multichannel_normxcorr(
        templates=templates, stream=stream)
    toc = time.time()
    print('Frequency-domain in serial took: %f seconds' % (toc-tic))
    print("Running frequency parallel")
    tic = time.time()
    multichannel_normxcorr = get_stream_xcorr(
        "fftw", concurrency="multiprocess")
    cccsums_f_p, no_chans, chans = multichannel_normxcorr(
        templates=templates, stream=stream, cores=4)
    toc = time.time()
    print('Frequency-domain in parallel took: %f seconds' % (toc-tic))
    print("Running frequency openmp parallel")
    tic = time.time()
    multichannel_normxcorr = get_stream_xcorr(
        "fftw", concurrency="concurrent")
    cccsums_f_op, no_chans, chans = multichannel_normxcorr(
        templates=templates, stream=stream, cores=4)
    toc = time.time()
    print('Frequency-domain in parallel took: %f seconds' % (toc-tic))
    print("Running frequency openmp parallel outer")
    tic = time.time()
    multichannel_normxcorr = get_stream_xcorr(
        "fftw", concurrency="concurrent")
    cccsums_f_outer_op, no_chans, chans = multichannel_normxcorr(
        templates=templates, stream=stream, cores=1, cores_outer=4)
    toc = time.time()
    print('Frequency-domain in parallel took: %f seconds' % (toc-tic))
    print("Finished")
    assert(np.allclose(cccsums_t_s, cccsums_t_p, atol=0.00001))
    assert(np.allclose(cccsums_f_s, cccsums_f_p, atol=0.00001))
    assert(np.allclose(cccsums_f_s, cccsums_f_op, atol=0.00001))
    assert(np.allclose(cccsums_f_s, cccsums_f_outer_op, atol=0.00001))
    assert(np.allclose(cccsums_t_p, cccsums_f_s, atol=0.001))


def check_c_locations():
    from eqcorrscan.utils import libnames

    libdir = os.path.join(os.path.dirname(libnames.__file__), 'lib')
    lib_files = glob.glob(os.path.join(libdir, "*"))
    print(f"Found the following files in the Library: {lib_files}")

    libname = libnames._get_lib_name("libutils")
    libpath = os.path.join(libdir, libname)
    static_fftw = os.path.join(libdir, 'libfftw3-3.dll')
    static_fftwf = os.path.join(libdir, 'libfftw3f-3.dll')
    print(f"Expected libutils here: {libpath}")
    print(f"Expected static fftw here: {static_fftw}")
    print(f"Expected static fftwf here: {static_fftwf}")


if __name__ == '__main__':
    """
    Run core tests
    """
    check_c_locations()
    test_multi_channel_xcorr()
