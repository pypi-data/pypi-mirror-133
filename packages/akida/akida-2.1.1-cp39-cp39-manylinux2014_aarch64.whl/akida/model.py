from copy import copy
import functools
import numpy as np

from .core import ModelBase, Layer, LayerType
from .statistics import Statistics
from .input_data import InputData


# Private utility functions
def _copy_layer_variables(layer, copied_layer):
    for var in copied_layer.get_variable_names():
        layer.set_variable(var, copied_layer.get_variable(var))


def _copy_layer(model, layer):
    new_layer = Layer(layer.parameters, layer.name)
    inbounds = []
    # For each original inbound layer
    for inbound in layer.inbounds:
        # Get the corresponding layer copied in the new model
        new_inbound = model.get_layer(inbound.name)
        if new_inbound is None:
            if layer.parameters.layer_type == LayerType.Concat:
                raise ValueError(
                    f"Missing {layer.name} inbound layer {inbound.name}")
            # Use the last layer of the target model
            new_inbound = model.layers[-1]
        inbounds.append(new_inbound)
    model.add(new_layer, inbounds)
    if layer.learning:
        # Recompile model with layer parameters
        learn_params = {
            attr: getattr(layer.learning, attr)
            for attr in dir(layer.learning)
            if '__' not in attr and 'learning_type' not in attr
        }
        model.compile(**learn_params)
    _copy_layer_variables(new_layer, layer)


def _inference(method):
    """Decorator to wrap inference methods
    """

    @functools.wraps(method)
    def fetch_events(self, *args, **kwargs):
        # Call decorated method
        res = method(self, *args, **kwargs)
        hw_device = self.hw_device
        if hw_device:
            # Model is mapped to a HardwareDevice
            soc = hw_device.soc
            if soc and soc.power_measurement_enabled:
                # The device collects power events: fetch them
                self.power_events = soc.power_meter.events()
        return res

    return fetch_events


