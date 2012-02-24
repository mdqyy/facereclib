#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Manuel Guenther <Manuel.Guenther@idiap.ch>

import bob
import numpy

class LGBPHS:
  """Extractor for local Gabor binary pattern histogram sequences"""
  
  def __init__(self, setup):
    """Initializes the local Gabor binary pattern histogram sequence tool chain with the given file selector object"""
    # Initializes LBPHS processor
    self.m_lgbphs_extractor = bob.ip.LBPHSFeatures(
          setup.BLOCK_H, setup.BLOCK_W, setup.OVERLAP_H, setup.OVERLAP_W, 
          setup.RADIUS, setup.P_N, setup.CIRCULAR,
          setup.TO_AVERAGE, setup.ADD_AVERAGE_BIT, setup.UNIFORM, setup.ROT_INV
    )
    
    kwargs = {}
    if hasattr(setup, 'GABOR_DIRECTIONS'): kwargs['number_of_angles'] = setup.GABOR_DIRECTIONS
    if hasattr(setup, 'GABOR_SCALES'): kwargs['number_of_scales'] = setup.GABOR_SCALES
    if hasattr(setup, 'GABOR_SIGMA'): kwargs['sigma'] = setup.GABOR_SIGMA
    if hasattr(setup, 'GABOR_K_MAX'): kwargs['k_max'] = setup.GABOR_K_MAX
    if hasattr(setup, 'GABOR_K_FAC'): kwargs['k_fac'] = setup.GABOR_K_FAC
    
    self.m_gwt = bob.ip.GaborWaveletTransform(**kwargs)
    self.m_trafo_image = None
    self.m_abs_image = None
  
  def __call__(self, image):
    """Extracts the local Gabor binary pattern histogram sequence from the given image"""
    # perform GWT on image
    if self.m_trafo_image == None or self.m_trafo_image.shape[1:2] != image.shape:
      # create jet image
      self.m_trafo_image = self.m_gwt.trafo_image(image)
      self.m_abs_image = numpy.ndarray(image.shape, dtype=numpy.float)
      
    # convert image to complex
    image = image.astype(numpy.complex128)
    self.m_gwt(image, self.m_trafo_image)
    
    lgbphs_array = None
    # iterate through the layers of the trafo image
    for j in range(self.m_gwt.number_of_kernels):
      # compute absolute part of complex response
      bob.core.array.get_part(self.m_trafo_image[j,:,:], self.m_abs_image)
      # Computes LBP histograms
      lbphs_blocks = self.m_lgbphs_extractor(self.m_abs_image)
      
      # TODO: complete this!
      # Converts to Blitz++ array
      n_bins = self.m_lgbphs_extractor.NBins
      n_blocks = len(lbphs_blocks)
      start = j * n_bins * n_blocks

      if lgbphs_array == None:
        lgbphs_array = numpy.ndarray((n_blocks * n_bins * self.m_gwt.number_of_kernels,), 'float64')

      for bi in range(0,n_blocks):
        start2 = bi*n_bins + start
        for j in range(n_bins):
          lgbphs_array[start2 + j] = lbphs_blocks[bi][j]
          
    # return the concatenated list of all histograms
    return lgbphs_array

    
