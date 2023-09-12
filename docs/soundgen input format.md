# soundgen formats (reading from text input, before there will be one program to generate sound and read files)
## alpha
format for alpha was just frequencies separated by space</br>

## beta
format for soundgen input is N of elements like : f"{volume frequency instrument automation}" with "\n" on end</br>
`volume` is int between 0 and 255</br>
`frequency` is frequency float</br>
`instrument` is value from 0 to 255</br>
`automation` is value from 0 to 255</br>
