//-----------------------------------------------------------------------------
//
//  $Id: FilterHighPassIIR.cc 874 2014-09-08 02:21:29Z weegreenblobbie $
//
//  Copyright (c) 2007 Nick Hilton
//
//  weegreenblobbie2_gmail_com (replace '_' with '@' and '.')
//
//-----------------------------------------------------------------------------

//-----------------------------------------------------------------------------
//
//  This program is free software; you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation; either version 2 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU Library General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program; if not, write to the Free Software
//  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
//
//-----------------------------------------------------------------------------

#include <Nsound/AudioStream.h>
#include <Nsound/Buffer.h>
#include <Nsound/FilterHighPassIIR.h>
#include <Nsound/Plotter.h>

#include <cmath>
#include <cstdio>
#include <iostream>

using namespace Nsound;

//-----------------------------------------------------------------------------
FilterHighPassIIR::
FilterHighPassIIR(
    const float64 & sample_rate,
    uint32 n_poles,
    const float64 & frequency,
    const float64 & percent_ripple)
    :
    FilterStageIIR(
        FilterStageIIR::HIGH_PASS,
        sample_rate,
        n_poles,
        frequency,
        percent_ripple)
{
    frequency_ = frequency;
    kernel_size_ = n_poles;
}

AudioStream
FilterHighPassIIR::
filter(const AudioStream & x)
{
    return Filter::filter(x);
}

AudioStream
FilterHighPassIIR::
filter(const AudioStream & x, const float64 & f)
{
    return FilterStageIIR::filter(x, f);
}

AudioStream
FilterHighPassIIR::
filter(const AudioStream & x, const Buffer & frequencies)
{
    return Filter::filter(x, frequencies);
}

//-----------------------------------------------------------------------------v
Buffer
FilterHighPassIIR::
filter(const Buffer & x)
{
    return Filter::filter(x);
}

Buffer
FilterHighPassIIR::
filter(const Buffer & x, const float64 & f)
{
    return FilterStageIIR::filter(x, f);
}

Buffer
FilterHighPassIIR::
filter(const Buffer & x, const Buffer & frequencies)
{
    return Filter::filter(x, frequencies);
}

float64
FilterHighPassIIR::
filter(const float64 & x)
{
    return FilterStageIIR::filter(x);
}

float64
FilterHighPassIIR::
filter(const float64 & x, const float64 & frequency)
{
    return FilterStageIIR::filter(x, frequency);
}

void
FilterHighPassIIR::
makeKernel(const float64 & frequency)
{
    FilterStageIIR::makeKernel(frequency);
}

void
FilterHighPassIIR::
plot(boolean show_fc, boolean show_phase)
{
    char title[128];
    sprintf(title,
        "High Pass IIR Frequency Response\n"
        "order = %d, fc = %0.1f Hz, sr = %0.1f Hz",
        n_poles_ - 1, frequency_, sample_rate_);

    Filter::plot(show_phase);

    Plotter pylab;

    uint32 n_rows = 1;

    if(show_phase)
    {
        n_rows = 2;
    }

    if(show_fc)
    {
        pylab.subplot(n_rows, 1, 1);

        pylab.axvline(frequency_,"color='red'");

        pylab.title(title);
    }

}


void
FilterHighPassIIR::
reset()
{
    FilterStageIIR::reset();
}


