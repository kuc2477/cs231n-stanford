import itertools
import numpy as np


def affine_forward(x, w, b):
  """
  Computes the forward pass for an affine (fully-connected) layer.

  The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
  examples, where each example x[i] has shape (d_1, ..., d_k). We will
  reshape each input into a vector of dimension D = d_1 * ... * d_k, and
  then transform it to an output vector of dimension M.

  Inputs:
  - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
  - w: A numpy array of weights, of shape (D, M)
  - b: A numpy array of biases, of shape (M,)
  
  Returns a tuple of:
  - out: output, of shape (N, M)
  - cache: (x, w, b)
  """
  out = None
  #############################################################################
  # TODO: Implement the affine forward pass. Store the result in out. You     #
  # will need to reshape the input into rows.                                 #
  #############################################################################
  N = x.shape[0]
  reshaped = x.reshape(N, np.prod(x.shape[1:]))
  out = reshaped.dot(w) + b
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b)
  return out, cache


def affine_backward(dout, cache):
  """
  Computes the backward pass for an affine layer.

  Inputs:
  - dout: Upstream derivative, of shape (N, M)
  - cache: Tuple of:
    - x: Input data, of shape (N, d_1, ... d_k)
    - w: Weights, of shape (D, M)

  Returns a tuple of:
  - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
  - dw: Gradient with respect to w, of shape (D, M)
  - db: Gradient with respect to b, of shape (M,)
  """
  x, w, b = cache
  dx, dw, db = None, None, None
  ############################################################################# 
  # TODO: Implement the affine backward pass.                                 #
  #############################################################################
  N = x.shape[0]
  reshaped = x.reshape(N, np.prod(x.shape[1:]))

  dx = dout.dot(w.T).reshape(x.shape)
  dw = reshaped.T.dot(dout)
  db = np.sum(dout, axis=0)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def relu_forward(x):
  """
  Computes the forward pass for a layer of rectified linear units (ReLUs).

  Input:
  - x: Inputs, of any shape

  Returns a tuple of:
  - out: Output, of the same shape as x
  - cache: x
  """
  out = None
  #############################################################################
  # TODO: Implement the ReLU forward pass.                                    #
  #############################################################################
  out = np.maximum(x, 0)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = x
  return out, cache


def relu_backward(dout, cache):
  """
  Computes the backward pass for a layer of rectified linear units (ReLUs).

  Input:
  - dout: Upstream derivatives, of any shape
  - cache: Input x, of same shape as dout

  Returns:
  - dx: Gradient with respect to x
  """
  dx, x = None, cache
  #############################################################################
  # TODO: Implement the ReLU backward pass.                                   #
  #############################################################################
  dx = dout
  dx[x <= 0] = 0
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def batchnorm_forward(x, gamma, beta, bn_param):
  """
  Forward pass for batch normalization.
  
  During training the sample mean and (uncorrected) sample variance are
  computed from minibatch statistics and used to normalize the incoming data.
  During training we also keep an exponentially decaying running mean of the mean
  and variance of each feature, and these averages are used to normalize data
  at test-time.

  At each timestep we update the running averages for mean and variance using
  an exponential decay based on the momentum parameter:

  running_mean = momentum * running_mean + (1 - momentum) * sample_mean
  running_var = momentum * running_var + (1 - momentum) * sample_var

  Note that the batch normalization paper suggests a different test-time
  behavior: they compute sample mean and variance for each feature using a
  large number of training images rather than using a running average. For
  this implementation we have chosen to use running averages instead since
  they do not require an additional estimation step; the torch7 implementation
  of batch normalization also uses running averages.

  Input:
  - x: Data of shape (N, D)
  - gamma: Scale parameter of shape (D,)
  - beta: Shift paremeter of shape (D,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features

  Returns a tuple of:
  - out: of shape (N, D)
  - cache: A tuple of values needed in the backward pass
  """
  mode = bn_param['mode']
  eps = bn_param.get('eps', 1e-5)
  momentum = bn_param.get('momentum', 0.9)

  N, D = x.shape
  running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
  running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

  out, cache = None, None
  if mode == 'train':
    #############################################################################
    # TODO: Implement the training-time forward pass for batch normalization.   #
    # Use minibatch statistics to compute the mean and variance, use these      #
    # statistics to normalize the incoming data, and scale and shift the        #
    # normalized data using gamma and beta.                                     #
    #                                                                           #
    # You should store the output in the variable out. Any intermediates that   #
    # you need for the backward pass should be stored in the cache variable.    #
    #                                                                           #
    # You should also use your computed sample mean and variance together with  #
    # the momentum variable to update the running mean and running variance,    #
    # storing your result in the running_mean and running_var variables.        #
    #############################################################################
    # compute sample mean and variance
    sample_mean = np.mean(x, axis=0)
    sample_var = np.var(x, axis=0)

    # compute running mean and variance
    running_mean = momentum * running_mean + (1 - momentum) * sample_mean
    running_var = momentum * running_var + (1 - momentum) * sample_var

    # 1. normalize the data with the sample mean and variance 
    a = x
    b = sample_mean
    c = sample_var + eps
    xhat = (a - b) / np.sqrt(c)

    # 2. scale & shift the normalized data 
    out = gamma * xhat + beta

    # set intermediate statistics on the cache
    cache = (gamma, beta, eps, x, xhat, a, b, c, )
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  elif mode == 'test':
    #############################################################################
    # TODO: Implement the test-time forward pass for batch normalization. Use   #
    # the running mean and variance to normalize the incoming data, then scale  #
    # and shift the normalized data using gamma and beta. Store the result in   #
    # the out variable.                                                         #
    #############################################################################

    # 1. normalize the data with the running mean and variance calculated in
    #    the traning phase.
    xhat = (x - running_mean) / np.sqrt(running_var + eps)

    # 2. scale & shift the normalized data with the gamma and beta learned in
    #    the traning phase.
    out = gamma * xhat + beta

    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  else:
    raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

  # Store the updated running means back into bn_param
  bn_param['running_mean'] = running_mean
  bn_param['running_var'] = running_var

  return out, cache


