#  pycrc -- flexible CRC calculation utility and C source file generator
# -*- coding: Latin-1 -*-

#  Copyright (c) 2006-2007  Thomas Pircher  <tehpeh@gmx.net>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.


"""
Option parsing library for pycrc.
use as follows:

   from crc_opt import Options

   opt = Options("0.6")
   opt.parse(sys.argv)

This file is part of pycrc.
"""

from optparse import OptionParser, Option, OptionValueError
from copy import copy
import string
import sys


# function check_hex
###############################################################################
def check_hex(option, opt, value):
    """
    Checks if a value is given in a decimal integer of hexadecimal reppresentation.
    Returns the converted value or rises an exception on error.
    """
    try:
        if value.lower().startswith("0x"):
            return string.atoi(value, 16)
        else:
            return string.atoi(value)
    except ValueError:
        raise OptionValueError("option %s: invalid integer or hexadecimal value: %r" % (opt, value))

# function check_bool
###############################################################################
def check_bool(option, opt, value):
    """
    Checks if a value is given as a boolean value (either 0 or 1 or "true" or "false")
    Returns the converted value or rises an exception on error.
    """
    if value.isdigit():
        return string.atoi(value, 10) != 0
    elif value.lower() == "false":
        return False
    elif value.lower() == "true":
        return True
    else:
        raise OptionValueError("option %s: invalid boolean value: %r" % (opt, value))


# Class MyOption
###############################################################################
class MyOption(Option):
    """
    New option parsing class extends the Option class
    """
    TYPES = Option.TYPES + ("hex", "bool")
    TYPE_CHECKER = copy(Option.TYPE_CHECKER)
    TYPE_CHECKER["hex"] = check_hex
    TYPE_CHECKER["bool"] = check_bool


# function model_cb
###############################################################################
def model_cb(option, opt_str, value, parser):
    """
    This function sets up the single parameters if the 'model' option has been selected
    by the user.
    """
    mod = value.lower();
    if   mod == "crc-8":
        setattr(parser.values, "width",         8)
        setattr(parser.values, "poly",          0x07L)
        setattr(parser.values, "reflect_in",    False)
        setattr(parser.values, "xor_in",        0x0L)
        setattr(parser.values, "reflect_out",   False)
        setattr(parser.values, "xor_out",       0x0L)
    elif mod == "crc-16":
        setattr(parser.values, "width",         16)
        setattr(parser.values, "poly",          0x8005L)
        setattr(parser.values, "reflect_in",    True)
        setattr(parser.values, "xor_in",        0x0L)
        setattr(parser.values, "reflect_out",   True)
        setattr(parser.values, "xor_out",       0x0L)
    elif mod == "ccitt":
        setattr(parser.values, "width",         16)
        setattr(parser.values, "poly",          0x1021L)
        setattr(parser.values, "reflect_in",    False)
        setattr(parser.values, "xor_in",        0xffffL)
        setattr(parser.values, "reflect_out",   False)
        setattr(parser.values, "xor_out",       0x0L)
    elif mod == "kermit":
        setattr(parser.values, "width",         16)
        setattr(parser.values, "poly",          0x1021L)
        setattr(parser.values, "reflect_in",    True)
        setattr(parser.values, "xor_in",        0x0L)
        setattr(parser.values, "reflect_out",   True)
        setattr(parser.values, "xor_out",       0x0L)
    elif mod == "x-25":
        setattr(parser.values, "width",         16)
        setattr(parser.values, "poly",          0x1021L)
        setattr(parser.values, "reflect_in",    True)
        setattr(parser.values, "xor_in",        0xffffL)
        setattr(parser.values, "reflect_out",   True)
        setattr(parser.values, "xor_out",       0xffffL)
    elif mod == "xmodem":
        setattr(parser.values, "width",         16)
        setattr(parser.values, "poly",          0x8408L)
        setattr(parser.values, "reflect_in",    True)
        setattr(parser.values, "xor_in",        0x0L)
        setattr(parser.values, "reflect_out",   True)
        setattr(parser.values, "xor_out",       0x0L)
    elif mod == "zmodem":
        setattr(parser.values, "width",         16)
        setattr(parser.values, "poly",          0x1021L)
        setattr(parser.values, "reflect_in",    False)
        setattr(parser.values, "xor_in",        0x0L)
        setattr(parser.values, "reflect_out",   False)
        setattr(parser.values, "xor_out",       0x0L)
    elif mod == "crc-32":
        setattr(parser.values, "width",         32)
        setattr(parser.values, "poly",          0x4c11db7L)
        setattr(parser.values, "reflect_in",    True)
        setattr(parser.values, "xor_in",        0xffffffffL)
        setattr(parser.values, "reflect_out",   True)
        setattr(parser.values, "xor_out",       0xffffffffL)
    elif mod == "crc-32c":
        setattr(parser.values, "width",         32)
        setattr(parser.values, "poly",          0x1edc6f41L)
        setattr(parser.values, "reflect_in",    True)
        setattr(parser.values, "xor_in",        0xffffffffL)
        setattr(parser.values, "reflect_out",   True)
        setattr(parser.values, "xor_out",       0xffffffffL)
    elif mod == "posix":
        setattr(parser.values, "width",         32)
        setattr(parser.values, "poly",          0x4c11db7L)
        setattr(parser.values, "reflect_in",    False)
        setattr(parser.values, "xor_in",        0x0L)
        setattr(parser.values, "reflect_out",   False)
        setattr(parser.values, "xor_out",       0xffffffffL)
    elif mod == "jam":
        setattr(parser.values, "width",         32)
        setattr(parser.values, "poly",          0x4c11db7L)
        setattr(parser.values, "reflect_in",    True)
        setattr(parser.values, "xor_in",        0xffffffffL)
        setattr(parser.values, "reflect_out",   True)
        setattr(parser.values, "xor_out",       0x0L)
    elif mod == "xfer":
        setattr(parser.values, "width",         32)
        setattr(parser.values, "poly",          0x000000afL)
        setattr(parser.values, "reflect_in",    False)
        setattr(parser.values, "xor_in",        0x0L)
        setattr(parser.values, "reflect_out",   False)
        setattr(parser.values, "xor_out",       0x0L)
    else:
        raise OptionValueError("Error: unsupported model %s" % (value))
        sys.exit(1)

