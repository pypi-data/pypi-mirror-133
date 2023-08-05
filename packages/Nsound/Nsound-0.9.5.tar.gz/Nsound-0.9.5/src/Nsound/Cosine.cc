//-----------------------------------------------------------------------------
//
//  $Id: Cosine.cc 874 2014-09-08 02:21:29Z weegreenblobbie $
//
//  Copyright (c) 2009-Present Nick Hilton
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

#include <Nsound/Buffer.h>
#include <Nsound/Cosine.h>

#include <cmath>

using namespace Nsound;

//-----------------------------------------------------------------------------
Cosine::
Cosine(const float64 & sample_rate)
    : Generator(sample_rate)
{
    Buffer waveform = drawSine2(1.0, 1.0, 0.5);
    ctor(sample_rate, waveform);
}
