//  Copyright (C) 2006-2007  Thomas Pircher
//
//  This program is free software; you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation; either version 2 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License along
//  with this program; if not, write to the Free Software Foundation, Inc.,
//  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

#include "crc.h"
#include <unistd.h>
#include <getopt.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>
#include <string.h>

static bool atob(const char *str);
static int atox(const char *str);
static int get_config(int argc, char *argv[], crc_cfg_t *cfg);


static bool verbose = false;
static unsigned char str[256] = "123456789";

bool atob(const char *str)
{
    if (!str) {
        return 0;
    }
    if (isdigit(str[0])) {
        return (bool)atoi(str);
    }
    if (tolower(str[0]) == 't') {
        return true;
    }
    return false;
}

int atox(const char *str)
{
    int ret = 0;

    if (!str) {
        return 0;
    }
    if (str[0] == '0' && tolower(str[1]) == 'x') {
        str += 2;
        while (*str) {
            if (isdigit(*str))
                ret = 16 * ret + *str - '0';
            else if (isxdigit(*str))
                ret = 16 * ret + tolower(*str) - 'a' + 10;
            else
                return ret;
            str++;
        }
    } else if (isdigit(*str)) {
        while (*str) {
            if (isdigit(*str))
                ret = 10 * ret + *str - '0';
            else
                return ret;
            str++;
        }
    }
    return ret;
}


int get_config(int argc, char *argv[], crc_cfg_t *cfg)
{
    int c;
    int this_option_optind;
    int option_index;
    static struct option long_options[] = {
        {"width",           1, 0, 'w'},
        {"poly",            1, 0, 'p'},
        {"reflect_in",      1, 0, 'n'},
        {"xor_in",          1, 0, 'i'},
        {"reflect_out",     1, 0, 'u'},
        {"xor_out",         1, 0, 'o'},
        {"verbose",         0, 0, 'v'},
        {"check_string",    1, 0, 's'},
        {"table_idx_with",  1, 0, 't'},
        {0, 0, 0, 0}
    };

    while (1) {
        this_option_optind = optind ? optind : 1;
        option_index = 0;

        c = getopt_long (argc, argv, "w:p:ni:uo:v", long_options, &option_index);
        if (c == -1)
            break;

        switch (c) {
            case 0:
                printf ("option %s", long_options[option_index].name);
                if (optarg)
                    printf (" with arg %s", optarg);
                printf ("\n");
            case 'w':
                cfg->width = atoi(optarg);
                break;
            case 'p':
                cfg->poly = atox(optarg);
                break;
            case 'n':
                cfg->reflect_in = atob(optarg);
                break;
            case 'i':
                cfg->xor_in = atox(optarg);
                break;
            case 'u':
                cfg->reflect_out = atob(optarg);
                break;
            case 'o':
                cfg->xor_out = atox(optarg);
                break;
            case 's':
                memcpy(str, optarg, strlen(optarg) < sizeof(str) ? strlen(optarg) + 1 : sizeof(str));
                str[sizeof(str) - 1] = '\0';
                break;
            case 'v':
                verbose = true;
                break;
            case 't':
                // ignore --table_idx_with option
                break;
            case '?':
                return -1;
            case ':':
                fprintf(stderr, "missing argument to option %c\n", c);
                return -1;
            default:
                fprintf(stderr, "unhandled option %c\n", c);
                return -1;
        }
    }
    cfg->msb_mask = 1 << (cfg->width - 1);
    cfg->crc_mask = (cfg->msb_mask - 1) | cfg->msb_mask;

    cfg->poly           &= cfg->crc_mask;
    cfg->xor_in         &= cfg->crc_mask;
    cfg->xor_out        &= cfg->crc_mask;
    return 0;
}


int main(int argc, char *argv[])
{
    crc_cfg_t cfg = {
        0,      // width
        0,      // poly
        0,      // xor_in
        0,      // reflect_in
        0,      // xor_out
        0,      // reflect_out

        0,      // crc_mask
        0,      // msb_mask
    };
    crc_t crc;
    char format[20];
    int ret;

    ret = get_config(argc, argv, &cfg);
    if (ret == 0) {
#       ifdef CRC_ALGO_TABLE_DRIVEN
        crc_table_gen(&cfg);
#       endif       // CRC_ALGO_TABLE_DRIVEN
        crc = crc_init(&cfg);
        crc = crc_update(&cfg, crc, str, strlen((char *)str));
        crc = crc_finalize(&cfg, crc);

        if (verbose) {
            snprintf(format, sizeof(format), "%%-16s = 0x%%0%dx\n", (unsigned int)(cfg.width + 3) / 4);
            printf("%-16s = %d\n", "width", (unsigned int)cfg.width);
            printf(format, "poly", (unsigned int)cfg.poly);
            printf("%-16s = %s\n", "reflect_in", cfg.reflect_in ? "true": "false");
            printf(format, "xor_in", cfg.xor_in);
            printf("%-16s = %s\n", "reflect_out", cfg.reflect_out ? "true": "false");
            printf(format, "xor_out", (unsigned int)cfg.xor_out);
            printf(format, "crc_mask", (unsigned int)cfg.crc_mask);
            printf(format, "msb_mask", (unsigned int)cfg.msb_mask);
        }
        printf("0x%lx\n", (long)crc);
    }
    return !ret;
}