# Class Options
###############################################################################
class Options(object):
    """
    The options parsing and validationg class
    """

    """
    Bitmap of the algorithms
    """
    Algo_Bit_by_Bit         = 0x01
    Algo_Bit_by_Bit_Fast    = 0x02
    Algo_Table_Driven       = 0x04

    # Class constructor
    ###############################################################################
    def __init__(self, version):
        self.ProgramName    = "pycrc"
        self.Version        = version
        self.VersionStr     = "%s v%s" % (self.ProgramName, self.Version)
        self.WebAddress     = "http://www.tty1.net/pycrc/"
        self.Width          = None
        self.Poly           = None
        self.ReflectIn      = None
        self.XorIn          = None
        self.ReflectOut     = None
        self.XorOut         = None
        self.TableIdxWidth  = 8
        self.TableWidth     = 1 << self.TableIdxWidth
        self.Verbose        = False
        self.CheckString    = "123456789"

        self.Algorithm      = 0x00
        self.SymbolPrefix   = "crc_"
        self.OutputFile     = None
        self.Action         = "check_string"
        self.CStd           = None

    # function parse
    ###############################################################################
    def parse(self, argv = None):
        """
        Parses and validates the options given as arguments
        """
        usage = """\
%prog [OPTIONS]

To generate the checksum of a string:
    %prog [model] --check-string "123456789"

To generate the checksum of a file:
    %prog [model] --check-file filename

To generate the c-source and write it to filename:
    %prog [model] --generate c -o filename

The model can be defined by the --model switch or by specifying each of the
following parameters:
    --width --poly --reflect-in --xor-in --reflect-out --xor-out"""

        parser = OptionParser(option_class=MyOption, usage=usage, version=self.VersionStr)
        parser.add_option("-v", "--verbose",
                        action="store_true", dest="verbose", default=False,
                        help="print information about the model")
        parser.add_option("--check-string",
                        action="store", type="string", dest="check_string",
                        help="calculate the checksum of the given string ('123456789' default)", metavar="STRING")
        parser.add_option("--check-file",
                        action="store", type="string", dest="check_file",
                        help="calculate the checksum of the given file", metavar="FILE")
        parser.add_option("--generate",
                        action="store", type="string", dest="generate", default=None,
                        help="choose which type of code to generate from {c, h, c-main, table}", metavar="CODE")
        parser.add_option("--std",
                        action="store", type="string", dest="c_std", default="C99",
                        help="C standard style of the generated code from {C89, ANSI, C99}", metavar="STD")
        parser.add_option("--algorithm",
                        action="store", type="string", dest="algorithm", default="all",
                        help="choose an algorithm from {bit-by-bit, bit-by-bit-fast, table-driven, all}", metavar="ALGO")
        parser.add_option("--model",
                        action="callback", callback=model_cb, type="string", dest="model", default=None,
                        help="choose a parameter set from {crc-8, crc-16, ccitt, kermit, x-25, xmodem, zmodem, crc-32, crc-32c, posix, jam, xfer}", metavar="MODEL")
        parser.add_option("--width",
                        action="store", type="hex", dest="width",
                        help="use WIDTH bits in the polynom", metavar="WIDTH")
        parser.add_option("--poly",
                        action="store", type="hex", dest="poly",
                        help="use HEX as Polynom", metavar="HEX")
        parser.add_option("--reflect-in",
                        action="store", type="bool", dest="reflect_in",
                        help="reflect input bytes", metavar="BOOL")
        parser.add_option("--xor-in",
                        action="store", type="hex", dest="xor_in",
                        help="use HEX as initial value", metavar="HEX")
        parser.add_option("--reflect-out",
                        action="store", type="bool", dest="reflect_out",
                        help="reflect output bytes", metavar="BOOL")
        parser.add_option("--xor-out",
                        action="store", type="hex", dest="xor_out",
                        help="xor the final crc value with HEX", metavar="HEX")
        parser.add_option("--table-idx-width",
                        action="store", type="int", dest="table_idx_width",
                        help="use WIDTH bits to index the crc table; WIDTH one of {1, 2, 4, 8}", metavar="WIDTH")
        parser.add_option("--symbol-prefix",
                        action="store", type="string", dest="symbol_prefix",
                        help="when generating source code, use STRING as prefix to the generated symbols", metavar="STRING")
        parser.add_option("-o", "--output",
                        action="store", type="string", dest="output_file",
                        help="write the generated code to file instead to stdout", metavar="FILE")

        (options, args) = parser.parse_args()

        undefined_params = []
        if options.width != None:
            self.Width          = options.width
        else:
            undefined_params.append("--width")
        if options.poly != None:
            self.Poly           = options.poly
        else:
            undefined_params.append("--poly")
        if options.reflect_in != None:
            self.ReflectIn      = options.reflect_in
        else:
            undefined_params.append("--reflect-in")
        if options.xor_in != None:
            self.XorIn          = options.xor_in
        else:
            undefined_params.append("--xor-in")
        if options.reflect_out != None:
            self.ReflectOut     = options.reflect_out
        else:
            undefined_params.append("--reflect-out")
        if options.xor_out != None:
            self.XorOut         = options.xor_out
        else:
            undefined_params.append("--xor-out")
        if options.table_idx_width != None:
            if options.table_idx_width == 1 or \
                    options.table_idx_width == 2 or \
                    options.table_idx_width == 4 or \
                    options.table_idx_width == 8:
                self.TableIdxWidth = options.table_idx_width
                self.TableWidth = 1 << options.table_idx_width
            else:
                sys.stderr.write("Error: unsupported table-idx-width %d\n" % options.table_idx_width)
                sys.exit(1)

        if self.Width != None:
            if self.Width <= 0:
                sys.stderr.write("Error: Width must be strictly positive\n")
                sys.exit(1)
            self.MSB_Mask = 0x1 << (self.Width - 1)
            self.Mask = ((self.MSB_Mask - 1) << 1) | 1
            if self.Poly != None:
                self.Poly = self.Poly & self.Mask
            if self.XorIn != None:
                self.XorIn = self.XorIn & self.Mask
            if self.XorOut != None:
                self.XorOut = self.XorOut & self.Mask
        else:
            self.MSB_Mask = None
            self.Mask = None

        if self.Width           == None or \
                self.Poly       == None or \
                self.ReflectIn  == None or \
                self.XorIn      == None or \
                self.ReflectOut == None or \
                self.XorOut     == None:
            self.UndefinedCrcParameters = True
        else:
            self.UndefinedCrcParameters = False

        if options.algorithm != None:
            alg = options.algorithm.lower()
            if alg == "bit-by-bit" or alg == "all":
                self.Algorithm      |= self.Algo_Bit_by_Bit
            if alg == "bit-by-bit-fast"  or alg == "all":
                self.Algorithm      |= self.Algo_Bit_by_Bit_Fast
            if alg == "table-driven" or alg == "all":
                self.Algorithm      |= self.Algo_Table_Driven
            if self.Algorithm == 0:
                sys.stderr.write("Error: unknown algorithm %s\n" % options.algorithm)
                sys.exit(1)
        if self.Width != None and (self.Width % 8) != 0:
            if options.algorithm == "bit-by-bit-fast" or options.algorithm == "table-driven":
                sys.stderr.write("Error: width non aligned to byte boundaries, algorithm %s not applicable\n" % options.algorithm)
                sys.exit(1)
            else:
                self.Algorithm &= ~(self.Algo_Bit_by_Bit_Fast | self.Algo_Table_Driven)
        if self.Width != None and self.Width < 8:
            if options.algorithm == "table-driven":
                sys.stderr.write("Error: width < 8, algorithm %s not applicable\n" % options.algorithm)
                sys.exit(1)
            else:
                self.Algorithm &= ~(self.Algo_Table_Driven)

        if options.c_std != None:
            std = options.c_std.upper()
            if std == "ANSI" or std == "C89":
                self.CStd = "C89"
            elif std == "C99":
                self.CStd = std
            else:
                sys.stderr.write("Error: unknown C standard %s\n" % options.c_std)
                sys.exit(1)
        if options.symbol_prefix != None:
            self.SymbolPrefix = options.symbol_prefix
        if options.output_file != None:
            self.OutputFile = options.output_file
        op_count = 0
        if options.check_string != None:
            self.Action         = "check_string"
            self.CheckString    = options.check_string
            op_count += 1
        if options.check_file != None:
            self.Action         = "check_file"
            self.CheckFile      = options.check_file
            op_count += 1
        if options.generate != None:
            arg = options.generate.lower()
            if arg != 'c' and arg != 'h' and arg != "c-main" and arg != "table":
                sys.stderr.write("Error: unknown operation %s\n" % options.generate)
                sys.exit(1)
            self.Action = "generate_" + arg
            op_count += 1
            if self.Action == "generate_table":
                if self.Algorithm & self.Algo_Table_Driven == 0:
                    sys.stderr.write("Error: the --generate table option is incompatible with the --algorithm option\n")
                    sys.exit(1)
                self.Algorithm = self.Algo_Table_Driven
            elif self.Algorithm != self.Algo_Bit_by_Bit and self.Algorithm != self.Algo_Bit_by_Bit_Fast and self.Algorithm != self.Algo_Table_Driven:
                sys.stderr.write("Error: select an algorithm to be used in the generated file\n")
                sys.exit(1)
        if op_count == 0:
            self.Action         = "check_string"
        if op_count > 1:
            sys.stderr.write("Error: too many actions scecified\n")
            sys.exit(1)

        if self.UndefinedCrcParameters and (self.Action == "check_string" or self.Action == "check_file" or self.Action == "generate_table"):
            sys.stderr.write("Error: undefined parameters: Add %s or use --model\n" % ", ".join(undefined_params))
            sys.exit(1)
        self.Verbose            = options.verbose
