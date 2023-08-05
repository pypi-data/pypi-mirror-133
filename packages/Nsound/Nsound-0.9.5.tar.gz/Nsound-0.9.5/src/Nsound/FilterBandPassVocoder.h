//-----------------------------------------------------------------------------
//
//  $Id: FilterBandPassVocoder.h 874 2014-09-08 02:21:29Z weegreenblobbie $
//
//  Nsound is a C++ library and Python module for audio synthesis featuring
//  dynamic digital filters. Nsound lets you easily shape waveforms and write
//  to disk or plot them. Nsound aims to be as powerful as Csound but easy to
//  use.
//
//  Copyright (c) 2009 - Present Nick Hilton
//
//  weegreenblobbie2_gmail_com (replace '_' with '@' and '.')
//
//  This Band Pass Filter is based on the band pass filter found in
//  Achim Settelmeier's vocoder implementation.
//
//  See http://www.sirlab.de/linux/descr_vocoder.html for more details.
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
#ifndef _NSOUND_FILTER_BAND_PASS_VOCODER_H_
#define _NSOUND_FILTER_BAND_PASS_VOCODER_H_

#include <Nsound/Filter.h>

#include <set>

namespace Nsound
{

class AudioStream;
class Buffer;

//-----------------------------------------------------------------------------
class FilterBandPassVocoder : public Filter
{
    public:

    FilterBandPassVocoder(
        const float64 & sample_rate,
        const float64 & frequency_low,
        const float64 & frequency_high);

    virtual ~FilterBandPassVocoder();

    AudioStream
    filter(const AudioStream & x);

    AudioStream
    filter(const AudioStream & x, const Buffer & frequencies);

    AudioStream
    filter(
        const AudioStream & x,
        const Buffer & low_frequencies,
        const Buffer & high_frequencies);

    Buffer
    filter(const Buffer & x);

    Buffer
    filter(const Buffer & x, const Buffer & frequencies);

    Buffer
    filter(
        const Buffer & x,
        const Buffer & frequencies_Hz_low,
        const Buffer & frequencies_Hz_high);

    virtual
    float64
    filter(const float64 & x);

    virtual
    float64
    filter(const float64 & x, const float64 & frequency_Hz);

    virtual
    float64
    filter(
        const float64 & x,
        const float64 & frequency_Hz_low,
        const float64 & frequency_Hz_high);

    void
    plot(boolean show_fc = true, boolean show_phase = false);

    //! Resets interal history buffer and sets the cut off frequency to the one
    //! used at declaration.
    void
    reset();

    protected:

    void
    makeKernel(const float64 & f_low, const float64 & f_high);

    float64 frequency_low_;
    float64 frequency_high_;
    float64 omega2_;
    float64 f_;
    float64 att_;
    float64 low1_;
    float64 low2_;
    float64 mid1_;
    float64 mid2_;
    float64 high1_;
    float64 high2_;

    private:

    FilterBandPassVocoder(const FilterBandPassVocoder & copy);

    FilterBandPassVocoder &
    operator=(const FilterBandPassVocoder & rhs);

}; // class FilterBandPassIIR

} // namespace Nsound

// :mode=c++: jEdit modeline
#endif
