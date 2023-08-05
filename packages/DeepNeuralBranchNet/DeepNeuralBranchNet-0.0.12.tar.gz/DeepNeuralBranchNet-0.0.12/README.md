# Neural network with branching output
This package can be used to train neural network for classification with option of multiple outputs by branching at different layers. 


__Features available__
- Customizable layers with option of selecting activation function
- No limits on adding number of layers and number of neurons in each layers
- By default gradient descent for optimization but in further version, other optimization methods are to be included
- Multiple outputs can be selected at different layers with just one method call

## Requirements
This package is developed at very low-level python coding so there is no much requirement other than numpy library.
[Numpy](https://numpy.org/)



## Installation
To install a stable version, use the following command

```
pip install DeepNeuralBranchNet
```


## Example of how to use

Import module 
```
from DeepNeuralBranchNet import neuralnet
```
Initiate the neural network object class

```
example=NeuralNet()
```
Add input by passing number of nput features as parameter
```
example.add_input(input_length=16)
```

Add layer sequentially by passing number of neurons and activation function
```
example.add_layer(10,activation_function="relu")
```
If you want to add multiple output(or opting for branching), then trigger branching by following line of code and then keep adding layers
```
example.do_branching()
```

Run model to update parameters such as weights and bias and for training.
- input_array : Input matrix in the form of array
- output_array : Output matrix in the form of array
- number_of_iterations : Total number of times you want to run back propagations to update weights
- multiple_output : If you have branches then set it to True
```
example.run_model(input_array,output_array, number_of_iterations=1000, learning_rate=0.001, multiple_output=False)
```
Finally predict by calling predict method
```
example.predict()
```
