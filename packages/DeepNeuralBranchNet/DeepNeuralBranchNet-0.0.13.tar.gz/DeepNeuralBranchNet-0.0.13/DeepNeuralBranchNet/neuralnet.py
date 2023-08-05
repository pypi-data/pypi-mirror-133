import numpy as np
import math
class NeuralNet:
    def __init__(self,layer=None,activation=None,list_of_parameters=None,input_features=None,model_layers=None, cost_f=None,param_f=None,input=None,output=None):
        self.layer=[]
        self.list_of_parameters={}
        self.input_features=None
        self.activation=[]
        self.model_layers=[]
        self.cost_f=None
        self.param_f=None
        self.input=input
        self.output=output

    count=1
    def add_input(self,input_length):
        if len(self.layer) ==0:
            self.layer.append(input_length)
        else:
            self.layer=[input_length]+self.layer
            
    def add_layer(self,number_of_neurons,activation_function="relu"):
        self.layer.append(number_of_neurons)
        self.activation.append(activation_function)
        return self.layer


    def paramter_initialize(self,factor=0.1):

        for i in range(len(self.layer)):
            if(i != (len(self.layer)-1)):
                print(self.layer[i+1])
                print(len(self.layer))
                self.list_of_parameters['w'+str(i+1)]=np.random.randn(self.layer[i+1],self.layer[i])*factor
                self.list_of_parameters['b' + str(i+1)] = np.random.randn(self.layer[i + 1], self.layer[i]) * factor
            else:
                break
        return self.list_of_parameters

    def paramter_initialize_multiple(self,layer,factor=0.1):
        list_of_parameters=[]
        for i in range(len(layer)):
            if(i != (len(layer)-1)):
                print(layer[i+1])
                print(len(layer))
                list_of_parameters['w'+str(i+1)]=np.random.randn(layer[i+1],layer[i])*factor
                list_of_parameters['b' + str(i+1)] = np.random.randn(layer[i + 1], layer[i]) * factor
            else:
                break
        return list_of_parameters
    def forward_function(self,previous_layer_activation,weight,bias):
        z_func=np.dot(previous_layer_activation,weight)+bias
        temp=(previous_layer_activation,weight,bias)
        return z_func,temp
    def relu(self,x):
        return x*(x > 0)
    def sig(self,x):
        return (1 / (1 + math.exp(-x)))
    def linear_forward_one_step(self,previous_layer_activation,weight,bias,activation):
        if activation == "relu":
            z,linear_residual=self.forward_function(previous_layer_activation,weight,bias)
            (Activation, activation_residual) =relu(z) , z

        elif activation == "sigmoid":
            z,linear_residual=self.forward_function(previous_layer_activation,weight,bias)
            (Activation, activation_residual) =sig(z) , z

        return Activation,activation_residual

    # forward propagation will take input from parameter_iniitalize input_from_weight_initialization
    def forward_propagation(self,input, input_from_weight_initialization):
        number_of_layer=self.layer
        Activation=input #input layer
        residuals=[]
        for i in range(1,number_of_layer):
            activation_previous=Activation

            Activation,residual=linear_forward_one_step(activation_previous,input_from_weight_initialization['w'+str(i)],linear_forward_one_step['w'+str(i)],self.activation[i])
            residuals.append(residual)

            return Activation,residuals

    def cost_calculation(self,activation,y):

        m=y.shape[1]
        j = (-1 / m) * (np.dot(y, np.log(activation).T) + np.dot((1 - y), np.log(1 - activation).T))

        return j

    def back_linear_onestep(self,dz,residual):

        activation_previous,w,b= residual
        m= activation_previous.shape[1]

        dw = (1 / m) * np.dot(dz, activation_previous.T)
        db = (1 / m) * np.sum(dz, axis=1, keepdims=True)
        da_prev = np.dot(w.T, dz)

        return da_prev, dw,db

    def relu_back(self,da,activation_residual):
        dz=np.array(da,copy=True)
        z=activation_residual
        dz[z < 0] = 0
        return dz

    def sig_back(self,da,activation_residual):
        z = activation_residual
        f = 1 / (1 + np.exp(-z))
        dz = da * f * (1 - f)
        return dz

    def back_linear(self,da,residual,activation):
        linear_residual, activation_residual=residual
        if activation == "relu":
            dz=self.relu_back(activation_residual,z)

        elif activation == "sigmoid":
            dz = self.sig_back(activation_residual,z)

        da_prev,wb,db=self.back_linear_onestep(dz,linear_residual)

        return Activation,activation_residual


    def back_propagation(self,a,y,residuals):
        gradient={}

        number_of_layers=len(self.layer)
        m=a.shape[1]
        y=y.reshape(a.shape)
        residual_pointer=residuals[number_of_layers-1]


        dal= - (np.divide(y, a) - np.divide(1 - y, 1 - a))

        gradient["da" + str(number_of_layers - 1)], gradient["dw" + str(number_of_layers)], gradient[
            "db" + str(number_of_layers)] = back_linear(dal,
                                            residual_pointer,
                                            "sigmoid")
        for i in reversed(range(number_of_layers-1)):
            residual_pointer = residuals[i]
            da_t, dw_t, db_t = back_linear(grads["da" + str(i + 1)], residual_pointer,
                                                                        activation="relu")
            grads["da" + str(i)] = da_t
            grads["dw" + str(i + 1)] = dw_t
            grads["db" + str(i + 1)] = db_t

        return gradient

    def update_parameters(self,parameters,gradients,learning_rate):

        number_of_layers= len(self.layer)
        parameters=parameters.copy()
        for i in range(number_of_layers):
            parameters['w'+str(i+1)] = parameters["w" + str(i+1)] - learning_rate * gradients["dw" + str(i+1)]
            parameters['b' + str(i + 1)] = parameters["b" + str(i + 1)] - learning_rate * gradients["db" + str(i + 1)]


        return parameters
    def do_branching(self):
        self.model_layers['output'+count]=self.layer
        count=count+1

    def predict_func(self,input, output, parameters):

        m = input.shape[1]
        n = len(self.layer)
        prediction = np.zeros((1, m))

        prob, caches = self.forward_propagation(input, parameters)

        for i in range(0, prob.shape[1]):
            if prob[0, i] > 0.5:
                prediction[0, i] = 1
            else:
                prediction[0, i] = 0

        return prediction

    def run_model(self,input_array,output_array, number_of_iterations=1000, learning_rate=0.001, multiple_output=False):


        if multiple_output == False:
            costs = []
            parameters= self.paramter_initialize()

            for i in range(0,number_of_iterations):
                al,residual=self.forward_propagation(input_array,parameters)
                cost= self.cost_calculation(al,output_array)
                gradient=self.back_propagation(al,output_array,residual)
                parameters=self.update_parameters(parameters,gradient,learning_rate)

                #print cost at every 100th iterations
                if i % 100 == 0:
                    costs.append(cost)

        else:
            costs={}
            for i in range(count):
                cost_temp=[]
                parameters = self.paramter_initialize_multiple(self.model_layers[i])

                for i in range(0, number_of_iterations):
                    al, residual = self.forward_propagation(input_array, parameters)
                    cost = self.cost_calculation(al, output_array)
                    gradient = self.back_propagation(al, output_array, residual)
                    parameters = self.update_parameters(parameters, gradient, learning_rate)

                    if i % 100 == 0:
                        cost_temp.append(cost)
                costs['output'+i]=cost_temp

        self.cost_f=costs
        self.param_f=parameters
        self.input=input_array
        self.output=output_array
        return parameters,costs







    def predict(self):
        if type(self.cost_f) is dict:
            prediction=[]
            for i in range(len(self.cost_f)):
                prediction.append(self.predict_func(self.input,self.output,self.param_f))


        else:
            prediction=self.predict_func(self.input,self.output,self.param_f)

        return prediction






