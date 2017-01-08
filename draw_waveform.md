http://www.supermegaultragroovy.com/2009/10/06/drawing-waveforms/

Three phases:

- acquisition
- reduction
- storage
- drawing


possible priorities:
- speed
- accuracy
- display quality


# Acquisition
- read files
- auxiliary thread; making application responsive

# Reduction

- sampling. Split up audio into "chunks" and map this chunk to a single value.

if display quality is important, there are several options of how:

- min/max pair
- maximum
- average
- "energy" ? --> not present in the source page, info got from V.H.





http://www.bbc.co.uk/rd/blog/2013/10/audio-waveforms

> The summary information is computed by finding the minimum and maximum sample
> amplitude values over groups of 256 input audio samples over the entire length
> of the audio file. To support zooming out to view long time durations (several hours),
> Audacity also computes summary information over groups of 65,536 input samples.


# Sample application

      https://github.com/bbc/audiowaveform

        --> C++ cmd-line application to generate waveforms

      https://github.com/bbc/waveform-data.js

        -->  JavaScript lib for zoomable, browsable and segmentable audio waveforms.

interesting cmdline arguments:

-zoom <zoom>			Zoom level (samples per pixel), default: 256.
				Not valid if --end or --pixels-per-second is also specified

--pixels-per-second <zoom>	Zoom level (pixels per second), default: 100. Not valid if
				--end or --zoom is also specified

--start <seconds>		Start time (seconds), default: 0
--end <seconds>			End time (seconds). Not valid if --zoom is also specified

--width <width>			Width of output image (pixels), default: 800
--height <height>		Height of output image (pixels), default: 250

--output-filename <filename>	Output waveform data (.dat or .json), audio (.wav), or PNG image
				(.png) file name


# Drawing

Chris F and Thomas dedicated a sprint to decide whether we would use HTML5 canvas, SVG or WebGL to display the audio waveforms.

Despite this, we favoured Canvas. We also felt Canvas would be more efficient at dealing with user interactions and synchronising them between the several views, especially overlapping segments and draggable offsets. Its ability to be updated using the browser requestAnimationFrame  API makes it a clear winner for our purpose.