class Model(ModelBase):
    """An Akida neural ``Model``, represented as a hierarchy of layers.

    The ``Model`` class is the main interface to Akida and allows:

    - to create an empty ``Model`` to which you can add layers programmatically
      using the sequential API,
    - to reload a full ``Model`` from a serialized file or a memory buffer,
    - to create a new ``Model`` from a list of layers taken from an existing
      ``Model``.

    It provides methods to instantiate, train, test and save models.

    Args:
        filename (str, optional): path to the serialized Model.
            If None, an empty sequential model will be created, or filled
            with the layers in the layers parameter.
        serialized_buffer (bytes, optional): binary buffer containing a
            serialized Model.
        layers (:obj:`list`, optional): list of layers that will be copied
            to the new model. If the list does not start with an input layer,
            it will be added automatically.

    """

    def __init__(self, filename=None, layers=None):
        try:
            if (filename is not None) and (layers is not None):
                raise ValueError("filename and layer list should not be passed"
                                 " at the same time")
            if filename is not None:
                ModelBase.__init__(self, filename)
            else:
                ModelBase.__init__(self)
                if layers is not None:
                    if not isinstance(layers, list):
                        raise ValueError("layers should be a list of layers")
                    if any(not isinstance(l, Layer) for l in layers):
                        raise ValueError("layers should only contain a list of"
                                         " layers")
                    input_layer_types = (LayerType.InputConvolutional,
                                         LayerType.InputData)
                    ltype = layers[0].parameters.layer_type
                    # Add an InputData layer
                    if ltype not in input_layer_types:
                        input_dims = layers[0].input_dims
                        input_data = InputData(input_dims,
                                               input_bits=layers[0].input_bits)
                        self.add(input_data)
                    for layer in layers:
                        _copy_layer(self, layer)
            self.power_events = []
        except:
            self = None
            raise

    def __str__(self):
        data = "akida.Model, layer_count=" + str(self.get_layer_count())
        data += ", sequence_count=" + str(len(self.sequences))
        out_dims = self.output_shape if self.get_layer_count() else []
        data += ", output_shape=" + str(out_dims)
        return data

    def __repr__(self):
        out_dims = self.output_shape if self.get_layer_count() else []
        data = "<akida.Model, layer_count=" + str(self.get_layer_count())
        data += ", output_shape=" + str(out_dims)
        data += ", sequences=" + repr(self.sequences) + ">"
        return data

    @property
    def statistics(self):
        """Get statistics by sequence for this model.

        Returns:
            a dictionary of obj:`SequenceStatistics` indexed by name.

        """
        return Statistics(self)

    @_inference
    def predict(self, inputs, num_classes=None, batch_size=None):
        """Returns the model class predictions.

        Forwards an input tensor (images or events) through the model
        and compute predictions based on the neuron id.
        If the number of output neurons is greater than the number of classes,
        the neurons are automatically assigned to a class by dividing their id
        by the number of classes.

        The expected input tensor dimensions are:

        - n, representing the number of frames or samples,
        - w, representing the width,
        - h, representing the height,
        - c, representing the channel, or more generally the feature.

        If the inputs are events, the input shape must be (n, w, h, c), but if
        the inputs are images their shape must be (n, h, w, c).

        Note: only grayscale (c=1) or RGB (c=3) images (arrays) are supported.

        Note that the predictions are based on the activation values of the last
        layer: for most use cases, you may want to disable activations for that
        layer (ie setting ``activation=False``) to get a better
        accuracy.

        Args:
            inputs (:obj:`numpy.ndarray`): a numpy.ndarray
            num_classes (int, optional): optional parameter (defaults to the
                number of neurons in the last layer).
            batch_size (int, optional): maximum number of inputs that should be
                processed at a time

        Returns:
            :obj:`numpy.ndarray`: an array of shape (n).

        Raises:
            TypeError: if the input is not a numpy.ndarray.

        """
        if num_classes is None:
            num_classes = self.output_shape[2]
        return super().predict(inputs, num_classes,
                               0 if batch_size is None else batch_size)

    @_inference
    def fit(self, inputs, input_labels=None, batch_size=None):
        """Trains a set of images or events through the model.

        Trains the model with the specified input tensor (numpy array).

        The expected input tensor dimensions are:

        - n, representing the number of frames or samples,
        - w, representing the width,
        - h, representing the height,
        - c, representing the channel, or more generally the feature.

        If the inputs are events, the input shape must be (n, w, h, c), but if
        the inputs are images, their shape must be (n, h, w, c).

        Note: only grayscale (c=1) or RGB (c=3) images (arrays) are supported.

        If activations are enabled for the last layer, the output is an uint8
        tensor.

        If activations are disabled for the last layer, the output is an int32
        tensor.

        Args:
            inputs (:obj:`numpy.ndarray`): a numpy.ndarray
            input_labels (list(int), optional): input labels.
                Must have one label per input, or a single label for all inputs.
                If a label exceeds the defined number of classes, the input will
                be discarded. (Default value = None).
            batch_size (int, optional): maximum number of inputs that should be
                processed at a time

        Returns:
            a numpy array of shape (n, out_w, out_h, out_c).

        Raises:
            TypeError: if the input is not a numpy.ndarray.
            ValueError: if the input doesn't match the required shape,
                format, etc.

        """
        if input_labels is None:
            input_labels = []
        elif isinstance(input_labels, (int, np.integer)):
            input_labels = [input_labels]
        elif isinstance(input_labels, (list, np.ndarray)):
            if any(not isinstance(x, (int, np.integer)) for x in input_labels):
                raise TypeError("fit expects integer as labels")
        outputs = super().fit(inputs, input_labels,
                              0 if batch_size is None else batch_size)
        return outputs

    @_inference
    def forward(self, inputs, batch_size=None):
        """Forwards a set of images or events through the model.

        Forwards an input tensor through the model and returns an output tensor.

        The expected input tensor dimensions are:

        - n, representing the number of frames or samples,
        - w, representing the width,
        - h, representing the height,
        - c, representing the channel, or more generally the feature.

        If the inputs are events, the input shape must be (n, w, h, c), but if
        the inputs are images, their shape must be (n, h, w, c).

        Note: only grayscale (c=1) or RGB (c=3) images (arrays) are supported.

        If activations are enabled for the last layer, the output is an uint8
        tensor.

        If activations are disabled for the last layer, the output is an int32
        tensor.

        Args:
            inputs (:obj:`numpy.ndarray`): a numpy.ndarray
            batch_size (int, optional): maximum number of inputs that should be
                processed at a time

        Returns:
            a numpy array of shape (n, out_w, out_h, out_c).

        Raises:
            TypeError: if the input is not a numpy.ndarray.
            ValueError: if the inputs doesn't match the required shape,
                format, etc.

        """
        outputs = super().forward(inputs,
                                  0 if batch_size is None else batch_size)
        return outputs

    def evaluate(self, inputs, batch_size=None):
        """Evaluates a set of images or events through the model.

        Forwards an input tensor through the model and returns a float array.

        It applies ONLY to models without an activation on the last layer.
        The output values are obtained from the model discrete potentials by
        applying a shift and a scale.

        The expected input tensor dimensions are:

        - n, representing the number of frames or samples,
        - w, representing the width,
        - h, representing the height,
        - c, representing the channel, or more generally the feature.

        If the inputs are events, the input shape must be (n, w, h, c), but if
        the inputs are images (numpy array), their shape must be (n, h, w, c).

        Note: only grayscale (c=1) or RGB (c=3) images (arrays) are supported.

        Args:
            inputs (:obj:`numpy.ndarray`): a (n, w, h, c) numpy.ndarray
            batch_size (int, optional): maximum number of inputs that should be
                processed at a time

        Returns:
           :obj:`numpy.ndarray`: a float array of shape (n, w, h, c).

        Raises:
            TypeError: if the input is not a numpy.ndarray.
            RuntimeError: if the model last layer has an activation.
            ValueError: if the input doesn't match the required shape,
                format, or if the model only has an InputData layer.

        """
        outputs = super().evaluate(inputs,
                                   0 if batch_size is None else batch_size)
        return outputs

    def summary(self):
        """Prints a string summary of the model.

        This method prints a summary of the model with details for every layer,
        grouped by sequences:

        - name and type in the first column
        - output shape
        - kernel shape

        If there is any layer with unsupervised learning enabled, it will list
        them, with these details:

        - name of layer
        - number of incoming connections
        - number of weights per neuron

        """

        def _model_summary(model):
            # prepare headers
            headers = ['Input shape', 'Output shape', 'Sequences', 'Layers']
            # prepare an empty table
            table = [headers]
            row = [
                str(model.input_shape),
                str(model.output_shape),
                str(len(model.sequences)),
                str(len(model.layers))
            ]
            table.append(row)
            print_table(table, "Model Summary")

        def _layers_summary(sequence):
            # Prepare headers
            headers = ['Layer (type)', 'Output shape', 'Kernel shape']
            program = sequence.program
            if program is not None:
                headers.append('NPs')
            # prepare an empty table
            table = [headers]
            for p in sequence.passes:
                for l in p.layers:
                    nps = None if l.mapping is None else l.mapping.nps
                    # layer name (type)
                    layer_type = l.parameters.layer_type
                    # kernel shape
                    if "weights" in l.get_variable_names():
                        kernel_shape = l.get_variable("weights").shape
                    else:
                        kernel_shape = "N/A"
                    # Prepare row and add it
                    row = [str(l), str(l.output_dims), str(kernel_shape)]
                    if nps is not None:
                        if layer_type == LayerType.InputConvolutional:
                            row.append('N/A')
                        else:
                            row.append(len(nps))
                    table.append(row)
                    if layer_type == LayerType.SeparableConvolutional:
                        # Add pointwise weights on a second line
                        kernel_pw_shape = l.get_variable("weights_pw").shape
                        row = ['', '', kernel_pw_shape]
                        if nps is not None:
                            row.append('')
                        table.append(row)
            # Get backend info
            backend = str(sequence.backend).split('.')[-1]
            title = sequence.name + " (" + backend + ")"
            if program is not None:
                title += " - size: " + str(len(program)) + " bytes"
            print_table(table, title)

        def _learning_summary(layer):
            if not layer.learning:
                return
            # Prepare headers
            headers = ["Learning Layer", "# Input Conn.", "# Weights"]
            table = [headers]
            name = layer.name
            # Input connections is the product of input dims
            input_connections = np.prod(layer.input_dims)
            # Num non zero weights per neuron (counted on first neuron)
            weights = layer.get_variable("weights")
            incoming_conn = np.count_nonzero(weights[:, :, :, 0])
            # Prepare row and add it
            row = [name, str(input_connections), incoming_conn]
            table.append(row)
            print()
            print_table(table, "Learning Summary")

        # Print first the general Model summary
        _model_summary(self)
        for sequence in iter(self.sequences):
            print()
            # Print sequence summary
            _layers_summary(sequence)
        # Print learning summary if we have more than one input layer
        if len(self.layers) > 1:
            # Only the last layer of a model can learn
            _learning_summary(self.layers[-1])
        print()

    def add_classes(self, num_add_classes):
        """Adds classes to the last layer of the model.

        A model with a compiled last layer is ready to learn using the Akida
        built-in learning algorithm. This function allows to add new classes
        (i.e. new neurons) to the last layer, keeping the previously learned
        neurons.

        Args:
            num_add_classes (int): number of classes to add to the last layer

        Raises:
            RuntimeError: if the last layer is not compiled
        """
        # Get current layer's parameters and variables
        layer = self.get_layer(self.get_layer_count() - 1)
        params = copy(layer.parameters)
        if params.layer_type != LayerType.FullyConnected:
            raise TypeError(
                "Add classes can only be used on a FullyConnected layer.")

        units = params.units
        learn_params = {
            attr: getattr(layer.learning, attr)
            for attr in dir(layer.learning)
            if not '__' in attr and not 'learning_type' in attr
        }
        if not learn_params:
            raise RuntimeError("'add_classes' function must be called when "
                               "the last layer of the model is compiled.")
        num_nrns_per_class = units // learn_params['num_classes']
        var_names = layer.get_variable_names()
        variables = {var: layer.get_variable(var) for var in var_names}

        # Update parameters for new future layer
        learn_params['num_classes'] += num_add_classes
        params.units = learn_params['num_classes'] * num_nrns_per_class

        # Replace last layer with new one
        self.pop_layer()
        new_layer = Layer(params, layer.name)
        self.add(new_layer)
        self.compile(**learn_params)

        # Fill variables with previous values
        for var in var_names:
            new_var = new_layer.get_variable(var)
            new_var[..., :units] = variables[var]
            new_layer.set_variable(var, new_var)


def print_table(table, title):
    # Convert to np.array
    to_str = np.vectorize(str, otypes=['O'])
    table = to_str(table)
    # get column lengths
    str_len_f = np.vectorize(lambda cell: len(str(cell)))
    str_lens = np.amax(str_len_f(table), 0)
    line_len = np.sum(str_lens)
    # Prepare format rows
    size_formats = np.vectorize(lambda cell: f"{{:{cell}.{cell}}}")
    format_strings = size_formats(str_lens)
    format_row = "  ".join(format_strings)
    # Generate separators
    separator_len = line_len + 2 * len(table[0])
    separator = "_" * separator_len
    double_separator = "=" * separator_len

    # Print header
    center_format = f"{{:^{separator_len}}}"
    print(center_format.format(title))
    print(separator)
    print(format_row.format(*table[0]))
    print(double_separator)
    # Print body
    for row in table[1:, :]:
        print(format_row.format(*row))
        print(separator)