def batchnorm_backward(dout, cache):
  """
  Backward pass for batch normalization.
  
  For this implementation, you should write out a computation graph for
  batch normalization on paper and propagate gradients backward through
  intermediate nodes.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, D)
  - cache: Variable of intermediates from batchnorm_forward.
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs x, of shape (N, D)
  - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
  - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
  """
  dx, dgamma, dbeta = None, None, None

  # get intermediate statistics from the cache
  gamma, beta, eps, x, xhat, a, b, c = cache

  # get shape of the input data x
  N, D = x.shape

  #############################################################################
  # TODO: Implement the backward pass for batch normalization. Store the      #
  # results in the dx, dgamma, and dbeta variables.                           #
  #############################################################################

  # (N, D), (D,), (D,)
  dout_dxhat = dout * gamma
  dout_dgamma = xhat
  dout_dbeta = 1.

  # (N, D), (D,), (D,)
  dout_da = dout_dxhat / np.sqrt(c)
  dout_db = np.sum(-dout_dxhat / np.sqrt(c), axis=0)
  dout_dc = np.sum(-dout_dxhat * 0.5 * (a - b) * (c ** -1.5), axis=0)

  # (N, D), (N, D), (N, D), (D,)
  da_dx = 1.
  db_dx = 1. / N
  dc_dx = (2. / N) * (x - b)
  dc_db = np.sum((-2. / N) * (x - b), axis=0)

  # (D,), (N, D)
  dout_db += dout_dc * dc_db
  dout_dx = dout_da * da_dx + dout_db * db_dx + dout_dc * dc_dx

  # (N, D), (D,), (D,)
  dx = dout_dx
  dgamma = np.sum(dout * dout_dgamma, axis=0)
  dbeta = np.sum(dout * dout_dbeta, axis=0)

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return dx, dgamma, dbeta


