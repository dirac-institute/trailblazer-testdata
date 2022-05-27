"""
Utilities used to crop, update the center and dimensions of fits files in order
to reduce their size.

Utility will, by default, replace files in-place.
"""


import os
import argparse

import astropy.io.fits as fits


def crop_and_shift(hdu, centerpix, crop=200):
    endSize = int(crop*2)
    cr1, cr2 = centerpix
    hdu.data = hdu.data[cr1-crop:cr1+crop, cr2-crop:cr2+crop]
    hdu.header["NAXIS1"] = endSize
    hdu.header["NAXIS2"] = endSize
    return hdu


def reduce_lbt(hdulist):
    for i in range(1, 5):
        x, y = hdulist[i].header["NAXIS1"], hdulist[i].header["NAXIS2"]
        hdulist[i] = crop_and_shift(hdulist[i], (int(x/2), int(y/2)), crop = 100)
    return hdulist

def reduce_moa(hdulist):
    primary = hdulist[0]
    cr1, cr2 = int(primary.header["NAXIS1"]/2), int(primary.header["NAXIS2"]/2)
    return crop_and_shift(primary, (cr1, cr2))


def reduce_lcogt(hdulist):
    primary = hdulist[0]
    cr1, cr2 = primary.header["CRPIX1"], primary.header["CRPIX2"]
    return crop_and_shift(primary, (cr1, cr2))


def reduce_sdss(hdulist):
    primary = hdulist[0]
    cr1, cr2 = int(primary.header["CRPIX1"]), int(primary.header["CRPIX2"])
    return crop_and_shift(primary, (cr1, cr2))


def reduce_rubin_decam(hdulist):
    # we have an old version of a file, but it's the only one with lines in it
    # and this is a problem because we can't actually do it with vanilla astropy
    #    https://github.com/astropy/astropy/issues/10554
    # # Fix requires editing io/fits/hdu/compressed.py
    # l. 1666 and removing ZQUANTIZ flag from header by, for example:
    #     if self._header.get("ZQUANTIZ", False) == "NONE":
    #         del self._header["ZQUANTIZ"]
    # otherwise it will fail with an RuntimeError in the compression C code
    for i in range(1, 4):
        cr1, cr2 = int(hdulist[i].header["CRPIX1"]), int(hdulist[i].header["CRPIX2"])
        hdulist[i] = crop_and_shift(hdulist[i], (cr1, cr2))

    return hdulist


def reduce_hsc(hdulist):
    primary = hdulist[0]
    primary.data = primary.data[1700:2100, 0:400]
    primary.header["CRPIX2"] -= 1700
    primary.header["NAXIS1"] = 400
    primary.header["NAXIS2"] = 400

    return hdulist


def reduce_community_decam(hdulist):
    for ext in hdulist[1:]:
        # crpix in deca
        # cr1, cr2 = int(ext.header["CRPIX1"]), int(ext.header["CRPIX2"])
        cr1, cr2 = int(ext.header["NAXIS1"]/2), int(ext.header["NAXIS2"]/2)
        ext.header["CRPIX1"] = ext.header["CRPIX1"] - (cr1-50)
        ext.header["CRPIX2"] = ext.header["CRPIX2"] - (cr2-50)
        # for some reason we are not allowed to touch NAXIS here
        # ext.header["NAXIS1"] = 400
        # ext.header["NAXIS2"] = 400
        ext.data = ext.data[cr1-50:cr1+50, cr2-50:cr2+50]

    return hdulist




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utility for cropping and reframing of fits files.")
    parser.add_argument("-i", "--input", nargs="?",  default="../static/upload/fits/",
                        help=("Directory containing unresized fits files. Default: ../static/upload/fits/"))
    parser.add_argument("-o", "--output", nargs="?",  default="../static/upload/fits/",
                        help=("Output directory. Default: ../static/upload/fits/"))
    args = parser.parse_args()

    if os.path.exists(args.input) and os.path.isdir(args.input):
        datadir = os.path.abspath(args.input)
    else:
        raise ValueError("Input location is not a directory or doesn't exist!")

    outdir = os.path.abspath(args.output)
    if not os.path.exists(args.output):
        os.mkdir(args.output)

    files = os.listdir(datadir)
    for f in files:
        if "fits" in f:
            try:
                fullpath = os.path.join(datadir, f)
                hdulist = fits.open(fullpath)
                if f.startswith("frame"):
                    hdulist = reduce_sdss(hdulist)
                elif f.startswith("bi"):
                    hdulist = reduce_lcogt(hdulist)
                elif ("obstel" in hdulist[0].header) and \
                     ("moa" in hdulist[0].header["OBSTEL"].lower()):
                    hdulist = reduce_moa(hdulist)
                elif f.startswith("calexp"): # this might need updating later
                    hdulist = reduce_rubin_decam(hdulist)
                elif f.startswith("HSC"):
                    hdulist = reduce_hsc(hdulist)
                elif f.startswith("c4d"):
                    hdulist = reduce_community_decam(hdulist)
                elif f.startswith("lbcb") or f.startswith("lbcr"):
                    hdulist = reduce_lbt(hdulist)
                else:
                    pass
                hdulist.writeto(os.path.join(outdir, f), overwrite=True)
            except Exception as e:
                print(f"Could not process {f}:\n{e}\n\n")
