## Synthetic Population Spatial Sampler

  - Run a population synthesizer as usual
  - Specify a sample rate for each zone
  - Assign HHs into bins by income, size, workers by zone
  - Sample HHs by bin to match zone level sample rates
  - Set the expansion weight of each record
  - Run travel model as usual
  - Average trip matrices before assignment

  - For example: 
    - Oversample study area zones @ 400%
      - Replicate a synthetic household four times
      - Set the weight to 0.25
    - Undersample zones outside study area @ 25%
      - Select 1 in 4 synthetic households 
      - Set the weight to 4

## Example

``test\test_popsampler.py``

## See Also

https://github.com/RSGInc/populationsim