def batchnorm_backward_alt(dout, cache):
  """
  Alternative backward pass for batch normalization.
  
  For this implementation you should work out the derivatives for the batch
  normalizaton backward pass on paper and simplify as much as possible. You
  should be able to derive a simple expression for the backward pass.
  
  Note: This implementation should expect to receive the same cache variable
  as batchnorm_backward, but might not use all of the values in the cache.
  
  Inputs / outputs: Same as batchnorm_backward
  """
  # get intermediate statistics from the cache
  gamma, beta, eps, x, xhat, a, b, c = cache

  # get shape of the input data x
  N, D = x.shape

  dx, dgamma, dbeta = None, None, None

  #############################################################################
  # TODO: Implement the backward pass for batch normalization. Store the      #
  # results in the dx, dgamma, and dbeta variables.                           #
  #                                                                           #
  # After computing the gradient with respect to the centered inputs, you     #
  # should be able to compute gradients with respect to the inputs in a       #
  # single statement; our implementation fits on a single 80-character line.  #
  #############################################################################
  dgamma = np.sum(dout * xhat, axis=0)
  dbeta = np.sum(dout, axis=0)
  dx = (1. / N) \
      * gamma \
      * (1 / np.sqrt(c)) \
      * (N * dout - np.sum(dout, axis=0) - 
         ((x - b) * np.sum(dout * (x - b), axis=0)) / c)

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  
  return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
  """
  Performs the forward pass for (inverted) dropout.

  Inputs:
  - x: Input data, of any shape
  - dropout_param: A dictionary with the following keys:
    - p: Dropout parameter. We drop each neuron output with probability p.
    - mode: 'test' or 'train'. If the mode is train, then perform dropout;
      if the mode is test, then just return the input.
    - seed: Seed for the random number generator. Passing seed makes this
      function deterministic, which is needed for gradient checking but not in
      real networks.

  Outputs:
  - out: Array of the same shape as x.
  - cache: A tuple (dropout_param, mask). In training mode, mask is the dropout
    mask that was used to multiply the input; in test mode, mask is None.
  """
  p, mode = dropout_param['p'], dropout_param['mode']
  if 'seed' in dropout_param:
    np.random.seed(dropout_param['seed'])

  mask = None
  out = None

  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase forward pass for inverted dropout.   #
    # Store the dropout mask in the mask variable.                            #
    ###########################################################################
    mask = (np.random.rand(*x.shape) < p) / p
    out = x * mask
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    ###########################################################################
    # TODO: Implement the test phase forward pass for inverted dropout.       #
    ###########################################################################
    mask = None
    out = x
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

  cache = (dropout_param, mask)
  out = out.astype(x.dtype, copy=False)

  return out, cache


def dropout_backward(dout, cache):
  """
  Perform the backward pass for (inverted) dropout.

  Inputs:
  - dout: Upstream derivatives, of any shape
  - cache: (dropout_param, mask) from dropout_forward.
  """
  dropout_param, mask = cache
  mode = dropout_param['mode']
  
  dx = None
  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase backward pass for inverted dropout.  #
    ###########################################################################
    dx = dout * mask
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    dx = dout
  return dx


def conv_forward_naive(x, w, b, conv_param):
  """
  A naive implementation of the forward pass for a convolutional layer.

  The input consists of N data points, each with C channels, height H and width
  W. We convolve each input with F different filters, where each filter spans
  all C channels and has height HH and width HH.

  Input:
  - x: Input data of shape (N, C, H, W)
  - w: Filter weights of shape (F, C, HH, WW)
  - b: Biases, of shape (F,)
  - conv_param: A dictionary with the following keys:
    - 'stride': The number of pixels between adjacent receptive fields in the
      horizontal and vertical directions.
    - 'pad': The number of pixels that will be used to zero-pad the input.

  Returns a tuple of:
  - out: Output data, of shape (N, F, H', W') where H' and W' are given by
    H' = 1 + (H + 2 * pad - HH) / stride
    W' = 1 + (W + 2 * pad - WW) / stride
  - cache: (x, w, b, conv_param)
  """

  S = conv_param['stride']
  P = conv_param['pad']

  N, C, H, W = x.shape
  F, C, HH, WW = w.shape

  HOUT = 1 + (H + 2 * P - HH) / S
  WOUT = 1 + (W + 2 * P - WW) / S
  out = np.zeros((N, F, HOUT, WOUT))

  #############################################################################
  # TODO: Implement the convolutional forward pass.                           #
  # Hint: you can use the function np.pad for padding.                        #
  #############################################################################
  for i, j, f, n in itertools.product(
          xrange(HOUT), xrange(WOUT), 
          xrange(F), xrange(N)):
      # zero-pad the training instance
      x_padded = np.zeros((C, H + 2 * P, W + 2 * P))
      x_padded[:, P:-P, P:-P] = x[n]

      # resolve local connectivity's boundaries
      h_start = i * S
      h_end = h_start + HH
      w_start = j * S
      w_end = w_start + WW

      # process dot product with neuron on resolved local connectivity
      local = x_padded[:, h_start:h_end, w_start:w_end]
      out[n, f, i, j] = np.sum(local * w[f]) + b[f]

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b, conv_param)
  return out, cache


def conv_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a convolutional layer.

  Inputs:
  - dout: Upstream derivatives.
  - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

  Returns a tuple of:
  - dx: Gradient with respect to x
  - dw: Gradient with respect to w
  - db: Gradient with respect to b
  """
  # unpack the cache
  x, w, b, conv_param = cache

  # set aliases for spatial hyperparameters and shapes
  S = conv_param['stride']
  P = conv_param['pad']
  N, C, H, W = x.shape
  F, C, HH, WW = w.shape
  HOUT = 1 + (H + 2 * P - HH) / S
  WOUT = 1 + (W + 2 * P - WW) / S

  # set shape of gradients for each parameters
  dx, dw, db = None, None, None
  dx = np.zeros(x.shape)
  dw = np.zeros(w.shape)
  db = np.zeros(b.shape)

  #############################################################################
  # TODO: Implement the convolutional backward pass.                          #
  #############################################################################
  for n in xrange(N):
      # zero-pad the training instance
      x_padded = np.zeros((C, H + 2 * P, W + 2 * P))
      x_padded[:, P:-P, P:-P] = x[n]

      # set gradient for x_padded
      dx_padded = np.zeros(x_padded.shape)

      for i, j, f in itertools.product(xrange(HOUT), xrange(WOUT), xrange(F)):
          # resolve local connectivity's boundaries
          h_start = i * S
          h_end = h_start + HH
          w_start = j * S
          w_end = w_start + WW

          # process dot product with neuron on resolved local connectivity
          local = x_padded[:, h_start:h_end, w_start:w_end]

          # backprop gradients on dout
          dout_dlocal = w[f]
          dout_dw = local
          dout_db = 1
          
          # backprop gradients on dlocal
          dlocal_dx_padded = np.zeros(x_padded.shape)
          dlocal_dx_padded[:, h_start:h_end, w_start:w_end] = 1

          # backprop gradients on dw, db and dx_padded
          dw[f] += dout[n, f, i, j] * dout_dw
          db[f] += dout[n, f, i, j] * dout_db
          dx_padded[:, h_start:h_end, w_start:w_end] += \
              dout[n, f, i, j] \
              * dout_dlocal \
              * dlocal_dx_padded[:, h_start:h_end, w_start:w_end]

      # derivate dx from dx_padded
      dx[n] = dx_padded[:, P:-P, P:-P]
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def max_pool_forward_naive(x, pool_param):
  """
  A naive implementation of the forward pass for a max pooling layer.

  Inputs:
  - x: Input data, of shape (N, C, H, W)
  - pool_param: dictionary with the following keys:
    - 'pool_height': The height of each pooling region
    - 'pool_width': The width of each pooling region
    - 'stride': The distance between adjacent pooling regions

  Returns a tuple of:
  - out: Output data
  - cache: (x, pool_param)
  """
  N, C, H, W = x.shape
  HH = pool_param['pool_height']
  WW = pool_param['pool_width']
  S = pool_param['stride']

  HOUT = 1 + (H - HH) / S
  WOUT = 1 + (W - WW) / S
  out = np.zeros((N, C, HOUT, WOUT))

  #############################################################################
  # TODO: Implement the max pooling forward pass                              #
  #############################################################################
  for i, j in itertools.product(xrange(HOUT), xrange(WOUT)):
      h_start = i * S
      h_end = h_start + HH
      w_start = j * S
      w_end = w_start + WW

      pools = x[:, :, h_start:h_end, w_start:w_end]
      out[:, :, i, j] = np.max(pools, axis=(2, 3))
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, pool_param)
  return out, cache


def max_pool_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a max pooling layer.

  Inputs:
  - dout: Upstream derivatives
  - cache: A tuple of (x, pool_param) as in the forward pass.

  Returns:
  - dx: Gradient with respect to x
  """
  x, pool_param = cache

  N, C, H, W = x.shape
  HH = pool_param['pool_height']
  WW = pool_param['pool_width']
  S = pool_param['stride']

  HOUT = 1 + (H - HH) / S
  WOUT = 1 + (W - WW) / S

  dx = np.zeros(x.shape)

  #############################################################################
  # TODO: Implement the max pooling backward pass                             #
  #############################################################################
  for n, c, i, j in itertools.product(
          xrange(N), xrange(C), 
          xrange(HOUT), xrange(WOUT)):
      h_start = i * S
      h_end = h_start + HH
      w_start = j * S
      w_end = w_start + WW

      pool = x[n, c, h_start:h_end, w_start:w_end]
      mask = pool == np.max(pool)

      dx[n, c, h_start:h_end, w_start:w_end] = \
          dout[n, c, i, j] * mask / np.sum(mask) 
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def spatial_batchnorm_forward(x, gamma, beta, bn_param):
  """
  Computes the forward pass for spatial batch normalization.
  
  Inputs:
  - x: Input data of shape (N, C, H, W)
  - gamma: Scale parameter, of shape (C,)
  - beta: Shift parameter, of shape (C,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance. momentum=0 means that
      old information is discarded completely at every time step, while
      momentum=1 means that new information is never incorporated. The
      default of momentum=0.9 should work well in most situations.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features
    
  Returns a tuple of:
  - out: Output data, of shape (N, C, H, W)
  - cache: Values needed for the backward pass
  """
  out, cache = None, None

  N, C, H, W = x.shape

  #############################################################################
  # TODO: Implement the forward pass for spatial batch normalization.         #
  #                                                                           #
  # HINT: You can implement spatial batch normalization using the vanilla     #
  # version of batch normalization defined above. Your implementation should  #
  # be very short; ours is less than five lines.                              #
  #############################################################################
  reshaped = x.reshape(N * H * W, C)
  out, cache = batchnorm_forward(reshaped, gamma, beta, bn_param)
  out = out.reshape(N, C, H, W)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return out, cache


def spatial_batchnorm_backward(dout, cache):
  """
  Computes the backward pass for spatial batch normalization.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, C, H, W)
  - cache: Values from the forward pass
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs, of shape (N, C, H, W)
  - dgamma: Gradient with respect to scale parameter, of shape (C,)
  - dbeta: Gradient with respect to shift parameter, of shape (C,)
  """
  dx, dgamma, dbeta = None, None, None
  N, C, H, W = dout.shape

  #############################################################################
  # TODO: Implement the backward pass for spatial batch normalization.        #
  #                                                                           #
  # HINT: You can implement spatial batch normalization using the vanilla     #
  # version of batch normalization defined above. Your implementation should  #
  # be very short; ours is less than five lines.                              #
  #############################################################################
  dout_reshaped = dout.reshape(N * H * W, C)
  dx, dgamma, dbeta = batchnorm_backward(dout_reshaped, cache)
  dx = dx.reshape(N, C, H, W)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return dx, dgamma, dbeta
  

def svm_loss(x, y):
  """
  Computes the loss and gradient using for multiclass SVM classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  N = x.shape[0]
  correct_class_scores = x[np.arange(N), y]
  margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
  margins[np.arange(N), y] = 0
  loss = np.sum(margins) / N
  num_pos = np.sum(margins > 0, axis=1)
  dx = np.zeros_like(x)
  dx[margins > 0] = 1
  dx[np.arange(N), y] -= num_pos
  dx /= N
  return loss, dx


def softmax_loss(x, y):
  """
  Computes the loss and gradient for softmax classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  probs = np.exp(x - np.max(x, axis=1, keepdims=True))
  probs /= np.sum(probs, axis=1, keepdims=True)
  N = x.shape[0]
  loss = -np.sum(np.log(probs[np.arange(N), y])) / N
  dx = probs.copy()
  dx[np.arange(N), y] -= 1
  dx /= N
  return loss, dx
